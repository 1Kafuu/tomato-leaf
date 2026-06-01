# Product Requirements Document (PRD)

## Project Name

Tomato Leaf Health Detection App

---

# Product Overview

Aplikasi berbasis web untuk mendeteksi kesehatan tanaman tomat melalui analisis gambar daun menggunakan metode Fuzzy Sugeno. Pengguna dapat mengunggah foto daun tomat dan sistem akan mengidentifikasi kondisi kesehatan tanaman berdasarkan karakteristik visual daun.

Sistem menggunakan pendekatan fuzzy logic untuk membantu pengambilan keputusan berdasarkan parameter citra daun seperti luas bercak dan perubahan warna daun.

Fokus utama aplikasi:
- Deteksi penyakit daun tomat.
- Prediksi cepat berbasis fuzzy logic.
- Antarmuka sederhana untuk penggunaan mobile maupun desktop.

---

# Problem Statement

Petani tomat sering mengalami:
- Keterlambatan identifikasi penyakit tanaman.
- Kesulitan membedakan jenis penyakit daun.
- Kerugian hasil panen akibat penyebaran penyakit.

Identifikasi manual membutuhkan pengalaman dan waktu. Banyak petani tidak memiliki akses cepat ke ahli pertanian.

Aplikasi ini membantu proses identifikasi penyakit daun tomat secara otomatis menggunakan foto daun.

---

# Product Goals

## Business Goals

- Membantu petani tomat mendeteksi penyakit lebih cepat.
- Mengurangi risiko gagal panen.
- Menjadi solusi digital pertanian berbasis AI.

## User Goals

- Mendapat hasil diagnosis cepat.
- Mudah digunakan dari smartphone.
- Tidak membutuhkan pengetahuan teknis pertanian.

## Technical Goals

- Prediksi kondisi daun secara real-time.
- Implementasi metode Fuzzy Sugeno untuk klasifikasi.
- Akurasi sistem tinggi untuk daun tomat.
- Arsitektur scalable dan modular.

---

# Target Users

## Primary Users

### Petani Tomat

Kebutuhan:
- Deteksi penyakit dini.
- Penggunaan sederhana.
- Hasil cepat.

### Pengguna Rumahan

Kebutuhan:
- Mengecek kondisi tanaman tomat pribadi.
- Mengetahui jenis penyakit daun.

---

# Scope MVP

## Included Features

### 1. User Authentication

Fitur:
- Register
- Login
- Logout

Priority:
High

---

### 2. Upload Tomato Leaf Image

Fitur:
- Upload gambar daun tomat
- Preview gambar
- Validasi format file

Supported format:
- JPG
- JPEG
- PNG

Priority:
High

---

### 3. Tomato Disease Prediction

Deskripsi:
Sistem menganalisis gambar daun tomat menggunakan ekstraksi ciri citra dan metode Fuzzy Sugeno untuk menentukan kondisi kesehatan tanaman.

Parameter fuzzy yang digunakan:
- Luas bercak daun
- Perubahan warna daun

Output:
- Nama penyakit
- Status kesehatan tanaman
- Nilai hasil fuzzy

Priority:
High

---

### 4. Detection History

Fitur:
- Riwayat deteksi
- Detail hasil prediksi
- Timestamp

Priority:
Medium

---

### 5. Admin Dashboard

Fitur:
- Monitoring penggunaan
- Statistik prediksi

Priority:
Low

---

# Out of Scope MVP

- Deteksi multi tanaman
- Realtime camera detection
- IoT integration
- Mobile native app
- Offline prediction
- Marketplace pertanian

---

# Fuzzy Sugeno Method

## Overview

Metode utama yang digunakan adalah Fuzzy Sugeno orde 0.

Sistem melakukan klasifikasi kondisi daun tomat berdasarkan parameter luas bercak dan perubahan warna daun.

## Workflow Fuzzy Sugeno

1. User upload gambar daun tomat.
2. Sistem melakukan preprocessing gambar.
3. Sistem melakukan ekstraksi fitur.
4. Sistem menghitung luas bercak daun.
5. Sistem mendeteksi perubahan warna daun.
6. Sistem melakukan fuzzification.
7. Sistem menjalankan rule fuzzy.
8. Sistem menghitung output Sugeno.
9. Sistem menampilkan hasil diagnosis.

---

# Fuzzy Input Variables

## Variable 1: Luas Bercak

Membership:
- Kecil
- Sedang
- Besar
- Sangat Besar

## Variable 2: Perubahan Warna

Membership:

| Kategori | Rentang |
|---|---|
| Rendah | 0% – 20% |
| Sedang | 21% – 40% |
| Tinggi | 41% – 70% |
| Sangat Tinggi | > 70% |

Deskripsi:
Perubahan warna dihitung berdasarkan persentase perubahan warna daun dari kondisi hijau normal menuju warna kuning, coklat, atau hitam akibat penyakit.

---

# Fuzzy Rule Base

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

# Defuzzification Formula

Metode defuzzifikasi menggunakan weighted average Sugeno:

