# AI Model Requirement Document

## Project Name

Tomato Leaf Health Detection System Using Fuzzy Sugeno

---

# AI Module Overview

Modul AI bertugas melakukan analisis kondisi daun tomat berdasarkan citra gambar daun menggunakan metode **Fuzzy Sugeno Orde 0** dengan 16 aturan fuzzy. Sistem dikembangkan secara **data-driven** menggunakan **K-Means Clustering (k=4)** pada **4.952 sampel PlantVillage Tomato Dataset** untuk menentukan parameter membership function.

Sistem melakukan:
1. Preprocessing gambar (resize 256×256, konversi RGB ke HSV).
2. Segmentasi daun (HSV Green Mask + Largest Contour + Morphological Cleanup).
3. Ekstraksi fitur (5 fitur visual: spot_area, yellow_ratio, brown_ratio, dark_ratio, color_change).
4. Fuzzifikasi parameter (Triangular Membership Function).
5. Evaluasi fuzzy rules (16 rules dengan operator AND/minimum).
6. Defuzzifikasi Sugeno (Weighted Average).
7. Penentuan kondisi kesehatan daun.

---

# AI Objectives

## Main Objectives

- Mengidentifikasi kondisi kesehatan daun tomat berdasarkan citra digital.
- Mengklasifikasikan tingkat penyakit menggunakan 2 variabel input fuzzy: Spot Area dan Color Change.
- Memberikan output diagnosis berbasis fuzzy logic dengan skor numerik (0–100).

## Expected Output

- Nama kondisi daun (6 kelas penyakit + sehat).
- Nilai fuzzy akhir (weighted average score).
- Tingkat kesehatan tanaman (severity level).
- Status tanaman (Sehat/Terinfeksi).
- 5 nilai fitur visual hasil ekstraksi.

---

# AI Scope

## Included

- Image preprocessing (resize, konversi warna, normalisasi).
- Leaf segmentation (HSV green masking, morphological cleanup, contour detection).
- Feature extraction (spot_area, yellow_ratio, brown_ratio, dark_ratio, color_change).
- Fuzzy Sugeno inference (fuzzifikasi, rule evaluation, defuzzifikasi).
- Disease classification (6 kelas penyakit + sehat).

## Excluded

- Deep learning / CNN classification.
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
| Healthy | 1.000 |
| Early Blight | 1.000 |
| Late Blight | 1.000 |
| Septoria Leaf Spot | 1.000 |
| Leaf Mold | 952 |
| **Total** | **4.952** |

## Dataset Usage

| Kegunaan | Deskripsi |
|---|---|
| **Pembentukan Membership Function** | Seluruh 4.952 gambar diekstrak fiturnya, kemudian dianalisis menggunakan K-Means Clustering (k=4) untuk menentukan pusat cluster sebagai parameter Triangular Membership Function. |
| **Evaluasi Sistem** | Dataset digunakan untuk menguji akurasi sistem dalam mengklasifikasikan penyakit daun tomat (target ≥ 80%). |
| **Validasi Parameter** | Parameter fuzzy (rule base, konstanta Sugeno) divalidasi menggunakan subset data uji. |

## Supported Disease Classes

| Class |
|---|
| Healthy |
| Early Blight |
| Late Blight |
| Leaf Mold |
| Septoria Leaf Spot |

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

Sistem mengekstrak **5 fitur numerik** dari area daun hasil segmentasi. Seluruh fitur dihitung sebagai persentase terhadap total area daun.

## Daftar Fitur

| No | Fitur | Satuan | Deskripsi |
|---|---|---|---|
| 1 | **spot_area** | % | Persentase area daun yang tertutup bercak (warna coklat/kuning) |
| 2 | **yellow_ratio** | % | Persentase area daun yang menunjukkan warna kuning (klorosis) |
| 3 | **brown_ratio** | % | Persentase area daun yang menunjukkan warna coklat (nekrosis) |
| 4 | **dark_ratio** | % | Persentase area daun yang menunjukkan warna gelap/hitam |
| 5 | **color_change** | % | Total perubahan warna daun: yellow_ratio + brown_ratio + dark_ratio |

## Definisi Matematis

### Spot Area

```
spot_area = (spot_pixels / leaf_pixels) × 100
```

Rentang HSV untuk deteksi bercak: `[0, 20, 20]` hingga `[40, 255, 180]`

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

