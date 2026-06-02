import LogoPill from "./LogoPill";

type Disease = {
  name: string;
  range: string;
  desc: string;
};

const diseases: Disease[] = [
  {
    name: "Sangat Sehat",
    range: "90 – 100",
    desc: "Daun dalam kondisi optimal, hijau segar, tanpa gejala penyakit.",
  },
  {
    name: "Sehat",
    range: "75 – 89",
    desc: "Daun sehat dengan sedikit variasi warna normal yang dapat diterima.",
  },
  {
    name: "Early Blight",
    range: "60 – 74",
    desc: "Bercak kecil coklat pada daun bawah, tahap awal infeksi jamur Alternaria.",
  },
  {
    name: "Late Blight",
    range: "45 – 59",
    desc: "Bercak tidak beraturan dengan tepi daun mengering, infeksi Phytophthora.",
  },
  {
    name: "Leaf Mold",
    range: "25 – 44",
    desc: "Perubahan warna kuning masif dengan bercak halus pada permukaan daun.",
  },
  {
    name: "Septoria Leaf Spot",
    range: "10 – 24",
    desc: "Bercak bulat kecil dengan tepi gelap dan pusat keabuan.",
  },
  {
    name: "Sangat Buruk",
    range: "0 – 9",
    desc: "Kerusakan daun sangat parah, hampir tidak ada jaringan sehat tersisa.",
  },
];

export default function DiseaseSection() {
  return (
    <div id="penyakit" className="mt-24 md:mt-32 px-5 md:px-10 max-w-7xl mx-auto">
      <div className="flex flex-col gap-6">
        <div className="mx-auto">
          <LogoPill text="Penyakit yang Terdeteksi" />
        </div>
        <div className="flex flex-col gap-6 pb-8 border-b border-border-default max-w-3xl mx-auto text-center">
          <h1 className="h1-heading font-bold text-text-heading">
            Sistem mengenali 5 jenis penyakit utama daun tomat
          </h1>
          <p className="md-default text-text-placeholder leading-relaxed">
            Dilatih dengan 4.952 sampel dari PlantVillage Dataset dan
            parameter membership function yang dibangun dengan K-Means
            clustering.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mt-10">
        {diseases.map((d) => (
          <div
            key={d.name}
            className="border-2 border-border-default rounded-2xl bg-neutral-white p-5 hover:border-border-action transition-colors"
          >
            <div className="flex items-start justify-between mb-3">
              <h1 className="md-semibold text-text-heading">{d.name}</h1>
              <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-neutral-surface text-text-heading border border-border-default">
                {d.range}
              </span>
            </div>
            <p className="sm-default text-text-placeholder leading-relaxed">
              {d.desc}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
