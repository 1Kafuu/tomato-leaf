# Database Schema Suggestion

## Overview

Dokumen ini menyajikan suggestion tabel database untuk project Tomato Leaf Health Detection App menggunakan PostgreSQL.

---

## Tables

### 1. users

Tabel untuk menyimpan data pengguna.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | ID unik user |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email user |
| password | VARCHAR(255) | NOT NULL | Password (hashed) |
| name | VARCHAR(255) | NOT NULL | Nama lengkap |
| created_at | TIMESTAMP | DEFAULT NOW() | Waktu registrasi |
| updated_at | TIMESTAMP | DEFAULT NOW() | Waktu update terakhir |

---

### 2. predictions

Tabel untuk menyimpan hasil prediksi deteksi daun tomat.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | ID unik prediksi |
| user_id | INTEGER | FOREIGN KEY → users(id) | ID user |
| image_url | VARCHAR(500) | NOT NULL | Path/URL gambar |
| spot_area_percentage | FLOAT | NOT NULL | Persentase luas bercak |
| color_change_percentage | FLOAT | NOT NULL | Persentase perubahan warna |
| fuzzy_score | FLOAT | NOT NULL | Nilai fuzzy hasil |
| disease_name | VARCHAR(100) | NOT NULL | Nama penyakit |
| plant_status | VARCHAR(100) | NOT NULL | Status tanaman |
| created_at | TIMESTAMP | DEFAULT NOW() | Waktu prediksi |

---

### 3. fuzzy_rules_log (Optional)

Tabel untuk logging rule yang aktif saat prediksi (debugging).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | ID log |
| prediction_id | INTEGER | FOREIGN KEY → predictions(id) | ID prediksi |
| rule_name | VARCHAR(10) | NOT NULL | Nama rule (R1-R16) |
| firing_strength | FLOAT | NOT NULL | Nilai αi |
| constant | INTEGER | NOT NULL | Konstanta output |

---

### 4. sessions

Tabel untuk menyimpan token session/JWT.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | ID session |
| user_id | INTEGER | FOREIGN KEY → users(id) | ID user |
| token | TEXT | NOT NULL | JWT token |
| expires_at | TIMESTAMP | NOT NULL | Waktu expired |
| created_at | TIMESTAMP | DEFAULT NOW() | Waktu dibuat |

---

## ER Diagram

```
┌─────────────┐       ┌───────────────┐
│   users     │       │  predictions  │
├─────────────┤       ├───────────────┤
│ id (PK)     │◄──────│ user_id (FK)  │
│ email       │       │ id (PK)        │
│ password    │       │ image_url     │
│ name        │       │ spot_area_%   │
│ role        │       │ color_change_%│
│ created_at  │       │ fuzzy_score   │
│ updated_at  │       │ disease_name  │
└─────────────┘       │ plant_status  │
                      │ created_at    │
                      └───────────────┘
```

---

## Query Examples

### Get user prediction history

```sql
SELECT 
  id,
  image_url,
  disease_name,
  fuzzy_score,
  plant_status,
  created_at
FROM predictions
WHERE user_id = ?
ORDER BY created_at DESC;
```

### Get prediction detail with fuzzy values

```sql
SELECT 
  p.*,
  u.name as user_name,
  u.email as user_email
FROM predictions p
JOIN users u ON p.user_id = u.id
WHERE p.id = ?;
```

### Admin: Get statistics

```sql
SELECT 
  COUNT(*) as total_predictions,
  COUNT(DISTINCT user_id) as total_users,
  disease_name,
  COUNT(disease_name) as count
FROM predictions
GROUP BY disease_name;
```

---

## Notes

- Password harus di-hash dengan bcrypt atau argon2
- Gunakan JWT untuk authentication
- Image disimpan di storage (local/S3) dan simpan URL di database
- Tambahkan index pada user_id untuk query history yang cepat