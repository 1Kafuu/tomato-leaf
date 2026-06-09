import type {
  SeverityLevel,
  SeverityColor,
  SeverityMeta,
} from "@/app/types";
import { SEVERITY_META } from "@/app/types";

export function formatDate(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("id-ID", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatPercent(n: number): string {
  return `${n.toFixed(2)}%`;
}

export function formatNumber(n: number, digits = 2): string {
  return n.toFixed(digits);
}

export type SeverityColorClasses = {
  bg: string;
  text: string;
  border: string;
  pill: string;
  bar: string;
};

export function severityColorClasses(
  level: SeverityLevel | string
): SeverityColorClasses {
  const meta: SeverityMeta | undefined = SEVERITY_META[
    level as SeverityLevel
  ];
  const color: SeverityColor = meta?.color ?? "tomato";
  switch (color) {
    case "green":
      return {
        bg: "bg-surface-primary-light",
        text: "text-surface-primary",
        border: "border-surface-primary",
        pill: "bg-surface-primary-light text-text-action border border-border-action",
        bar: "bg-surface-primary",
      };
    case "lime":
      return {
        bg: "bg-lime-50",
        text: "text-lime-700",
        border: "border-lime-500",
        pill: "bg-lime-50 text-lime-700 border border-lime-500",
        bar: "bg-lime-500",
      };
    case "yellow":
      return {
        bg: "bg-secondary-100",
        text: "text-secondary-700",
        border: "border-secondary-default",
        pill: "bg-secondary-100 text-secondary-700 border border-secondary-default",
        bar: "bg-secondary-default",
      };
    case "tomato":
      return {
        bg: "bg-tomato-50",
        text: "text-tomato-700",
        border: "border-tomato-default",
        pill: "bg-tomato-50 text-tomato-700 border border-tomato-default",
        bar: "bg-tomato-default",
      };
    case "red":
      return {
        bg: "bg-tomato-100",
        text: "text-tomato-800",
        border: "border-tomato-700",
        pill: "bg-tomato-100 text-tomato-800 border border-tomato-700",
        bar: "bg-tomato-700",
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
