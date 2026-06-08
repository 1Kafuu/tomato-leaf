# Frontend Dashboard Documentation

Dokumen ini menjelaskan rancangan dan implementasi frontend (Next.js 16) untuk halaman **Dashboard** dan **History** pada aplikasi **TomaCheck — Tomato Leaf Health Detection App**.

Dokumen ini melengkapi dokumentasi yang sudah ada di folder `docs/` (`prd_tomato_leaf.md`, `backend_documentation.md`, `model_usage.md`, `project_structure.md`).

---

## 1. Overview

Frontend TomaCheck dibangun dengan **Next.js 16 (App Router)**, **TypeScript 5**, **Tailwind CSS 4**, dan **Supabase JS Client** untuk autentikasi & storage. Backend komunikasi melalui **FastAPI** (lihat `backend_documentation.md`).

### Alur End-to-End yang Didukung Frontend

```
[ Landing Page ]
       │  (klik "Mulai Deteksi")
       ▼
[ Register / Login ]  ◀── Supabase Auth (signUp / signInWithPassword)
       │  (JWT tersimpan di localStorage + Supabase session)
       ▼
[ Dashboard ] ─────► Upload gambar (multipart)
       │              ▼
       │          POST /api/v1/predict (Bearer token)
       │              ▼
       │          Tampilkan Result Card (disease_name, fuzzy_score,
       │                                  severity_level, features)
       │              ▼
       │          Auto-saved ke history (backend)
       │
       ├──► [ History ] ──► GET /api/v1/history/  (paginated)
       │              ▼
       │          GET /api/v1/history/{id}  (detail)
       │
       └──► [ Logout ] ──► Supabase signOut + hapus token
```

### Halaman yang Sudah Ada (Referensi Style)

| Halaman | Path | Status | Keterangan |
|---|---|---|---|
| Landing Page | `app/(landing)/page.tsx` | ✅ Selesai | Hero + Fitur + Cara Kerja + Penyakit + CTA + FAQ |
| Login | `app/(auth)/login/page.tsx` | ✅ Selesai (UI) | Form + validasi UI, integrasi API = TODO |
| Register | `app/(auth)/register/page.tsx` | ✅ Selesai (UI) | Form + password strength, integrasi API = TODO |
| Dashboard | `app/(landing)/dashboard/page.tsx` | ❌ TODO | Upload + Result |
| History | `app/(landing)/history/page.tsx` | ❌ TODO | Tabel riwayat + pagination |
| Detail History | `app/(landing)/history/[id]/page.tsx` | ❌ TODO | Detail + gambar besar |

> **Catatan Penting**: Berdasarkan `project_structure.md`, route group `(landing)/` adalah layout untuk halaman yang **belum login boleh akses** (landing page) dan halaman **setelah login** (dashboard, history). Untuk memperbaiki separation, lihat **section 8 (Rekomendasi Struktur)**.

---

## 2. Design System (Konsistensi dengan Halaman Existing)

Semua styling mengikuti design tokens yang sudah didefinisikan di `app/globals.css`. Tidak ada token baru — cukup reuse yang ada.

### 2.1 Color Tokens (sudah ada di globals.css)

| Token | Hex | Penggunaan |
|---|---|---|
| `text-heading` | `#18181B` | Judul, teks utama |
| `text-label` | `#3F3F46` | Label, sub-judul |
| `text-body` | `#52525B` | Body text |
| `text-placeholder` | `#71717A` | Placeholder, caption |
| `text-action` / `surface-primary` | `#097315` | Hijau TomaCheck (primary) |
| `text-action-hover` / `surface-primary-hover` | `#076011` | Hover hijau |
| `surface-primary-light` | `#E6F5E8` | Background light (badge sehat) |
| `border-default` | `#E4E4E7` | Border netral |
| `border-action` | `#097315` | Border focus/hover |
| `tomato-default` | `#E5591D` | Status warning/infeksi |
| `secondary-default` | `#EFDF67` | Status sedang |
| `surface-default` | `#FAFAFA` | Background section alternatif |

### 2.2 Typography Classes (sudah ada di globals.css)

Gunakan class yang sudah ada: `h1-heading`, `h2-heading`, `md-default`, `md-semibold`, `sm-default`, `sm-semibold`, `xs-default`, `xs-semibold`, `label-semibold`, `lg-default`, `lg-semibold`.

### 2.3 Komponen Reusable yang Sudah Ada

Reuse komponen ini di dashboard & history:

| Komponen | Path | Fungsi |
|---|---|---|
| `Navbar` | `app/components/landing/Navbar.tsx` | Header global, dengan conditional CTA (Login/Register vs Dashboard/Logout) |
| `Footer` | `app/components/landing/Footer.tsx` | Footer global |
| `LogoPill` | `app/components/landing/LogoPill.tsx` | Tag header section |
| `Button` | `app/components/landing/Button.tsx` | Tombol primary/secondary (mendukung `inv`, `icon`, `fullWidth`, `href`, `disabled`) |
| `FeatureCard` | `app/components/landing/FeatureCard.tsx` | Kartu info (untuk status panel dashboard) |
| `PageHeading` | `app/components/landing/PageHeading.tsx` | Hero — **referensi gaya Result Card** |

> **Penting**: `Button` component saat ini membungkus `<a>` jika `href` ada, dan `<button>` jika tidak. Untuk submit form atau onClick biasa, gunakan tanpa `href`. Untuk navigasi, bungkus manual dengan `<Link>` dari `next/link` atau gunakan `href` (akan render `<a>`).

### 2.4 Icon System

Mengikuti pattern existing: **inline SVG** dengan `stroke="currentColor"`, `strokeWidth="2"`. Tidak pakai icon library agar konsisten dengan landing page, login, dan register.

---

## 3. Backend API Contract (Ringkasan)

Detail lengkap ada di `backend_documentation.md` dan `prd_tomato_leaf.md`. Berikut ringkasan yang dipakai frontend:

### 3.1 POST /api/v1/auth/register

**Request** (JSON):
```json
{ "email": "user@mail.com", "password": "min8char", "full_name": "Nama Lengkap" }
```

**Response 200** (backend mengembalikan `UserResponse`):
```json
{
  "id": "uuid",
  "email": "user@mail.com",
  "full_name": "Nama Lengkap",
  "created_at": "2026-06-08T10:00:00Z"
}
```

> Setelah register, frontend **otomatis** memanggil `POST /api/v1/auth/login` untuk mendapatkan token (karena endpoint register di backend tidak mengembalikan token, hanya `UserResponse`).

### 3.2 POST /api/v1/auth/login

**Request** (JSON):
```json
{ "email": "user@mail.com", "password": "min8char" }
```

**Response 200**:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": { "id": "uuid", "email": "...", "full_name": "...", "created_at": "..." }
}
```

### 3.3 POST /api/v1/predict

**Request**: `multipart/form-data` dengan field `image` (file). Header `Authorization: Bearer {token}`.

**Response 200**:
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
      "yellow_ratio": 15.20,
      "brown_ratio": 2.80,
      "dark_ratio": 12.50,
      "color_change": 30.50
    }
  }
}
```

### 3.4 GET /api/v1/history/

**Query**: `skip=0&limit=10` (backend pakai skip/limit, bukan page/limit)

**Response 200**: array langsung (bukan wrapped object):
```json
[
  {
    "id": "uuid",
    "image_url": "https://...supabase.co/storage/v1/object/public/images/predictions/uuid.jpg",
    "disease_name": "Early Blight",
    "fuzzy_score": 71.25,
    "severity_level": "Ringan",
    "created_at": "2026-06-08T10:30:00Z"
  }
]
```

