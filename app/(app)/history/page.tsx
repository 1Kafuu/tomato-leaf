"use client";

import { useEffect } from "react";
import Link from "next/link";
import LogoPill from "../../components/landing/LogoPill";
import HistoryItem from "../../components/history/HistoryItem";
import { useHistory } from "../../hooks/usePrediction";

export default function HistoryPage() {
  const { items, loading, error, hasMore, loadMore } = useHistory();

  useEffect(() => {
    loadMore();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-5 md:px-10 py-10 md:py-16">
      <div className="flex justify-center mb-6">
        <LogoPill text="Riwayat Deteksi" />
      </div>
      <h1 className="h1-heading font-bold text-text-heading mb-3 text-center">
        Riwayat Prediksi Anda
      </h1>
      <p className="md-default text-text-placeholder text-center max-w-2xl mx-auto mb-10">
        Daftar lengkap deteksi yang pernah Anda lakukan. Klik item untuk
        melihat detail.
      </p>

      {error && (
        <div className="mb-6 p-4 rounded-2xl border-2 border-tomato-default bg-tomato-50 sm-default text-tomato-700">
          {error}
        </div>
      )}

      {items.length === 0 && !loading && (
        <div className="border-2 border-dashed border-border-default rounded-2xl p-12 text-center">
          <p className="md-default text-text-placeholder mb-4">
            Belum ada riwayat deteksi
          </p>
          <Link
            href="/dashboard"
            className="inline-flex h-12 items-center px-6 rounded-2xl bg-surface-primary text-neutral-white sm-semibold hover:bg-surface-primary-hover transition-colors"
          >
            Mulai Deteksi
          </Link>
        </div>
      )}

      <div className="flex flex-col gap-3">
        {items.map((it) => (
          <HistoryItem key={it.id} item={it} />
        ))}
      </div>

      {hasMore && (
        <div className="flex justify-center mt-8">
          <button
            onClick={loadMore}
            disabled={loading}
            className="h-12 px-6 rounded-2xl border-2 border-border-default hover:border-border-action-hover text-text-heading sm-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Memuat..." : "Muat Lebih Banyak"}
          </button>
        </div>
      )}
    </div>
  );
}
