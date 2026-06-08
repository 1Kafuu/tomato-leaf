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

// Prediction
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
  plant_status: string;
  features: PredictionFeatures;
}

export interface PredictionResponse {
  success: boolean;
  message: string;
  data: PredictionData;
}

// History list item (tanpa features)
export interface PredictionHistoryItem {
  id: string;
  image_url: string;
  disease_name: string;
  fuzzy_score: number;
  severity_level: string;
  created_at: string;
}

// History detail (dengan features)
export interface PredictionHistoryDetail extends PredictionHistoryItem {
  spot_area: number;
  yellow_ratio: number;
  brown_ratio: number;
  dark_ratio: number;
  color_change: number;
  plant_status?: string;
}

// API error
export interface ApiError {
  detail: string;
  status: number;
}

// Disease metadata
export type DiseaseName =
  | "Sangat Sehat"
  | "Sehat"
  | "Early Blight"
  | "Late Blight"
  | "Leaf Mold"
  | "Septoria Leaf Spot"
  | "Sangat Buruk";

export type DiseaseColor = "green" | "yellow" | "tomato" | "red";

export interface DiseaseMeta {
  name: DiseaseName;
  minScore: number;
  maxScore: number;
  color: DiseaseColor;
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