### 3.5 GET /api/v1/history/{id}

**Response 200**:
```json
{
  "id": "uuid",
  "image_url": "https://...",
  "disease_name": "Early Blight",
  "fuzzy_score": 71.25,
  "severity_level": "Ringan",
  "created_at": "2026-06-08T10:30:00Z",
  "spot_area": 12.34,
  "yellow_ratio": 15.20,
  "brown_ratio": 2.80,
  "dark_ratio": 12.50,
  "color_change": 30.50
}
```

### 3.6 Error Response Format

Backend menggunakan `HTTPException` FastAPI standar (bukan wrapped `{success, message}`). Format error:
```json
{ "detail": "Email already registered in local DB" }
```

Frontend perlu handle: `401` (unauthorized → redirect ke login), `400` (validation), `413` (file too large), `500` (server error).

---

## 4. Data Models (TypeScript)

File: `app/types/index.ts` (saat ini kosong/TODO). Lengkapi dengan interface berikut:

```ts
// app/types/index.ts

// ===== USER =====
export interface User {
  id: string;
  email: string;
  full_name: string;
  created_at: string;
}

export interface AuthToken {
  access_token: string;
  token_type: "bearer";
  user: User;
}

// ===== PREDICTION =====
export interface PredictionFeatures {
  spot_area: number;
  yellow_ratio: number;
  brown_ratio: number;
  dark_ratio: number;
  color_change: number;
}

export interface PredictionData {
  disease_name: string;
  fuzzy_score: number;
  severity_level: string;
  plant_status: "Sehat" | "Terinfeksi";
  features: PredictionFeatures;
}

export interface PredictionResponse {
  success: boolean;
  message: string;
  data: PredictionData;
}

// Item pada GET /history/ (tanpa features)
export interface PredictionHistoryItem {
  id: string;
  image_url: string;
  disease_name: string;
  fuzzy_score: number;
  severity_level: string;
  created_at: string;
}

// Item pada GET /history/{id} (dengan features)
export interface PredictionHistoryDetail extends PredictionHistoryItem {
  spot_area: number;
  yellow_ratio: number;
  brown_ratio: number;
  dark_ratio: number;
  color_change: number;
}

// ===== API ERROR =====
export interface ApiError {
  detail: string;
  status: number;
}

// ===== DISEASE METADATA (untuk UI) =====
export type DiseaseName =
  | "Sangat Sehat"
  | "Sehat"
  | "Early Blight"
  | "Late Blight"
  | "Leaf Mold"
  | "Septoria Leaf Spot"
  | "Sangat Buruk";

export type SeverityLevel =
  | "Tidak Ada"
  | "Ringan"
  | "Sedang"
  | "Berat"
  | "Sangat Berat";

export interface DiseaseMeta {
  name: DiseaseName;
  minScore: number;
  maxScore: number;
  color: "green" | "yellow" | "tomato" | "red";
  description: string;
}

export const DISEASE_META: Record<DiseaseName, DiseaseMeta> = {
  "Sangat Sehat": {
    name: "Sangat Sehat",
    minScore: 90, maxScore: 100, color: "green",
    description: "Daun dalam kondisi optimal, hijau segar, tanpa gejala penyakit.",
  },
  "Sehat": {
    name: "Sehat",
    minScore: 75, maxScore: 89, color: "green",
    description: "Daun sehat dengan sedikit variasi warna normal.",
  },
  "Early Blight": {
    name: "Early Blight",
    minScore: 60, maxScore: 74, color: "yellow",
    description: "Bercak kecil coklat pada daun bawah, tahap awal infeksi jamur Alternaria.",
  },
  "Late Blight": {
    name: "Late Blight",
    minScore: 45, maxScore: 59, color: "yellow",
    description: "Bercak tidak beraturan dengan tepi daun mengering, infeksi Phytophthora.",
  },
  "Leaf Mold": {
    name: "Leaf Mold",
    minScore: 25, maxScore: 44, color: "tomato",
    description: "Perubahan warna kuning masif dengan bercak halus pada permukaan daun.",
  },
  "Septoria Leaf Spot": {
    name: "Septoria Leaf Spot",
    minScore: 10, maxScore: 24, color: "tomato",
    description: "Bercak bulat kecil dengan tepi gelap dan pusat keabuan.",
  },
  "Sangat Buruk": {
    name: "Sangat Buruk",
    minScore: 0, maxScore: 9, color: "red",
    description: "Kerusakan daun sangat parah, hampir tidak ada jaringan sehat tersisa.",
  },
};
```

---

## 5. API Client & Auth Utilities

### 5.1 `app/lib/api.ts` — Axios Client dengan Auto-Token

```ts
// app/lib/api.ts
import axios, { AxiosError } from "axios";
import type { ApiError } from "@/app/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30_000, // 30s (target backend < 5s; toleransi jaringan)
});

// Inject token dari localStorage sebelum setiap request
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("toma_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Auto-logout pada 401
api.interceptors.response.use(
  (r) => r,
  (err: AxiosError<{ detail?: string }>) => {
    if (err.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("toma_token");
      localStorage.removeItem("toma_user");
      if (!window.location.pathname.startsWith("/login")) {
        window.location.href = "/login";
      }
    }
    return Promise.reject(err);
  }
);

export function getApiError(err: unknown): ApiError {
  if (axios.isAxiosError(err)) {
    return {
      detail: err.response?.data?.detail || err.message || "Terjadi kesalahan",
      status: err.response?.status || 500,
    };
  }
  return { detail: "Terjadi kesalahan tidak dikenal", status: 500 };
}
```

### 5.2 `app/lib/supabase.ts` — Browser Client (untuk Auth saja)

> **Catatan**: Image upload ditangani oleh **backend** (FastAPI), bukan dari Supabase langsung. Frontend **hanya** butuh Supabase client untuk **Auth** (`signUp` / `signInWithPassword` / `signOut` / `getSession`) — sinkron dengan logika di `backend/app/api/v1/endpoints/auth.py`.

```ts
// app/lib/supabase.ts
import { createBrowserClient } from "@supabase/ssr"; // opsional, atau @supabase/auth-helpers
// Jika hanya butuh client-side sederhana, gunakan:
import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || "";
const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
```

> **Tambahan dependency yang perlu di-install**:
> ```bash
> npm install @supabase/supabase-js axios
> ```
> Tambahkan di `package.json` dependencies, lalu import di `lib/api.ts` dan `lib/supabase.ts`.

### 5.3 `app/lib/utils.ts` — Format Helpers

