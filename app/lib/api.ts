import axios, { AxiosError, AxiosInstance } from "axios";
import type { ApiError } from "@/app/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const API_V2_BASE_URL =
  process.env.NEXT_PUBLIC_API_V2_URL || "http://localhost:8000/api/v2";

function createApi(baseURL: string): AxiosInstance {
  const instance = axios.create({
    baseURL,
    timeout: 30_000,
  });

  instance.interceptors.request.use((config) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("toma_token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  });

  instance.interceptors.response.use(
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

  return instance;
}

export const api = createApi(API_BASE_URL);
export const apiV2 = createApi(API_V2_BASE_URL);

export function getApiError(err: unknown): ApiError {
  if (axios.isAxiosError(err)) {
    return {
      detail:
        err.response?.data?.detail || err.message || "Terjadi kesalahan",
      status: err.response?.status || 500,
    };
  }
  return { detail: "Terjadi kesalahan tidak dikenal", status: 500 };
}