### Color Change Severity

```
color_change = yellow_ratio + brown_ratio + dark_ratio
```

## Input Variables untuk Fuzzy Inference

Sistem hanya menggunakan **2 variabel input** untuk inferensi fuzzy:

| Variabel | Satuan | Rentang Data (P1–P99) | Deskripsi |
|---|---|---|---|
| **Spot Area** | % | 0,06 – 48,48 | Persentase luas bercak terhadap total area daun |
| **Color Change** | % | 0,19 – 99,79 | Total perubahan warna (yellow + brown + dark) |

> **Catatan:** Yellow Ratio, Brown Ratio, dan Dark Ratio merupakan fitur pendukung yang dihitung dan disimpan dalam riwayat prediksi, namun tidak digunakan langsung sebagai input fuzzy. Ketiganya berkontribusi pada perhitungan Color Change.

---

# Feature Statistics

Statistik deskriptif dari seluruh fitur yang diekstrak dari 4.952 sampel PlantVillage Dataset.

## Tabel Statistik

| Variable | Min | Max | Mean | Median | Std | P1 | P99 |
|---|---|---|---|---|---|---|---|
| spot_area | 0,00 | 81,99 | 13,23 | 11,08 | 11,48 | 0,06 | 48,48 |
| color_change | 0,00 | 136,45 | 28,24 | 23,98 | 21,89 | 0,19 | 99,79 |
| yellow_ratio | 0,00 | 100,00 | 14,81 | 6,59 | 20,15 | 0,00 | 93,63 |
| brown_ratio | 0,00 | 24,03 | 0,56 | 0,14 | 1,19 | 0,00 | 5,10 |
| dark_ratio | 0,00 | 81,99 | 12,87 | 10,68 | 11,42 | 0,01 | 48,27 |

## Insight

- **Spot Area** memiliki distribusi yang menceng ke kanan (mean 13,23 > median 11,08), menunjukkan mayoritas sampel memiliki bercak kecil.
- **Brown Ratio** memiliki nilai sangat rendah (mean 0,56%, max 24,03%), mengindikasikan bahwa warna coklat murni relatif jarang ditemukan.
- **Yellow Ratio** memiliki variasi sangat tinggi (std 20,15), menunjukkan klorosis sangat bervariasi antar sampel.
- **Color Change** memiliki nilai maksimum 136,45% (teoritis bisa >100% karena merupakan penjumlahan 3 rasio yang tumpang tindih).

---

# Cluster Analysis

Parameter membership function ditentukan menggunakan **K-Means Clustering (k=4)** pada data fitur yang telah diekstrak.

## Silhouette Score

Silhouette score digunakan untuk mengevaluasi kualitas clustering.

| Variable | Best K | Silhouette (k=4) | Silhouette (Best) |
|---|---|---|---|
| spot_area | 4 | 0,5928 | 0,6134 |
| color_change | 4 | 0,5602 | 0,6219 |
| yellow_ratio | 4 | 0,6646 | 0,7741 |
| brown_ratio | 4 | 0,7255 | 0,8143 |
| dark_ratio | 4 | 0,5919 | 0,6162 |

**Interpretasi:** Seluruh variabel memiliki silhouette score > 0,5 pada k=4, mengindikasikan struktur cluster yang cukup baik (reasonable structure).

## Cluster Centers

Pusat cluster (nilai representatif) setelah diurutkan dari nilai terkecil ke terbesar.

### Spot Area

| Cluster | Label | Center Value |
|---|---|---|
| Cluster 0 | Kecil | 3,22% |
| Cluster 1 | Sedang | 13,48% |
| Cluster 2 | Besar | 24,23% |
| Cluster 3 | Sangat Besar | 39,33% |

### Color Change

| Cluster | Label | Center Value |
|---|---|---|
| Cluster 0 | Rendah | 8,05% |
| Cluster 1 | Sedang | 25,68% |
| Cluster 2 | Tinggi | 46,70% |
| Cluster 3 | Sangat Tinggi | 81,59% |

### Yellow Ratio

| Cluster | Label | Center Value |
|---|---|---|
| Cluster 0 | Rendah | 3,76% |
| Cluster 1 | Sedang | 19,03% |
| Cluster 2 | Tinggi | 44,99% |
| Cluster 3 | Sangat Tinggi | 79,29% |

