"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { apiV2, getApiError } from "../../../lib/api";
import LogoPill from "../../../components/landing/LogoPill";
import {
  severityColorClasses,
  formatDate,
  formatPercent,
  formatNumber,
} from "../../../lib/utils";
import type {
  PredictionHistoryDetail,
  SeverityLevel,
} from "../../../types";
import { SEVERITY_META } from "../../../types";

export default function HistoryDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [data, setData] = useState<PredictionHistoryDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const { data } = await apiV2.get<PredictionHistoryDetail>(
          `/history/${id}`
        );
        if (!cancelled) setData(data);
      } catch (err) {
        if (!cancelled) setError(getApiError(err).detail);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-5 md:px-10 py-10 md:py-16">
        <div className="flex flex-col items-center justify-center py-20 gap-3">
          <svg
            className="animate-spin text-icon-action"
            width="32"
            height="32"
            viewBox="0 0 24 24"
            fill="none"
          >
            <circle
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="3"
              className="opacity-25"
            />
            <path
              d="M4 12a8 8 0 018-8"
              stroke="currentColor"
              strokeWidth="3"
              strokeLinecap="round"
            />
          </svg>
          <p className="md-default text-text-placeholder">Memuat detail...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-5xl mx-auto px-5 md:px-10 py-10 md:py-16">
        <button
          onClick={() => router.back()}
          className="inline-flex items-center gap-2 sm-default text-text-label hover:text-text-action transition-colors mb-6"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path
              d="M19 12H5M12 19L5 12L12 5"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          Kembali
        </button>
        <div className="p-6 rounded-2xl border-2 border-tomato-default bg-tomato-50 sm-default text-tomato-700 text-center">
          {error}
        </div>
      </div>
    );
  }

  if (!data) return null;

  const color = severityColorClasses(data.severity_level as SeverityLevel);
  const meta = SEVERITY_META[data.severity_level as SeverityLevel];
  const fuzzy = data.fuzzy_score;
  const severity = data.severity_score ?? 0;

  return (
    <div className="max-w-5xl mx-auto px-5 md:px-10 py-10 md:py-16">
      <button
        onClick={() => router.back()}
        className="inline-flex items-center gap-2 sm-default text-text-label hover:text-text-action transition-colors mb-6 group"
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          className="transition-transform group-hover:-translate-x-0.5"
        >
          <path
            d="M19 12H5M12 19L5 12L12 5"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        Kembali
      </button>

      <div className="flex justify-center mb-6">
        <LogoPill text="Detail Prediksi" />
      </div>
      <h1 className="h1-heading font-bold text-text-heading mb-2 text-center">
        {data.severity_level}
      </h1>
      <p className="sm-default text-text-placeholder text-center mb-10">
        {formatDate(data.created_at)} • Status:{" "}
        <span className="sm-semibold text-text-heading">
          {data.plant_status}
        </span>
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="relative w-full aspect-square md:aspect-auto md:min-h-[420px] rounded-2xl overflow-hidden border-2 border-border-default bg-surface-default">
          {data.image_url ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={data.image_url}
              alt={data.severity_level}
              className="w-full h-full object-contain"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-icon-default">
              Gambar tidak tersedia
            </div>
          )}
        </div>

        <div className="space-y-4">
          {/* Skor Fuzzy */}
          <div className="border-2 border-border-default rounded-2xl p-5">
            <div className="flex items-center justify-between mb-3">
              <p className="xs-semibold text-text-placeholder uppercase tracking-wider">
                Skor Fuzzy
              </p>
              <span
                className={`px-3 py-1.5 rounded-full xs-semibold ${color.pill}`}
              >
                {data.severity_level}
              </span>
            </div>
            <div className="flex items-end justify-between mb-3">
              <p className="text-[40px] md:text-[48px] leading-none font-bold text-text-action">
                {fuzzy.toFixed(2)}
              </p>
            </div>
            <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
              <div
                className={`h-full ${color.bar}`}
                style={{ width: `${Math.max(0, Math.min(100, fuzzy))}%` }}
              />
            </div>
          </div>

          {/* Severity Score */}
          <div className="border-2 border-border-default rounded-2xl p-5">
            <p className="xs-semibold text-text-placeholder uppercase tracking-wider mb-3">
              Severity Score
            </p>
            <div className="flex items-end justify-between mb-3">
              <p className="text-[32px] md:text-[40px] leading-none font-bold text-text-label">
                {severity.toFixed(2)}
              </p>
            </div>
            <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-tomato-default"
                style={{
                  width: `${Math.max(0, Math.min(100, severity))}%`,
                }}
              />
            </div>
          </div>

          {/* Rekomendasi */}
          {meta && (
            <div
              className={`rounded-2xl p-5 border-2 ${color.bg} ${color.border}`}
            >
              <p className="xs-semibold uppercase tracking-wider text-text-placeholder mb-2">
                Deskripsi & Rekomendasi
              </p>
              <p className={`sm-default ${color.text} mb-2`}>
                {meta.description}
              </p>
              <p className={`sm-semibold ${color.text}`}>
                {meta.recommendation}
              </p>
            </div>
          )}

          {/* Fitur Visual (7 fitur V2) */}
          <div className="border-2 border-border-default rounded-2xl p-5">
            <p className="xs-semibold text-text-placeholder uppercase tracking-wider mb-4">
              Fitur Visual
            </p>
            <div className="space-y-3">
              <FeatureRow
                label="Spot Area"
                value={data.spot_area}
                format="percent"
              />
              <FeatureRow
                label="Color Change"
                value={data.color_change}
                format="percent"
              />
              <FeatureRow
                label="Yellow Ratio"
                value={data.yellow_ratio}
                format="percent"
              />
              <FeatureRow
                label="Brown Ratio"
                value={data.brown_ratio}
                format="percent"
              />
              <FeatureRow
                label="Dark Ratio"
                value={data.dark_ratio ?? 0}
                format="percent"
              />
              <FeatureRow
                label="Spot Count"
                value={data.spot_count ?? 0}
                format="count"
              />
              <FeatureRow
                label="Texture Var"
                value={data.texture_var ?? 0}
                format="number"
              />
            </div>
          </div>

          <Link
            href="/dashboard"
            className="block w-full h-12 md:h-14 rounded-2xl bg-surface-primary hover:bg-surface-primary-hover text-neutral-white md-semibold text-center leading-[3rem] md:leading-[3.5rem] transition-colors"
          >
            Deteksi Baru
          </Link>
        </div>
      </div>
    </div>
  );
}

type RowFormat = "percent" | "count" | "number";

function FeatureRow({
  label,
  value,
  format,
}: {
  label: string;
  value: number;
  format: RowFormat;
}) {
  let display: string;
  if (format === "percent") display = formatPercent(value);
  else if (format === "count") display = formatNumber(value, 0);
  else display = formatNumber(value, 2);

  // Untuk count/number, gunakan representasi 0-100% (clamp) hanya sebagai visual bar
  // Spot count bisa ratusan, jadi batasi visualisasinya.
  const barWidth = format === "count"
    ? Math.max(0, Math.min(100, (value / 100) * 100))
    : Math.max(0, Math.min(100, value));

  return (
    <div className="flex items-center gap-3">
      <span className="sm-default text-text-label w-32 shrink-0">{label}</span>
      <div className="flex-1 h-2 bg-neutral-100 rounded-full overflow-hidden">
        <div
          className="h-full bg-surface-primary rounded-full"
          style={{ width: `${barWidth}%` }}
        />
      </div>
      <span className="sm-semibold text-text-heading w-20 text-right">
        {display}
      </span>
    </div>
  );
}
