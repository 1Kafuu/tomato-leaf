import Link from "next/link";
import type { PredictionHistoryItem, SeverityLevel } from "@/app/types";
import { severityColorClasses, formatDate } from "@/app/lib/utils";

export default function HistoryItem({ item }: { item: PredictionHistoryItem }) {
  const color = severityColorClasses(item.severity_level as SeverityLevel);
  return (
    <Link
      href={`/history/${item.id}`}
      className="grid grid-cols-[64px_1fr_auto] md:grid-cols-[80px_1fr_140px_140px_180px_24px] gap-3 md:gap-4 items-center p-3 md:p-4 border-2 border-border-default rounded-2xl bg-neutral-white hover:border-border-action transition-colors"
    >
      <div className="relative w-16 h-16 md:w-20 md:h-20 rounded-2xl overflow-hidden border border-border-default bg-surface-default shrink-0">
        {item.image_url ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={item.image_url}
            alt={item.severity_level}
            className="w-full h-full object-cover"
            loading="lazy"
            onError={(e) => {
              const target = e.currentTarget;
              target.style.display = "none";
              const parent = target.parentElement;
              if (parent && !parent.querySelector(".img-fallback")) {
                const fb = document.createElement("div");
                fb.className =
                  "img-fallback w-full h-full flex items-center justify-center text-icon-default text-xs";
                fb.textContent = "No img";
                parent.appendChild(fb);
              }
            }}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-icon-default text-xs">
            No img
          </div>
        )}
      </div>

      <div className="min-w-0">
        <span
          className={`inline-block px-2.5 py-1 rounded-full text-xs font-semibold ${color.pill} mb-1`}
        >
          {item.severity_level}
        </span>
        <p className="sm-default text-text-placeholder md:hidden">
          {formatDate(item.created_at)}
        </p>
      </div>

      <p className="hidden md:block md-default text-text-label">
        {item.plant_status || "—"}
      </p>

      <div className="hidden md:flex items-center gap-2">
        <span className="text-[20px] font-bold text-text-action leading-none">
          {item.fuzzy_score.toFixed(1)}
        </span>
        <div className="flex-1 h-1.5 bg-neutral-100 rounded-full overflow-hidden">
          <div
            className={`h-full ${color.bar}`}
            style={{ width: `${Math.max(0, Math.min(100, item.fuzzy_score))}%` }}
          />
        </div>
      </div>

      <p className="hidden md:block sm-default text-text-placeholder">
        {formatDate(item.created_at)}
      </p>

      <svg
        className="text-icon-default"
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
      >
        <path
          d="M7.5 15L12.5 10L7.5 5"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </Link>
  );
}