### Brown Ratio

| Cluster | Label | Center Value |
|---|---|---|
| Cluster 0 | Rendah | 0,12% |
| Cluster 1 | Sedang | 0,92% |
| Cluster 2 | Tinggi | 2,28% |
| Cluster 3 | Sangat Tinggi | 4,48% |

### Dark Ratio

| Cluster | Label | Center Value |
|---|---|---|
| Cluster 0 | Rendah | 2,84% |
| Cluster 1 | Sedang | 12,57% |
| Cluster 2 | Tinggi | 23,21% |
| Cluster 3 | Sangat Tinggi | 38,63% |

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

| Kategori | Batas Awal (a) | Nilai Representatif (b) | Batas Akhir (c) |
|---|---|---|---|
| Kecil | 0,06 | 3,22 | 8,35 |
| Sedang | 8,35 | 13,48 | 18,85 |
| Besar | 18,85 | 24,23 | 31,78 |
| Sangat Besar | 31,78 | 39,33 | 48,48 |

**Interpretasi Klinis:**

| Kategori | Rentang (%) | Makna Biologis |
|---|---|---|
| Kecil | 0,06 – 8,35 | Daun sehat dengan sedikit atau tanpa bercak |
| Sedang | 8,35 – 18,85 | Mulai muncul bercak, tahap awal infeksi |
| Besar | 18,85 – 31,78 | Bercak menyebar, infeksi cukup parah |
| Sangat Besar | 31,78 – 48,48 | Bercak dominan, infeksi sangat parah |

## Variabel Input 2: Color Change Severity (%)

| Kategori | Batas Awal (a) | Nilai Representatif (b) | Batas Akhir (c) |
|---|---|---|---|
| Rendah | 0,19 | 8,05 | 16,86 |
| Sedang | 16,86 | 25,68 | 36,19 |
| Tinggi | 36,19 | 46,70 | 64,15 |
| Sangat Tinggi | 64,15 | 81,59 | 99,79 |

**Interpretasi Klinis:**

| Kategori | Rentang (%) | Makna Biologis |
|---|---|---|
| Rendah | 0,19 – 16,86 | Daun dominan hijau, sedikit atau tanpa perubahan warna |
| Sedang | 16,86 – 36,19 | Mulai muncul klorosis (kuning) pada beberapa area |
| Tinggi | 36,19 – 64,15 | Perubahan warna signifikan, daun mulai mengering |
| Sangat Tinggi | 64,15 – 99,79 | Daun mengalami perubahan warna masif, hampir tidak tersisa jaringan hijau |

## Variabel Pendukung: Yellow Ratio (%)

| Kategori | Batas Awal (a) | Nilai Representatif (b) | Batas Akhir (c) |
|---|---|---|---|
| Rendah | 0,00 | 3,76 | 11,40 |
| Sedang | 11,40 | 19,03 | 32,01 |
| Tinggi | 32,01 | 44,99 | 62,14 |
| Sangat Tinggi | 62,14 | 79,29 | 93,63 |

## Variabel Pendukung: Brown Ratio (%)

| Kategori | Batas Awal (a) | Nilai Representatif (b) | Batas Akhir (c) |
|---|---|---|---|
| Rendah | 0,00 | 0,12 | 0,52 |
| Sedang | 0,52 | 0,92 | 1,60 |
| Tinggi | 1,60 | 2,28 | 3,38 |
| Sangat Tinggi | 3,38 | 4,48 | 5,10 |

## Variabel Pendukung: Dark Ratio (%)

| Kategori | Batas Awal (a) | Nilai Representatif (b) | Batas Akhir (c) |
|---|---|---|---|
| Rendah | 0,01 | 2,84 | 7,70 |
| Sedang | 7,70 | 12,57 | 17,89 |
| Tinggi | 17,89 | 23,21 | 30,92 |
| Sangat Tinggi | 30,92 | 38,63 | 48,27 |

---

# Fuzzy Sugeno Method

## Method

**Fuzzy Sugeno Orde 0** — menggunakan konstanta output (orde 0) sehingga perhitungan defuzzifikasi menggunakan weighted average.

## Input Variables (Fuzzy Inference)

| Variable | Membership Categories |
|---|---|
| Spot Area | Kecil, Sedang, Besar, Sangat Besar |
| Color Change | Rendah, Sedang, Tinggi, Sangat Tinggi |

