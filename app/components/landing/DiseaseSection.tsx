import LogoPill from "./LogoPill";

type Status = {
  name: string;
  range: string;
  desc: string;
};

const statuses: Status[] = [
  {
    name: "Sehat",
    range: "85 – 100",
    desc: "Daun dalam kondisi optimal, hijau segar, tanpa gejala penyakit yang berarti.",
  },
  {
    name: "Terinfeksi Ringan",
    range: "70 – 84",
    desc: "Infeksi tingkat ringan, biasanya berupa bercak awal atau perubahan warna minor.",
  },
  {
    name: "Terinfeksi Sedang",
    range: "50 – 69",
    desc: "Infeksi tingkat sedang, bercak dan perubahan warna mulai meluas pada daun.",
  },
  {
    name: "Terinfeksi Berat",
    range: "25 – 49",
    desc: "Infeksi tingkat berat, sebagian besar jaringan daun rusak dan perlu penanganan.",
  },
  {
    name: "Terinfeksi Sangat Berat",
    range: "0 – 24",
    desc: "Kerusakan daun sangat parah, jaringan sehat hampir tidak tersisa.",
  },
];

export default function DiseaseSection() {
  return (
    <div id="penyakit" className="mt-24 md:mt-32 px-5 md:px-10 max-w-7xl mx-auto">
      <div className="flex flex-col gap-6">
        <div className="mx-auto">
          <LogoPill text="Status Daun Tomat" />
        </div>
        <div className="flex flex-col gap-6 pb-8 border-b border-border-default max-w-3xl mx-auto text-center">
          <h1 className="h1-heading font-bold text-text-heading">
            Sistem mengklasifikasikan daun tomat menjadi Sehat dan 4 tingkat
            infeksi
          </h1>
          <p className="md-default text-text-placeholder leading-relaxed">
            Mulai dari Sehat, Terinfeksi Ringan, Terinfeksi Sedang, Terinfeksi
            Berat, hingga Terinfeksi Sangat Berat. Didukung oleh analisis citra
            digital dan metode Fuzzy Sugeno.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4 mt-10">
        {statuses.map((s) => (
          <div
            key={s.name}
            className="border-2 border-border-default rounded-2xl bg-neutral-white p-5 hover:border-border-action transition-colors"
          >
            <div className="flex items-start justify-between mb-3">
              <h1 className="md-semibold text-text-heading">{s.name}</h1>
              <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-neutral-surface text-text-heading border border-border-default">
                {s.range}
              </span>
            </div>
            <p className="sm-default text-text-placeholder leading-relaxed">
              {s.desc}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
