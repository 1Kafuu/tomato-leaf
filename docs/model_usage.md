# Model Usage Documentation

## Package Overview

`backend/app/core/model/` adalah package Python untuk **Fuzzy Sugeno Orde 0** yang digunakan mendeteksi kesehatan daun tomat dari citra digital. Package ini mencakup seluruh pipeline: segmentasi daun, ekstraksi fitur, inferensi fuzzy, dan klasifikasi penyakit.

---

## Directory Structure

```
backend/app/core/model/
├── __init__.py          # Ekspor publik (predict)
├── config.py            # Parameter MF, rule base, HSV ranges, konstanta
├── segmenter.py         # Segmentasi daun (HSV green mask + contour)
├── feature_extractor.py # Ekstraksi 5 fitur visual dari area daun
├── fuzzy_engine.py      # Triangular MF, fuzzifikasi, 16 rules, Sugeno WA
├── pipeline.py          # Orchestrator: segment → extract → infer → classify
└── main.py              # CLI entry point untuk testing
```

---

## Module Descriptions

### 1. `__init__.py`

Ekspor fungsi utama `predict()` dari `pipeline.py`.

```python
from .pipeline import predict

__all__ = ["predict"]
```

### 2. `config.py` — Configuration & Parameters

Berisi seluruh parameter yang digunakan oleh modul lain:

| Section | Isi |
|---|---|
| **Membership Functions** | Parameter triangular (a, b, c) untuk Spot Area, Color Change, Yellow Ratio, Brown Ratio, Dark Ratio |
| **Rule Base** | 16 aturan fuzzy dalam format `(spot_cat, color_cat, konstanta)` |
| **Output Classes** | 7 kelas output dengan rentang skor, nama penyakit, severity, status |
| **HSV Ranges** | Lower/upper bound untuk deteksi warna (yellow, brown, dark, spot) |
| **Image Processing** | Ukuran resize (256x256), kernel morfologi (5x5) |

**Key Constants:**

| Constant | Value | Description |
|---|---|---|
| `SPOT_AREA_MF` | `dict` | Triangular MF params for spot area |
| `COLOR_CHANGE_MF` | `dict` | Triangular MF params for color change |
| `RULES` | `list[tuple]` | 16 fuzzy rules |
| `OUTPUT_CLASSES` | `list[tuple]` | 7 output classes with score ranges |
| `DEFAULT_FUZZY_SCORE` | `50` | Fallback when no rule fires |
| `IMAGE_SIZE` | `(256, 256)` | Resize dimensions |
| `GREEN_MASK_LOWER/UPPER` | `np.ndarray` | HSV threshold for leaf segmentation |
| `HSV_RANGES` | `dict` | HSV bounds for yellow, brown, dark, spot detection |

### 3. `segmenter.py` — Leaf Segmentation

**Function:** `segment(image_path: str) -> tuple[np.ndarray, np.ndarray]`

Pipeline segmentasi:

```
Input Image → Resize 256×256 → BGR→HSV → Green Mask [35,40,40]–[90,255,255]
→ Morph CLOSE (ellipse 5×5, 2x) → Morph OPEN (ellipse 5×5, 1x)
→ Largest Contour → Leaf Mask (binary) → Masked Image
```

**Returns:**
- `leaf_mask`: Binary mask (uint8, 0 or 255) — area daun
- `masked_image`: Gambar asli dengan background dihilangkan

**Fallback:** Jika tidak ada kontur terdeteksi, seluruh area digunakan sebagai mask.

### 4. `feature_extractor.py` — Feature Extraction

**Function:** `extract(masked_img: np.ndarray, leaf_mask: np.ndarray) -> dict`

Mengekstrak **5 fitur** hanya pada area daun (background diabaikan):

