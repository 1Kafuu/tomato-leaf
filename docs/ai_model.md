# AI Model Requirement Document

## Project Name

Tomato Leaf Health Detection System Using Fuzzy Sugeno

---

# AI Module Overview

Modul AI bertugas melakukan analisis kondisi daun tomat berdasarkan citra gambar daun menggunakan metode Fuzzy Sugeno orde 0.

Sistem melakukan:
1. Preprocessing gambar.
2. Ekstraksi fitur daun.
3. Fuzzifikasi parameter.
4. Evaluasi fuzzy rules.
5. Defuzzifikasi Sugeno.
6. Penentuan kondisi kesehatan daun.

---

# AI Objectives

## Main Objectives

- Mengidentifikasi kondisi kesehatan daun tomat.
- Mengklasifikasikan tingkat penyakit berdasarkan parameter visual.
- Memberikan output diagnosis berbasis fuzzy logic.

## Expected Output

- Nama kondisi daun.
- Nilai fuzzy akhir.
- Tingkat kesehatan tanaman.

---

# AI Scope

## Included

- Image preprocessing
- Spot area calculation
- Color change analysis
- Fuzzy Sugeno inference
- Disease classification

## Excluded

- Deep learning classification
- Realtime video detection
- Multi plant classification
- Disease treatment recommendation

---

# Input Data Requirement

## Input Type

Image daun tomat.

## Supported Format

- JPG
- JPEG
- PNG

## Image Requirement

- Gambar jelas.
- Fokus pada daun.
- Pencahayaan cukup.
- Background tidak terlalu kompleks.

## Maximum File Size

10 MB

---

# Dataset Requirement

## Dataset Source

PlantVillage Tomato Dataset

## Dataset Usage

Dataset digunakan untuk:
- Referensi kondisi penyakit.
- Pengujian sistem fuzzy.
- Kalibrasi parameter fuzzy.

## Supported Disease Classes

| Class |
|---|
| Healthy |
| Early Blight |
| Late Blight |
| Leaf Mold |
| Septoria Leaf Spot |
| Severe Damage |

---

# Image Processing Requirement

## Preprocessing

Tahapan preprocessing:
1. Resize image
2. Noise reduction
3. Color normalization
4. Image segmentation

## Recommended Library

- OpenCV
- NumPy
- Pillow

---

# Feature Extraction Requirement

## Feature 1: Spot Area Percentage

### Description

Menghitung persentase luas bercak penyakit terhadap total area daun.

### Formula

Spot Area Percentage = (Spot Area / Leaf Area) × 100%

### Membership Range

| Category | Range |
|---|---|
| Kecil | 0% – 20% |
| Sedang | 21% – 40% |
| Besar | 41% – 70% |
| Sangat Besar | > 70% |

---

## Feature 2: Color Change Percentage

### Description

Menghitung tingkat perubahan warna daun dari hijau normal menuju warna abnormal.

### Formula

Color Change Percentage = (Abnormal Color Pixels / Total Leaf Pixels) × 100%

### Membership Range

| Category | Range |
|---|---|
| Rendah | 0% – 20% |
| Sedang | 21% – 40% |
| Tinggi | 41% – 70% |
| Sangat Tinggi | > 70% |

---

# Fuzzy Sugeno Requirement

## Method

Fuzzy Sugeno Orde 0

## Input Variables

| Variable | Membership |
|---|---|
| Luas Bercak | Kecil, Sedang, Besar, Sangat Besar |
| Perubahan Warna | Rendah, Sedang, Tinggi, Sangat Tinggi |

## Output Variable

| Output |
|---|
| Sangat Sehat |
| Sehat |
| Early Blight Ringan |
| Late Blight |
| Leaf Mold |
| Septoria Leaf Spot |
| Sangat Buruk |

---

# Fuzzy Rule Base

Total rules: 16

