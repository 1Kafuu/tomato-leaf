import LogoPill from "./LogoPill";
import StatCard from "./StatCard";

export default function ProblemSection() {
  const stats = [
    {
      title: "Waktu Diagnosis Manual",
      date: "Rata-rata pengamatan konvensional",
      volume: "+2 Hari",
      desc: "Lama identifikasi penyakit",
    },
    {
      title: "Subjektivitas Pengamat",
      date: "Antar petani atau penyuluh",
      volume: "±40%",
      desc: "Tingkat perbedaan diagnosis",
    },
    {
      title: "Risiko Gagal Panen",
      date: "Akibat deteksi terlambat",
      volume: "30-60%",
      desc: "Potensi kehilangan hasil",
    },
  ];

  return (
    <div className="mt-24 md:mt-32 px-5 md:px-10 max-w-7xl mx-auto">
      <div className="flex flex-col gap-6">
        <div className="mx-auto">
          <LogoPill text="The Problem" />
        </div>
        <div className="flex flex-col gap-6 pb-8 border-b border-border-default max-w-3xl mx-auto text-center">
          <h1 className="h1-heading font-bold text-text-heading">
            Identifikasi penyakit daun tomat masih menjadi tantangan serius
            bagi petani.
          </h1>
          <p className="md-default text-text-placeholder leading-relaxed">
            Keterlambatan deteksi, subjektivitas diagnosis, dan keterbatasan
            akses ahli fitopatologi menyebabkan banyak petani gagal panen
            sebelum penyakit terdeteksi.
          </p>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-5 mt-10">
        {stats.map((data, i) => (
          <StatCard key={i} {...data} />
        ))}
      </div>
    </div>
  );
}
