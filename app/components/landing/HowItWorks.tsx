import LogoPill from "./LogoPill";
import StepCard from "./StepCard";

export default function HowItWorks() {
  const steps = [
    {
      step: "Langkah 1",
      title: "Unggah Gambar",
      desc: "Pilih atau ambil foto daun tomat dari perangkat Anda. Pastikan pencahayaan cukup dan fokus pada daun.",
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path
            d="M4 16L8.586 11.414C8.96106 11.0391 9.46967 10.8284 10 10.8284C10.5303 10.8284 11.0389 11.0391 11.414 11.414L16 16M14 14L15.586 12.414C15.9611 12.0391 16.4697 11.8284 17 11.8284C17.5303 11.8284 18.0389 12.0391 18.414 12.414L20 14M14 8H14.01M6 20H18C19.1046 20 20 19.1046 20 18V6C20 4.89543 19.1046 4 18 4H6C4.89543 4 4 4.89543 4 6V18C4 19.1046 4.89543 20 6 20Z"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      ),
    },
    {
      step: "Langkah 2",
      title: "Analisis Otomatis",
      desc: "Sistem melakukan segmentasi daun, ekstraksi 5 fitur visual, dan inferensi Fuzzy Sugeno Orde 0 secara otomatis.",
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path
            d="M9.75 17L9 20L-1.31134e-07 17L5.33906 7.69937C5.61506 7.13945 6.19385 6.7955 6.81619 6.7955H11.6838C12.3061 6.7955 12.8849 7.13945 13.1609 7.69937L18.5 17L9.75 17ZM9.75 17H19.5M15 12.75V14.25M15 9.75V11.25M18 11.25V12.75M18 8.25V9.75M21 11.25V12.75M21 8.25V9.75"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      ),
    },
    {
      step: "Langkah 3",
      title: "Lihat Diagnosis",
      desc: "Hasil diagnosis menampilkan nama penyakit, skor fuzzy, tingkat keparahan, dan nilai fitur secara lengkap.",
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path
            d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      ),
    },
  ];

  return (
    <div id="cara-kerja" className="mt-24 md:mt-32 px-5 md:px-10 max-w-7xl mx-auto">
      <div className="flex flex-col gap-6">
        <div className="mx-auto">
          <LogoPill text="Cara Kerja" />
        </div>
        <div className="flex flex-col gap-6 pb-8 border-b border-border-default max-w-3xl mx-auto text-center">
          <h1 className="h1-heading font-bold text-text-heading">
            Tiga langkah sederhana untuk diagnosis yang akurat
          </h1>
          <p className="md-default text-text-placeholder leading-relaxed">
            Dari foto hingga diagnosis, semua terjadi secara otomatis tanpa
            memerlukan pengetahuan teknis.
          </p>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-5 mt-10">
        {steps.map((s, i) => (
          <StepCard key={i} {...s} />
        ))}
      </div>
    </div>
  );
}
