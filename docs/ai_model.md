# AI Model Documentation

## Tomato Leaf Health Detection Using Fuzzy Sugeno

Dokumentasi ini berdasarkan kode aktual di `backend/app/core/model/` dan data dari `model-reference/`.

---

## 1. Overview

Sistem mendeteksi kondisi kesehatan daun tomat dari citra gambar menggunakan **Fuzzy Sugeno Orde 0** dengan 16 aturan fuzzy. Sistem dikembangkan secara **data-driven** menggunakan **K-Means Clustering (k=4)** pada **4.952 sampel PlantVillage Tomato Dataset**.

### Fitur Sistem

| No | Fitur | Keterangan |
|---|---|---|
| 1 | Segmentasi daun | HSV green mask + largest contour |
| 2 | Ekstraksi fitur | 7 fitur visual |
| 3 | Fuzzy inference | 16 rules Sugeno Orde 0 |
| 4 | Severity score | Perhitungan berbobot 6 fitur |

---

## 2. Pipeline Flow

```
Input Image (JPG/JPEG/PNG)
    │
    ▼
┌─────────────────────────────────┐
│ segmenter.py                    │
│ 1. Resize256×256                │
│ 2. BGR → HSV                    │
│ 3. Green mask (HSV threshold)   │
│ 4. Morphological cleanup │
│ 5. Largest contour detection    │
└─────────────────────────────────┘
    │
    ▼ leaf_mask, masked_image
┌─────────────────────────────────┐
│ feature_extractor.py │
│ Ekstrak 7 fitur dari area daun  │
└─────────────────────────────────┘
    │
    ▼ features dict (7 keys)
┌─────────────────────────────────┐
│ fuzzy_engine.py                 │
│ 1. Fuzzification (Triangular MF)│
│ 2. Rule evaluation (16 rules)    │
│ 3. Defuzzification (weighted avg)│
│ 4. Classification │
│ 5. Severity score calculation   │
└─────────────────────────────────┘
    │
    ▼
Output: {plant_status, severity_level, fuzzy_score, severity_score, features}
```

---

## 3. Module Reference

| Module | Path | Fungsi |
|---|---|---|
| `pipeline.py` | `backend/app/core/model/pipeline.py` | Orchestrate full flow: segment → extract → infer → classify → severity |
| `segmenter.py` | `backend/app/core/model/segmenter.py` | Leaf segmentation via HSV green mask + largest contour |
| `feature_extractor.py` | `backend/app/core/model/feature_extractor.py` | Extract 7 visual features from segmented leaf |
| `fuzzy_engine.py` | `backend/app/core/model/fuzzy_engine.py` | Fuzzy inference engine + severity calculation |
| `config.py` | `backend/app/core/model/config.py` | Configuration: MF params, rules, weights, HSV ranges |

---

## 4. Image Processing

### Parameters (config.py)

| Parameter | Value |
|---|---|
| IMAGE_SIZE | (256, 256) |
| MORPH_KERNEL_SIZE | 5 |
| MORPH_CLOSE_ITERATIONS | 2 |
| MORPH_OPEN_ITERATIONS | 1 |

### HSV Ranges (config.py)

| Range | Lower | Upper | Purpose |
|---|---|---|---|
| GREEN_MASK | [35, 40, 40] | [90, 255, 255] | Detect leaf area |
| yellow | [20, 50, 50] | [35, 255, 255] | Klorosis detection |
| brown | [0, 20, 20] | [20, 255, 120] | Nekrosis detection |
| dark | [0, 0, 0] | [180, 255, 60] | Dark spot detection |
| spot | [0, 20, 20] | [40, 255, 180] | Combined spot detection |

### Segmentation Flow (segmenter.py)

1. **Read& resize** → 256×256
2. **BGR → HSV** conversion
3. **Green mask** → HSV threshold
4. **MORPH_CLOSE** → fill small holes (kernel 5×5 ellipse, 2 iterations)
5. **MORPH_OPEN** → remove small noise (kernel 5×5 ellipse, 1 iteration)
6. **Largest contour** → `cv2.findContours(RETR_EXTERNAL)` → fill with white
7. **Bitwise_and** → masked image (only leaf area)

### Fallback

Jika tidak ada kontur terdeteksi → gunakan seluruh area gambar sebagai leaf mask.

