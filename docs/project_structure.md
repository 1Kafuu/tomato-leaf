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
│   │   ├── history/
│   │   │   └── page.tsx
│   │   └── upload/
│   │       └── page.tsx
│   ├── components/
│   │   ├── ui/                  # Reusable UI components
│   │   ├── auth/                # Auth components
│   │   └── prediction/          # Prediction components
│   ├── lib/
│   │   ├── api.ts               # Axios client
│   │   ├── auth.ts              # Auth utilities
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
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── auth.py
│   │   │       │   ├── prediction.py
│   │   │       │   └── history.py
│   │   │       └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── prediction.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── prediction.py
│   │   │   └── auth.py
│   │   ├── services/
│   │   │   ├── fuzzy_engine.py
│   │   │   ├── image_processor.py
│   │   │   └── auth_service.py
│   │   ├── crud/
│   │   │   ├── user.py
│   │   │   └── prediction.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
│
├── docs/                        # Documentation
│   ├── project_prd.md
│   ├── ai_model.md
│   ├── database_schema.md
│   └── project_structure.md
│
├── public/                     # Static assets
│   └── images/
│
├── sql/                        # Database scripts
│   ├── init.sql
│   └── migrations/
│
├── .env.example
├── package.json
├── tsconfig.json
├── next.config.ts
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
| `lib/` | Utilities (API client, auth, utils) |
| `hooks/` | Custom React hooks |
| `types/` | TypeScript type definitions |

### `backend/` - Python FastAPI

| Folder | Description |
|--------|-------------|
| `api/v1/endpoints/` | API route handlers |
| `core/` | Config, security, database setup |
| `models/` | SQLAlchemy models |
| `schemas/` | Pydantic schemas |
| `services/` | Business logic (fuzzy engine, image processing) |
| `crud/` | Database operations |

### `sql/` - Database Scripts

| File | Description |
|------|-------------|
| `init.sql` | Initial table creation |
| `migrations/` | Schema change scripts |

---

## Tech Stack Summary

| Layer | Technology |
|-------|-------------|
| Frontend | Next.js 16, React 19, Tailwind CSS 4 |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| AI/ML | OpenCV, NumPy, scikit-fuzzy |
| Deployment | Vercel (frontend), Railway/Render (backend) |

---

## API Communication

```
┌──────────────┐      axios       ┌──────────────┐
│   Frontend   │  ──────────────►│    Backend   │
│  (Next.js)   │◄───────────────  │  (FastAPI)   │
└──────────────┘                  └──────────────┘
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │  PostgreSQL  │
                                   └──────────────┘
```

Frontend berkomunikasi dengan backend via HTTP REST API menggunakan Axios.