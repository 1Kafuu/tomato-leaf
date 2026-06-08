"use client";

import { useState } from "react";
import LogoPill from "../../components/landing/LogoPill";
import UploadArea from "../../components/dashboard/UploadArea";
import ResultCard from "../../components/dashboard/ResultCard";
import LoadingState from "../../components/dashboard/LoadingState";
import { usePrediction } from "../../hooks/usePrediction";

export default function DashboardPage() {
  const { result, loading, error, previewUrl, predict, reset, setFile } =
    usePrediction();
  const [file, setLocalFile] = useState<File | null>(null);

  const handleFileSelected = (f: File) => {
    setLocalFile(f);
    setFile(f);
  };

  const handleClearFile = () => {
    setLocalFile(null);
    setFile(null);
  };

  const handleDetect = async () => {
    if (file) await predict(file);
  };

  const handleRetake = () => {
    setLocalFile(null);
    reset();
  };

  return (
    <div className="max-w-4xl mx-auto px-5 md:px-10 py-10 md:py-16">
      <div className="flex justify-center mb-6">
        <LogoPill text="Deteksi Daun Tomat" />
      </div>
      <h1 className="h1-heading font-bold text-text-heading mb-3 text-center">
        Unggah Foto Daun Tomat Anda
      </h1>
      <p className="md-default text-text-placeholder text-center max-w-2xl mx-auto mb-10 leading-relaxed">
        Sistem akan melakukan segmentasi, ekstraksi fitur, dan inferensi Fuzzy
        Sugeno untuk memberikan diagnosis dalam hitungan detik.
      </p>

      {error && (
        <div className="mb-6 p-4 rounded-2xl border-2 border-tomato-default bg-tomato-50 sm-default text-tomato-700">
          {error}
        </div>
      )}

      {!result && !loading && (
        <div className="space-y-4">
          <UploadArea
            previewUrl={previewUrl}
            onFileSelected={handleFileSelected}
            onClear={handleClearFile}
          />
          <button
            onClick={handleDetect}
            disabled={!file}
            className="w-full h-14 rounded-2xl bg-surface-primary hover:bg-surface-primary-hover text-neutral-white md-semibold transition-colors disabled:bg-surface-disabled disabled:text-text-disabled disabled:cursor-not-allowed"
          >
            Deteksi Sekarang
          </button>
        </div>
      )}

      {loading && <LoadingState />}

      {result && !loading && <ResultCard data={result} onRetake={handleRetake} />}
    </div>
  );
}
