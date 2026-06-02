# Product Requirements Document (PRD)

## Tomato Leaf Health Detection App

| Dokumen | Product Requirements Document |
|---|---|
| Proyek | Tomato Leaf Health Detection App |
| Versi | 2.0 |
| Status | Draft |
| Penulis | Tim Pengembang |

---

# Project Overview

**Tomato Leaf Health Detection App** adalah aplikasi berbasis web yang mendeteksi kesehatan daun tomat melalui analisis citra digital menggunakan metode **Fuzzy Sugeno Orde 0**. Pengguna cukup mengunggah foto daun tomat, dan sistem akan secara otomatis melakukan segmentasi daun, ekstraksi fitur visual, inferensi fuzzy, dan menampilkan diagnosis penyakit beserta tingkat keparahan.

Aplikasi ini dikembangkan untuk membantu petani dan pengguna rumahan dalam mengidentifikasi penyakit daun tomat secara cepat, objektif, dan tanpa memerlukan keahlian khusus di bidang fitopatologi.

---

# Problem Statement

Penyakit daun tomat merupakan salah satu faktor utama yang menyebabkan gagal panen dan kerugian ekonomi bagi petani. Identifikasi penyakit secara manual memiliki beberapa kendala:

- **Keterlambatan deteksi**: Petani sering baru menyadari penyakit ketika gejala sudah parah dan sulit dikendalikan.
- **Subjektivitas diagnosis**: Identifikasi manual sangat bergantung pada pengalaman dan pengetahuan individu, sehingga hasilnya bisa berbeda antar pengamat.
- **Keterbatasan akses ahli**: Tidak semua petani memiliki akses cepat ke penyuluh pertanian atau laboratorium fitopatologi.
- **Kesulitan diferensiasi**: Beberapa jenis penyakit daun tomat (Early Blight, Late Blight, Septoria Leaf Spot, Leaf Mold) memiliki gejala visual yang mirip, sehingga sulit dibedakan tanpa pengalaman.

Solusi yang ditawarkan adalah sistem berbasis web yang dapat mendiagnosis penyakit daun tomat secara otomatis dari foto daun menggunakan metode Fuzzy Sugeno, sehingga diagnosis menjadi lebih cepat, konsisten, dan mudah diakses oleh siapa saja.

---

# Product Goals

## Business Goals

1. Menyediakan alat deteksi dini penyakit daun tomat yang mudah diakses oleh petani.
2. Membantu mengurangi risiko gagal panen akibat keterlambatan identifikasi penyakit.
3. Mendukung transformasi digital sektor pertanian dengan solusi berbasis kecerdasan buatan yang terjangkau.

## User Goals

1. Mendapatkan diagnosis penyakit daun tomat dalam waktu kurang dari 5 detik.
2. Menggunakan aplikasi dari perangkat apa pun (desktop maupun ponsel) tanpa instalasi.
3. Tidak memerlukan pengetahuan teknis di bidang pengolahan citra atau kecerdasan buatan.

## Technical Goals

1. Menerapkan pipeline segmentasi daun yang akurat untuk menghilangkan background.
2. Mengekstrak fitur visual daun (spot_area, color_change, yellow_ratio, brown_ratio, dark_ratio) secara konsisten.
3. Mengimplementasikan metode Fuzzy Sugeno Orde 0 dengan 16 aturan fuzzy.
4. Menjaga waktu respons prediksi di bawah 5 detik.
5. Membangun arsitektur yang modular, scalable, dan mudah dipelihara.

---

# Target Users

## Primary User: Petani Tomat

| Karakteristik | Deskripsi |
|---|---|
| Latar belakang | Petani tomat skala kecil hingga menengah |
| Kebutuhan utama | Deteksi penyakit secara dini dan cepat |
| Perangkat | Smartphone Android dengan koneksi internet |
| Tingkat literasi teknologi | Rendah hingga menengah |
| Frekuensi penggunaan | Harian selama musim tanam |

## Secondary User: Pengguna Rumahan

| Karakteristik | Deskripsi |
|---|---|
| Latar belakang | Individu yang menanam tomat di pekarangan/rumah |
| Kebutuhan utama | Mengecek kondisi tanaman tomat pribadi |
| Perangkat | Smartphone atau laptop |
| Tingkat literasi teknologi | Menengah |
| Frekuensi penggunaan | Mingguan atau sesuai kebutuhan |

## Tertiary User: Peneliti/Mahasiswa

| Karakteristik | Deskripsi |
|---|---|
| Latar belakang | Mahasiswa atau peneliti di bidang pertanian/komputer |
| Kebutuhan utama | Referensi implementasi fuzzy logic untuk deteksi penyakit |
| Perangkat | Laptop/desktop |
| Tingkat literasi teknologi | Tinggi |

---

# Scope MVP

## Fitur Wajib (Must Have)

| Fitur | Prioritas |
|---|---|
| Upload gambar daun tomat (JPG, JPEG, PNG) | P0 |
| Segmentasi daun otomatis (buang background) | P0 |
| Ekstraksi fitur visual (5 fitur) | P0 |
| Inferensi Fuzzy Sugeno Orde 0 | P0 |
| Menampilkan hasil diagnosis penyakit | P0 |
| Responsive UI (desktop & mobile) | P0 |
| Registrasi dan login pengguna | P0 |
| Validasi format dan ukuran file | P0 |

## Fitur Pendukung (Should Have)

| Fitur | Prioritas |
|---|---|
| Riwayat deteksi pengguna | P1 |
| Visualisasi nilai fuzzy | P1 |

## Fitur Tambahan (Could Have)

| Fitur | Prioritas |
|---|---|
| Dashboard admin dengan statistik penggunaan | P2 |

---

# Out of Scope

Berikut adalah fitur yang tidak termasuk dalam cakupan MVP dan tidak akan dikembangkan pada fase ini:

- Deteksi multi-jenis tanaman (tidak terbatas pada tomat)
- Deteksi real-time melalui kamera
- Integrasi dengan perangkat IoT (sensor kelembaban, suhu, dll.)
- Aplikasi mobile native (Android/iOS)
- Prediksi offline tanpa koneksi internet
- Marketplace atau platform jual-beli hasil pertanian
- Rekomendasi pengobatan atau pupuk secara otomatis
- Integrasi dengan sistem irigasi atau drone pertanian

---

# System Architecture

