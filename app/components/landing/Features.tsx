import LogoPill from "./LogoPill";
import FeatureCard from "./FeatureCard";

export default function Features() {
  const features = [
    {
      title: "Cepat",
      desc: "Diagnosis hasilkan dalam waktu kurang dari 5 detik setelah gambar diunggah, tanpa perlu menunggu pakar.",
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path
            d="M12 6V12L16 14M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      ),
    },
    {
      title: "Akurat",
      desc: "Metode Fuzzy Sugeno Orde 0 dengan 16 aturan yang parameter membership-nya dibangun dari 4.952 sampel dataset.",
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
    {
      title: "Mudah",
      desc: "Cukup unggah foto daun tomat dari smartphone. Tidak perlu keahlian teknis di bidang pengolahan citra.",
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
  ];

  return (
    <div id="fitur" className="mt-24 md:mt-32 px-5 md:px-10 max-w-7xl mx-auto">
      <div className="flex flex-col gap-6">
        <div className="mx-auto">
          <LogoPill text="Fitur Unggulan" />
        </div>
        <div className="flex flex-col gap-6 pb-8 border-b border-border-default max-w-3xl mx-auto text-center">
          <h1 className="h1-heading font-bold text-text-heading">
            Solusi modern untuk diagnosis penyakit daun tomat
          </h1>
          <p className="md-default text-text-placeholder leading-relaxed">
            Tiga pilar utama yang membuat TomaCheck dapat diandalkan untuk
            mendeteksi penyakit tanaman Anda.
          </p>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-5 mt-10">
        {features.map((f, i) => (
          <FeatureCard key={i} {...f} />
        ))}
      </div>
    </div>
  );
}
