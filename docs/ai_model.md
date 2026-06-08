# AI Model Requirement Document

## Project Name

Tomato Leaf Health Detection System Using Fuzzy Sugeno

---

# AI Module Overview

Modul AI bertugas melakukan analisis kondisi daun tomat berdasarkan citra gambar daun menggunakan metode **Fuzzy Sugeno Orde 0** dengan 16 aturan fuzzy. Sistem dikembangkan secara **data-driven** menggunakan **K-Means Clustering (k=4)** pada **4.952 sampel PlantVillage Tomato Dataset** untuk menentukan parameter membership function.

Sistem melakukan:
1. Preprocessing gambar (resize 256×256, konversi RGB ke HSV).
2. Segmentasi daun (HSV Green Mask + Largest Contour + Morphological Cleanup).
3. Ekstraksi fitur (7 fitur visual).
4. Fuzzifikasi parameter (Triangular Membership Function).
5. Evaluasi fuzzy rules (16 rules dengan operator AND/minimum).
6. Defuzzifikasi Sugeno (Weighted Average).
7. Klasifikasi severity dan penentuan kondisi kesehatan daun.

---

# AI Objectives

## Main Objectives

- Mengidentifikasi kondisi kesehatan daun tomat berdasarkan citra digital.
- Mengklasifikasikan tingkat keparahan penyakit menggunakan 2 variabel input fuzzy: Spot Area dan Color Change.
- Memberikan output diagnosis berbasis fuzzy logic dengan skor numerik (0–100).

## Expected Output

- Status tanaman: Sehat / Terinfeksi
- Tingkat keparahan: Sehat / Ringan / Sedang / Berat / Sangat Berat
- Fuzzy score (0-100)
- Severity score berbobot (0-100)
- 7 nilai fitur visual hasil ekstraksi

---

# AI Scope

## Included

- Image preprocessing (resize, konversi warna, normalisasi).
- Leaf segmentation (HSV green masking, morphological cleanup, contour detection).
- Feature extraction (7 fitur: spot_area, color_change, yellow_ratio, brown_ratio, dark_ratio, spot_count, texture_var).
- Fuzzy Sugeno inference (fuzzifikasi, rule evaluation, defuzzifikasi).
- Severity classification (5 level).

## Excluded

- Deep learning / CNN classification.
- Specific disease identification (Early Blight, Late Blight, dll).
- Realtime video detection.
- Multi plant classification.
- Disease treatment recommendation.

---

# Input Data Requirement

## Input Type

Image daun tomat.

## Supported Format

- JPG
- JPEG
- PNG

## Image Requirement

- Gambar jelas dan fokus pada daun.
- Pencahayaan cukup (tidak terlalu gelap atau terlalu terang).
- Background tidak terlalu kompleks (daun sebagai objek utama).

## Maximum File Size

10 MB

---

# Dataset

## Dataset Source

**PlantVillage Tomato Dataset** — dataset publik berisi gambar daun tomat sehat dan berpenyakit.

## Dataset Distribution

| Kelas | Jumlah Gambar |
|---|---|
| Tomato_Healthy | ~600 |
| Tomato_Early_Blight | ~1.000 |
| Tomato_Late_Blight | ~1.000 |
| Tomato_Septoria_Leaf_Spot | ~1.000 |
| Tomato_Leaf_Mold | ~952 |
| **Total** | **~4.952** |

## Dataset Usage

| Kegunaan | Deskripsi |
|---|---|
| **Pembentukan Membership Function** | Seluruh gambar diekstrak fiturnya, kemudian dianalisis menggunakan K-Means Clustering (k=4) untuk menentukan pusat cluster sebagai parameter Triangular Membership Function. |
| **Evaluasi Sistem** | Dataset digunakan untuk menguji akurasi sistem dalam mengklasifikasikan kondisi daun tomat. |
| **Validasi Parameter** | Parameter fuzzy (rule base, konstanta Sugeno) divalidasi menggunakan subset data uji. |

---

# Image Processing Pipeline

## Preprocessing Steps

1. **Resize** — Ubah ukuran gambar menjadi 256×256 piksel.
2. **Color Conversion** — Konversi RGB ke HSV (cv2.COLOR_BGR2HSV).
3. **Green Mask** — Threshold HSV untuk mendeteksi area hijau daun.
   - Lower bound: `[35, 40, 40]`
   - Upper bound: `[90, 255, 255]`