z = Σ(αi × ki) / Σαi

Keterangan:
- αi = firing strength setiap rule
- ki = konstanta output rule
- z = output akhir sistem fuzzy

---

# Output Interpretation

| Rentang Nilai | Kategori Output |
|---|---|
| 90 – 100 | Sangat Sehat |
| 75 – 89 | Sehat |
| 60 – 74 | Early Blight Ringan |
| 45 – 59 | Late Blight |
| 25 – 44 | Leaf Mold |
| 10 – 24 | Septoria Leaf Spot |
| 0 – 9 | Sangat Buruk |

---

# Tomato Diseases Coverage

Sistem mendukung klasifikasi:
- Healthy
- Early Blight
- Late Blight
- Leaf Mold
- Septoria Leaf Spot
- Sangat Buruk

Dataset referensi:
PlantVillage Tomato Dataset

---

# User Flow

## Main Flow

1. User membuka aplikasi.
2. User login/register.
3. User upload gambar daun tomat.
4. Sistem melakukan preprocessing.
5. Sistem menjalankan fuzzy inference.
6. Sistem menghitung hasil Sugeno.
7. Sistem menampilkan hasil diagnosis.
8. Hasil tersimpan di history.

---

# Functional Requirements

## FR-01 Authentication

User dapat membuat akun dan login menggunakan email dan password.

---

## FR-02 Upload Image

User dapat upload gambar daun tomat dengan format valid.

---

## FR-03 Feature Extraction

Sistem dapat mendeteksi:
- Luas bercak daun
- Perubahan warna daun

---

## FR-04 Fuzzy Inference

Sistem menjalankan fuzzy inference Sugeno berdasarkan rule base.

---

## FR-05 Prediction Result

Sistem menampilkan:
- Nama penyakit
- Nilai fuzzy akhir
- Status kesehatan tanaman

---

## FR-06 History

Sistem menyimpan hasil deteksi user.

---

# Non Functional Requirements

## Performance

- Waktu prediksi maksimal 5 detik.
- Upload maksimal 10 MB.

## Security

- Password hashing
- JWT authentication
- File validation

## Scalability

- Frontend dan backend dipisah.
- API modular.

## Availability

- Target uptime 95%.

---

# Tech Stack

## Frontend

- Next.js
- Tailwind CSS
- Axios

## Backend API

- Python
- FastAPI

## AI Processing

- OpenCV
- NumPy
- scikit-fuzzy
- Pillow

## Database

- PostgreSQL

## Deployment

- Frontend → Vercel
- Backend → Railway atau Render
- Database → Supabase

---

# API Requirement

## POST /predict

Function:
Mengirim gambar daun tomat untuk diprediksi.

Request:
- image

Response:
- disease_name
- fuzzy_score
- plant_status

---

## GET /history

Function:
Mengambil riwayat prediksi user.

---

# UI Pages

## Landing Page

- Penjelasan aplikasi
- CTA upload

## Login/Register

- Authentication form

## Dashboard

- Upload daun tomat
- Result prediction

## History

- Riwayat deteksi

## Admin Dashboard

- Statistik penggunaan

---

# Timeline Estimation

## Week 1

- Requirement gathering
- System architecture
- Dataset preparation
- Setup frontend dan backend
- UI/UX wireframe

## Week 2

- Implementasi preprocessing citra
- Implementasi fuzzy membership function
- Implementasi fuzzy rule base
- Frontend upload feature
- Backend API setup

## Week 3

- Integrasi frontend dan backend
- Implementasi history
- Testing fuzzy inference
- Bug fixing

## Week 4

- Optimization
- Deployment
- Final testing
- Presentation preparation

---

# Development Priority

## Must Have

- Upload gambar daun tomat
- Fuzzy Sugeno inference
- Result page
- Basic authentication
- Responsive UI

## Should Have

- Detection history
- Nilai fuzzy visualization

## Could Have

- Admin dashboard sederhana

## Won't Have

- Realtime camera detection
- Multi plant detection
- IoT integration
- Mobile native app

---

# Success Metrics

## Technical KPI

- Response prediction < 5 detik
- Akurasi klasifikasi ≥ 80%
- Sistem fuzzy berjalan stabil

## Product KPI

- Jumlah prediksi harian
- User retention
- Total active users

---

# Risk Assessment

## Risk

Ekstraksi fitur citra tidak akurat

Mitigation
- Optimasi preprocessing gambar
- Validasi dataset
- Testing beberapa threshold

---

## Risk

Rule fuzzy tidak optimal

Mitigation
- Evaluasi membership function
- Kalibrasi konstanta Sugeno
- Pengujian manual hasil fuzzy

---

## Risk

Inference lambat

Mitigation
- Resize image sebelum proses
- Optimasi algoritma preprocessing

---

# Future Roadmap

## Phase 2

- Rekomendasi penanganan penyakit
- Kamera realtime
- Multi-language

## Phase 3

- Multi plant detection
- Mobile application
- Smart farming dashboard

