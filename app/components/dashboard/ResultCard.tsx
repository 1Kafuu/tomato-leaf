import Link from "next/link";
import type { PredictionData, SeverityLevel } from "@/app/types";
import { SEVERITY_META } from "@/app/types";
import { severityColorClasses, formatPercent, formatNumber } from "@/app/lib/utils";

type Props = {
  data: PredictionData;
  onRetake: () => void;
};

export default function ResultCard({ data, onRetake }: Props) {
  const color = severityColorClasses(data.severity_level as SeverityLevel);
  const meta = SEVERITY_META[data.severity_level as SeverityLevel];
  const fuzzy = data.fuzzy_score;
  const severity = data.severity_score;

  return (
    <div className="border-2 border-border-default rounded-2xl bg-neutral-white overflow-hidden">
      {/* Header: hasil diagnosis */}
      <div className="p-5 md:p-6 border-b-2 border-border-default flex items-center gap-3">
        <div className="w-12 h-12 rounded-2xl bg-surface-default text-icon-default border-2 border-border-default flex items-center justify-center shrink-0">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path
              d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        <div className="flex-1 min-w-0">
          <p className="xs-semibold text-text-placeholder uppercase tracking-wider mb-1">
            Hasil Diagnosis
          </p>
          <h2 className="h2-heading text-text-heading truncate">
            {data.severity_level}
          </h2>
        </div>
        <span
          className={`px-3 py-1.5 rounded-full xs-semibold ${color.pill} shrink-0`}
        >
          {data.plant_status}
        </span>
      </div>

      {/* Score panel: fuzzy + severity */}
      <div className="p-5 md:p-6 border-b-2 border-border-default space-y-4">
        <div>
          <div className="flex justify-between items-end mb-2">
            <p className="xs-semibold text-text-placeholder uppercase tracking-wider">
              Skor Fuzzy
            </p>
            <p className="text-[32px] md:text-[40px] leading-none font-bold text-text-action">
              {formatNumber(fuzzy)}
            </p>
          </div>
          <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full transition-all ${color.bar}`}
              style={{ width: `${Math.max(0, Math.min(100, fuzzy))}%` }}
            />
          </div>
        </div>
        <div>
          <div className="flex justify-between items-end mb-2">
            <p className="xs-semibold text-text-placeholder uppercase tracking-wider">
              Severity Score
            </p>
            <p className="text-[20px] md:text-[24px] leading-none font-bold text-text-label">
              {formatNumber(severity)}
            </p>
          </div>
          <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all bg-tomato-default"
              style={{ width: `${Math.max(0, Math.min(100, severity))}%` }}
            />
          </div>
        </div>
      </div>

      {/* Description & recommendation */}
      {meta && (
        <div className="p-5 md:p-6 border-b-2 border-border-default space-y-3">
          <p className="sm-default text-text-label leading-relaxed">
            {meta.description}
          </p>
          <div className={`p-4 rounded-2xl ${color.bg} border ${color.border}`}>
            <p className="xs-semibold uppercase tracking-wider text-text-placeholder mb-1">
              Rekomendasi
            </p>
            <p className={`sm-default ${color.text}`}>
              {meta.recommendation}
            </p>
          </div>
        </div>
      )}

      {/* Features (7 fitur V2) */}
      <div className="p-5 md:p-6 border-b-2 border-border-default">
        <p className="xs-semibold text-text-placeholder uppercase tracking-wider mb-4">
          Fitur Visual
        </p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <FeatureItem label="Spot Area" value={data.features.spot_area} suffix="%" />
          <FeatureItem label="Color Change" value={data.features.color_change} suffix="%" />
          <FeatureItem label="Kuning" value={data.features.yellow_ratio} suffix="%" />
          <FeatureItem label="Coklat" value={data.features.brown_ratio} suffix="%" />
          <FeatureItem label="Gelap" value={data.features.dark_ratio} suffix="%" />
          <FeatureItem
            label="Spot Count"
            value={data.features.spot_count}
            suffix=""
            digits={0}
          />
          <FeatureItem
            label="Texture Var"
            value={data.features.texture_var}
            suffix=""
            digits={2}
          />
        </div>
      </div>

      <div className="p-5 md:p-6 flex flex-col md:flex-row gap-3">
        <button
          onClick={onRetake}
          className="flex-1 h-12 md:h-14 rounded-2xl bg-surface-primary hover:bg-surface-primary-hover text-neutral-white md-semibold transition-colors"
        >
          Deteksi Lagi
        </button>
        <Link
          href="/history"
          className="flex-1 h-12 md:h-14 rounded-2xl border-2 border-border-default hover:border-border-action-hover text-text-heading md-semibold transition-colors flex items-center justify-center"
        >
          Lihat Riwayat
        </Link>
      </div>
    </div>
  );
}

function FeatureItem({
  label,
  value,
  suffix = "%",
  digits = 2,
}: {
  label: string;
  value: number;
  suffix?: string;
  digits?: number;
}) {
  return (
    <div className="text-center py-3 px-2 border-2 border-border-default rounded-2xl">
      <p className="xs-default text-text-placeholder mb-1">{label}</p>
      <p className="md-semibold text-text-heading">
        {suffix === "%" ? formatPercent(value) : formatNumber(value, digits)}
      </p>
    </div>
  );
}