| Rule | Kondisi IF | Output THEN | Konstanta |
|---|---|---|---|
| R1 | Luas Bercak Kecil AND Perubahan Warna Rendah | Sangat Sehat | 100 |
| R2 | Luas Bercak Kecil AND Perubahan Warna Sedang | Sehat | 90 |
| R3 | Luas Bercak Kecil AND Perubahan Warna Tinggi | Early Blight Ringan | 80 |
| R4 | Luas Bercak Kecil AND Perubahan Warna Sangat Tinggi | Leaf Mold | 40 |
| R5 | Luas Bercak Sedang AND Perubahan Warna Rendah | Sehat | 85 |
| R6 | Luas Bercak Sedang AND Perubahan Warna Sedang | Early Blight Sedang | 70 |
| R7 | Luas Bercak Sedang AND Perubahan Warna Tinggi | Late Blight | 55 |
| R8 | Luas Bercak Sedang AND Perubahan Warna Sangat Tinggi | Leaf Mold | 40 |
| R9 | Luas Bercak Besar AND Perubahan Warna Rendah | Early Blight Sedang | 70 |
| R10 | Luas Bercak Besar AND Perubahan Warna Sedang | Late Blight | 55 |
| R11 | Luas Bercak Besar AND Perubahan Warna Tinggi | Septoria Leaf Spot | 20 |
| R12 | Luas Bercak Besar AND Perubahan Warna Sangat Tinggi | Sangat Buruk | 10 |
| R13 | Luas Bercak Sangat Besar AND Perubahan Warna Rendah | Late Blight | 50 |
| R14 | Luas Bercak Sangat Besar AND Perubahan Warna Sedang | Septoria Leaf Spot | 20 |
| R15 | Luas Bercak Sangat Besar AND Perubahan Warna Tinggi | Sangat Buruk | 10 |
| R16 | Luas Bercak Sangat Besar AND Perubahan Warna Sangat Tinggi | Sangat Buruk | 5 |

---

# Defuzzification Requirement

Metode defuzzifikasi menggunakan Weighted Average Sugeno.

z = Σ(αi × ki) / Σαi

Keterangan:
- αi = firing strength
- ki = konstanta rule
- z = output akhir

---

# Output Interpretation

| Range | Classification |
|---|---|
| 90 – 100 | Sangat Sehat |
| 75 – 89 | Sehat |
| 60 – 74 | Early Blight Ringan |
| 45 – 59 | Late Blight |
| 25 – 44 | Leaf Mold |
| 10 – 24 | Septoria Leaf Spot |
| 0 – 9 | Sangat Buruk |

---

# AI Performance Requirement

| Requirement | Target |
|---|---|
| Response Time | < 5 detik |
| Classification Accuracy | ≥ 80% |
| Error Rate | < 10% |

---

# AI Architecture

## Flow

1. User upload image.
2. API menerima gambar.
3. Preprocessing citra.
4. Segmentasi daun.
5. Ekstraksi fitur.
6. Fuzzification.
7. Rule evaluation.
8. Defuzzification Sugeno.
9. Return diagnosis result.

---

# API Integration Requirement

## POST /predict

### Request
- image

### Response

```json
{
  "disease_name": "Late Blight",
  "fuzzy_score": 56,
  "plant_status": "Late Blight"
}
```

---

# AI Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Image Processing | OpenCV |
| Numerical Computation | NumPy |
| Fuzzy Logic | scikit-fuzzy |
| API Framework | FastAPI |

---

# AI Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Segmentasi daun gagal | Gunakan preprocessing dan thresholding |
| Rule fuzzy kurang akurat | Kalibrasi membership function |
| Pencahayaan gambar buruk | Tambahkan validasi input image |
| Noise gambar tinggi | Terapkan noise reduction |

---

# Future Improvement

## Phase 2

- Adaptive fuzzy membership
- Hybrid fuzzy + CNN
- Automatic disease recommendation

## Phase 3

- Realtime camera analysis
- Mobile AI inference
- Multi plant detection