| Feature | HSV Range | Description |
|---|---|---|
| `spot_area` | [0,20,20] – [40,255,180] | % area bercak (coklat/kuning) |
| `yellow_ratio` | [20,50,50] – [35,255,255] | % area kuning (klorosis) |
| `brown_ratio` | [0,20,20] – [20,255,120] | % area coklat (nekrosis) |
| `dark_ratio` | [0,0,0] – [180,255,60] | % area gelap/hitam |
| `color_change` | — | yellow + brown + dark |

**Edge case:** Jika `leaf_pixels == 0`, seluruh fitur dikembalikan dengan nilai `0.0`.

### 5. `fuzzy_engine.py` — Fuzzy Sugeno Inference

**Functions:**

| Function | Description |
|---|---|
| `triangular_mf(x, a, b, c) -> float` | Triangular membership function |
| `fuzzify(value, mf_dict, labels) -> dict` | Fuzzifikasi crisp → derajat keanggotaan |
| `infer(spot_area, color_change) -> float` | Inferensi: fuzzify → rule eval → weighted average |
| `classify(z) -> dict` | Mapping skor (0–100) ke kategori penyakit |

**Fuzzy Process:**

1. **Fuzzification** — Hitung derajat keanggotaan untuk Spot Area (4 kategori) dan Color Change (4 kategori) menggunakan Triangular MF.
2. **Rule Evaluation** — 16 rules, operator AND = `min(µ_spot, µ_color)`, menghasilkan firing strength `αi`.
3. **Defuzzification** — Weighted Average:
   ```
   z = Σ(αi × ki) / Σαi
   ```
4. **Classification** — Mapping `z` ke 7 kelas output.

**Edge Cases:**
- `Σαi = 0` → return `DEFAULT_FUZZY_SCORE` (50)
- `z < 0` → clip ke 0
- `z > 100` → clip ke 100

### 6. `pipeline.py` — Pipeline Orchestrator

**Function:** `predict(image_path: str) -> dict`

Menggabungkan seluruh pipeline menjadi satu fungsi siap pakai:

```
1. segment(image_path)       → leaf_mask, masked_img
2. extract(masked_img, mask) → features dict
3. infer(spot, color_change) → fuzzy_score (float)
4. classify(fuzzy_score)     → classification dict
5. return combined result
```

**Return format:**

```python
{
    "disease_name": "Early Blight",      # str — nama penyakit
    "fuzzy_score": 71.25,                # float — skor fuzzy 0–100
    "severity_level": "Ringan",          # str — tingkat keparahan
    "plant_status": "Terinfeksi",        # str — "Sehat" atau "Terinfeksi"
    "spot_area": 12.34,                  # float — % area bercak
    "color_change": 30.50,               # float — % perubahan warna
}
```

### 7. `main.py` — CLI Entry Point

CLI untuk testing langsung dari terminal.

```
python -m app.core.model.main <path/to/image>
```

---

## Usage

### A. CLI Mode (Testing Cepat)

Jalankan prediksi langsung dari terminal:

```bash
# Prediksi daun sehat
python -m app.core.model.main test_images/sehat.jpg

# Prediksi daun terserang Early Blight
python -m app.core.model.main test_images/early_blight.jpg

# Prediksi daun terserang Late Blight
python -m app.core.model.main test_images/late_blight.jpg
```

**Output contoh:**

```json
{
  "disease_name": "Early Blight",
  "fuzzy_score": 71.25,
  "severity_level": "Ringan",
  "plant_status": "Terinfeksi",
  "spot_area": 12.34,
  "color_change": 30.5
}
```

### B. Programmatic Usage (Python)

Gunakan langsung dari kode Python:

```python
from app.core.model import predict

# Prediksi dari path file
result = predict("test_images/sehat.jpg")
print(result["disease_name"])   # "Sangat Sehat"
print(result["fuzzy_score"])    # 95.5

# Prediksi lain
result2 = predict("test_images/early_blight.jpg")
print(result2["disease_name"])  # "Early Blight"
```

### C. Pipeline Manual (Per Komponen)

Gunakan setiap komponen secara terpisah untuk debugging atau analisis:

```python
from app.core.model.segmenter import segment
from app.core.model.feature_extractor import extract
from app.core.model.fuzzy_engine import infer, classify

# 1. Segmentasi
leaf_mask, masked_img = segment("test_images/sehat.jpg")
# leaf_mask: binary mask (0 atau 255)
# masked_img: gambar hanya area daun

# 2. Ekstraksi fitur
features = extract(masked_img, leaf_mask)
print(features)
# {
#     "spot_area": 3.22,
#     "yellow_ratio": 2.5,
#     "brown_ratio": 0.12,
#     "dark_ratio": 1.5,
#     "color_change": 4.12
# }

# 3. Inferensi fuzzy
fuzzy_score = infer(features["spot_area"], features["color_change"])
print(fuzzy_score)  # 95.5

# 4. Klasifikasi
classification = classify(fuzzy_score)
print(classification)
# {
#     "disease_name": "Sangat Sehat",
#     "severity_level": "Tidak Ada",
#     "plant_status": "Sehat"
# }
```

### D. Fuzzification Manual

Untuk melihat derajat keanggotaan suatu nilai:

```python
from app.core.model.fuzzy_engine import fuzzify
from app.core.model.config import SPOT_AREA_MF, SPOT_AREA_LABELS

degrees = fuzzify(12.0, SPOT_AREA_MF, SPOT_AREA_LABELS)
print(degrees)
# {
#     "kecil": 0.0,
#     "sedang": 0.75,    # 12 termasuk kategori sedang
#     "besar": 0.25,
#     "sangat_besar": 0.0
# }
```

---

## Integration with FastAPI

Berikut pola integrasi dengan endpoint FastAPI:

```python
from fastapi import APIRouter, UploadFile, File
from app.core.model.pipeline import predict
import tempfile
import os

router = APIRouter()

@router.post("/predict")
async def predict_endpoint(image: UploadFile = File(...)):
    # Simpan file upload ke temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        content = await image.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Jalankan pipeline model
        result = predict(tmp_path)
        return {"success": True, "message": "Prediksi berhasil", "data": result}
    finally:
        os.unlink(tmp_path)  # Hapus file temporary
```

---

## Edge Cases & Error Handling

| Skenario | Behavior | Handling |
|---|---|---|
| File gambar tidak ditemukan | `FileNotFoundError` | Di-raise oleh `segmenter.segment()` |
| Format file tidak didukung | OpenCV gagal membaca | `cv2.imread` return None → `FileNotFoundError` |
| Mask kosong (tidak ada daun) | Fallback: seluruh area jadi mask | `segmenter` return full white mask |
| Leaf pixels = 0 | Semua fitur = 0.0 | `feature_extractor` return zeros |
| Tidak ada aturan fuzzy aktif (Σαi=0) | Fuzzy score default = 50 | `fuzzy_engine.infer()` return 50 |
| Fuzzy score < 0 atau > 100 | Clipping ke [0, 100] | `fuzzy_engine.infer()` clamp |
| Gambar terlalu besar (>10MB) | Harus divalidasi sebelum masuk pipeline | Validasi di layer API |

---

## Configuration Reference

### Membership Function Parameters

#### Spot Area (%)

| Kategori | a (batas) | b (pusat) | c (batas) |
|---|---|---|---|
| kecil | 0.06 | 3.22 | 8.35 |
| sedang | 8.35 | 13.48 | 18.85 |
| besar | 18.85 | 24.23 | 31.78 |
| sangat_besar | 31.78 | 39.33 | 48.48 |

#### Color Change (%)

| Kategori | a (batas) | b (pusat) | c (batas) |
|---|---|---|---|
| rendah | 0.19 | 8.05 | 16.86 |
| sedang | 16.86 | 25.68 | 36.19 |
| tinggi | 36.19 | 46.70 | 64.15 |
| sangat_tinggi | 64.15 | 81.59 | 99.79 |

### Fuzzy Rules (16 Rules)