4. **Morphological Cleanup** — Membersihkan noise pada mask.
   - **Close** (cv2.MORPH_CLOSE): kernel ellipse 5×5, iterasi 2
   - **Open** (cv2.MORPH_OPEN): kernel ellipse 5×5, iterasi 1
5. **Largest Contour Detection** — Mendeteksi kontur terluas (diasumsikan sebagai daun) menggunakan `cv2.findContours` dengan `RETR_EXTERNAL`.
6. **Leaf Mask** — Membuat binary mask area daun dari kontur terluas.

## Output

Binary mask area daun yang digunakan untuk membatasi perhitungan fitur hanya pada area daun (background dihilangkan).

## Recommended Library

- OpenCV (cv2)
- NumPy
- Pillow

---

# Feature Extraction

Sistem mengekstrak **7 fitur numerik** dari area daun hasil segmentasi. Seluruh fitur dihitung sebagai persentase terhadap total area daun.

## Daftar Fitur

| No | Fitur | Satuan | Deskripsi |
|---|---|---|---|
| 1 | **spot_area** | % | Persentase area daun yang tertutup bercak (warna coklat/kuning) |
| 2 | **color_change** | % | Total perubahan warna: yellow_ratio + brown_ratio + dark_ratio |
| 3 | **yellow_ratio** | % | Persentase area daun yang menunjukkan warna kuning (klorosis) |
| 4 | **brown_ratio** | % | Persentase area daun yang menunjukkan warna coklat (nekrosis) |
| 5 | **dark_ratio** | % | Persentase area daun yang menunjukkan warna gelap/hitam |
| 6 | **spot_count** | count | Jumlah bercak/lesi terpisah (kontur dengan area ≥ 5 piksel) |
| 7 | **texture_var** | - | Variansi tekstur (standard deviation grayscale) |

## Definisi Matematis

### Spot Area

```
spot_area = (spot_pixels / leaf_pixels) × 100
```

Rentang HSV untuk deteksi bercak: `[0, 20, 20]` hingga `[40, 255, 180]`

### Color Change Severity

```
color_change = yellow_ratio + brown_ratio + dark_ratio
```

### Yellow Ratio

```
yellow_ratio = (yellow_pixels / leaf_pixels) × 100
```

Rentang HSV: `[20, 50, 50]` hingga `[35, 255, 255]`

### Brown Ratio

```
brown_ratio = (brown_pixels / leaf_pixels) × 100
```

Rentang HSV: `[0, 20, 20]` hingga `[20, 255, 120]`

### Dark Ratio

```
dark_ratio = (dark_pixels / leaf_pixels) × 100
```

Rentang HSV: `[0, 0, 0]` hingga `[180, 255, 60]`

### Spot Count

```
spot_count = count(contours where area >= 5 pixels)
```

### Texture Variance

```
texture_var = std(grayscale_pixels within leaf_mask)
```

## Input Variables untuk Fuzzy Inference

Sistem hanya menggunakan **2 variabel input** untuk inferensi fuzzy:

| Variabel | Satuan | Rentang Data (P1–P99) | Deskripsi |
|---|---|---|---|
| **Spot Area** | % | 0,06 – 48,48 | Persentase luas bercak terhadap total area daun |
| **Color Change** | % | 0,19 – 99,79 | Total perubahan warna (yellow + brown + dark) |

> **Catatan:** Yellow Ratio, Brown Ratio, Dark Ratio, Spot Count, dan Texture Variance merupakan fitur pendukung yang digunakan untuk menghitung severity score berbobot.

---

# Feature Statistics

Statistik deskriptif dari seluruh fitur yang diekstrak dari 4.952 sampel PlantVillage Dataset.

## Tabel Statistik