---

## 5. Feature Extraction

### 7 Features (feature_extractor.py)

| No | Feature | Unit | Formula | HSV Range |
|---|---|---|---|---|
| 1 | spot_area | % | (spot_pixels / leaf_pixels) × 100 | [0, 20, 20] - [40, 255, 180] |
| 2 | color_change | % | yellow_ratio + brown_ratio + dark_ratio | - |
| 3 | yellow_ratio | % | (yellow_pixels / leaf_pixels) × 100 | [20, 50, 50] - [35, 255, 255] |
| 4 | brown_ratio | % | (brown_pixels / leaf_pixels) × 100 | [0, 20, 20] - [20, 255, 120] |
| 5 | dark_ratio | % | (dark_pixels / leaf_pixels) × 100 | [0, 0, 0] - [180, 255, 60] |
| 6 | spot_count | count | count(contours with area ≥ 5) | - |
| 7 | texture_var | - | std(grayscale_pixels) | - |

### Feature Statistics (stats_6features.csv)

| Variable | Min | Max | Mean | Median | Std | P1 | P99 |
|---|---|---|---|---|---|---|---|
| spot_area | 0.00 | 81.99 | 13.23 | 11.08 | 11.48 | 0.06 | 48.48 |
| color_change | 0.00 | 136.45 | 28.24 | 23.98 | 21.89 | 0.19 | 99.79 |
| yellow_ratio | 0.00 | 100.00 | 14.81 | 6.58 | 20.15 | 0.00 | 93.63 |
| brown_ratio | 0.00 | 24.03 | 0.56 | 0.14 | 1.19 | 0.00 | 5.11 |
| spot_count | 0.00 | 1083.00 | 203.05 | 154.00 | 181.20 | 4.00 | 794.49 |
| texture_var | 9.47 | 67.01 | 33.07 | 32.08 | 10.51 | 14.96 | 56.86 |

---

## 6. Fuzzy Inference

### Input Variables

| Variable | Categories | Fuzzy Input |
|---|---|---|
| spot_area | small, medium, large, very_large | ✅ Used in inference |
| color_change | low, medium, high, very_high | ✅ Used in inference |
| yellow_ratio | - | ❌ Supporting feature only |
| brown_ratio | - | ❌ Supporting feature only |
| dark_ratio | - | ❌ Supporting feature only |
| spot_count | - | ❌ Supporting feature only |
| texture_var | - | ❌ Supporting feature only |

### Triangular Membership Function (fuzzy_engine.py)

```python
def triangular_mf(x, a, b, c):
    if x <= a or x >= c: return 0.0
    if a < x <= b: return (x - a) / (b - a)
    if b < x < c: return (c - x) / (c - b)
    return 0.0
```

### Membership Function Parameters (config.py)

#### Spot Area (%)

| Label | a | b | c |
|---|---|---|---|
| small | 0.06 | 3.23 | 8.36 |
| medium | 8.36 | 13.49 | 18.86 |
| large | 18.86 | 24.23 | 31.78 |
| very_large | 31.78 | 39.33 | 48.48 |

#### Color Change (%)

| Label | a | b | c |
|---|---|---|---|
| low | 0.19 | 8.05 | 16.86 |
| medium | 16.86 | 25.67 | 36.18 |
| high | 36.18 | 46.69 | 64.14 |
| very_high | 64.14 | 81.59 | 99.79 |

### Supporting MF Parameters (config.py)

#### Yellow Ratio (%)

| Label | a | b | c |
|---|---|---|---|
| low | 0.00 | 3.76 | 11.40 |
| medium | 11.40 | 19.03 | 32.01 |
| high | 32.01 | 44.99 | 62.14 |
| very_high | 62.14 | 79.29 | 93.63 |

#### Brown Ratio (%)

| Label | a | b | c |
|---|---|---|---|
| low | 0.00 | 0.12 | 0.51 |
| medium | 0.51 | 0.91 | 1.59 |
| high | 1.59 | 2.26 | 3.37 |
| very_high | 3.37 | 4.48 | 5.11 |

#### Spot Count

| Label | a | b | c |
|---|---|---|---|
| few | 4.00 | 16.33 | 30.46 |
| moderate | 30.46 | 44.60 | 58.27 |
| many | 58.27 | 71.95 | 85.74 |
| very_many | 85.74 | 99.54 | 100.00 |