## Output Variable

| Output Classes |
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

## Matriks Rule Base (4 × 4)

```
                      Color Change
              Rendah   Sedang   Tinggi   S.Tinggi
                ↓        ↓        ↓         ↓
   Kecil    → [100]    [ 90]    [ 80]     [ 40]
   Sedang    → [ 85]    [ 70]    [ 55]     [ 40]
   Besar     → [ 70]    [ 55]    [ 20]     [ 10]
 S.Besar     → [ 50]    [ 20]    [ 10]     [  5]

              ↑                        ↑
         Output tertinggi         Output terendah
         (Sangat Sehat)           (Sangat Buruk)
```

**Pola Umum:**
- Semakin kecil bercak dan perubahan warna → output semakin tinggi (sehat)
- Semakin besar bercak dan perubahan warna → output semakin rendah (sakit parah)
- Kombinasi bercak kecil dengan perubahan warna tinggi mengindikasikan Leaf Mold
- Kombinasi bercak besar/sedang dengan perubahan warna sedang/tinggi mengindikasikan Late Blight atau Septoria

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

## Contoh Perhitungan

**Diketahui:**
- Input: `spot_area = 12%`, `color_change = 30%`

**Aturan yang aktif (setelah fuzzifikasi):**

| Rule | αi (firing strength) | ki (konstanta) | αi × ki |
|---|---|---|---|
| R2 | 0,30 | 90 | 27,00 |
| R3 | 0,20 | 80 | 16,00 |
| R6 | 0,70 | 70 | 49,00 |
| R7 | 0,40 | 55 | 22,00 |

| Σαi | Σ(αi × ki) | z |
|---|---|---|
| 1,60 | 114,00 | **71,25** |

**Hasil:** `z = 71,25` → diklasifikasikan sebagai **Early Blight Ringan** (60–74)

## Penanganan Kasus Khusus

| Skenario | Penanganan |
|---|---|
| Σαi = 0 (tidak ada aturan aktif) | Output default = 50 |
| z < 0 | Clipping ke 0 |
| z > 100 | Clipping ke 100 |

---

# Output Classification

Output numerik hasil defuzzifikasi (z) diklasifikasikan ke dalam kategori penyakit berdasarkan rentang nilai.

## Tabel Klasifikasi

| Rentang Skor | Klasifikasi Penyakit | Deskripsi |
|---|---|---|
| 90 – 100 | **Sangat Sehat** | Daun dalam kondisi optimal, hijau segar, tanpa gejala penyakit |
| 75 – 89 | **Sehat** | Daun sehat dengan sedikit variasi warna normal |
| 60 – 74 | **Early Blight Ringan** | Gejala awal Early Blight: bercak kecil coklat pada daun bawah |
| 45 – 59 | **Late Blight** | Gejala Late Blight: bercak tidak beraturan, tepi daun mengering |
| 25 – 44 | **Leaf Mold** | Gejala Leaf Mold: perubahan warna kuning masif, bercak halus |
| 10 – 24 | **Septoria Leaf Spot** | Gejala Septoria: bercak bulat kecil dengan tepi gelap |
| 0 – 9 | **Sangat Buruk** | Kerusakan daun sangat parah, hampir tidak ada jaringan sehat |

## Output yang Ditampilkan ke Pengguna

| Field | Tipe | Contoh |
|---|---|---|
| disease_name | string | "Early Blight" |
| fuzzy_score | float | 71,25 |
| severity_level | string | "Ringan" |
| plant_status | string | "Terinfeksi" |
| features | object | {spot_area, color_change, yellow_ratio, brown_ratio, dark_ratio} |

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

**Response (Error — 400):**
```json
{
  "success": false,
  "message": "Format file tidak didukung",
  "error_code": "INVALID_FILE_FORMAT"
}
```

## GET /history