```
+-------------------+         +--------------------+         +-----------------+
|                   |  HTTP   |                    |  SQL    |                 |
|   Next.js App     +-------->+   FastAPI Server   +-------->+   PostgreSQL    |
|   (Frontend)      |<--------+   (Backend API)    |<--------+   (Database)    |
|                   |  JSON   |                    |  Rows   |                 |
+-------------------+         +--------------------+         +-----------------+
         |                            |
         | Axios POST /predict        | OpenCV + NumPy
         | (FormData: image)          | scikit-fuzzy
         |                            |
         v                            v
  [User Browser]              [Inference Engine]
                              1. Leaf Segmentation
                              2. Feature Extraction
                              3. Fuzzification
                              4. Rule Evaluation
                              5. Defuzzification
                              6. Classification
```

## Arsitektur Layers

| Layer | Teknologi | Fungsi |
|---|---|---|
| Presentation | Next.js + Tailwind CSS | UI/UX pengguna |
| API Gateway | FastAPI Python | REST endpoint, validasi request |
| Processing | OpenCV + NumPy | Segmentasi daun, ekstraksi fitur |
| Inference | scikit-fuzzy | Fuzzifikasi, evaluasi rule, defuzzifikasi |
| Persistence | PostgreSQL | Menyimpan user, history prediksi |
| Deployment Frontend | Vercel | Hosting Next.js |
| Deployment Backend | Railway / Render | Hosting FastAPI |
| Database Cloud | Supabase | PostgreSQL managed |

## Alur Data End-to-End

```
Browser           Frontend           Backend              Database
   |                  |                  |                     |
   |-- Upload Image ->|                  |                     |
   |                  |-- POST /predict -|->                   |
   |                  |   (FormData)     |                     |
   |                  |                  |-- Segmentasi Daun --|
   |                  |                  |-- Ekstraksi Fitur --|
   |                  |                  |-- Inferensi Fuzzy --|
   |                  |                  |-- Simpan History -->|
   |                  |<- JSON Response -|                     |
   |<- Tampilkan -----|                  |                     |
   |   Hasil          |                  |                     |
```

---

# System Workflow

Berikut adalah alur sistem yang berjalan saat pengguna melakukan prediksi. Proses ini adalah workflow utama aplikasi dan tidak mencakup proses pengembangan seperti pembuatan membership function.

```
+-------------------+
|  User Upload      |
|  Image            |
+--------+----------+
         |
         v
+-------------------+
|  1. Image         |
|    Preprocessing  |
|    (Resize 256x256)|
+--------+----------+
         |
         v
+-------------------+
|  2. Leaf          |
|    Segmentation   |
|    (HSV Green     |
|     Mask +        |
|     Largest       |
|     Contour)      |
+--------+----------+
         |
         v
+-------------------+
|  3. Feature       |
|    Extraction     |
|    (Spot Area,    |
|     Yellow Ratio, |
|     Brown Ratio,  |
|     Dark Ratio,   |
|     Color Change) |
+--------+----------+
         |
         v
+-------------------+
|  4. Fuzzification |
|    (Membership    |
|     Functions     |
|     Triangular)   |
+--------+----------+
         |
         v
+-------------------+
|  5. Rule          |
|    Evaluation     |
|    (16 Rules     |
|     Sugeno Orde 0)|
+--------+----------+
         |
         v
+-------------------+
|  6. Sugeno        |
|    Inference      |
|    Engine         |
+--------+----------+
         |
         v
+-------------------+
|  7. Weighted      |
|    Average        |
|    Defuzzification|
+--------+----------+
         |
         v
+-------------------+
|  8. Disease       |
|    Classification |
|    + Severity     |
|    Level          |
+--------+----------+
         |
         v
+-------------------+
|  9. Result        |
|    Display        |
|    (Nama Penyakit,|
|     Skor Fuzzy,   |
|     Tingkat       |
|     Keparahan)    |
+-------------------+
```

---

# Dataset Reference

Sistem menggunakan **PlantVillage Tomato Dataset** sebagai referensi untuk pembentukan parameter membership function dan evaluasi sistem. Dataset tidak digunakan secara langsung saat prediksi; sistem hanya menggunakan parameter fuzzy yang telah ditentukan sebelumnya.

## Distribusi Data

| Kelas | Jumlah Gambar |
|---|---|
| Healthy | 1.000 |
| Early Blight | 1.000 |
| Late Blight | 1.000 |
| Septoria Leaf Spot | 1.000 |
| Leaf Mold | 952 |
| **Total** | **4.952** |

## Penggunaan Dataset

| Kegunaan | Deskripsi |
|---|---|
| Pembentukan Membership Function | Data diekstrak fiturnya, kemudian dianalisis menggunakan K-Means Clustering untuk menentukan pusat cluster sebagai parameter membership function. |
| Evaluasi Sistem | Dataset digunakan untuk menguji akurasi sistem dalam mengklasifikasikan penyakit daun tomat. |
| Validasi Parameter | Parameter fuzzy (rule base, konstanta Sugeno) divalidasi menggunakan subset data uji. |

## Catatan

- Dataset bersifat publik dan dapat diunduh dari platform PlantVillage.
- Seluruh gambar telah melalui proses segmentasi dan ekstraksi fitur untuk menghasilkan nilai numerik.
- Nilai membership function yang dihasilkan bersifat data-driven (tidak ditentukan secara manual/arbitrer).

---

# Image Processing

Sebelum fitur diekstraksi, sistem melakukan segmentasi daun untuk memisahkan area daun dari background. Hal ini penting karena background (tanah, pot, objek lain) dapat mengganggu perhitungan fitur.

## Pipeline Image Processing

```
+-------------------+
|  Input Image      |
|  (JPG/JPEG/PNG)   |
+--------+----------+
         |
         v
+-------------------+
|  Resize ke        |
|  256 x 256        |
|  piksel           |
+--------+----------+
         |
         v
+-------------------+
|  Konversi RGB     |
|  ke HSV           |
+--------+----------+
         |
         v
+-------------------+
|  Green Mask       |
|  (HSV Range:      |
|   H:35-90,        |
|   S:40-255,       |
|   V:40-255)       |
+--------+----------+
         |
         v
+-------------------+
|  Morphological    |
|  Cleanup (Close   |
|  + Open, kernel   |
|  ellipse 5x5)     |
+--------+----------+
         |
         v
+-------------------+
|  Largest Contour  |
|  Detection        |
|  (asumsi = daun)  |
+--------+----------+
         |
         v
+-------------------+
|  Leaf Mask        |
|  (binary mask     |
|   area daun)      |
+--------+----------+
         |
         v
+-------------------+
|  Feature          |
|  Extraction       |
|  (hanya pada      |
|   area daun)      |
+-------------------+
```

## Detail Segmentasi