```ts
// app/lib/utils.ts
import type { DiseaseName } from "@/app/types";
import { DISEASE_META } from "@/app/types";

export function formatDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString("id-ID", {
    day: "numeric", month: "long", year: "numeric",
    hour: "2-digit", minute: "2-digit",
  });
}

export function formatPercent(n: number): string {
  return `${n.toFixed(2)}%`;
}

export function diseaseColorClasses(name: DiseaseName) {
  const meta = DISEASE_META[name];
  switch (meta.color) {
    case "green":
      return {
        bg: "bg-surface-primary-light",
        text: "text-surface-primary",
        border: "border-surface-primary",
        pill: "bg-surface-primary-light text-text-action border border-border-action",
      };
    case "yellow":
      return {
        bg: "bg-secondary-100",
        text: "text-secondary-700",
        border: "border-secondary-default",
        pill: "bg-secondary-100 text-secondary-700 border border-secondary-default",
      };
    case "tomato":
      return {
        bg: "bg-tomato-50",
        text: "text-tomato-700",
        border: "border-tomato-default",
        pill: "bg-tomato-50 text-tomato-700 border border-tomato-default",
      };
    case "red":
      return {
        bg: "bg-tomato-100",
        text: "text-tomato-800",
        border: "border-tomato-700",
        pill: "bg-tomato-100 text-tomato-800 border border-tomato-700",
      };
  }
}

export const ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png"];
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB

export function validateImageFile(file: File): string | null {
  if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
    return "Format file harus JPG, JPEG, atau PNG";
  }
  if (file.size > MAX_FILE_SIZE) {
    return "Ukuran file maksimal 10 MB";
  }
  return null;
}
```

---

## 6. Custom Hooks

### 6.1 `app/hooks/useAuth.ts`

```ts
// app/hooks/useAuth.ts
"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { api, getApiError } from "@/app/lib/api";
import type { AuthToken, User } from "@/app/types";

export function useAuth() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hydrated, setHydrated] = useState(false);

  // Restore session dari localStorage
  useEffect(() => {
    const t = localStorage.getItem("toma_token");
    const u = localStorage.getItem("toma_user");
    if (t && u) {
      setToken(t);
      try { setUser(JSON.parse(u)); } catch { /* ignore */ }
    }
    setHydrated(true);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    setLoading(true); setError(null);
    try {
      const { data } = await api.post<AuthToken>("/auth/login", { email, password });
      localStorage.setItem("toma_token", data.access_token);
      localStorage.setItem("toma_user", JSON.stringify(data.user));
      setToken(data.access_token);
      setUser(data.user);
      router.push("/dashboard");
    } catch (err) {
      const e = getApiError(err);
      setError(e.detail === "Incorrect email or password"
        ? "Email atau kata sandi salah"
        : e.detail);
    } finally {
      setLoading(false);
    }
  }, [router]);

  const register = useCallback(async (email: string, password: string, full_name: string) => {
    setLoading(true); setError(null);
    try {
      // 1. Register (backend tidak return token)
      await api.post("/auth/register", { email, password, full_name });
      // 2. Auto-login untuk dapat token
      const { data } = await api.post<AuthToken>("/auth/login", { email, password });
      localStorage.setItem("toma_token", data.access_token);
      localStorage.setItem("toma_user", JSON.stringify(data.user));
      setToken(data.access_token);
      setUser(data.user);
      router.push("/dashboard");
    } catch (err) {
      const e = getApiError(err);
      setError(e.detail);
    } finally {
      setLoading(false);
    }
  }, [router]);

  const logout = useCallback(() => {
    localStorage.removeItem("toma_token");
    localStorage.removeItem("toma_user");
    setToken(null);
    setUser(null);
    router.push("/login");
  }, [router]);

  return { user, token, loading, error, hydrated, login, register, logout };
}
```

### 6.2 `app/hooks/usePrediction.ts`

```ts
// app/hooks/usePrediction.ts
"use client";

import { useState, useCallback } from "react";
import { api, getApiError } from "@/app/lib/api";
import { validateImageFile } from "@/app/lib/utils";
import type { PredictionResponse } from "@/app/types";

export function usePrediction() {
  const [result, setResult] = useState<PredictionResponse["data"] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const reset = useCallback(() => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setResult(null);
    setError(null);
    setPreviewUrl(null);
  }, [previewUrl]);

  const setFile = useCallback((file: File | null) => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    if (file) setPreviewUrl(URL.createObjectURL(file));
    else setPreviewUrl(null);
  }, [previewUrl]);

  const predict = useCallback(async (file: File) => {
    const validation = validateImageFile(file);
    if (validation) { setError(validation); return; }

    setLoading(true); setError(null); setResult(null);
    try {
      const formData = new FormData();
      formData.append("image", file);
      const { data } = await api.post<PredictionResponse>("/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(data.data);
    } catch (err) {
      const e = getApiError(err);
      setError(e.detail);
    } finally {
      setLoading(false);
    }
  }, []);

  return { result, loading, error, previewUrl, predict, reset, setFile };
}

export function useHistory() {
  const [items, setItems] = useState<PredictionHistoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const [skip, setSkip] = useState(0);
  const LIMIT = 10;

  const loadMore = useCallback(async () => {
    if (loading || !hasMore) return;
    setLoading(true); setError(null);
    try {
      const { data } = await api.get<PredictionHistoryItem[]>(
        `/history/?skip=${skip}&limit=${LIMIT}`
      );
      if (data.length < LIMIT) setHasMore(false);
      setItems((prev) => [...prev, ...data]);
      setSkip((s) => s + LIMIT);
    } catch (err) {
      setError(getApiError(err).detail);
    } finally {
      setLoading(false);
    }
  }, [skip, loading, hasMore]);

  const reset = useCallback(() => {
    setItems([]); setSkip(0); setHasMore(true); setError(null);
  }, []);

  return { items, loading, error, hasMore, loadMore, reset };
}
```

---

## 7. Environment Variables

Buat `.env.local` di root project Next.js (sejajar dengan `package.json`):

```env
# Backend FastAPI
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Supabase (untuk Auth browser-side)
NEXT_PUBLIC_SUPABASE_URL=https://yourproject.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

> **Note**: `NEXT_PUBLIC_*` artinya terexpose ke browser. `SUPABASE_ANON_KEY` aman untuk di-browse karena dilindungi RLS Supabase.

---

## 8. Rekomendasi Struktur Route Group

Berdasarkan `project_structure.md` dan kondisi saat ini (halaman dashboard/history ada di dalam `(landing)/` group yang dipakai landing page), **sangat disarankan** memisahkan route group agar:

- `(marketing)/` — landing, login, register (public, no auth required)
- `(app)/` — dashboard, history (protected, butuh JWT)

### Struktur yang Disarankan

```
app/
├── (marketing)/
│   ├── layout.tsx           # Navbar + Footer (seperti (landing)/layout.tsx saat ini)
│   ├── page.tsx             # Landing page (rename dari (landing)/page.tsx)
│   ├── login/page.tsx
│   └── register/page.tsx
│
├── (app)/
│   ├── layout.tsx           # AuthenticatedLayout: Navbar + cek token + redirect ke /login
│   ├── dashboard/page.tsx
│   ├── history/page.tsx
│   └── history/[id]/page.tsx
│
├── components/
│   ├── marketing/           # Rename dari components/landing/ → components/marketing/
│   ├── auth/                # Form components (LoginForm, RegisterForm)
│   ├── dashboard/           # BARU: UploadArea, ResultCard, FeatureTable
│   └── history/             # BARU: HistoryTable, HistoryItem, DetailView
│
├── lib/                     # api.ts, supabase.ts, utils.ts
├── hooks/                   # useAuth.ts, usePrediction.ts, useHistory.ts
├── types/                   # index.ts
└── globals.css
```

> Jika tidak ingin rename folder existing, **minimal**: pindahkan `app/(landing)/dashboard/` dan `app/(landing)/history/` ke dalam **group baru** `app/(app)/` agar bisa menambahkan proteksi auth di layout.

### Auth Guard di `(app)/layout.tsx`

```tsx
// app/(app)/layout.tsx
"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/app/components/marketing/Navbar"; // atau components/landing/Navbar
import Footer from "@/app/components/marketing/Footer";
import { useAuth } from "@/app/hooks/useAuth";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const { user, hydrated, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (hydrated && !user) router.replace("/login");
  }, [hydrated, user, router]);

  if (!hydrated || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse md-default text-text-placeholder">Memuat...</div>
      </div>
    );
  }

  return (
    <>
      <Navbar user={user} onLogout={logout} />
      <main className="flex-1">{children}</main>
      <Footer />
    </>
  );
}
```

> **Update `Navbar.tsx`**: tambah prop `user` & `onLogout` untuk render menu **Dashboard / Riwayat / Logout** saat login, dan **Masuk / Daftar** saat tidak login. Pattern ini sudah umum di Navbar existing — hanya perlu kondisional.

---

## 9. Komponen Dashboard (BARU)

### 9.1 `components/dashboard/UploadArea.tsx`

Area drag-and-drop + tombol "Pilih Gambar" + preview.

```tsx
// app/components/dashboard/UploadArea.tsx
"use client";
import { useRef, useState, DragEvent, ChangeEvent } from "react";
import Image from "next/image";
import { ALLOWED_IMAGE_TYPES, MAX_FILE_SIZE } from "@/app/lib/utils";

