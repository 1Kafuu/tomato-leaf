<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# Project: Tomato Leaf Health Detection App

## Overview

Aplikasi berbasis web untuk mendeteksi kesehatan daun tomat melalui analisis citra digital menggunakan metode **Fuzzy Sugeno Orde 0**. Pengguna mengunggah foto daun tomat, sistem melakukan segmentasi daun, ekstraksi fitur visual, inferensi fuzzy, dan menampilkan diagnosis penyakit.

Sistem dirujuk dari PRD: `docs/prd_tomato_leaf.md`

---

## Tech Stack

| Layer | Teknologi | Versi |
|---|---|---|
| Frontend | Next.js, TypeScript, Tailwind CSS, Axios | 16 / 5.x / 4.x / 1.x |
| Backend API | Python, FastAPI, Uvicorn | 3.14 / 0.x |
| Image Processing | OpenCV, NumPy, Pillow | 4.x / 1.x / 10.x |
| Fuzzy Engine | scikit-fuzzy (atau custom) | 0.x |
| Database | PostgreSQL / Supabase | 16 |
| Deployment | Vercel (FE) / Railway-Render (BE) | — |

---

## AI Model Specification

### Method

Fuzzy Sugeno Orde 0 — menggunakan Weighted Average defuzzification.

### Input Data

- **Format**: JPG, JPEG, PNG
- **Max Size**: 10 MB
- **Requirement**: Gambar jelas, fokus pada daun, pencahayaan cukup

### System Workflow (Saat Prediksi)

```
User Upload Image
→ Leaf Segmentation (HSV Green Mask + Largest Contour + Morphological Cleanup)
→ Feature Extraction (5 fitur)
→ Fuzzification (Triangular Membership Function)
→ Rule Evaluation (16 rules, operator AND/minimum)
→ Sugeno Inference Engine
→ Weighted Average Defuzzification
→ Disease Classification
→ Result Display
```

### Image Processing Pipeline

```
Input Image
→ Resize 256×256
→ RGB to HSV
→ Green Mask (HSV [35,40,40] – [90,255,255])
→ Morphological Cleanup (CLOSE + OPEN, kernel ellipse 5×5)
→ Largest Contour Detection
→ Leaf Mask (binary)
→ Hanya area daun yang diproses untuk ekstraksi fitur
```

### Features to Extract (5 fitur)

Semua fitur dihitung **hanya pada area daun hasil segmentasi** (background dihilangkan).

#### 1. Spot Area (%)
Persentase area bercak (coklat/kuning) terhadap total area daun.
```
spot_area = (spot_pixels / leaf_pixels) × 100
```
| Category | Range (K-Means) |
|---|---|
| Kecil | 0,06 – 8,35 (representatif: 3,22) |
| Sedang | 8,35 – 18,85 (representatif: 13,48) |
| Besar | 18,85 – 31,78 (representatif: 24,23) |
| Sangat Besar | 31,78 – 48,48 (representatif: 39,33) |

#### 2. Yellow Ratio (%)
Persentase area daun yang menunjukkan warna kuning (klorosis).
HSV range: [20, 50, 50] hingga [35, 255, 255]

#### 3. Brown Ratio (%)
Persentase area daun yang menunjukkan warna coklat (nekrosis).
HSV range: [0, 20, 20] hingga [20, 255, 120]

#### 4. Dark Ratio (%)
Persentase area daun yang menunjukkan warna gelap/hitam.
HSV range: [0, 0, 0] hingga [180, 255, 60]

#### 5. Color Change Severity (%)
Total perubahan warna daun: penjumlahan yellow + brown + dark ratio.
```
color_change = yellow_ratio + brown_ratio + dark_ratio
```
| Category | Range (K-Means) |
|---|---|
| Rendah | 0,19 – 16,86 (representatif: 8,05) |
| Sedang | 16,86 – 36,19 (representatif: 25,68) |
| Tinggi | 36,19 – 64,15 (representatif: 46,70) |
| Sangat Tinggi | 64,15 – 99,79 (representatif: 81,59) |

### Input Variables

