const marqueeItems = [
  "Deteksi Cepat",
  "Akurasi Tinggi",
  "Mudah Digunakan",
  "Fuzzy Sugeno",
  "5 Penyakit Terdeteksi",
  "Tanpa Instalasi",
  "Akses 24/7",
  "Mobile Friendly",
  "Hasil Real-time",
  "Untuk Semua Petani",
];

export default function Marquee() {
  // Gandakan item untuk efek infinite scroll seamless
  const doubled = [...marqueeItems, ...marqueeItems];

  return (
    <section className="pt-14 pb-14 md:pt-20 md:pb-20 overflow-hidden border-y-2 border-border-default bg-surface-default">
      <div className="overflow-hidden">
        <div className="flex flex-none gap-12 whitespace-nowrap marquee-track">
          {doubled.map((item, index) => (
            <div key={index} className="flex items-center gap-12 shrink-0">
              <svg
                width="32"
                height="32"
                viewBox="0 0 24 24"
                fill="none"
                className="shrink-0"
                aria-hidden
              >
                <path
                  d="M12 2L13.5 8.5L20 10L13.5 11.5L12 18L10.5 11.5L4 10L10.5 8.5L12 2Z"
                  fill="#097315"
                />
              </svg>
              <span className="text-2xl md:text-3xl font-semibold text-text-heading">
                {item}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