type Props = {
  previewUrl: string | null;
  onFileSelected: (file: File) => void;
  onClear: () => void;
  disabled?: boolean;
};

export default function UploadArea({ previewUrl, onFileSelected, onClear, disabled }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);

  const handleFile = (file: File) => {
    setLocalError(null);
    if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
      setLocalError("Format harus JPG, JPEG, atau PNG");
      return;
    }
    if (file.size > MAX_FILE_SIZE) {
      setLocalError("Ukuran file maksimal 10 MB");
      return;
    }
    onFileSelected(file);
  };

  const onDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault(); setIsDragging(false);
    if (disabled) return;
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  if (previewUrl) {
    return (
      <div className="border-2 border-border-default rounded-2xl bg-neutral-white p-4 md:p-6">
        <div className="relative w-full aspect-square md:aspect-video rounded-2xl overflow-hidden border-2 border-border-default bg-surface-default">
          <Image src={previewUrl} alt="Preview" fill className="object-contain" />
        </div>
        <div className="flex gap-3 mt-4">
          <button
            type="button"
            onClick={() => inputRef.current?.click()}
            disabled={disabled}
            className="flex-1 h-12 rounded-2xl border-2 border-border-default hover:border-border-action-hover text-text-heading sm-semibold transition-colors disabled:opacity-50"
          >
            Ganti Gambar
          </button>
          <button
            type="button"
            onClick={onClear}
            disabled={disabled}
            className="h-12 px-5 rounded-2xl border-2 border-border-default hover:border-tomato-default text-tomato-700 sm-semibold transition-colors disabled:opacity-50"
          >
            Hapus
          </button>
        </div>
        <input ref={inputRef} type="file" accept="image/jpeg,image/jpg,image/png" onChange={onChange} className="hidden" />
      </div>
    );
  }

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); if (!disabled) setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={onDrop}
      onClick={() => !disabled && inputRef.current?.click()}
      className={`border-2 border-dashed rounded-2xl bg-neutral-white p-8 md:p-12 text-center cursor-pointer transition-colors ${
        isDragging ? "border-border-action bg-surface-primary-light" : "border-border-default hover:border-border-action-hover"
      } ${disabled ? "opacity-50 cursor-not-allowed" : ""}`}
    >
      <div className="w-16 h-16 mx-auto rounded-2xl bg-surface-default border-2 border-border-default flex items-center justify-center mb-4 text-icon-default">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
          <path d="M12 16V4M12 4L6 10M12 4L18 10M4 20H20" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </div>
      <h3 className="md-semibold text-text-heading mb-1">Seret gambar ke sini</h3>
      <p className="sm-default text-text-placeholder mb-4">atau klik untuk pilih file dari perangkat</p>
      <p className="xs-default text-text-placeholder">Format: JPG, JPEG, PNG • Maks 10 MB</p>
      <input ref={inputRef} type="file" accept="image/jpeg,image/jpg,image/png" onChange={onChange} className="hidden" />
      {localError && <p className="sm-default text-tomato-700 mt-4">{localError}</p>}
    </div>
  );
}
```

### 9.2 `components/dashboard/ResultCard.tsx`

Mirip gaya card di `PageHeading.tsx`, tampilkan hasil diagnosis lengkap.

```tsx
// app/components/dashboard/ResultCard.tsx
import type { PredictionData } from "@/app/types";
import { diseaseColorClasses, formatPercent } from "@/app/lib/utils";
import type { DiseaseName } from "@/app/types";

type Props = { data: PredictionData; onRetake: () => void; onViewHistory: () => void; };

export default function ResultCard({ data, onRetake, onViewHistory }: Props) {
  const color = diseaseColorClasses(data.disease_name as DiseaseName);
  const score = data.fuzzy_score;

  return (
    <div className="border-2 border-border-default rounded-2xl bg-neutral-white overflow-hidden">
      {/* Header — disease + status */}
      <div className="p-5 md:p-6 border-b-2 border-border-default flex items-center gap-3">
        <div className="w-12 h-12 rounded-2xl bg-surface-default text-icon-default border-2 border-border-default flex items-center justify-center shrink-0">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
        <div className="flex-1 min-w-0">
          <p className="xs-semibold text-text-placeholder uppercase tracking-wider mb-1">Hasil Diagnosis</p>
          <h2 className="h2-heading text-text-heading truncate">{data.disease_name}</h2>
        </div>
        <span className={`px-3 py-1.5 rounded-full xs-semibold ${color.pill} shrink-0`}>
          {data.severity_level || "Tanpa gejala"}
        </span>
      </div>

      {/* Score bar */}
      <div className="p-5 md:p-6 border-b-2 border-border-default">
        <div className="flex justify-between items-end mb-3">
          <div>
            <p className="xs-default text-text-placeholder mb-1">Skor Fuzzy</p>
            <p className="text-[40px] md:text-[48px] leading-none font-bold text-text-action">{score.toFixed(2)}</p>
          </div>
          <p className="sm-default text-text-placeholder">Status: <span className="sm-semibold text-text-heading">{data.plant_status}</span></p>
        </div>
        <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
          <div className="h-full bg-surface-primary rounded-full transition-all" style={{ width: `${score}%` }} />
        </div>
      </div>

      {/* Features */}
      <div className="p-5 md:p-6 border-b-2 border-border-default">
        <p className="xs-semibold text-text-placeholder uppercase tracking-wider mb-4">Fitur Visual</p>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          <FeatureItem label="Spot Area" value={data.features.spot_area} />
          <FeatureItem label="Kuning" value={data.features.yellow_ratio} />
          <FeatureItem label="Coklat" value={data.features.brown_ratio} />
          <FeatureItem label="Gelap" value={data.features.dark_ratio} />
          <FeatureItem label="Perubahan" value={data.features.color_change} />
        </div>
      </div>

      {/* Actions */}
      <div className="p-5 md:p-6 flex flex-col md:flex-row gap-3">
        <button onClick={onRetake} className="flex-1 h-12 md:h-14 rounded-2xl bg-surface-primary hover:bg-surface-primary-hover text-neutral-white md-semibold transition-colors">
          Deteksi Lagi
        </button>
        <button onClick={onViewHistory} className="flex-1 h-12 md:h-14 rounded-2xl border-2 border-border-default hover:border-border-action-hover text-text-heading md-semibold transition-colors">
          Lihat Riwayat
        </button>
      </div>
    </div>
  );
}