**Headers:** `Authorization: Bearer {token}`
**Query:** `page`, `limit`, `sort`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "image_name": "daun_tomat.jpg",
      "disease_name": "Early Blight",
      "fuzzy_score": 71.25,
      "severity_level": "Ringan",
      "created_at": "2026-06-01T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 45,
    "total_pages": 5
  }
}
```

## GET /history/{id}

**Headers:** `Authorization: Bearer {token}`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "image_name": "daun_tomat.jpg",
    "image_url": "https://api.domain.com/images/uuid.jpg",
    "spot_area": 12.34,
    "color_change": 30.50,
    "yellow_ratio": 15.20,
    "brown_ratio": 2.80,
    "dark_ratio": 12.50,
    "fuzzy_score": 71.25,
    "disease_name": "Early Blight",
    "severity_level": "Ringan",
    "plant_status": "Terinfeksi",
    "created_at": "2026-06-01T10:30:00Z"
  }
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

1. User upload image.
2. API menerima gambar.
3. Resize 256×256 + konversi RGB ke HSV.
4. Segmentasi daun (HSV Green Mask + Largest Contour + Morphological Cleanup).
5. Ekstraksi fitur (5 fitur: spot_area, yellow_ratio, brown_ratio, dark_ratio, color_change).
6. Fuzzification (Triangular MF untuk Spot Area dan Color Change).
7. Rule evaluation (16 rules, operator AND/minimum).
8. Sugeno Inference Engine.
9. Weighted Average Defuzzification.
10. Disease Classification.
11. Return diagnosis result.

---

# AI Technology Stack

| Component | Technology | Version |
|---|---|---|
| Programming Language | Python | 3.14 |
| Image Processing | OpenCV | 4.x |
| Numerical Computation | NumPy | 1.x |
| Image Format Handling | Pillow | 10.x |
| Fuzzy Logic | scikit-fuzzy (atau custom engine) | 0.x |
| API Framework | FastAPI | 0.x |
| Clustering (pengembangan) | scikit-learn (K-Means) | — |

---

# Script Reference

| Script | Path | Fungsi |
|---|---|---|
| dataset_to_csv.py | `model-reference/dataset_to_csv.py` | Ekstraksi fitur dari dataset PlantVillage → CSV |
| csv_to_membership_new.py | `model-reference/csv_to_membership_new.py` | K-Means Clustering → parameter Triangular MF |
| membership_kmeans.csv | `model-reference/membership_kmeans.csv` | Parameter Triangular MF (a, b, c) untuk seluruh fitur |
| feature_statistics.csv | `model-reference/feature_statistics.csv` | Statistik deskriptif per fitur (min, max, mean, median, std, P1, P99) |
| cluster_report.csv | `model-reference/cluster_report.csv` | Silhouette score dan pusat cluster K-Means |

## Code Reference (Production)

| Module | Path | Fungsi |
|---|---|---|
| `pipeline.py` | `backend/app/core/model/pipeline.py` | Orchestrates full prediction flow: segment → extract → fuzzy inference |
| `segmenter.py` | `backend/app/core/model/segmenter.py` | Leaf segmentation via HSV green mask + largest contour |
| `feature_extractor.py` | `backend/app/core/model/feature_extractor.py` | Extracts 5 visual features from segmented leaf |
| `fuzzy_engine.py` | `backend/app/core/model/fuzzy_engine.py` | Triangular MF + 16-rule Sugeno inference engine |
| `config.py` | `backend/app/core/model/config.py` | Fuzzy parameters (MF bounds, rule constants) |


### Pipeline Flow (Production Code)

```
Input Image
    ↓
segmenter.py → Binary leaf mask (HSV green mask + contour)
    ↓
feature_extractor.py → 5 features (spot_area, yellow_ratio, brown_ratio, dark_ratio, color_change)
    ↓
fuzzy_engine.py → Fuzzification → Rule evaluation (16 rules) → Defuzzification (weighted average)
    ↓
Output: {disease_name, fuzzy_score, severity_level, plant_status, features}
```

### API Integration

- **v1** (`POST /api/v1/predict`): Returns prediction result directly
- **v2** (`POST /api/v2/predict`): Same logic via `pipeline.predict()`, auto-saves to DB, returns `PredictionRecordResponse`

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

- Adaptive fuzzy membership (parameter MF dapat disesuaikan secara dinamis).
- Hybrid fuzzy + CNN untuk meningkatkan akurasi.
- Automatic disease recommendation (rekomendasi penanganan).

## Phase 3

- Realtime camera analysis (deteksi langsung dari kamera via WebRTC).
- Mobile AI inference.
- Multi plant detection (tanaman cabai, kentang, terong).

---

*Dokumen ini diperbarui berdasarkan data aktual dari hasil clustering K-Means pada PlantVillage Tomato Dataset (4.952 sampel).*