| Tahap | Metode | Parameter |
|---|---|---|
| Color Space | RGB → HSV | cv2.COLOR_BGR2HSV |
| Green Mask | HSV Threshold | Lower: [35, 40, 40], Upper: [90, 255, 255] |
| Morphological Close | cv2.MORPH_CLOSE, kernel ellipse 5×5 | Iterasi: 2 |
| Morphological Open | cv2.MORPH_OPEN, kernel ellipse 5×5 | Iterasi: 1 |
| Contour Detection | cv2.findContours, RETR_EXTERNAL | Ambil kontur terluas |
| Masking | cv2.drawContours + cv2.bitwise_and | Filled contour |

## Tujuan Segmentasi

1. **Menghilangkan background** yang dapat menjadi noise pada perhitungan fitur.
2. **Memastikan perhitungan hanya dilakukan pada area daun**, sehingga nilai fitur lebih akurat secara biologis.
3. **Mengurangi false positive** pada deteksi bercak karena background (tanah, pot) tidak ikut terhitung sebagai bercak.

---

# Feature Extraction

Sistem mengekstrak **5 fitur numerik** dari area daun hasil segmentasi. Seluruh fitur dihitung berdasarkan persentase terhadap total area daun.

## Daftar Fitur

| No | Fitur | Satuan | Rentang | Deskripsi |
|---|---|---|---|---|
| 1 | spot_area | % | 0 – 100 | Persentase area daun yang tertutup bercak (warna coklat/kuning) |
| 2 | yellow_ratio | % | 0 – 100 | Persentase area daun yang menunjukkan warna kuning (klorosis) |
| 3 | brown_ratio | % | 0 – 100 | Persentase area daun yang menunjukkan warna coklat (nekrosis) |
| 4 | dark_ratio | % | 0 – 100 | Persentase area daun yang menunjukkan warna gelap/hitam |
| 5 | color_change | % | 0 – 100 | Persentase total perubahan warna daun (yellow_ratio + brown_ratio + dark_ratio) |

## Definisi Matematis

### Spot Area

```
spot_area = (spot_pixels / leaf_pixels) x 100
```

Keterangan:
- spot_pixels = jumlah piksel dalam rentang HSV [0,20,20] hingga [40,255,180] pada area daun
- leaf_pixels = total piksel area daun hasil segmentasi

### Color Change

```
color_change = yellow_ratio + brown_ratio + dark_ratio
```

### Yellow Ratio

```
yellow_ratio = (yellow_pixels / leaf_pixels) x 100
```

Rentang HSV: [20, 50, 50] hingga [35, 255, 255]

### Brown Ratio

```
brown_ratio = (brown_pixels / leaf_pixels) x 100
```

Rentang HSV: [0, 20, 20] hingga [20, 255, 120]

### Dark Ratio

```
dark_ratio = (dark_pixels / leaf_pixels) x 100
```

Rentang HSV: [0, 0, 0] hingga [180, 255, 60]

## Ilustrasi Perhitungan

```
+---------------------------+
|   Area Daun Hasil         |
|   Segmentasi              |  ← leaf_pixels = 42.500
|                           |
|  +---------------------+  |
|  | Bercak Coklat       |  |  ← brown_pixels = 850
|  +---------------------+  |
|  +------+                  |
|  |Kuning|                 |  ← yellow_pixels = 2.125
|  +------+                  |
|                           |
+---------------------------+

brown_ratio  = (850 / 42.500) x 100 = 2,00%
yellow_ratio = (2.125 / 42.500) x 100 = 5,00%
spot_area    = (850+2.125 / 42.500) x 100 = 7,00%
color_change = 2,00% + 5,00% + 0% = 7,00%
```

---

# Fuzzy Sugeno Method

Sistem menggunakan metode **Fuzzy Sugeno Orde 0** sebagai inti dari mesin inferensi. Metode ini dipilih karena:

1. **Komputasi efisien** — menggunakan konstanta output (orde 0) sehingga perhitungan defuzzifikasi lebih sederhana dibandingkan Mamdani.
2. **Output numerik langsung** — menghasilkan nilai numerik yang mudah diinterpretasikan sebagai skor kesehatan.
3. **Cocok untuk kontrol/klasifikasi** — orde 0 Sugeno banyak digunakan untuk sistem klasifikasi berbasis aturan.

## Tahapan Fuzzy Sugeno

### 1. Fuzzification

Mengubah nilai input numerik (crisp) menjadi derajat keanggotaan fuzzy menggunakan Triangular Membership Function.

Proses:
- Input: `spot_area` dan `color_change` (nilai numerik)
- Output: Derajat keanggotaan untuk setiap kategori fuzzy
- Contoh: Jika `spot_area = 12%`, maka derajat "Sedang" = 0,8 dan derajat "Besar" = 0,2

### 2. Rule Evaluation

Menerapkan 16 aturan fuzzy yang telah ditentukan. Setiap aturan berbentuk:

```
IF spot_area IS [Kategori] AND color_change IS [Kategori] THEN output = k
```

Nilai firing strength (αi) setiap aturan dihitung menggunakan operator AND (minimum):

```
αi = min(μ_spot_area, μ_color_change)
```

### 3. Inference Engine

Menggabungkan hasil dari seluruh aturan yang aktif. Setiap aturan menghasilkan:

- Firing strength (αi)
- Konstanta output (ki)

### 4. Weighted Average Defuzzification

Menghitung output akhir sistem menggunakan rumus rata-rata terbobot:

```
        Σ (αi × ki)
z = ─────────────────
         Σ (αi)
```

Keterangan:
- z = output akhir (fuzzy score)
- αi = firing strength aturan ke-i
- ki = konstanta output aturan ke-i
- Σ = notasi sigma (penjumlahan seluruh aturan)

Jika tidak ada aturan yang aktif (Σαi = 0), maka sistem mengembalikan output default (z = 50).

---

# Membership Functions

Sistem menggunakan **Triangular Membership Function** untuk setiap variabel fuzzy.

## Definisi Triangular Membership Function

Triangular membership function didefinisikan dengan tiga parameter:

| Parameter | Istilah | Definisi |
|---|---|---|
| a | **Batas Awal** | Nilai minimum di mana fungsi mulai aktif (derajat keanggotaan > 0) |
| b | **Nilai Representatif** | Nilai yang paling mewakili kategori (derajat keanggotaan = 1) |
| c | **Batas Akhir** | Nilai maksimum di mana fungsi masih aktif (derajat keanggotaan > 0) |

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

## Visualisasi

