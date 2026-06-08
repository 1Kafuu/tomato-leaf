import LogoPill from "./LogoPill";
import Accordion from "./Accordion";

export default function FAQSection() {
  const faqs = [
    {
      title: "Format gambar apa yang didukung?",
      content:
        "Kami mendukung format JPG, JPEG, dan PNG dengan ukuran maksimal 10 MB. Pastikan gambar jelas, fokus pada daun tomat, dan pencahayaan cukup untuk hasil terbaik.",
    },
    {
      title: "Apakah sistem ini bisa mendeteksi penyakit tanaman lain?",
      content:
        "Saat ini, TomaCheck hanya mendukung deteksi penyakit pada daun tomat. Kami berencana mengembangkan fitur untuk tanaman lain seperti cabai dan kentang pada versi mendatang.",
    },
    {
      title: "Berapa lama waktu yang dibutuhkan untuk diagnosis?",
      content:
        "Waktu respons target kami adalah kurang dari 5 detik dari saat gambar diunggah hingga hasil diagnosis ditampilkan. Proses mencakup segmentasi daun, ekstraksi fitur, dan inferensi Fuzzy Sugeno.",
    },
    {
      title: "Bagaimana cara interpretasi skor fuzzy?",
      content:
        "Skor fuzzy berkisar 0-100 dan diklasifikasikan menjadi 7 kategori: Sangat Sehat (90-100), Sehat (75-89), Early Blight Ringan (60-74), Late Blight (45-59), Leaf Mold (25-44), Septoria Leaf Spot (10-24), dan Sangat Buruk (0-9).",
    },
    {
      title: "Apakah data saya aman?",
      content:
        "Ya, semua gambar yang diunggah disimpan dengan aman di Supabase Storage. Kami menggunakan enkripsi end-to-end dan tidak membagikan data Anda kepada pihak ketiga tanpa izin.",
    },
  ];

  return (
    <div id="faq" className="mt-24 md:mt-32 mb-24 md:mb-32 px-5 md:px-10 max-w-4xl mx-auto">
      <div className="flex flex-col gap-8 items-center text-center">
        <div>
          <LogoPill text="FAQ" />
        </div>
        <div className="flex flex-col gap-6 pb-8 border-b border-border-default w-full">
          <h1 className="h1-heading font-bold text-text-heading">
            Frequently Asked Questions
          </h1>
          <p className="md-default text-text-placeholder leading-relaxed max-w-2xl mx-auto">
            Pertanyaan umum seputar deteksi penyakit daun tomat dan cara
            menggunakan TomaCheck.
          </p>
        </div>
      </div>

      <div className="flex flex-col gap-4 mt-10 text-left">
        {faqs.map((faq, index) => (
          <Accordion key={index} title={faq.title} content={faq.content} />
        ))}
      </div>
    </div>
  );
}