| Variable | Min | Max | Mean | Median | Std | P1 | P99 |
|---|---|---|---|---|---|---|---|
| spot_area | 0,00 | 81,99 | 13,23 | 11,08 | 11,48 | 0,06 | 48,48 |
| color_change | 0,00 | 136,45 | 28,24 | 23,98 | 21,89 | 0,19 | 99,79 |
| yellow_ratio | 0,00 | 100,00 | 14,81 | 6,59 | 20,15 | 0,00 | 93,63 |
| brown_ratio | 0,00 | 24,03 | 0,56 | 0,14 | 1,19 | 0,00 | 5,11 |
| dark_ratio | 0,00 | 81,99 | 12,87 | 10,68 | 11,42 | 0,01 | 48,27 |
| spot_count | 0 | 1000+ | ~50 | ~30 | ~70 | 4 | 794,49 |
| texture_var | 0 | 60+ | ~30 | ~28 | ~10 | 14,96 | 56,86 |

## Insight

- **Spot Area** memiliki distribusi yang menceng ke kanan (mean 13,23 > median 11,08), menunjukkan mayoritas sampel memiliki bercak kecil.
- **Brown Ratio** memiliki nilai sangat rendah (mean 0,56%, max 24,03%), mengindikasikan bahwa warna coklat murni relatif jarang ditemukan.
- **Yellow Ratio** memiliki variasi sangat tinggi (std 20,15), menunjukkan klorosis sangat bervariasi antar sampel.
- **Spot Count** memiliki silhouette score tertinggi (0,8352), menunjukkan clustering paling konsisten.
- **Color Change** memiliki nilai maksimum 136,45% (teoritis bisa >100% karena merupakan penjumlahan 3 rasio yang tumpang tindih).

---

# Cluster Analysis

Parameter membership function ditentukan menggunakan **K-Means Clustering (k=4)** pada data fitur yang telah diekstrak.

## Silhouette Score

Silhouette score digunakan untuk mengevaluasi kualitas clustering.

| Variable | Silhouette (k=4) | Interpretation |
|---|---|---|
| spot_count | 0,8352 | ⭐ Best clustered |
| brown_ratio | 0,7254 | Strong |
| yellow_ratio | 0,6647 | Good |
| spot_area | 0,5928 | Moderate |
| color_change | 0,5601 | Moderate |
| texture_var | 0,5537 | Moderate |

**Interpretasi:** Seluruh variabel memiliki silhouette score > 0,5 pada k=4, mengindikasikan struktur cluster yang cukup baik.

## Cluster Centers

Pusat cluster (nilai representatif) dari `cluster_report_6features.csv`.

### Spot Area

| Cluster | Label | Center Value |
|---|---|---|
| Cluster 0 | small | 3,23% |
| Cluster 1 | medium | 13,49% |
| Cluster 2 | large | 24,23% |
| Cluster 3 | very_large | 39,33% |

### Color Change

| Cluster | Label | Center Value |
|---|---|---|
| Cluster 0 | low | 8,05% |
| Cluster 1 | medium | 25,67% |
| Cluster 2 | high | 46,69% |
| Cluster 3 | very_high | 81,59% |

### Yellow Ratio

| Cluster | Label | Center Value |
|---|---|---|
| Cluster 0 | low | 3,76% |
| Cluster 1 | medium | 19,03% |
| Cluster 2 | high | 44,99% |
| Cluster 3 | very_high | 79,29% |

### Brown Ratio

| Cluster | Label | Center Value |
|---|---|---|
| Cluster 0 | low | 0,12% |
| Cluster 1 | medium | 0,91% |
| Cluster 2 | high | 2,26% |
| Cluster 3 | very_high | 4,48% |

### Spot Count

| Cluster | Label | Center Value |
|---|---|---|
| Cluster 0 | few | 16,33 |
| Cluster 1 | moderate | 44,60 |
| Cluster 2 | many | 71,95 |
| Cluster 3 | very_many | 99,54 |

### Texture Variance

| Cluster | Label | Center Value |
|---|---|---|
| Cluster 0 | low | 20,06 |
| Cluster 1 | medium | 28,99 |
| Cluster 2 | high | 37,69 |
| Cluster 3 | very_high | 49,27 |

---

# Membership Functions

Sistem menggunakan **Triangular Membership Function** untuk setiap variabel fuzzy. Parameter (a, b, c) ditentukan secara **data-driven** dari hasil K-Means Clustering.

## Definisi Triangular Membership Function

Triangular MF didefinisikan dengan tiga parameter:

