# Project Structure

## Overview

Struktur project untuk Tomato Leaf Health Detection App dengan Next.js frontend + Python FastAPI backend + PostgreSQL database.

---

## Directory Structure

```
tomato-leaf/
├── app/                          # Next.js Frontend
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   ├── (dashboard)/
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   └── history/
│   │       └── page.tsx
│   ├── components/
│   │   ├── ui/                  # Reusable UI components
│   │   ├── auth/                # Auth components
│   │   └── prediction/          # Prediction components
│   ├── lib/
│   │   ├── api.ts               # Axios client
│   │   ├── supabase.ts          # Supabase client (browser)
│   │   └── utils.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   └── usePrediction.ts
│   ├── types/
│   │   └── index.ts
│   ├── layout.tsx
│   ├── page.tsx                 # Landing page
│   └── globals.css
│
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
│
├── docs/                        # Documentation
│   ├── project_prd.md
│   ├── prd_tomato_leaf.md       # PRD utama (acuan)
│   ├── ai_model.md
│   ├── database_schema.md
│   └── project_structure.md
│
├── public/                     # Static assets
│   └── images/
│       └── .gitkeep
│
├── sql/                        # Database scripts
│   ├── init.sql
│   └── README.md
│
├── dataset/                     # PlantVillage dataset
├── model-reference/             # Model development scripts
├── .env.example
├── package.json
├── tsconfig.json
├── next.config.ts
├── eslint.config.mjs
├── postcss.config.mjs
└── README.md
```

---

## Folder Descriptions

### `app/` - Next.js Frontend

| Folder | Description |
|--------|-------------|
| `(auth)/` | Route group untuk login & register |
| `(dashboard)/` | Route group untuk dashboard pages |
| `components/` | Reusable React components |
| `lib/` | Utilities (API client, Supabase client, utils) |
| `hooks/` | Custom React hooks |
| `types/` | TypeScript type definitions |

### `backend/` - Python FastAPI

| Folder | Description |
|--------|-------------|
| `api/` | API package init files |
| `api/v1/` | API version 1 router + endpoints |
| `api/v1/endpoints/` | API route handlers (auth, prediction, history) |
| `core/` | Config, database setup |
| `models/` | SQLAlchemy models (base.py, user, prediction) |
| `schemas/` | Pydantic schemas for request/response |
| `services/` | Business logic (fuzzy engine, image processing, Supabase) |
| `crud/` | Database operations |
| `dependencies.py` | FastAPI dependencies (get_db, get_current_user) |

### `sql/` - Database Scripts

| File | Description |
|------|-------------|
| `init.sql` | Initial table creation |
| `README.md` | Setup instructions for Supabase database |

---

## Tech Stack Summary

| Layer | Technology |
|-------|-------------|
| Frontend | Next.js 16, React 19, Tailwind CSS 4 |
| Backend | Python, FastAPI |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth |
| Storage | Supabase Storage |
| AI/ML | OpenCV, NumPy, scikit-fuzzy |
| Deployment | Vercel (frontend), Railway/Render (backend) |

---

## API Communication

```
┌──────────────┐      axios       ┌──────────────┐       ┌──────────────┐
│   Frontend   │  ──────────────►│    Backend   │──────►│   Supabase   │
│  (Next.js)   │◄───────────────  │  (FastAPI)   │◄──────│  (PostgreSQL │
└──────────────┘                  └──────────────┘       │   + Auth +   │
                                                          │   Storage)   │
                                                          └──────────────┘
```

Frontend berkomunikasi dengan backend via HTTP REST API menggunakan Axios.
Backend menggunakan Supabase untuk database (asyncpg), autentikasi, dan penyimpanan gambar.