function FeatureItem({ label, value }: { label: string; value: number }) {
  return (
    <div className="text-center py-3 px-2 border-2 border-border-default rounded-2xl">
      <p className="xs-default text-text-placeholder mb-1">{label}</p>
      <p className="md-semibold text-text-heading">{formatPercent(value)}</p>
    </div>
  );
}
```

### 9.3 `components/dashboard/LoadingState.tsx`

Loading spinner dengan pesan "Sedang menganalisis...".

```tsx
// app/components/dashboard/LoadingState.tsx
export default function LoadingState() {
  return (
    <div className="border-2 border-border-default rounded-2xl bg-neutral-white p-8 md:p-12 text-center">
      <div className="w-16 h-16 mx-auto rounded-2xl bg-surface-primary-light border-2 border-border-action flex items-center justify-center mb-4">
        <svg className="animate-spin" width="28" height="28" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" className="opacity-25" />
          <path d="M4 12a8 8 0 018-8" stroke="currentColor" strokeWidth="3" strokeLinecap="round" className="text-icon-action" />
        </svg>
      </div>
      <h3 className="md-semibold text-text-heading mb-1">Sedang Menganalisis...</h3>
      <p className="sm-default text-text-placeholder">Proses ini biasanya memakan waktu kurang dari 5 detik</p>
    </div>
  );
}
```

---

## 10. Halaman Dashboard

### 10.1 `app/(app)/dashboard/page.tsx` (atau `app/(landing)/dashboard/page.tsx`)

```tsx
// app/(app)/dashboard/page.tsx
"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import LogoPill from "@/app/components/landing/LogoPill";
import UploadArea from "@/app/components/dashboard/UploadArea";
import ResultCard from "@/app/components/dashboard/ResultCard";
import LoadingState from "@/app/components/dashboard/LoadingState";
import { usePrediction } from "@/app/hooks/usePrediction";

export default function DashboardPage() {
  const router = useRouter();
  const { result, loading, error, previewUrl, predict, reset, setFile } = usePrediction();
  const [file, setLocalFile] = useState<File | null>(null);

  const handleFileSelected = (f: File) => { setLocalFile(f); setFile(f); };
  const handleDetect = async () => { if (file) await predict(file); };
  const handleRetake = () => { setLocalFile(null); reset(); };
  const handleViewHistory = () => router.push("/history");

  return (
    <div className="max-w-4xl mx-auto px-5 md:px-10 py-10 md:py-16">
      <div className="flex justify-center mb-6">
        <LogoPill text="Deteksi Daun Tomat" />
      </div>
      <h1 className="h1-heading font-bold text-text-heading mb-3 text-center">
        Unggah Foto Daun Tomat Anda
      </h1>
      <p className="md-default text-text-placeholder text-center max-w-2xl mx-auto mb-10 leading-relaxed">
        Sistem akan melakukan segmentasi, ekstraksi fitur, dan inferensi Fuzzy Sugeno
        untuk memberikan diagnosis dalam hitungan detik.
      </p>

      {error && (
        <div className="mb-6 p-4 rounded-2xl border-2 border-tomato-default bg-tomato-50 sm-default text-tomato-700">
          {error}
        </div>
      )}

      {!result && !loading && (
        <div className="space-y-4">
          <UploadArea previewUrl={previewUrl} onFileSelected={handleFileSelected} onClear={() => { setLocalFile(null); setFile(null); }} />
          <button
            onClick={handleDetect}
            disabled={!file}
            className="w-full h-14 rounded-2xl bg-surface-primary hover:bg-surface-primary-hover text-neutral-white md-semibold transition-colors disabled:bg-surface-disabled disabled:text-text-disabled"
          >
            Deteksi Sekarang
          </button>
        </div>
      )}

      {loading && <LoadingState />}

      {result && !loading && (
        <ResultCard data={result} onRetake={handleRetake} onViewHistory={handleViewHistory} />
      )}
    </div>
  );
}
```

---

## 11. Halaman History

### 11.1 `components/history/HistoryItem.tsx`

```tsx
// app/components/history/HistoryItem.tsx
import Link from "next/link";
import Image from "next/image";
import type { PredictionHistoryItem } from "@/app/types";
import { diseaseColorClasses, formatDate } from "@/app/lib/utils";
import type { DiseaseName } from "@/app/types";

export default function HistoryItem({ item }: { item: PredictionHistoryItem }) {
  const color = diseaseColorClasses(item.disease_name as DiseaseName);
  return (
    <Link
      href={`/history/${item.id}`}
      className="grid grid-cols-[64px_1fr_auto] md:grid-cols-[80px_1fr_120px_140px_180px_auto] gap-3 md:gap-4 items-center p-3 md:p-4 border-2 border-border-default rounded-2xl bg-neutral-white hover:border-border-action transition-colors"
    >
      <div className="relative w-16 h-16 md:w-20 md:h-20 rounded-2xl overflow-hidden border border-border-default bg-surface-default shrink-0">
        {item.image_url ? (
          <Image src={item.image_url} alt={item.disease_name} fill className="object-cover" sizes="80px" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-icon-default text-xs">No img</div>
        )}
      </div>
      <div className="min-w-0">
        <span className={`inline-block px-2.5 py-1 rounded-full text-xs font-semibold ${color.pill} mb-1`}>
          {item.disease_name}
        </span>
        <p className="sm-default text-text-placeholder md:hidden">{formatDate(item.created_at)}</p>
      </div>
      <p className="hidden md:block md-default text-text-label">Ringan</p>
      <div className="hidden md:flex items-center gap-2">
        <span className="text-[20px] font-bold text-text-action leading-none">{item.fuzzy_score.toFixed(1)}</span>
        <div className="flex-1 h-1.5 bg-neutral-100 rounded-full overflow-hidden">
          <div className="h-full bg-surface-primary" style={{ width: `${item.fuzzy_score}%` }} />
        </div>
      </div>
      <p className="hidden md:block sm-default text-text-placeholder">{formatDate(item.created_at)}</p>
      <svg className="text-icon-default" width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </Link>
  );
}
```

### 11.2 `app/(app)/history/page.tsx`

```tsx
// app/(app)/history/page.tsx
"use client";
import { useEffect } from "react";
import LogoPill from "@/app/components/landing/LogoPill";
import HistoryItem from "@/app/components/history/HistoryItem";
import { useHistory } from "@/app/hooks/usePrediction"; // atau pisah hook

