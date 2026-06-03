# Backend Flow — FastAPI + Supabase

Ringkasan langkah implementasi backend untuk projek Tomato Leaf Health Detection menggunakan FastAPI (Python) dan Supabase (Postgres + Storage + Auth).

## Inti arsitektur
- Frontend (Next.js) → FastAPI (REST) → Supabase (Postgres, Storage, Auth)
- FastAPI melakukan: validasi upload, preprocessing gambar (OpenCV), ekstraksi fitur, fuzzy inference (Sugeno), menyimpan riwayat.

## Prasyarat
- Python 3.11+ atau 3.14
- Supabase project (URL + SERVICE_ROLE / ANON key)
- Virtual environment
- Dependencies (contoh): `fastapi`, `uvicorn`, `python-multipart`, `pydantic`, `opencv-python`, `numpy`, `pillow`, `scikit-fuzzy` (atau implementasi custom), `supabase` (supabase-py), `bcrypt`, `pyjwt`, `asyncpg`/`databases`/`sqlalchemy`.

Contoh `requirements.txt` minimal:

- fastapi
- uvicorn[standard]
- python-multipart
- pydantic
- opencv-python-headless
- numpy
- pillow
- scikit-fuzzy
- supabase
- asyncpg
- sqlalchemy
- bcrypt
- pyjwt

## Struktur direktori (saran)

├── backend/                     # Python FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app + CORS + lifespan
│   │   ├── dependencies.py      # FastAPI dependencies (get_db, get_current_user)
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── auth.py       # POST /auth/register, /auth/login
│   │   │           ├── prediction.py # POST /predict
│   │   │           └── history.py    # GET /history, GET /history/{id}
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # Pydantic Settings
│   │   │   └── database.py      # SQLAlchemy async engine
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # DeclarativeBase
│   │   │   ├── user.py          # User model (UUID)
│   │   │   └── prediction.py    # PredictionHistory model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── prediction.py
│   │   │   └── auth.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── fuzzy_engine.py     # Triangular MF + 16 rules + Sugeno
│   │   │   ├── image_processor.py  # HSV segment + 5 features
│   │   │   └── supabase_service.py # Supabase Auth + Storage
│   │   └── crud/
│   │       ├── __init__.py
│   │       ├── user.py
│   │       └── prediction.py
│   ├── requirements.txt
│   └── .env.example

## Langkah implementasi (rendah ke tinggi)

1) Inisialisasi proyek
   - buat venv, install dependencies
   - buat file `.env` untuk `SUPABASE_URL`, `SUPABASE_KEY`, `DATABASE_URL`, `SECRET_KEY`

2) Siapkan Supabase
   - Buat project Supabase
   - Aktifkan Storage bucket (mis. `images`) untuk menyimpan foto
   - Buat tabel (SQL) untuk `users` dan `prediction_history` (contoh di bawah)
   - Atur RLS (opsional) / policies sesuai kebutuhan

3) Database schema (contoh SQL)

```sql
-- users
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email varchar(255) UNIQUE NOT NULL,
  password_hash varchar NOT NULL,
  full_name varchar(100) NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- prediction_history
CREATE TABLE IF NOT EXISTS prediction_history (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id),
  image_url text NOT NULL,
  spot_area numeric(5,2) NOT NULL,
  yellow_ratio numeric(5,2) NOT NULL,
  brown_ratio numeric(5,2) NOT NULL,
  dark_ratio numeric(5,2) NOT NULL,
  color_change numeric(5,2) NOT NULL,
  fuzzy_score numeric(5,2) NOT NULL,
  disease_name varchar(100) NOT NULL,
  severity_level varchar(50) NOT NULL,
  created_at timestamptz DEFAULT now()
);
```

4) Implementasi endpoint utama `POST /api/v1/predict`
   - Validasi file (MIME type, ukuran ≤ 10MB)
   - Baca file ke memory (`BytesIO`) — jangan tulis ke disk bila tidak perlu
   - Segmentasi daun (HSV mask, morphological ops, largest contour)
   - Ekstraksi fitur (spot_area, yellow_ratio, brown_ratio, dark_ratio, color_change)
   - Panggil fuzzy engine → hitung `fuzzy_score` dan `disease_name`
   - Upload gambar ke Supabase Storage → dapatkan `image_url` (atau simpan bytea)
   - Simpan record ke tabel `prediction_history`
   - Kembalikan response JSON sesuai PRD

5) Auth
   - pakai Supabase Auth (lebih mudah) — frontend gunakan Supabase JS, backend verifikasi JWT

6) Integrasi Supabase (contoh singkat)
- Inisialisasi client:

```py
from supabase import create_client
SUPABASE_URL = env("SUPABASE_URL")
SUPABASE_KEY = env("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

- Upload image (pseudo):

```py
res = supabase.storage.from_('images').upload(path, file_bytes)
url = supabase.storage.from_('images').get_public_url(path)
```

Catatan: gunakan service role key untuk operasi server-side sensitif.

7) Error handling & performance
   - Batasi ukuran upload, cek MIME, tangani kasus mask kosong (fallback)
   - Resize gambar (256×256) untuk mempercepat processing
   - Gunakan async I/O di FastAPI untuk endpoint
   - Tambahkan rate limiting dan health check `/api/v1/health`

8) Testing
   - Unit test untuk modul `processing` dan `fuzzy_engine`
   - Integration test untuk endpoint `POST /predict` (upload sample images)

9) Deployment
   - Set env vars pada Railway / Render
   - Jalankan container atau Uvicorn via Gunicorn/UVicorn
   - Pastikan Supabase keys aman (no commit `.env`)

## Contoh snippet endpoint (konsep)

```py
from fastapi import FastAPI, UploadFile, File, Depends

app = FastAPI()

@app.post('/api/v1/predict')
async def predict(image: UploadFile = File(...), user=Depends(get_current_user)):
    # 1. validate
    # 2. read bytes
    # 3. processing.extract_features(bytes)
    # 4. fuzzy_engine.infer(features)
    # 5. storage.upload(...) -> image_url
    # 6. db.save_prediction(...)
    # 7. return JSON
    return {"success": True}
```

## Checklist cepat sebelum deploy
- [ ] Supabase project & keys tersedia
- [ ] Tabel `prediction_history` & `users` dibuat
- [ ] Storage bucket `images` dibuat dan public/private policy diset
- [ ] Env vars di deployment terpasang
- [ ] Unit tests untuk processing + fuzzy

## Next steps saya bantu
- Scaffold kode FastAPI minimal (boilerplate + endpoint `POST /predict`), atau
- Buat contoh implementasi `processing.py` + `fuzzy_engine.py` untuk pipeline

---
Dokumen ini merujuk ke spesifikasi yang ada di folder `docs/` (PRD, AI model, database schema).