```
Derajat
Keanggotaan
   1 ────────╱╲──────────
             ╱  ╲
            ╱    ╲
           ╱      ╲
          ╱        ╲
         ╱          ╲
   0 ───╱────────────╲───
        a      b      c
    Batas   Nilai   Batas
    Awal   Represen  Akhir
           -tatif
```

## Variabel Fuzzy 1: Spot Area (%)

| Kategori | Batas Awal (a) | Nilai Representatif (b) | Batas Akhir (c) |
|---|---|---|---|
| Kecil | 0,06 | 3,22 | 8,35 |
| Sedang | 8,35 | 13,48 | 18,85 |
| Besar | 18,85 | 24,23 | 31,78 |
| Sangat Besar | 31,78 | 39,33 | 48,48 |

**Interpretasi Klinis:**

| Kategori | Rentang (%) | Makna Biologis |
|---|---|---|
| Kecil | 0 – 10 | Daun sehat dengan sedikit atau tanpa bercak |
| Sedang | 5 – 20 | Mulai muncul bercak, tahap awal infeksi |
| Besar | 15 – 35 | Bercak menyebar, infeksi cukup parah |
| Sangat Besar | 30 – 50+ | Bercak dominan, infeksi sangat parah |

## Variabel Fuzzy 2: Color Change Severity (%)

| Kategori | Batas Awal (a) | Nilai Representatif (b) | Batas Akhir (c) |
|---|---|---|---|
| Rendah | 0,19 | 8,05 | 16,86 |
| Sedang | 16,86 | 25,68 | 36,19 |
| Tinggi | 36,19 | 46,70 | 64,15 |
| Sangat Tinggi | 64,15 | 81,59 | 99,79 |

**Interpretasi Klinis:**

| Kategori | Rentang (%) | Makna Biologis |
|---|---|---|
| Rendah | 0 – 20 | Daun dominan hijau, sedikit atau tanpa perubahan warna |
| Sedang | 15 – 40 | Mulai muncul klorosis (kuning) pada beberapa area |
| Tinggi | 35 – 65 | Perubahan warna signifikan, daun mulai mengering |
| Sangat Tinggi | 60 – 100 | Daun mengalami perubahan warna masif, hampir tidak tersisa jaringan hijau |

## Sumber Parameter Membership Function

Parameter membership function diperoleh secara **data-driven** menggunakan metode **K-Means Clustering (k=4)** pada 4.952 sampel PlantVillage Tomato Dataset. Pusat cluster yang telah diurutkan digunakan sebagai Nilai Representatif (b). Batas Awal (a) dan Batas Akhir (c) ditentukan dari titik tengah antar pusat cluster untuk menghasilkan overlap alami antar kategori.

---

# Rule Base

Sistem menggunakan 16 aturan fuzzy (rule base) yang merupakan kombinasi dari 4 kategori Spot Area dan 4 kategori Color Change.

## Format Aturan

```
IF spot_area IS [Kategori_A] AND color_change IS [Kategori_B] THEN output = k
```

Keterangan:
- Kategori_A ∈ {Kecil, Sedang, Besar, Sangat Besar}
- Kategori_B ∈ {Rendah, Sedang, Tinggi, Sangat Tinggi}
- k = konstanta output Sugeno (nilai numerik)

## Tabel Rule Base (4 × 4)

| | **Color Change: Rendah** | **Color Change: Sedang** | **Color Change: Tinggi** | **Color Change: Sangat Tinggi** |
|---|---|---|---|---|
| **Spot Area: Kecil** | R1 | R2 | R3 | R4 |
| **Spot Area: Sedang** | R5 | R6 | R7 | R8 |
| **Spot Area: Besar** | R9 | R10 | R11 | R12 |
| **Spot Area: Sangat Besar** | R13 | R14 | R15 | R16 |

## Detail Aturan

| Rule | IF | AND | THEN (Output) | Konstanta (k) |
|---|---|---|---|---|
| R1 | Spot Area = **Kecil** | Color Change = **Rendah** | Sangat Sehat | 100 |
| R2 | Spot Area = **Kecil** | Color Change = **Sedang** | Sehat | 90 |
| R3 | Spot Area = **Kecil** | Color Change = **Tinggi** | Early Blight Ringan | 80 |
| R4 | Spot Area = **Kecil** | Color Change = **Sangat Tinggi** | Leaf Mold | 40 |
| R5 | Spot Area = **Sedang** | Color Change = **Rendah** | Sehat | 85 |
| R6 | Spot Area = **Sedang** | Color Change = **Sedang** | Early Blight Sedang | 70 |
| R7 | Spot Area = **Sedang** | Color Change = **Tinggi** | Late Blight | 55 |
| R8 | Spot Area = **Sedang** | Color Change = **Sangat Tinggi** | Leaf Mold | 40 |
| R9 | Spot Area = **Besar** | Color Change = **Rendah** | Early Blight Sedang | 70 |
| R10 | Spot Area = **Besar** | Color Change = **Sedang** | Late Blight | 55 |
| R11 | Spot Area = **Besar** | Color Change = **Tinggi** | Septoria Leaf Spot | 20 |
| R12 | Spot Area = **Besar** | Color Change = **Sangat Tinggi** | Sangat Buruk | 10 |
| R13 | Spot Area = **Sangat Besar** | Color Change = **Rendah** | Late Blight | 50 |
| R14 | Spot Area = **Sangat Besar** | Color Change = **Sedang** | Septoria Leaf Spot | 20 |
| R15 | Spot Area = **Sangat Besar** | Color Change = **Tinggi** | Sangat Buruk | 10 |
| R16 | Spot Area = **Sangat Besar** | Color Change = **Sangat Tinggi** | Sangat Buruk | 5 |

## Matriks Rule Base Berdasarkan Nilai Output

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

Defuzzifikasi adalah proses mengubah nilai fuzzy menjadi nilai numerik (crisp) yang dapat diinterpretasikan sebagai skor kesehatan tanaman.

## Metode: Weighted Average (Sugeno Orde 0)

```
        Σ (αi × ki)
z = ─────────────────
         Σ (αi)
```

## Contoh Perhitungan

Diketahui:
- Input: `spot_area = 12%`, `color_change = 30%`
- Aturan yang aktif (setelah fuzzifikasi):

| Rule | αi (firing strength) | ki (konstanta) | αi × ki |
|---|---|---|---|
| R2 | 0,30 | 90 | 27,00 |
| R3 | 0,20 | 80 | 16,00 |
| R6 | 0,70 | 70 | 49,00 |
| R7 | 0,40 | 55 | 22,00 |

