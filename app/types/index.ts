// User
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

// Prediction (V2 - flat response, 7 features)
export interface PredictionFeatures {
  spot_area: number;
  color_change: number;
  yellow_ratio: number;
  brown_ratio: number;
  dark_ratio: number;
  spot_count: number;
  texture_var: number;
}

export interface PredictionData {
  id: string;
  plant_status: "Sehat" | "Terinfeksi" | string;
  severity_level:
    | "Sehat"
    | "Ringan"
    | "Sedang"
    | "Berat"
    | "Sangat Berat"
    | string;
  fuzzy_score: number;
  severity_score: number;
  features: PredictionFeatures;
  image_url?: string;
  created_at?: string;
}

// History list item (tanpa features, dari V1 endpoint)
export interface PredictionHistoryItem {
  id: string;
  image_url: string;
  plant_status: string;
  severity_level: string;
  fuzzy_score: number;
  severity_score: number;
  created_at: string;
}

// History detail (dengan features)
export interface PredictionHistoryDetail extends PredictionHistoryItem {
  spot_area: number;
  color_change: number;
  yellow_ratio: number;
  brown_ratio: number;
  dark_ratio: number;
  spot_count: number;
  texture_var: number;
}

// API error
export interface ApiError {
  detail: string;
  status: number;
}

// Severity metadata (V2 - severity-based, bukan nama penyakit)
export type SeverityLevel =
  | "Sehat"
  | "Ringan"
  | "Sedang"
  | "Berat"
  | "Sangat Berat";

export type SeverityColor = "green" | "lime" | "yellow" | "tomato" | "red";

export interface SeverityMeta {
  level: SeverityLevel;
  minScore: number;
  maxScore: number;
  color: SeverityColor;
  description: string;
  recommendation: string;
}

export const SEVERITY_META: Record<SeverityLevel, SeverityMeta> = {
  Sehat: {
    level: "Sehat",
    minScore: 85,
    maxScore: 100,
    color: "green",
    description:
      "Daun dalam kondisi optimal, hijau segar, tanpa gejala penyakit.",
    recommendation:
      "Pertahankan perawatan rutin. Lanjutkan jadwal penyiraman dan pemupukan.",
  },
  Ringan: {
    level: "Ringan",
    minScore: 70,
    maxScore: 84,
    color: "lime",
    description:
      "Gejala penyakit tingkat ringan terdeteksi pada sebagian kecil daun.",
    recommendation:
      "Pantau perkembangan 2-3 hari. Isolasi daun yang terinfeksi dan kurangi kelembapan berlebih.",
  },
  Sedang: {
    level: "Sedang",
    minScore: 50,
    maxScore: 69,
    color: "yellow",
    description:
      "Infeksi tingkat sedang. Perubahan warna dan bercak mulai meluas.",
    recommendation:
      "Aplikasikan fungisida nabati. Pangkas daun yang terinfeksi dan perbaiki sirkulasi udara.",
  },
  Berat: {
    level: "Berat",
    minScore: 25,
    maxScore: 49,
    color: "tomato",
    description:
      "Infeksi berat. Kerusakan daun signifikan dengan banyak bercak nekrosis.",
    recommendation:
      "Gunakan fungisida kimia sesuai dosis. Buang daun rusak parah dan karantina tanaman.",
  },
  "Sangat Berat": {
    level: "Sangat Berat",
    minScore: 0,
    maxScore: 24,
    color: "red",
    description:
      "Kerusakan sangat parah, sebagian besar jaringan daun rusak atau mati.",
    recommendation:
      "Konsultasi dengan ahli pertanian. Pertimbangkan pencabutan tanaman untuk mencegah penyebaran.",
  },
};
