import Link from "next/link";
import type { PredictionData, DiseaseName } from "@/app/types";
import { diseaseColorClasses, formatPercent } from "@/app/lib/utils";

type Props = {
  data: PredictionData;
  onRetake: () => void;
};

export default function ResultCard({ data, onRetake }: Props) {
  const color = diseaseColorClasses(data.disease_name as DiseaseName);
  const score = data.fuzzy_score;

  return (
    <div className="border-2 border-border-default rounded-2xl bg-neutral-white overflow-hidden">
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
            {data.disease_name}
          </h2>
        </div>
        <span
          className={`px-3 py-1.5 rounded-full xs-semibold ${color.pill} shrink-0`}
        >
          {data.severity_level || "Tanpa gejala"}
        </span>
      </div>

      <div className="p-5 md:p-6 border-b-2 border-border-default">
        <div className="flex justify-between items-end mb-3">
          <div>
            <p className="xs-default text-text-placeholder mb-1">Skor Fuzzy</p>
            <p className="text-[40px] md:text-[48px] leading-none font-bold text-text-action">
              {score.toFixed(2)}
            </p>
          </div>
          <p className="sm-default text-text-placeholder text-right">
            Status:{" "}
            <span className="sm-semibold text-text-heading">
              {data.plant_status}
            </span>
          </p>
        </div>
        <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all ${color.bar}`}
            style={{ width: `${Math.max(0, Math.min(100, score))}%` }}
          />
        </div>
      </div>

      <div className="p-5 md:p-6 border-b-2 border-border-default">
        <p className="xs-semibold text-text-placeholder uppercase tracking-wider mb-4">
          Fitur Visual
        </p>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          <FeatureItem label="Spot Area" value={data.features.spot_area} />
          <FeatureItem label="Kuning" value={data.features.yellow_ratio} />
          <FeatureItem label="Coklat" value={data.features.brown_ratio} />
          <FeatureItem label="Gelap" value={data.features.dark_ratio} />
          <FeatureItem label="Perubahan" value={data.features.color_change} />
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

function FeatureItem({ label, value }: { label: string; value: number }) {
  return (
    <div className="text-center py-3 px-2 border-2 border-border-default rounded-2xl">
      <p className="xs-default text-text-placeholder mb-1">{label}</p>
      <p className="md-semibold text-text-heading">{formatPercent(value)}</p>
    </div>
  );
}