export default function HistoryPage() {
  const { items, loading, error, hasMore, loadMore, reset } = useHistory();

  useEffect(() => { reset(); loadMore(); }, []); // eslint-disable-line

  return (
    <div className="max-w-5xl mx-auto px-5 md:px-10 py-10 md:py-16">
      <div className="flex justify-center mb-6">
        <LogoPill text="Riwayat Deteksi" />
      </div>
      <h1 className="h1-heading font-bold text-text-heading mb-3 text-center">Riwayat Prediksi Anda</h1>
      <p className="md-default text-text-placeholder text-center max-w-2xl mx-auto mb-10">
        Daftar lengkap deteksi yang pernah Anda lakukan. Klik untuk melihat detail.
      </p>

      {error && (
        <div className="mb-6 p-4 rounded-2xl border-2 border-tomato-default bg-tomato-50 sm-default text-tomato-700">{error}</div>
      )}

      {items.length === 0 && !loading && (
        <div className="border-2 border-dashed border-border-default rounded-2xl p-12 text-center">
          <p className="md-default text-text-placeholder mb-4">Belum ada riwayat deteksi</p>
          <a href="/dashboard" className="inline-flex h-12 items-center px-6 rounded-2xl bg-surface-primary text-neutral-white sm-semibold hover:bg-surface-primary-hover">
            Mulai Deteksi
          </a>
        </div>
      )}

      <div className="flex flex-col gap-3">
        {items.map((it) => <HistoryItem key={it.id} item={it} />)}
      </div>

      {hasMore && (
        <div className="flex justify-center mt-8">
          <button onClick={loadMore} disabled={loading} className="h-12 px-6 rounded-2xl border-2 border-border-default hover:border-border-action-hover text-text-heading sm-semibold transition-colors disabled:opacity-50">
            {loading ? "Memuat..." : "Muat Lebih Banyak"}
          </button>
        </div>
      )}
    </div>
  );
}
```

### 11.3 `app/(app)/history/[id]/page.tsx`

```tsx
// app/(app)/history/[id]/page.tsx
"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Image from "next/image";
import { api, getApiError } from "@/app/lib/api";
import { useAuth } from "@/app/hooks/useAuth";
import LogoPill from "@/app/components/landing/LogoPill";
import { diseaseColorClasses, formatDate, formatPercent } from "@/app/lib/utils";
import type { PredictionHistoryDetail, DiseaseName } from "@/app/types";

export default function HistoryDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const { hydrated, user } = useAuth();
  const [data, setData] = useState<PredictionHistoryDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!hydrated || !user) return;
    (async () => {
      try {
        const { data } = await api.get<PredictionHistoryDetail>(`/history/${id}`);
        setData(data);
      } catch (err) { setError(getApiError(err).detail); }
      finally { setLoading(false); }
    })();
  }, [id, hydrated, user]);

  if (loading) return <div className="p-10 text-center text-text-placeholder">Memuat...</div>;
  if (error) return <div className="p-10 text-center text-tomato-700">{error}</div>;
  if (!data) return null;

  const color = diseaseColorClasses(data.disease_name as DiseaseName);

  return (
    <div className="max-w-5xl mx-auto px-5 md:px-10 py-10 md:py-16">
      <button onClick={() => router.back()} className="inline-flex items-center gap-2 sm-default text-text-label hover:text-text-action transition-colors mb-6">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M19 12H5M12 19L5 12L12 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        Kembali
      </button>

      <div className="flex justify-center mb-6"><LogoPill text="Detail Prediksi" /></div>
      <h1 className="h1-heading font-bold text-text-heading mb-2 text-center">{data.disease_name}</h1>
      <p className="sm-default text-text-placeholder text-center mb-10">{formatDate(data.created_at)}</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="relative w-full aspect-square md:aspect-auto md:h-full rounded-2xl overflow-hidden border-2 border-border-default bg-surface-default">
          {data.image_url && <Image src={data.image_url} alt={data.disease_name} fill className="object-contain" />}
        </div>

        <div className="space-y-4">
          <div className="border-2 border-border-default rounded-2xl p-5">
            <p className="xs-semibold text-text-placeholder uppercase tracking-wider mb-2">Skor Fuzzy</p>
            <div className="flex items-end justify-between mb-3">
              <p className="text-[40px] font-bold text-text-action leading-none">{data.fuzzy_score.toFixed(2)}</p>
              <span className={`px-3 py-1.5 rounded-full xs-semibold ${color.pill}`}>{data.severity_level}</span>
            </div>
            <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
              <div className="h-full bg-surface-primary" style={{ width: `${data.fuzzy_score}%` }} />
            </div>
          </div>

          <div className="border-2 border-border-default rounded-2xl p-5">
            <p className="xs-semibold text-text-placeholder uppercase tracking-wider mb-4">Fitur Visual</p>
            <div className="space-y-3">
              <FeatureRow label="Spot Area" value={data.spot_area} />
              <FeatureRow label="Yellow Ratio" value={data.yellow_ratio} />
              <FeatureRow label="Brown Ratio" value={data.brown_ratio} />
              <FeatureRow label="Dark Ratio" value={data.dark_ratio} />
              <FeatureRow label="Color Change" value={data.color_change} />
            </div>
          </div>

          <a href="/dashboard" className="block w-full h-12 md:h-14 rounded-2xl bg-surface-primary hover:bg-surface-primary-hover text-neutral-white md-semibold text-center leading-[3.5rem] transition-colors">
            Deteksi Baru
          </a>
        </div>
      </div>
    </div>
  );
}

function FeatureRow({ label, value }: { label: string; value: number }) {
  return (
    <div className="flex items-center gap-3">
      <span className="sm-default text-text-label w-32 shrink-0">{label}</span>
      <div className="flex-1 h-2 bg-neutral-100 rounded-full overflow-hidden">
        <div className="h-full bg-surface-primary" style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
      <span className="sm-semibold text-text-heading w-16 text-right">{formatPercent(value)}</span>
    </div>
  );
}
```

---

## 12. Integrasi Auth (Login & Register)

### 12.1 Update `app/(auth)/login/page.tsx`

Hanya tambahkan hook `useAuth` ke handler submit (UI sudah ada):

```tsx
// Tambahkan di dalam LoginPage component:
import { useAuth } from "@/app/hooks/useAuth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

const { login, loading, error, user, hydrated } = useAuth();
const router = useRouter();

useEffect(() => { if (hydrated && user) router.replace("/dashboard"); }, [hydrated, user, router]);

const onSubmit = (e: React.FormEvent) => {
  e.preventDefault();
  if (!email || !password) return;
  login(email, password);
};

// Di form:
<form onSubmit={onSubmit} ...>
  {error && <p className="sm-default text-tomato-700 text-center">{error}</p>}
  <Button text={loading ? "Memproses..." : "Masuk"} inv={true} icon={false} fullWidth={true} />
  ...
</form>
```

### 12.2 Update `app/(auth)/register/page.tsx`

Sama seperti login, tambahkan `useAuth().register`:

```tsx
const { register, loading, error } = useAuth();
const onSubmit = (e: React.FormEvent) => {
  e.preventDefault();
  if (!fullName || !email || !password || password !== confirmPassword || !agree) return;
  register(email, password, fullName);
};
```

---

## 13. Update Navbar (Kondisional Auth)

`app/components/landing/Navbar.tsx` saat ini hanya menampilkan "Masuk / Daftar". Update untuk handle state login:

```tsx
// app/components/landing/Navbar.tsx (update)
"use client";
import Link from "next/link";
import Image from "next/image";
import { useAuth } from "@/app/hooks/useAuth";

type Props = { user?: any; onLogout?: () => void };