| Σαi | Σ(αi × ki) | z |
|---|---|---|
| 1,60 | 114,00 | **71,25** |

Hasil: `z = 71,25` → diklasifikasikan sebagai **Early Blight Ringan** (60–74)

## Penanganan Kasus Khusus

| Skenario | Penanganan |
|---|---|
| Σαi = 0 (tidak ada aturan aktif) | Output default = 50 |
| z < 0 | Dipotong ke 0 (clipping) |
| z > 100 | Dipotong ke 100 (clipping) |

---

# Disease Classification

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
| disease_name | string | "Late Blight" |
| fuzzy_score | float | 56,00 |
| severity_level | string | "Sedang" |
| plant_status | string | "Terinfeksi" |

## Format Response API

```json
{
  "success": true,
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

---

# User Flow

## Main Flow: Prediksi Penyakit

```
+------------+     +------------+     +------------+     +------------+
|   Start    |---->|  Upload    |---->|  Preview   |---->|  Confirm   |
|            |     |  Image     |     |  Image     |     |  & Submit  |
+------------+     +------------+     +------------+     +------------+
                                                                 |
                                                                 v
+------------+     +------------+     +------------+     +------------+
|   Result   |<----|  Loading   |<----|  API Call  |<----|  Validate  |
|   Display  |     |  (≤ 5 dtk) |     |  POST      |     |  File      |
+------------+     +------------+     +------------+     +------------+
      |
      v
+------------+     +------------+
|  Save to   |     |   Option:  |
|  History   |     |  Predict   |
|  (otomatis)|     |  Another   |
+------------+     +------------+
```

## Flow Detail

### Step 1: User membuka aplikasi

- User mengakses URL aplikasi melalui browser
- Halaman landing page ditampilkan dengan informasi aplikasi dan CTA "Mulai Deteksi"

### Step 2: Autentikasi

- User login atau register (jika belum memiliki akun)
- Setelah login, user diarahkan ke dashboard

### Step 3: Upload gambar

- User memilih gambar daun tomat dari perangkat
- Sistem menampilkan preview gambar + validasi format/ukuran

### Step 4: Submit prediksi

- User menekan tombol "Deteksi"
- Sistem mengirim gambar ke backend via AJAX (FormData)

### Step 5: Proses backend

- Sistem melakukan segmentasi daun → ekstraksi fitur → inferensi fuzzy → klasifikasi
- Durasi maksimal 5 detik

### Step 6: Tampilkan hasil

- Nama penyakit
- Skor fuzzy
- Tingkat keparahan
- Nilai fitur (opsional, detail)

### Step 7: Riwayat

- Hasil otomatis tersimpan di history pengguna
- User dapat melihat riwayat kapan saja

---

# Functional Requirements

## FR-01: Registrasi Pengguna

| ID | FR-01 |
|---|---|
| Judul | Registrasi Pengguna |
| Deskripsi | Pengguna dapat membuat akun baru menggunakan email dan password |
| Prioritas | P0 |
| Input | Email, password, nama lengkap |
| Output | Akun baru tersimpan di database, token JWT dikembalikan |
| Validasi | Email unik, password minimal 8 karakter, email valid |

## FR-02: Login Pengguna

| ID | FR-02 |
|---|---|
| Judul | Login Pengguna |
| Deskripsi | Pengguna dapat login menggunakan email dan password |
| Prioritas | P0 |
| Input | Email, password |
| Output | Token JWT untuk akses API |
| Validasi | Email terdaftar, password sesuai |

## FR-03: Upload Gambar

| ID | FR-03 |
|---|---|
| Judul | Upload Gambar Daun Tomat |
| Deskripsi | Pengguna dapat mengunggah gambar daun tomat untuk diprediksi |
| Prioritas | P0 |
| Input | File gambar (JPG, JPEG, PNG), maksimal 10 MB |
| Output | Preview gambar, status validasi |
| Validasi | Format file (JPG/JPEG/PNG), ukuran ≤ 10 MB |

## FR-04: Segmentasi Daun

| ID | FR-04 |
|---|---|
| Judul | Segmentasi Daun Otomatis |
| Deskripsi | Sistem melakukan segmentasi untuk memisahkan area daun dari background |
| Prioritas | P0 |
| Metode | HSV Green Mask + Largest Contour + Morphological Cleanup |
| Output | Binary mask area daun |

## FR-05: Ekstraksi Fitur

| ID | FR-05 |
|---|---|
| Judul | Ekstraksi Fitur Visual |
| Deskripsi | Sistem mengekstrak 5 fitur dari area daun hasil segmentasi |
| Prioritas | P0 |
| Fitur | spot_area, yellow_ratio, brown_ratio, dark_ratio, color_change |
| Output | Nilai numerik 5 fitur dalam persentase |

## FR-06: Inferensi Fuzzy

| ID | FR-06 |
|---|---|
| Judul | Inferensi Fuzzy Sugeno |
| Deskripsi | Sistem menjalankan inferensi Fuzzy Sugeno Orde 0 berdasarkan input fitur |
| Prioritas | P0 |
| Metode | Triangular MF + 16 rule + Weighted Average Defuzzification |
| Output | Skor fuzzy numerik (0–100) |

## FR-07: Klasifikasi Penyakit

| ID | FR-07 |
|---|---|
| Judul | Klasifikasi Penyakit |
| Deskripsi | Sistem mengklasifikasikan skor fuzzy ke dalam kategori penyakit |
| Prioritas | P0 |
| Output | Nama penyakit, tingkat keparahan, status tanaman |

## FR-08: Tampilkan Hasil

| ID | FR-08 |
|---|---|
| Judul | Tampilkan Hasil Diagnosis |
| Deskripsi | Sistem menampilkan hasil diagnosis lengkap ke pengguna |
| Prioritas | P0 |
| Output | Nama penyakit, skor fuzzy, tingkat keparahan, nilai fitur |

## FR-09: Riwayat Deteksi

| ID | FR-09 |
|---|---|
| Judul | Riwayat Deteksi |
| Deskripsi | Pengguna dapat melihat riwayat prediksi yang telah dilakukan |
| Prioritas | P1 |
| Output | Tabel riwayat: gambar, hasil, tanggal |

## FR-10: Validasi File

| ID | FR-10 |
|---|---|
| Judul | Validasi File Upload |
| Deskripsi | Sistem memvalidasi format dan ukuran file sebelum diproses |
| Prioritas | P0 |
| Validasi | Format: JPG/JPEG/PNG, Ukuran: ≤ 10 MB, Tidak corrupt |

---

# Non Functional Requirements

## Performance

| Parameter | Target | Metode Pengukuran |
|---|---|---|
| Waktu prediksi | < 5 detik | Dari submit hingga hasil tampil |
| Waktu upload | < 2 detik | Dari pilih file hingga preview tampil |
| Waktu loading halaman | < 3 detik | First Contentful Paint (FCP) |
| Throughput API | ≥ 100 request/menit | Load testing |
| Ukuran file maksimal | 10 MB | Validasi server-side |

## Security

| Aspek | Requirement |
|---|---|
| Autentikasi | JWT (JSON Web Token) dengan masa berlaku terbatas |
| Password | Di-hash menggunakan bcrypt |
| File upload | Validasi tipe MIME (tidak hanya ekstensi) |
| CORS | Terbatas pada domain frontend yang dikenal |
| Rate limiting | Maksimal 30 request/menit per pengguna |
| Environment | API key dan secret disimpan di environment variables |

## Scalability

| Aspek | Requirement |
|---|---|
| Arsitektur | Frontend dan backend terpisah (decoupled) |
| API | RESTful, stateless |
| Database | Connection pooling |
| Image processing | Tidak menyimpan file sementara di disk (proses di memory) |

## Availability

| Parameter | Target |
|---|---|
| Uptime | ≥ 95% (monthly) |
| Backup database | Harian otomatis |
| Error rate | < 1% dari total request |

## Usability

| Aspek | Requirement |
|---|---|
| Responsive | Mendukung layar dari 320px (mobile) hingga 1920px (desktop) |
| Bahasa | Bahasa Indonesia |
| Loading indicator | Progress bar atau spinner saat prediksi berjalan |
| Error handling | Pesan error yang jelas dan user-friendly |

## Maintainability

| Aspek | Requirement |
|---|---|
| Code style | Mengikuti PEP 8 (Python) dan ESLint/Biome (TypeScript) |
| Dokumentasi | Setiap endpoint API memiliki dokumentasi |
| Modular | Fungsi image processing dan fuzzy logic dipisahkan dalam modul terpisah |

---

# Database Design

## Entity Relationship Diagram

```
+----------------+          +-------------------+
|     users      |          | prediction_history |
+----------------+          +-------------------+
| id (PK)        |<-------->| id (PK)           |
| email          |    1    N| user_id (FK)      |
| password_hash  |          | image_name        |
| full_name      |          | image_data (bytea)|
| created_at     |          | spot_area         |
| updated_at     |          | color_change      |
+----------------+          | yellow_ratio      |
                            | brown_ratio       |
                            | dark_ratio        |
                            | fuzzy_score       |
                            | disease_name      |
                            | severity_level    |
                            | created_at        |
                            +-------------------+