| Variable | Kategori | Parameter Triangular (a, b, c) |
|---|---|---|
| Spot Area (%) | Kecil | (0,06, 3,22, 8,35) |
| Spot Area (%) | Sedang | (8,35, 13,48, 18,85) |
| Spot Area (%) | Besar | (18,85, 24,23, 31,78) |
| Spot Area (%) | Sangat Besar | (31,78, 39,33, 48,48) |
| Color Change (%) | Rendah | (0,19, 8,05, 16,86) |
| Color Change (%) | Sedang | (16,86, 25,68, 36,19) |
| Color Change (%) | Tinggi | (36,19, 46,70, 64,15) |
| Color Change (%) | Sangat Tinggi | (64,15, 81,59, 99,79) |

Membership function: **Triangular** dengan parameter:
- **a** = Batas Awal (nilai minimum kategori mulai aktif)
- **b** = Nilai Representatif (pusat cluster K-Means, derajat=1)
- **c** = Batas Akhir (nilai maksimum kategori)

### Output Classes

| Output | Rentang Skor |
|---|---|
| Sangat Sehat | 90 – 100 |
| Sehat | 75 – 89 |
| Early Blight Ringan | 60 – 74 |
| Late Blight | 45 – 59 |
| Leaf Mold | 25 – 44 |
| Septoria Leaf Spot | 10 – 24 |
| Sangat Buruk | 0 – 9 |

### Supported Disease Classes

| Class |
|---|
| Healthy |
| Early Blight |
| Late Blight |
| Leaf Mold |
| Septoria Leaf Spot |

### Fuzzy Rules (16 rules)

| Rule | IF Spot Area | AND Color Change | THEN | Konstanta (k) |
|---|---|---|---|---|
| R1 | Kecil | Rendah | Sangat Sehat | 100 |
| R2 | Kecil | Sedang | Sehat | 90 |
| R3 | Kecil | Tinggi | Early Blight Ringan | 80 |
| R4 | Kecil | Sangat Tinggi | Leaf Mold | 40 |
| R5 | Sedang | Rendah | Sehat | 85 |
| R6 | Sedang | Sedang | Early Blight Sedang | 70 |
| R7 | Sedang | Tinggi | Late Blight | 55 |
| R8 | Sedang | Sangat Tinggi | Leaf Mold | 40 |
| R9 | Besar | Rendah | Early Blight Sedang | 70 |
| R10 | Besar | Sedang | Late Blight | 55 |
| R11 | Besar | Tinggi | Septoria Leaf Spot | 20 |
| R12 | Besar | Sangat Tinggi | Sangat Buruk | 10 |
| R13 | Sangat Besar | Rendah | Late Blight | 50 |
| R14 | Sangat Besar | Sedang | Septoria Leaf Spot | 20 |
| R15 | Sangat Besar | Tinggi | Sangat Buruk | 10 |
| R16 | Sangat Besar | Sangat Tinggi | Sangat Buruk | 5 |

### Defuzzification

Weighted Average Sugeno Orde 0:
```
z = Σ(αi × ki) / Σαi
```
- αi = firing strength (min dari derajat keanggotaan)
- ki = konstanta output rule
- z = output akhir (fuzzy score, 0–100)

Penanganan khusus:
- Jika Σαi = 0 → output default = 50
- Jika z < 0 → clipping ke 0
- Jika z > 100 → clipping ke 100

### Performance Requirements

| Requirement | Target |
|---|---|
| Response Time | < 5 detik |
| Classification Accuracy | ≥ 80% |
| Max Upload Size | 10 MB |
| Uptime | ≥ 95% |

### API Integration

#### POST /predict
- **Request**: `image` (file, multipart/form-data)
- **Headers**: `Authorization: Bearer {token}`
- **Response**:
```json
{
  "success": true,
  "message": "Prediksi berhasil",
  "data": {
    "disease_name": "Early Blight",
    "fuzzy_score": 71.25,
    "severity_level": "Ringan",
    "plant_status": "Terinfeksi",
    "features": {
      "spot_area": 12.34,
      "color_change": 30.50,
      "yellow_ratio": 15.20,
      "brown_ratio": 2.80,
      "dark_ratio": 12.50
    }
  }
}
```