| Parameter | Istilah | Definisi |
|---|---|---|
| **a** | Batas Awal | Nilai minimum di mana fungsi mulai aktif (derajat keanggotaan > 0) |
| **b** | Nilai Representatif | Pusat cluster K-Means (derajat keanggotaan = 1) |
| **c** | Batas Akhir | Nilai maksimum di mana fungsi masih aktif (derajat keanggotaan > 0) |

Parameter (a) dan (c) ditentukan dari titik tengah antar pusat cluster untuk menghasilkan overlap alami antar kategori.

## Rumus Matematis

```
                ┌ 0,                         x ≤ a
                │
                │ (x - a) / (b - a),         a < x ≤ b
μ(x; a, b, c) = │
                │ (c - x) / (c - b),         b < x < c
                │
                └ 0,                         x ≥ c
```

## Variabel Input 1: Spot Area (%)

| Kategori | Batas Awal (a) | Nilai Rep. (b) | Batas Akhir (c) |
|---|---|---|---|
| small | 0,06 | 3,23 | 8,36 |
| medium | 8,36 | 13,49 | 18,86 |
| large | 18,86 | 24,23 | 31,78 |
| very_large | 31,78 | 39,33 | 48,48 |

## Variabel Input 2: Color Change (%)

| Kategori | Batas Awal (a) | Nilai Rep. (b) | Batas Akhir (c) |
|---|---|---|---|
| low | 0,19 | 8,05 | 16,86 |
| medium | 16,86 | 25,67 | 36,18 |
| high | 36,18 | 46,69 | 64,14 |
| very_high | 64,14 | 81,59 | 99,79 |

---

# Fuzzy Sugeno Method

## Method

**Fuzzy Sugeno Orde 0** — menggunakan konstanta output (orde 0) sehingga perhitungan defuzzifikasi menggunakan weighted average.

## Input Variables (Fuzzy Inference)

| Variable | Membership Categories |
|---|---|
| Spot Area | small, medium, large, very_large |
| Color Change | low, medium, high, very_high |

## Output Variable

Klasifikasi severity berdasarkan fuzzy score:

| Severity Level | Plant Status | Fuzzy Score Range |
|---|---|---|
| Sehat | Sehat | 85-100 |
| Ringan | Terinfeksi | 70-84 |
| Sedang | Terinfeksi | 50-69 |
| Berat | Terinfeksi | 25-49 |
| Sangat Berat | Terinfeksi | 0-24 |

---

# Fuzzy Rule Base

Total rules: **16** (kombinasi 4 × 4 dari Spot Area dan Color Change)

## Format Aturan

```
IF spot_area IS [Kategori_A] AND color_change IS [Kategori_B] THEN output = k
```

Keterangan:
- `αi = min(μ_spot_area, μ_color_change)` — firing strength (operator AND = minimum)
- `k` = konstanta output Sugeno

## Tabel Rule Base

| Rule | IF Spot Area | AND Color Change | THEN | Konstanta (k) |
|---|---|---|---|---|
| R1 | small | low | Healthy | 100 |
| R2 | small | medium | Healthy | 90 |
| R3 | small | high | Mild | 75 |
| R4 | small | very_high | Mild | 60 |
| R5 | medium | low | Healthy | 85 |
| R6 | medium | medium | Mild | 70 |
| R7 | medium | high | Moderate | 55 |
| R8 | medium | very_high | Moderate | 40 |
| R9 | large | low | Mild | 65 |
| R10 | large | medium | Moderate | 50 |
| R11 | large | high | Severe | 35 |
| R12 | large | very_high | Severe | 20 |
| R13 | very_large | low | Moderate | 45 |
| R14 | very_large | medium | Severe | 30 |
| R15 | very_large | high | Very Severe | 15 |
| R16 | very_large | very_high | Very Severe | 5 |

## Matriks Rule Base (4 × 4)

```
                      Color Change
              low       medium     high very_high
                ↓         ↓         ↓            ↓
   small      → [100]    [ 90]    [ 75]       [ 60]
   medium     → [ 85]    [ 70]    [ 55]       [ 40]
   large      → [ 65]    [ 50]    [ 35]       [ 20]
 very_large   → [ 45]    [ 30]    [ 15]       [5]

              ↑                        ↑
 Output tertinggi         Output terendah
 (Healthy)           (Very Severe)
```