#### Texture Variance

| Label | a | b | c |
|---|---|---|---|
| low | 14.96 | 20.06 | 24.53 |
| medium | 24.53 | 28.99 | 33.34 |
| high | 33.34 | 37.69 | 43.48 |
| very_high | 43.48 | 49.27 | 56.86 |

---

## 7. Fuzzy Rule Base

### 16 Rules (config.py)

Format: `(spot_area_category, color_change_category, output_constant)`

| Rule | Spot Area | Color Change | Output (k) | Interpretation |
|---|---|---|---|---|
| R1 | small | low | 100 | Healthy |
| R2 | small | medium | 90 | Healthy |
| R3 | small | high | 75 | Mild |
| R4 | small | very_high | 60 | Mild |
| R5 | medium | low | 85 | Healthy |
| R6 | medium | medium | 70 | Mild |
| R7 | medium | high | 55 | Moderate |
| R8 | medium | very_high | 40 | Moderate |
| R9 | large | low | 65 | Mild |
| R10 | large | medium | 50 | Moderate |
| R11 | large | high | 35 | Severe |
| R12 | large | very_high | 20 | Severe |
| R13 | very_large | low | 45 | Moderate |
| R14 | very_large | medium | 30 | Severe |
| R15 | very_large | high | 15 | Very Severe |
| R16 | very_large | very_high | 5 | Very Severe |

### Rule Matrix (4×4)

```
                 Color Change
           low      medium    high    very_high
            ↓         ↓        ↓          ↓
small    [100]      [ 90]    [ 75]      [ 60]
medium   [ 85]      [ 70]    [ 55]      [ 40]
large    [ 65]      [ 50]    [ 35]      [ 20]
very_large[ 45]     [ 30]    [ 15]      [  5]

↑                                    ↑
Healthy                      Very Severe
```

### Defuzzification Formula

```python
z = Σ(αi × ki) / Σαi

where:
  αi = min(μ_spot_area, μ_color_change)  # firing strength
  ki = output constant of rule i
  z = fuzzy score (0-100)
```

### Edge Cases

| Case | Handling |
|---|---|
| Σαi = 0 (no rules fired) | Return DEFAULT_FUZZY_SCORE = 50 |
| z < 0 | Clip to 0 |
| z > 100 | Clip to 100 |

---

## 8. Classification

### Output Classes (config.py)

| Fuzzy Score Range | Severity Level | Plant Status |
|---|---|---|
| 85 - 100 | Sehat | Sehat |
| 70 - 84 | Ringan | Terinfeksi |
| 50 - 69 | Sedang | Terinfeksi |
| 25 - 49 | Berat | Terinfeksi |
| 0 - 24 | Sangat Berat | Terinfeksi |

---

## 9. Severity Score Calculation

### Feature Weights (config.py)

| Feature | Weight |
|---|---|
| spot_area | 0.30 |
| color_change | 0.25 |
| brown_ratio | 0.15 |
| yellow_ratio | 0.10 |
| spot_count | 0.10 |
| texture_var | 0.10 |
| **Total** | **1.00** |

### Normalization Ranges - P99 (config.py)

| Feature | Min | Max |
|---|---|---|
| spot_area | 0.0 | 48.48 |
| color_change | 0.0 | 99.79 |
| yellow_ratio | 0.0 | 93.63 |
| brown_ratio | 0.0 | 5.11 |
| spot_count | 0.0 | 794.49 |
| texture_var | 0.0 | 56.86 |

### Normalization Formula

```python
normalized = ((value - min_val) / (max_val - min_val)) × 100
normalized = max(0.0, min(100.0, normalized))  # clip to [0, 100]
```

### Severity Score Formula

```python
severity_score = Σ(weight_i × normalized_i)
```

> **Note:** High severity_score = bad condition (high severity).
> Low severity_score = healthy condition.

---

## 10. Cluster Analysis

### Silhouette Scores (cluster_report_6features.csv)

| Variable | Silhouette (k=4) | Quality |
|---|---|---|
| spot_count | 0.8352 | ⭐ Best |
| brown_ratio | 0.7254 | Strong |
| yellow_ratio | 0.6647 | Good |
| spot_area | 0.5928 | Moderate |
| color_change | 0.5601 | Moderate |
| texture_var | 0.5537 | Moderate |

