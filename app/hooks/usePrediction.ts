"use client";

import { useState, useCallback, useEffect, useRef } from "react";
import { apiV2, getApiError } from "@/app/lib/api";
import { validateImageFile } from "@/app/lib/utils";
import type {
  PredictionData,
  PredictionHistoryItem,
} from "@/app/types";

export function usePrediction() {
  const [result, setResult] = useState<PredictionData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const reset = useCallback(() => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setResult(null);
    setError(null);
    setPreviewUrl(null);
  }, [previewUrl]);

  const setFile = useCallback(
    (file: File | null) => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
      if (file) setPreviewUrl(URL.createObjectURL(file));
      else setPreviewUrl(null);
    },
    [previewUrl]
  );

  // Cleanup object URL saat unmount
  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const predict = useCallback(async (file: File) => {
    const validation = validateImageFile(file);
    if (validation) {
      setError(validation);
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("image", file);
      // V2: flat response { id, image_url, plant_status, severity_level, fuzzy_score, severity_score, features, created_at }
      const { data } = await apiV2.post<{
        id: string;
        success?: boolean;
        message?: string;
        image_url?: string;
        plant_status: string;
        severity_level: string;
        fuzzy_score: number;
        severity_score: number;
        features: {
          spot_area: number;
          color_change: number;
          yellow_ratio: number;
          brown_ratio: number;
          dark_ratio: number;
          spot_count: number;
          texture_var: number;
        };
        created_at?: string;
      }>("/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult({
        id: data.id,
        plant_status: data.plant_status,
        severity_level: data.severity_level,
        fuzzy_score: data.fuzzy_score,
        severity_score: data.severity_score,
        image_url: data.image_url,
        created_at: data.created_at,
        features: data.features,
      });
    } catch (err) {
      const e = getApiError(err);
      setError(e.detail || "Gagal memproses gambar");
    } finally {
      setLoading(false);
    }
  }, []);

  return { result, loading, error, previewUrl, predict, reset, setFile };
}

export function useHistory(limit = 10) {
  const [items, setItems] = useState<PredictionHistoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const [skip, setSkip] = useState(0);

  // Ref untuk menandai request yang sedang in-flight.
  // Mencegah double-fetch di React StrictMode (effect dipanggil 2x saat mount).
  const inFlightRef = useRef(false);

  const loadMore = useCallback(async () => {
    if (inFlightRef.current) return;
    inFlightRef.current = true;
    setLoading(true);
    setError(null);
    try {
      // V2: history pakai prediction_records (lengkap dengan 7 fitur)
      const { data } = await apiV2.get<PredictionHistoryItem[]>(
        `/history/?skip=${skip}&limit=${limit}`
      );
      if (data.length < limit) setHasMore(false);
      // Dedupe by id sebagai safety net jika backend mengembalikan
      // item yang sama pada halaman berbeda.
      setItems((prev) => {
        const seen = new Set(prev.map((p) => p.id));
        const merged = [...prev];
        for (const item of data) {
          if (!seen.has(item.id)) merged.push(item);
        }
        return merged;
      });
      setSkip((s) => s + limit);
    } catch (err) {
      setError(getApiError(err).detail || "Gagal memuat riwayat");
    } finally {
      setLoading(false);
      inFlightRef.current = false;
    }
  }, [skip, limit]);

  const reset = useCallback(() => {
    setItems([]);
    setSkip(0);
    setHasMore(true);
    setError(null);
    inFlightRef.current = false;
  }, []);

  return { items, loading, error, hasMore, loadMore, reset };
}