export default function Navbar({ user, onLogout }: Props) {
  // Jika dipanggil tanpa props, pakai useAuth (untuk backward compat di landing page)
  const auth = useAuth();
  const currentUser = user ?? auth.user;
  const handleLogout = onLogout ?? auth.logout;

  return (
    <header className="sticky top-0 z-50 w-full border-b-2 border-border-default bg-neutral-white/90 backdrop-blur">
      <div className="max-w-7xl mx-auto px-5 md:px-10 h-16 md:h-20 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5">
          <Image src="/images/logo.svg" alt="TomaCheck" width={28} height={28} className="h-7 w-auto" />
          <span className="md-semibold text-text-heading">TomaCheck</span>
        </Link>

        {currentUser ? (
          <>
            <nav className="hidden md:flex items-center gap-8">
              <Link href="/dashboard" className="sm-default text-text-label hover:text-text-action transition-colors">Dashboard</Link>
              <Link href="/history" className="sm-default text-text-label hover:text-text-action transition-colors">Riwayat</Link>
            </nav>
            <div className="flex items-center gap-2 md:gap-3">
              <span className="hidden md:inline sm-default text-text-label">{currentUser.full_name}</span>
              <button onClick={handleLogout} className="inline-flex h-10 items-center px-4 md:px-5 rounded-2xl border-2 border-border-default hover:border-tomato-default text-tomato-700 sm-semibold transition-colors">
                Keluar
              </button>
            </div>
          </>
        ) : (
          <>
            <nav className="hidden md:flex items-center gap-8">
              <a href="/#fitur" className="sm-default text-text-label hover:text-text-action transition-colors">Fitur</a>
              <a href="/#cara-kerja" className="sm-default text-text-label hover:text-text-action transition-colors">Cara Kerja</a>
              <a href="/#penyakit" className="sm-default text-text-label hover:text-text-action transition-colors">Penyakit</a>
              <a href="/#faq" className="sm-default text-text-label hover:text-text-action transition-colors">FAQ</a>
            </nav>
            <div className="flex items-center gap-2 md:gap-3">
              <Link href="/login" className="hidden md:inline-flex h-10 items-center px-4 sm-semibold text-text-action hover:text-text-action-hover">Masuk</Link>
              <Link href="/register" className="inline-flex h-10 items-center px-4 md:px-5 rounded-2xl bg-surface-primary text-neutral-white sm-semibold hover:bg-surface-primary-hover">Daftar</Link>
            </div>
          </>
        )}
      </div>
    </header>
  );
}
```

---

## 14. Error Handling & UX

### 14.1 Error Codes dari Backend → User Message

| Status | Backend `detail` | User-facing message |
|---|---|---|
| 400 | "Email already registered in local DB" | "Email sudah terdaftar" |
| 400 | "File must be an image" | "File harus berupa gambar" |
| 400 | "Image size exceeds 10MB" | "Ukuran gambar melebihi 10 MB" |
| 401 | "Could not validate credentials" | "Sesi berakhir, silakan login ulang" |
| 401 | "Incorrect email or password" | "Email atau kata sandi salah" |
| 404 | "User not found in local DB" | "Akun tidak ditemukan" |
| 404 | "Prediction not found" | "Prediksi tidak ditemukan" |
| 403 | "Not authorized to access this prediction" | "Anda tidak memiliki akses" |
| 500 | "Supabase client not configured" | "Layanan tidak tersedia, hubungi admin" |
| 500 | "Prediction failed: ..." | "Gagal memproses gambar, coba lagi" |
| Network | — | "Tidak ada koneksi, periksa internet Anda" |

### 14.2 UX Patterns

- **Loading state**: Selalu tampilkan `LoadingState` selama request > 200ms (cegah flicker dengan `setTimeout` opsional).
- **Optimistic UI**: Tidak perlu untuk upload (gambar besar).
- **Disable button saat loading**: Hindari double-submit.
- **Auto-retry**: Tidak di MVP (sesuai PRD).
- **Toast notification**: Opsional untuk MVP; gunakan inline error dulu.
- **Logout otomatis pada 401**: Sudah dihandle di interceptor axios (Section 5.1).

---

## 15. Responsive Behavior

Mengikuti pola halaman existing:

| Breakpoint | Behavior |
|---|---|
| `< 768px` (mobile) | Single column, padding `px-5`, button full-width, Navbar collapse |
| `≥ 768px` (tablet) | Padding `px-10`, Navbar tampil link |
| `≥ 1440px` (desktop) | Max-width container `max-w-7xl` atau `max-w-4xl` |

Sudah menjadi default di Tailwind utility yang dipakai di landing/login/register.

---

## 16. Testing Checklist

### Manual Test (sesuai flow PRD)

- [ ] **Register**: Buka `/register` → isi form valid → submit → redirect ke `/dashboard` dengan user tersimpan di localStorage.
- [ ] **Login invalid**: Email/password salah → tampil error "Email atau kata sandi salah".
- [ ] **Login valid**: Redirect ke `/dashboard`.
- [ ] **Auth guard**: Buka `/dashboard` tanpa token → redirect ke `/login`.
- [ ] **Auth guard**: Buka `/history` tanpa token → redirect ke `/login`.
- [ ] **Upload invalid**: Upload `.pdf` → tampil error "Format harus JPG, JPEG, atau PNG".
- [ ] **Upload > 10MB**: Tampilkan error "Ukuran file maksimal 10 MB".
- [ ] **Upload valid**: Preview tampil, tombol "Deteksi Sekarang" enabled.
- [ ] **Predict**: Klik "Deteksi Sekarang" → LoadingState → ResultCard dengan skor & fitur.
- [ ] **Predict invalid image**: Backend error → tampil error message.
- [ ] **Deteksi Lagi**: Reset upload, kembali ke empty state.
- [ ] **Lihat Riwayat**: Navigasi ke `/history` dengan item baru.
- [ ] **History list**: Tampilkan item dengan thumbnail, disease, score, tanggal.
- [ ] **History detail**: Klik item → tampil detail dengan gambar besar & fitur.
- [ ] **History unauthorized**: Buka `/history/{id}` orang lain → tampil 403.
- [ ] **Logout**: Token dihapus, redirect ke `/login`, route protected redirect otomatis.
- [ ] **Responsive**: Test di mobile (375px), tablet (768px), desktop (1440px).

### Integration Verification

- [ ] Backend `/auth/register` membuat user di Supabase + local DB.
- [ ] Backend `/auth/login` return `{access_token, user}`.
- [ ] Backend `/predict` menyimpan ke `prediction_history` dengan `user_id` yang benar.
- [ ] Backend `/history/?skip=0&limit=10` return array dengan item user yang login.
- [ ] Backend `/history/{id}` validasi ownership (403 jika bukan milik user).
- [ ] Image yang diupload muncul di Supabase Storage bucket `images/predictions/`.

---

## 17. File Checklist (Implementasi)

### File BARU yang harus dibuat

```
app/
├── types/
│   └── index.ts                          # ✅ Update (User, AuthToken, PredictionData, dll)
├── lib/
│   ├── api.ts                            # ✅ Update (Axios client + interceptors)
│   ├── supabase.ts                       # ✅ Update (Browser client)
│   └── utils.ts                          # ✅ Update (format helpers, validateImageFile)
├── hooks/
│   ├── useAuth.ts                        # ✅ Update (login, register, logout)
│   └── usePrediction.ts                  # ✅ Update (predict, history)
├── components/
│   ├── dashboard/
│   │   ├── UploadArea.tsx                # 🆕
│   │   ├── ResultCard.tsx                # 🆕
│   │   └── LoadingState.tsx              # 🆕
│   └── history/
│       └── HistoryItem.tsx               # 🆕
├── (app)/
│   ├── layout.tsx                        # 🆕 (Auth guard)
│   ├── dashboard/
│   │   └── page.tsx                      # 🆕 atau update (landing)/dashboard/page.tsx
│   ├── history/
│   │   ├── page.tsx                      # 🆕 atau update (landing)/history/page.tsx
│   │   └── [id]/
│   │       └── page.tsx                  # 🆕
└── (auth)/
    ├── login/page.tsx                    # ✅ Update (panggil useAuth.login)
    └── register/page.tsx                 # ✅ Update (panggil useAuth.register)