#### GET /history
- **Headers**: `Authorization: Bearer {token}`
- **Query**: `page`, `limit`, `sort`
- **Response**: Array riwayat prediksi + pagination

#### GET /history/{id}
- **Headers**: `Authorization: Bearer {token}`
- **Response**: Detail prediksi (semua fitur + gambar)

---

## Features (MVP)

### P0: Must Have
- [x] Upload gambar daun tomat (JPG/JPEG/PNG, ≤10 MB)
- [x] Segmentasi daun (HSV Green Mask + Largest Contour)
- [x] Ekstraksi fitur (5 fitur: spot_area, yellow_ratio, brown_ratio, dark_ratio, color_change)
- [x] Fuzzy Sugeno inference (16 rules + weighted average)
- [x] Result page (nama penyakit, skor fuzzy, tingkat keparahan)
- [ ] Basic authentication (register + login JWT)
- [ ] Responsive UI (mobile-first)

### P1: Should Have
- [ ] Detection history (paginated, dengan detail)
- [ ] Fuzzy score visualization

### P2: Could Have
- [ ] Admin dashboard (statistik penggunaan)

### Won't Have
- Realtime camera detection
- Multi plant detection
- IoT integration
- Mobile native app
- Offline prediction

---

## UI Pages

| Page | Deskripsi |
|---|---|
| Landing Page | Hero + Fitur + Cara Kerja + CTA "Mulai Deteksi" |
| Login | Form email + password |
| Register | Form nama + email + password |
| Dashboard | Upload area (drag & drop) + preview + result card |
| History | Tabel riwayat prediksi + pagination |
| Detail History | Detail prediksi + gambar ukuran besar |

---

## Database Schema

### users
| Column | Type | Constraint |
|---|---|---|
| id | UUID | PK, DEFAULT gen_random_uuid() |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | NOT NULL |
| full_name | VARCHAR(100) | NOT NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

### prediction_history
| Column | Type | Constraint |
|---|---|---|
| id | UUID | PK, DEFAULT gen_random_uuid() |
| user_id | UUID | FK → users.id, NOT NULL |
| image_name | VARCHAR(255) | NOT NULL |
| image_data | BYTEA | NOT NULL |
| spot_area | DECIMAL(5,2) | NOT NULL |
| yellow_ratio | DECIMAL(5,2) | NOT NULL |
| brown_ratio | DECIMAL(5,2) | NOT NULL |
| dark_ratio | DECIMAL(5,2) | NOT NULL |
| color_change | DECIMAL(5,2) | NOT NULL |
| fuzzy_score | DECIMAL(5,2) | NOT NULL |
| disease_name | VARCHAR(50) | NOT NULL |
| severity_level | VARCHAR(20) | NOT NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |

---

## Dataset Reference

| Kelas | Jumlah Gambar |
|---|---|
| Healthy | 1.000 |
| Early Blight | 1.000 |
| Late Blight | 1.000 |
| Septoria Leaf Spot | 1.000 |
| Leaf Mold | 952 |
| **Total** | **4.952** |

Dataset PlantVillage digunakan untuk:
1. Pembentukan membership function (K-Means clustering)
2. Evaluasi akurasi sistem

---

## Script Reference

| Script | Path | Fungsi |
|---|---|---|
| dataset_to_csv.py | `model-reference/dataset_to_csv.py` | Ekstraksi fitur dari dataset → CSV |
| csv_to_membership_new.py | `model-reference/csv_to_membership_new.py` | K-Means clustering → parameter membership |
| membership_kmeans.csv | `model-reference/membership_kmeans.csv` | Parameter triangular MF (a, b, c) |
| feature_statistics.csv | `model-reference/feature_statistics.csv` | Statistik deskriptif per fitur |

---

## Development Priority (Timeline 4 Minggu)

| Minggu | Fokus |
|---|---|
| 1 | Foundation: requirement, setup proyek, dataset, UI wireframe |
| 2 | Core Logic: image processing, ekstraksi fitur, fuzzy inference |
| 3 | Integration: API endpoints, frontend pages, integrasi FE↔BE |
| 4 | Finalization: optimasi, deployment, testing, dokumentasi |