| Rule | Spot Area | Color Change | Output Konstanta |
|---|---|---|---|
| R1 | kecil | rendah | 100 |
| R2 | kecil | sedang | 90 |
| R3 | kecil | tinggi | 80 |
| R4 | kecil | sangat_tinggi | 40 |
| R5 | sedang | rendah | 85 |
| R6 | sedang | sedang | 70 |
| R7 | sedang | tinggi | 55 |
| R8 | sedang | sangat_tinggi | 40 |
| R9 | besar | rendah | 70 |
| R10 | besar | sedang | 55 |
| R11 | besar | tinggi | 20 |
| R12 | besar | sangat_tinggi | 10 |
| R13 | sangat_besar | rendah | 50 |
| R14 | sangat_besar | sedang | 20 |
| R15 | sangat_besar | tinggi | 10 |
| R16 | sangat_besar | sangat_tinggi | 5 |

### Output Classes

| Score Range | Disease Name | Severity | Status |
|---|---|---|---|
| 90–100 | Sangat Sehat | Tidak Ada | Sehat |
| 75–89 | Sehat | Tidak Ada | Sehat |
| 60–74 | Early Blight | Ringan | Terinfeksi |
| 45–59 | Late Blight | Sedang | Terinfeksi |
| 25–44 | Leaf Mold | Berat | Terinfeksi |
| 10–24 | Septoria Leaf Spot | Berat | Terinfeksi |
| 0–9 | Sangat Buruk | Sangat Berat | Terinfeksi |

### HSV Ranges

| Color | H | S | V |
|---|---|---|---|
| Green Mask (lower) | 35 | 40 | 40 |
| Green Mask (upper) | 90 | 255 | 255 |
| Yellow (lower) | 20 | 50 | 50 |
| Yellow (upper) | 35 | 255 | 255 |
| Brown (lower) | 0 | 20 | 20 |
| Brown (upper) | 20 | 255 | 120 |
| Dark (lower) | 0 | 0 | 0 |
| Dark (upper) | 180 | 255 | 60 |
| Spot (lower) | 0 | 20 | 20 |
| Spot (upper) | 40 | 255 | 180 |

### Image Processing Constants

| Constant | Value |
|---|---|
| Resize | 256 × 256 px |
| Morph Kernel | Ellipse 5×5 |
| Morph CLOSE iterations | 2 |
| Morph OPEN iterations | 1 |

---

## Testing

### Test with Sample Images

```bash
# Pastikan ada folder test_images/ dengan sample daun
python -m app.core.model.main test_images/healthy_1.jpg
python -m app.core.model.main test_images/early_blight_1.jpg
python -m app.core.model.main test_images/late_blight_1.jpg
python -m app.core.model.main test_images/leaf_mold_1.jpg
python -m app.core.model.main test_images/septoria_1.jpg
```

### Unit Test Coverage

| Module | Test Focus |
|---|---|
| `segmenter` | Mask shape, contour detection, fallback behavior |
| `feature_extractor` | Feature values for known inputs, zero mask edge case |
| `fuzzy_engine` | MF calculation, firing strength, weighted average, Σαi=0 |
| `pipeline` | End-to-end predict flow, FileNotFoundError |

---

## Dependencies

| Package | Usage |
|---|---|
| `opencv-python` (cv2) | Image reading, HSV conversion, segmentation, feature extraction |
| `numpy` | Array operations, HSV range constants |

> **Note:** Tidak memerlukan scikit-fuzzy; fuzzy engine diimplementasikan secara custom.

---

## Related Documents

| Document | Description |
|---|---|
| `docs/ai_model.md` | AI model requirement & specification (parameter source, cluster analysis) |
| `docs/prd_tomato_leaf.md` | Product requirement document |
| `docs/project_structure.md` | Project directory structure |
| `docs/database_schema.md` | Database schema for prediction history |
| `model-reference/` | Scripts dataset → CSV → K-Means → membership parameters |
