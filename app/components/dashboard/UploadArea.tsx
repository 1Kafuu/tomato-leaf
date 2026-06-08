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

export default function UploadArea({
  previewUrl,
  onFileSelected,
  onClear,
  disabled,
}: Props) {
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
    e.preventDefault();
    setIsDragging(false);
    if (disabled) return;
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  };

  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
    e.target.value = "";
  };

  if (previewUrl) {
    return (
      <div className="border-2 border-border-default rounded-2xl bg-neutral-white p-4 md:p-6">
        <div className="relative w-full aspect-square md:aspect-video rounded-2xl overflow-hidden border-2 border-border-default bg-surface-default">
          <Image
            src={previewUrl}
            alt="Preview daun tomat"
            fill
            unoptimized
            className="object-contain"
            sizes="(max-width: 768px) 100vw, 50vw"
          />
        </div>
        <div className="flex flex-col sm:flex-row gap-3 mt-4">
          <button
            type="button"
            onClick={() => inputRef.current?.click()}
            disabled={disabled}
            className="flex-1 h-12 rounded-2xl border-2 border-border-default hover:border-border-action-hover text-text-heading sm-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Ganti Gambar
          </button>
          <button
            type="button"
            onClick={onClear}
            disabled={disabled}
            className="h-12 px-5 rounded-2xl border-2 border-border-default hover:border-tomato-default text-tomato-700 sm-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Hapus
          </button>
        </div>
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/jpg,image/png"
          onChange={onChange}
          className="hidden"
        />
      </div>
    );
  }

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        if (!disabled) setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={onDrop}
      onClick={() => !disabled && inputRef.current?.click()}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if ((e.key === "Enter" || e.key === " ") && !disabled) {
          e.preventDefault();
          inputRef.current?.click();
        }
      }}
      className={`border-2 border-dashed rounded-2xl bg-neutral-white p-8 md:p-12 text-center cursor-pointer transition-colors ${
        isDragging
          ? "border-border-action bg-surface-primary-light"
          : "border-border-default hover:border-border-action-hover"
      } ${disabled ? "opacity-50 cursor-not-allowed" : ""}`}
    >
      <div className="w-16 h-16 mx-auto rounded-2xl bg-surface-default border-2 border-border-default flex items-center justify-center mb-4 text-icon-default">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
          <path
            d="M12 16V4M12 4L6 10M12 4L18 10M4 20H20"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
      <h3 className="md-semibold text-text-heading mb-1">Seret gambar ke sini</h3>
      <p className="sm-default text-text-placeholder mb-4">
        atau klik untuk pilih file dari perangkat
      </p>
      <p className="xs-default text-text-placeholder">
        Format: JPG, JPEG, PNG • Maks 10 MB
      </p>
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/jpg,image/png"
        onChange={onChange}
        className="hidden"
      />
      {localError && (
        <p className="sm-default text-tomato-700 mt-4">{localError}</p>
      )}
    </div>
  );
}