### Cluster Centers (cluster_report_6features.csv)

| Variable | small/few/low | medium/moderate | large/many/high | very_large/very_many/very_high |
|---|---|---|---|---|
| spot_area | 3.23 | 13.49 | 24.23 | 39.33 |
| color_change | 8.05 | 25.67 | 46.69 | 81.59 |
| yellow_ratio | 3.76 | 19.03 | 44.99 | 79.29 |
| brown_ratio | 0.12 | 0.91 | 2.26 | 4.48 |
| spot_count | 16.33 | 44.60 | 71.95 | 99.54 |
| texture_var | 20.06 | 28.99 | 37.69 | 49.27 |

---

## 11. Output Structure

### Pipeline Output (pipeline.py)

```python
{
    "plant_status": str,    # "Sehat" | "Terinfeksi"
    "severity_level": str,  # "Sehat" | "Ringan" | "Sedang" | "Berat" | "Sangat Berat"
    "fuzzy_score": float,   # 0-100 (Sugeno weighted average)
    "severity_score": float, # 0-100 (weighted feature calculation)
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

### Example Output

```json
{
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
```

---

## 12. API Integration

### POST /api/v2/predict

**Request:** `image` (file, multipart/form-data)
**Headers:** `Authorization: Bearer {token}`

**Response (200):**

```json
{
  "id": "uuid",
  "image_url": "https://storage.url/image.jpg",
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
  },
  "created_at": "2026-06-01T10:30:00Z"
}
```

### Database Schema (prediction_records)

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| user_id | UUID | Foreign key to users |
| image_url | String | Storage URL |
| spot_area | Numeric(5,2) | Feature |
| yellow_ratio | Numeric(5,2) | Feature |
| brown_ratio | Numeric(5,2) | Feature |
| dark_ratio | Numeric(5,2) | Feature |
| color_change | Numeric(5,2) | Feature |
| fuzzy_score | Numeric(5,2) | Fuzzy output |
| severity_score | Numeric(5,2) | Weighted severity |
| severity_level | String(50) | Classification |
| plant_status | String(50) | "Sehat" / "Terinfeksi" |
| created_at | DateTime | Timestamp |

---

## 13. Technology Stack

| Component | Technology | Version |
|---|---|---|
| Language | Python | 3.11+ |
| Image Processing | OpenCV | 4.9+ |
| Numerical | NumPy | 1.26+ |
| Image Format | Pillow | 10.0+ |
| API Framework | FastAPI | 0.x |
| Clustering | scikit-learn | - |

---

## 14. File Reference

### Source Code

| File | Path |
|---|---|
| Pipeline | `backend/app/core/model/pipeline.py` |
| Segmenter | `backend/app/core/model/segmenter.py` |
| Feature Extractor | `backend/app/core/model/feature_extractor.py` |
| Fuzzy Engine | `backend/app/core/model/fuzzy_engine.py` |
| Config | `backend/app/core/model/config.py` |

### Data Files

| File | Path | Description |
|---|---|---|
| Cluster Report | `model-reference/cluster_report_6features.csv` | Silhouette scores & cluster centers |
| Membership | `model-reference/membership_6features.csv` | MF parameters (a, b, c) |
| Statistics | `model-reference/stats_6features.csv` | Descriptive statistics |
| Features CSV | `model-reference/tomato_features_6.csv` | Raw extracted features |

### Scripts

| File | Path | Description |
|---|---|---|
| Dataset to CSV | `model-reference/dataset_to_csv_6features.py` | Extract features from dataset |
| CSV to Membership | `model-reference/csv_to_membership_6features.py` | K-Means clustering → MF params |

---

## 15. Known Limitations

1. **No disease identification** — System only outputs healthy/infected + severity level, not specific disease names (Early Blight, Late Blight, etc.)
2. **Python 3.14 incompatibility** — OpenCV may crash on Python 3.14; use Python 3.11+
3. **Lighting sensitivity** — Performance degrades with poor lighting conditions
4. **Single leaf detection** — Only detects the largest contour; may miss multiple leaves

---

*Dokumen ini berdasarkan kode aktual di `backend/app/core/model/` dan data di `model-reference/`.*