**Pola Umum:**
- Semakin kecil bercak dan perubahan warna → output semakin tinggi (sehat)
- Semakin besar bercak dan perubahan warna → output semakin rendah (severity tinggi)

---

# Defuzzification

## Metode

**Weighted Average Sugeno Orde 0:**

```
z = Σ(αi × ki) / Σαi
```

Keterangan:
- `αi` = firing strength aturan ke-i = min(μ_spot_area, μ_color_change)
- `ki` = konstanta output aturan ke-i
- `z` = output akhir (fuzzy score, 0–100)

## Penanganan Kasus Khusus

| Skenario | Penanganan |
|---|---|
| Σαi = 0 (tidak ada aturan aktif) | Output default = 50 |
| z < 0 | Clipping ke 0 |
| z > 100 | Clipping ke 100 |

---

# Severity Score Calculation

Selain fuzzy score, sistem menghitung **severity score** berbobot dari6 fitur:

## Feature Weights

| Feature | Weight |
|---|---|
| spot_area | 0,30 |
| color_change | 0,25 |
| brown_ratio | 0,15 |
| yellow_ratio | 0,10 |
| spot_count | 0,10 |
| texture_var | 0,10 |

## Normalization Formula

```
normalized = ((value - min_val) / (max_val - min_val)) × 100
```

## Normalization Ranges (P99)

| Feature | Min | Max |
|---|---|---|
| spot_area | 0,0 | 48,48 |
| color_change | 0,0 | 99,79 |
| yellow_ratio | 0,0 | 93,63 |
| brown_ratio | 0,0 | 5,11 |
| spot_count | 0,0 | 794,49 |
| texture_var | 0,0 | 56,86 |

## Severity Score Formula

```
severity_score = Σ(weight_i × normalized_i)
```

> **Catatan:** Severity score tinggi = kondisi buruk (severity tinggi).
> Severity score rendah = kondisi sehat.

---

# Output Classification

Output numerik hasil defuzzifikasi (z) diklasifikasikan ke dalam kategori kesehatan tanaman.

## Tabel Klasifikasi

| Rentang Skor | Severity Level | Plant Status | Deskripsi |
|---|---|---|---|
| 85 – 100 | Sehat | Sehat | Daun dalam kondisi optimal, hijau segar, tanpa gejala penyakit |
| 70 – 84 | Ringan | Terinfeksi | Gejala awal infeksi, bercak kecil |
| 50 – 69 | Sedang | Terinfeksi | Infeksi sedang, perubahan warna terlihat |
| 25 – 49 | Berat | Terinfeksi | Infeksi parah, banyak bercak |
| 0 – 24 | Sangat Berat | Terinfeksi | Kerusakan sangat parah |

## Output yang Ditampilkan ke Pengguna

| Field | Tipe | Contoh |
|---|---|---|
| plant_status | string | "Terinfeksi" |
| severity_level | string | "Ringan" |
| fuzzy_score | float | 75.50 |
| severity_score | float | 42.30 |
| features | object | {spot_area, color_change, yellow_ratio, brown_ratio, dark_ratio, spot_count, texture_var} |

---

# API Integration

## POST /predict

**Request:** `image` (file, multipart/form-data)
**Headers:** `Authorization: Bearer {token}`

**Response (Success — 200):**

```json
{
  "success": true,
  "message": "Prediksi berhasil",
  "data": {
    "plant_status": "Terinfeksi",
    "severity_level": "Ringan",
    "fuzzy_score": 75.50,
    "severity_score": 42.30,
    "features": {
      "spot_area": 12.34,
      "color_change": 30.50,
      "yellow_ratio": 15.20,
      "brown_ratio": 2.80,
      "dark_ratio": 12.50,
      "spot_count": 25,
      "texture_var": 28.45
    }
  }
}
```

**Response (Error — 400):**
```json
{
  "success": false,
  "message": "File must be an image"
}
```

## GET /history