```

## Tabel: users

| Kolom | Tipe | Constraint | Deskripsi |
|---|---|---|---|
| id | UUID | PK, DEFAULT gen_random_uuid() | Primary key |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email pengguna |
| password_hash | VARCHAR(255) | NOT NULL | Hash bcrypt dari password |
| full_name | VARCHAR(100) | NOT NULL | Nama lengkap pengguna |
| created_at | TIMESTAMP | DEFAULT NOW() | Waktu pembuatan akun |
| updated_at | TIMESTAMP | DEFAULT NOW() | Waktu update terakhir |

## Tabel: prediction_history

| Kolom | Tipe | Constraint | Deskripsi |
|---|---|---|---|
| id | UUID | PK, DEFAULT gen_random_uuid() | Primary key |
| user_id | UUID | FK → users.id, NOT NULL | ID pengguna |
| image_name | VARCHAR(255) | NOT NULL | Nama file asli |
| image_data | BYTEA | NOT NULL | Data gambar (binary) |
| spot_area | DECIMAL(5,2) | NOT NULL | Spot area (%) |
| yellow_ratio | DECIMAL(5,2) | NOT NULL | Yellow ratio (%) |
| brown_ratio | DECIMAL(5,2) | NOT NULL | Brown ratio (%) |
| dark_ratio | DECIMAL(5,2) | NOT NULL | Dark ratio (%) |
| color_change | DECIMAL(5,2) | NOT NULL | Color change (%) |
| fuzzy_score | DECIMAL(5,2) | NOT NULL | Skor fuzzy Sugeno |
| disease_name | VARCHAR(50) | NOT NULL | Nama penyakit hasil diagnosis |
| severity_level | VARCHAR(20) | NOT NULL | Tingkat keparahan |
| created_at | TIMESTAMP | DEFAULT NOW() | Waktu prediksi |

## Index

| Tabel | Kolom | Tipe Index | Tujuan |
|---|---|---|---|
| users | email | UNIQUE | Mempercepat login |
| prediction_history | user_id | BTREE | Mempercepat query history per user |
| prediction_history | created_at | BTREE | Sorting history berdasarkan waktu |

---

# API Requirements

## Base URL

```
Development : http://localhost:8000/api/v1
Production  : https://api.domain.com/api/v1
```

## Endpoint: POST /predict

Melakukan prediksi penyakit daun tomat dari gambar yang diunggah.

### Request

| Parameter | Tipe | Wajib | Deskripsi |
|---|---|---|---|
| image | File (multipart/form-data) | Ya | File gambar daun tomat (JPG/JPEG/PNG) |

### Response (Success — 200)

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

### Response (Error — 400)

```json
{
  "success": false,
  "message": "Format file tidak didukung",
  "error_code": "INVALID_FILE_FORMAT"
}
```

### Response (Error — 413)

```json
{
  "success": false,
  "message": "Ukuran file melebihi batas maksimal (10 MB)",
  "error_code": "FILE_TOO_LARGE"
}
```

### Response (Error — 500)

```json
{
  "success": false,
  "message": "Terjadi kesalahan internal server",
  "error_code": "INTERNAL_ERROR"
}
```

### Headers

| Header | Nilai | Deskripsi |
|---|---|---|
| Authorization | Bearer {token} | Token JWT autentikasi |
| Content-Type | multipart/form-data | Tipe konten upload file |

## Endpoint: GET /history

Mengambil riwayat prediksi pengguna yang sedang login.

### Request

| Parameter | Tipe | Wajib | Default | Deskripsi |
|---|---|---|---|---|
| page | integer | Tidak | 1 | Halaman (pagination) |
| limit | integer | Tidak | 10 | Jumlah data per halaman |
| sort | string | Tidak | "desc" | Urutan waktu (asc/desc) |

### Response (200)

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

## Endpoint: GET /history/{id}

Mengambil detail riwayat prediksi berdasarkan ID.

### Response (200)

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

## Endpoint: GET /health

Health check endpoint untuk monitoring.

### Response (200)

```json
{
  "status": "ok",
  "version": "2.0.0",
  "timestamp": "2026-06-01T10:00:00Z"
}
```

---

# UI Pages

## 1. Landing Page

| Elemen | Deskripsi |
|---|---|
| Header | Logo + Nama Aplikasi + Navbar (Login/Register) |
| Hero Section | Ilustrasi daun tomat + Tagline + CTA "Mulai Deteksi" |
| Feature Section | 3 kartu fitur utama (Cepat, Akurat, Mudah) |
| How It Works | 3 langkah: Upload → Analisis → Hasil |
| Footer | Copyright + Kontak |

## 2. Login Page

| Elemen | Deskripsi |
|---|---|
| Form | Email + Password |
| Tombol | "Masuk" |
| Link | "Belum punya akun? Daftar" |
| Validasi | Error message jika login gagal |

## 3. Register Page

| Elemen | Deskripsi |
|---|---|
| Form | Nama Lengkap + Email + Password + Konfirmasi Password |
| Tombol | "Daftar" |
| Link | "Sudah punya akun? Masuk" |
| Validasi | Error message jika validasi gagal |

## 4. Dashboard (Upload + Result)

| Elemen | Deskripsi |
|---|---|
| Upload Area | Drag & drop + tombol "Pilih Gambar" |
| Preview | Thumbnail gambar yang dipilih |
| Tombol Deteksi | "Deteksi Sekarang" (disabled jika belum ada gambar) |
| Loading | Spinner + "Sedang menganalisis..." |
| Result Card | Nama penyakit (besar), Skor fuzzy, Tingkat keparahan, Status tanaman |
| Fitur Detail | Tabel 5 fitur (opsional, bisa di-expand) |
| Tombol | "Deteksi Lagi" + "Lihat Riwayat" |

## 5. History Page

| Elemen | Deskripsi |
|---|---|
| Tabel | No, Gambar (thumbnail), Penyakit, Skor, Tanggal, Aksi (Detail) |
| Pagination | Navigasi halaman |
| Search | Filter berdasarkan nama penyakit (opsional) |
| Empty State | "Belum ada riwayat deteksi" (jika kosong) |

## 6. Detail History Page

| Elemen | Deskripsi |
|---|---|
| Gambar | Gambar daun yang diprediksi (ukuran besar) |
| Hasil | Nama penyakit, skor, tingkat keparahan |
| Detail Fitur | 5 fitur dalam bentuk tabel atau bar chart |
| Tombol | "Kembali ke Riwayat" + "Deteksi Baru" |

---

# Tech Stack

## Frontend

| Teknologi | Versi | Fungsi |
|---|---|---|
| Next.js | 16 | Framework React untuk frontend web |
| TypeScript | 5.x | Type safety |
| Tailwind CSS | 4.x | Utility-first CSS framework |
| Axios | 1.x | HTTP client untuk komunikasi API |
| React Dropzone | — | Komponen drag & drop upload |

## Backend API

| Teknologi | Versi | Fungsi |
|---|---|---|
| Python | 3.14 | Bahasa pemrograman backend |
| FastAPI | 0.x | Framework REST API asinkron |
| Uvicorn | — | ASGI server |
| python-multipart | — | Parsing file upload |
| Pydantic | 2.x | Validasi data request/response |
| PyJWT | 2.x | JWT token authentication |

## Image Processing

| Teknologi | Versi | Fungsi |
|---|---|---|
| OpenCV | 4.x | Segmentasi daun, masking, contour detection |
| NumPy | 1.x | Operasi matriks dan array numerik |
| Pillow | 10.x | Validasi dan konversi format gambar |

## Fuzzy Engine

| Teknologi | Versi | Fungsi |
|---|---|---|
| scikit-fuzzy | 0.x | Membership function, fuzzy inference |
| (custom) | — | Rule evaluation engine (bisa diimplementasikan manual) |

## Database

| Teknologi | Versi | Fungsi |
|---|---|---|
| PostgreSQL | 16 | Database relasional |
| Supabase | — | Managed PostgreSQL cloud + Auth |

## Deployment & DevOps

| Layanan | Fungsi |
|---|---|
| Vercel | Hosting frontend Next.js |
| Railway / Render | Hosting backend FastAPI |
| Supabase | Database PostgreSQL + Storage |
| GitHub | Version control + CI/CD |

---

# Timeline

## Fase Pengembangan (Estimasi: 4 Minggu)

### Minggu 1: Foundation

| Hari | Aktivitas | Output |
|---|---|---|
| 1–2 | Requirement gathering & analisis | PRD final |
| 3 | Setup proyek (Next.js + FastAPI + DB) | Repository + boilerplate |
| 4 | Persiapan dataset | Dataset tersimpan + siap diproses |
| 5 | UI/UX design (wireframe + mockup) | Figma prototype |

### Minggu 2: Core Logic

| Hari | Aktivitas | Output |
|---|---|---|
| 1–2 | Implementasi image processing (segmentasi + ekstraksi fitur) | Modul processing siap |
| 3 | Ekstraksi fitur seluruh dataset → CSV | Dataset fitur |
| 4 | Pembuatan membership function (K-Means) | Parameter membership |
| 5 | Implementasi fuzzy inference engine | Modul fuzzy siap |

### Minggu 3: Integration

| Hari | Aktivitas | Output |
|---|---|---|
| 1 | Backend API (POST /predict, GET /history) | Endpoint REST siap |
| 2 | Frontend (Upload, Dashboard, Result) | Halaman utama siap |
| 3 | Frontend (Auth, History, Landing) | Seluruh halaman siap |
| 4 | Integrasi frontend ↔ backend | Alur end-to-end berfungsi |
| 5 | Testing + bug fixing | Bug teratasi |

### Minggu 4: Finalization

| Hari | Aktivitas | Output |
|---|---|---|
| 1 | Performance optimization | Response < 5 detik |
| 2 | Deployment (Vercel + Railway + Supabase) | Aplikasi live |
| 3 | Final testing + UAT | Sign-off |
| 4 | Dokumentasi + presentasi | Dokumen final |

---

# Development Priority

## P0: Must Have (Critical Path)

| ID | Item | Dependensi |
|---|---|---|
| P0.1 | Image processing pipeline | — |
| P0.2 | Feature extraction | P0.1 |
| P0.3 | Fuzzy inference engine | P0.2 |
| P0.4 | POST /predict API | P0.3 |
| P0.5 | Upload image UI | — |
| P0.6 | Result display UI | P0.4 |
| P0.7 | User authentication | — |

## P1: Should Have (Important)

| ID | Item | Dependensi |
|---|---|---|
| P1.1 | Prediction history | P0.4 |
| P1.2 | History page UI | P1.1 |
| P1.3 | Detail history page | P1.1 |
| P1.4 | Responsive design | P0.5, P0.6 |

## P2: Could Have (Nice to Have)

| ID | Item | Dependensi |
|---|---|---|
| P2.1 | Admin dashboard | P0.4 |
| P2.2 | Fuzzy score visualization | P0.6 |
| P2.3 | Image preview enhancement | P0.5 |

---

# Success Metrics

## Technical Metrics

| Metrik | Target | Cara Ukur |
|---|---|---|
| Response time | < 5 detik (P95) | Logging server-side + APM |
| Akurasi klasifikasi | ≥ 80% | Confusion matrix pada test dataset |
| API availability | ≥ 99% | Uptime monitoring (ping/health) |
| Error rate | < 1% | Error tracking (Sentry/logs) |
| File validation success | 100% valid files accepted | Integration test |

## Product Metrics

| Metrik | Target | Cara Ukur |
|---|---|---|
| Daily active users | ≥ 50 user (month 1) | Database analytics |
| Total predictions | ≥ 500 (month 1) | History table count |
| User retention (week 1) | ≥ 30% | Cohort analysis |
| User satisfaction | ≥ 4/5 | Survey (opsional) |

---

# Risk Assessment

## Technical Risks

| Risiko | Probabilitas | Dampak | Mitigasi |
|---|---|---|---|
| Segmentasi daun gagal (daun tidak terdeteksi) | Sedang | Tinggi | Fallback: gunakan seluruh gambar jika mask kosong; tampilkan pesan ke user |
| Inferensi fuzzy lambat (> 5 detik) | Rendah | Sedang | Optimasi dengan resize gambar terlebih dahulu; caching jika diperlukan |
| Akurasi klasifikasi rendah | Sedang | Tinggi | Evaluasi membership function secara berkala; kalibrasi rule base |
| File upload corrupt | Rendah | Sedang | Validasi file di sisi client dan server; cek magic bytes |
| Database connection failure | Rendah | Tinggi | Connection pooling + retry logic + fallback |

## Product Risks

| Risiko | Probabilitas | Dampak | Mitigasi |
|---|---|---|---|
| User tidak paham hasil diagnosis | Sedang | Sedang | Desain UI yang informatif; gunakan bahasa Indonesia sederhana |
| Gambar tidak sesuai kualitas (gelap, blur, dll.) | Tinggi | Sedang | Tampilkan panduan pengambilan gambar yang baik |
| Penyakit tidak terdeteksi karena di luar coverage | Rendah | Rendah | Tampilkan "Tidak terdeteksi" + saran konsultasi ahli |

## Mitigation Summary

| Area | Action Plan |
|---|---|
| Image Processing | Fallback mechanism jika segmentasi gagal; validasi kualitas gambar |
| Fuzzy Engine | Unit test untuk setiap rule; validasi output dengan dataset |
| Performance | Profiling rutin; optimasi bottleneck |
| User Experience | Panduan penggunaan yang jelas; error message yang informatif |

---

# Future Roadmap

## Phase 2 (Post-MVP — 2–3 bulan)

| Fitur | Deskripsi | Estimasi |
|---|---|---|
| Rekomendasi Penanganan | Memberikan saran pengobatan/pestisida berdasarkan penyakit | 2 minggu |
| Peningkatan Akurasi | Penambahan fitur tekstur GLCM (contrast, homogeneity, energy) | 3 minggu |
| Multi-language | Dukungan bahasa Inggris dan bahasa daerah | 1 minggu |
| Kompresi Gambar | Kompresi otomatis sisi client sebelum upload | 1 minggu |

## Phase 3 (6–12 bulan)

| Fitur | Deskripsi | Prioritas |
|---|---|---|
| Deteksi Real-time | Kamera langsung dari browser (WebRTC + Canvas) | Tinggi |
| Multi-plant Detection | Perluasan untuk tanaman cabai, kentang, terong | Tinggi |
| Mobile App | Aplikasi Android/iOS native (React Native / Flutter) | Sedang |
| Smart Farming Dashboard | Dashboard untuk petani skala besar: monitoring, alert, analytics | Sedang |
| Model Hybrid | Integrasi Deep Learning (CNN) + Fuzzy Logic untuk akurasi lebih tinggi | Rendah |

## Long-term Vision

- **Platform deteksi penyakit tanaman terintegrasi** — tidak terbatas pada tomat
- **IoT Integration** — sensor kelembaban, suhu, dan cahaya untuk konteks tambahan
- **Community Feature** — forum diskusi antar petani dan ahli pertanian
- **AI-powered Recommendation** — rekomendasi pupuk dan pestisida berbasis data

---

# Appendix

## Glossary

| Istilah | Definisi |
|---|---|
| Fuzzy Sugeno | Metode inferensi fuzzy dengan output berupa konstanta atau fungsi linear |
| Membership Function | Fungsi matematis yang mendefinisikan derajat keanggotaan suatu nilai dalam himpunan fuzzy |
| Fuzzification | Proses mengubah input numerik menjadi derajat keanggotaan fuzzy |
| Defuzzification | Proses mengubah derajat keanggotaan fuzzy menjadi output numerik |
| Firing Strength | Derajat kebenaran suatu aturan fuzzy, dihitung dari kombinasi derajat keanggotaan input |
| Segmentasi | Proses memisahkan objek (daun) dari background dalam citra digital |
| PlantVillage | Dataset publik berisi gambar tanaman sakit dan sehat untuk penelitian |
| K-Means | Algoritma clustering yang mengelompokkan data berdasarkan jarak ke pusat cluster |
| Triangular MF | Membership function berbentuk segitiga dengan parameter a, b, c |

## References

1. PlantVillage Dataset — https://plantvillage.psu.edu/
2. Sugeno, M. (1985). Industrial applications of fuzzy control. Elsevier.
3. OpenCV Documentation — https://docs.opencv.org/
4. scikit-fuzzy Documentation — https://scikit-fuzzy.github.io/
5. FastAPI Documentation — https://fastapi.tiangolo.com/
6. Next.js Documentation — https://nextjs.org/docs

---

*Dokumen PRD ini disusun sebagai acuan pengembangan **Tomato Leaf Health Detection App** dan akan diperbarui sesuai kebutuhan selama siklus pengembangan.*