```

### File yang di-UPDATE

```
app/
├── components/
│   └── landing/
│       └── Navbar.tsx                    # ✅ Update (kondisional auth state)
├── (landing)/
│   ├── layout.tsx                        # (Opsional rename ke (marketing))
│   ├── page.tsx                          # (Opsional, jika rename)
│   ├── dashboard/page.tsx                # ✅ Update (isi implementasi)
│   └── history/page.tsx                  # ✅ Update (isi implementasi)
```

### Dependencies tambahan

```bash
npm install @supabase/supabase-js axios
```

### Environment variables

```env
# .env.local (root project)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SUPABASE_URL=https://yourproject.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOi...
```

---

## 18. Sinkronisasi dengan Model & Backend

### Alur Data Lengkap (Sinkron)

```
┌──────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js)                       │
│                                                                  │
│  [User]                                                          │
│    │                                                             │
│    ├──► Login form ──► POST /api/v1/auth/login                   │
│    │                  (axios + JSON body)                        │
│    │                          │                                 │
│    │                          ▼ Backend validate via Supabase    │
│    │                          ▼ Return {access_token, user}      │
│    │                          ▼ Save ke localStorage             │
│    │                                                             │
│    ├──► Dashboard upload ──► POST /api/v1/predict                │
│    │                        (multipart/form-data)                │
│    │                        Authorization: Bearer {token}        │
│    │                                │                            │
│    │                                ▼ FastAPI endpoint           │
│    │                                ▼ app.dependencies           │
│    │                                  .get_current_user          │
│    │                                  (verifies JWT via          │
│    │                                   Supabase)                 │
│    │                                ▼ app.core.model             │
│    │                                  .pipeline.predict()        │
│    │                                    │                        │
│    │                                    ├─► segmenter.segment()  │
│    │                                    ├─► feature_extractor    │
│    │                                    ├─► fuzzy_engine.infer() │
│    │                                    └─► fuzzy_engine         │
│    │                                        .classify()          │
│    │                                ▼ Return PredictionData     │
│    │                                ▼ Frontend tampil ResultCard│
│    │                                                             │
│    ├──► History ──► GET /api/v1/history/?skip=0&limit=10        │
│    │               (Bearer token)                                │
│    │                          │                                 │
│    │                          ▼ app.crud.prediction             │
│    │                            .get_user_predictions()          │
│    │                          ▼ Return array of items            │
│    │                                                             │
│    └──► History detail ──► GET /api/v1/history/{id}             │
│                           (Bearer token, ownership check)        │
└──────────────────────────────────────────────────────────────────┘
```

### Kesesuaian dengan `model_usage.md`

| Komponen Model (Backend) | Output | Dipakai Frontend di |
|---|---|---|
| `predict()` return `disease_name` | string | `ResultCard`, `HistoryItem` |
| `predict()` return `fuzzy_score` | float | `ResultCard` (score bar) |
| `predict()` return `severity_level` | string | `ResultCard` (badge), `HistoryItem` |
| `predict()` return `plant_status` | string | `ResultCard` |
| `predict()` return `spot_area` | float | `ResultCard.features`, detail page |
| `predict()` return `yellow_ratio` | float | `ResultCard.features`, detail page |
| `predict()` return `brown_ratio` | float | `ResultCard.features`, detail page |
| `predict()` return `dark_ratio` | float | `ResultCard.features`, detail page |
| `predict()` return `color_change` | float | `ResultCard.features`, detail page |

**Catatan**: `pipeline.predict()` mengembalikan 9 field sesuai `model_usage.md` Section "Return format", dan backend `prediction.py` endpoint membungkus ke `PredictionData.features` (object). Frontend mengakses `data.features.spot_area`, dst. — **sesuai**.

### Kesesuaian dengan `prd_tomato_leaf.md`

| PRD Requirement | Status Implementasi |
|---|---|
| FR-01: Registrasi dengan validasi | ✅ Hook `register` + form validation di `register/page.tsx` |
| FR-02: Login dengan JWT | ✅ Hook `login` + token di localStorage |
| FR-03: Upload JPG/JPEG/PNG ≤ 10 MB | ✅ `validateImageFile` di utils + `UploadArea` UI |
| FR-08: Tampilkan hasil diagnosis | ✅ `ResultCard` |
| FR-09: Riwayat deteksi paginated | ✅ `useHistory` + `HistoryItem` (infinite scroll, equivalent dengan paginasi) |
| FR-10: Validasi file (MIME + size) | ✅ Client-side + backend tetap validasi |
| Responsive UI (320px – 1920px) | ✅ Pakai utility Tailwind responsif yang sama dengan landing |
| Bahasa Indonesia | ✅ Semua copy dalam Bahasa Indonesia |
| Loading indicator | ✅ `LoadingState` component |
| Error handling user-friendly | ✅ Section 14 |

---

## 19. Catatan & Limitasi MVP

1. **Refresh token**: Belum diimplementasi. JWT Supabase default expire 1 jam; untuk MVP, user harus login ulang setelahnya. PRD menentukan `ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7` di backend config tapi `auth.py` saat ini hanya pakai session Supabase. Untuk production, tambahkan refresh token flow.

2. **Sinkronisasi user profile**: `get_current_user` di backend lookup by email. Pastikan setiap register di Supabase Auth SELALU disertai insert ke local DB (sudah ada di `crud/user.py`).

3. **Image storage URL**: `upload_image_to_storage` saat ini return URL public Supabase Storage. Frontend bisa langsung pakai URL ini untuk `<Image src=...>`. Pastikan RLS bucket `images` mengizinkan public read untuk path `predictions/`.

4. **Tidak ada delete/edit history di MVP**: Sesuai PRD (P1 only — "Detection history paginated, dengan detail"). Delete/edit belum di-scope.

5. **No real-time updates**: Jika user deteksi dari device lain, history tidak auto-refresh. Implementasi: pull-to-refresh di mobile atau refresh button.

6. **Single device assumption**: Token di localStorage tidak sync antar device/tab — by design.

7. **Backend skip/limit vs PRD page/limit**: PRD menyebutkan `page` dan `limit`, tapi backend `history.py` pakai `skip` dan `limit`. Frontend hook `useHistory` di Section 6.2 menggunakan `skip` agar sesuai dengan backend aktual. Jika PRD adalah acuan final, update backend (atau transform di frontend).

---

## 20. Referensi Silang

| Topik | Lihat dokumen |
|---|---|
| Spesifikasi model (pipeline, MF, rules) | `docs/model_usage.md` |
| API contract lengkap | `docs/backend_documentation.md` |
| Alur backend + struktur direktori | `docs/backend_flow.md` |
| Database schema PostgreSQL | `docs/prd_tomato_leaf.md` (Section Database Design) |
| Frontend structure plan | `docs/project_structure.md` |
| Aturan fuzzy + output classes | `docs/prd_tomato_leaf.md` (Section Rule Base, Disease Classification) |
| Style tokens & utility classes | `app/globals.css` |
| Komponen existing reference | `app/components/landing/*.tsx`, `app/(auth)/*/page.tsx` |

---

*Dokumen ini menjadi acuan untuk mengimplementasikan halaman Dashboard, History, dan integrasi Auth agar seluruh flow aplikasi (Landing → Register/Login → Dashboard → Predict → History → Detail → Logout) berjalan end-to-end dengan frontend, backend, dan model Fuzzy Sugeno yang sudah ada.*