**Headers:** `Authorization: Bearer {token}`
**Query:** `page`, `limit`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "image_url": "https://storage.url/image.jpg",
      "plant_status": "Terinfeksi",
      "severity_level": "Ringan",
      "fuzzy_score": 75.50,
      "severity_score": 42.30,
      "created_at": "2026-06-01T10:30:00Z"
    }
  ]
}
```

---

# Performance Requirements

| Requirement | Target |
|---|---|
| Response Time | < 5 detik |
| Classification Accuracy | ≥ 80% |
| Max Upload Size | 10 MB |
| Uptime | ≥ 95% |

---

# AI Architecture

## Flow

```
Input Image
    ↓
segmenter.py → Binary leaf mask (HSV green mask + contour)
    ↓
feature_extractor.py → 7 features
    ↓
fuzzy_engine.py → Fuzzification → Rule evaluation (16 rules) → Defuzzification (weighted average)
    ↓
calculate_severity_score → Weighted severity calculation from 6 features
    ↓
Output: {plant_status, severity_level, fuzzy_score, severity_score, features}
```

---

# AI Technology Stack

| Component | Technology | Version |
|---|---|---|
| Programming Language | Python | 3.11+ |
| Image Processing | OpenCV | 4.9+ |
| Numerical Computation | NumPy | 1.26+ |
| Image Format Handling | Pillow | 10.0+ |
| Fuzzy Logic | Custom engine (scikit-fuzzy reference) | — |
| API Framework | FastAPI | 0.x |
| Clustering (pengembangan) | scikit-learn (K-Means) | — |

---

# Code Reference (Production)

| Module | Path | Fungsi |
|---|---|---|
| `pipeline.py` | `backend/app/core/model/pipeline.py` | Orchestrates full prediction flow: segment → extract → fuzzy inference → severity score |
| `segmenter.py` | `backend/app/core/model/segmenter.py` | Leaf segmentation via HSV green mask + largest contour |
| `feature_extractor.py` | `backend/app/core/model/feature_extractor.py` | Extracts 7 visual features from segmented leaf |
| `fuzzy_engine.py` | `backend/app/core/model/fuzzy_engine.py` | Triangular MF + 16-rule Sugeno inference engine + severity calculation |
| `config.py` | `backend/app/core/model/config.py` | Fuzzy parameters (MF bounds, rules, weights, HSV ranges) |

## Pipeline Output Structure

```python
{
    "plant_status": str, # "Sehat" | "Terinfeksi"
    "severity_level": str,     # "Sehat" | "Ringan" | "Sedang" | "Berat" | "Sangat Berat"
    "fuzzy_score": float,     # 0-100 (Sugeno weighted average)
    "severity_score": float,   # 0-100 (weighted feature calculation)
    "features": {
        "spot_area": float,
        "color_change": float,
        "yellow_ratio": float,
        "brown_ratio": float,
        "dark_ratio": float,
        "spot_count": int,
        "texture_var": float,
    }
}
```

## API Integration

- **v1** (`POST /api/v1/predict`): Upload → predict → save to DB
- **v2** (`POST /api/v2/predict`): Same logic, returns `PredictionRecordResponse`

---

# AI Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Segmentasi daun gagal (daun tidak terdeteksi) | Fallback: gunakan seluruh gambar jika mask kosong; tampilkan pesan warning |
| Rule fuzzy kurang akurat | Kalibrasi membership function berdasarkan data aktual; evaluasi berkala |
| Pencahayaan gambar buruk | Tambahkan validasi kualitas input image sebelum diproses |
| Noise gambar tinggi | Terapkan noise reduction (Gaussian Blur) sebelum segmentasi |
| Akurasi klasifikasi rendah | Evaluasi dengan confusion matrix; tuning rule base |

---

# Future Improvement

## Phase 2

- Specific disease identification (Early Blight, Late Blight, Leaf Mold, Septoria).
- Adaptive fuzzy membership (parameter MF dapat disesuaikan secara dinamis).
- Hybrid fuzzy + CNN untuk meningkatkan akurasi.
- Automatic disease recommendation (rekomendasi penanganan).

## Phase 3

- Realtime camera analysis (deteksi langsung dari kamera via WebRTC).
- Mobile AI inference.
- Multi plant detection (tanaman cabai, kentang, terong).

---

*Dokumen ini diperbarui berdasarkan kode aktual di `backend/app/core/model/` dan hasil clustering K-Means pada PlantVillage Tomato Dataset (4.952 sampel).*
