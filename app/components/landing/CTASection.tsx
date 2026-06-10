import Image from "next/image";
import Button from "./Button";
import LogoPill from "./LogoPill";

export default function CTASection() {
  return (
    <div className="px-5 md:px-10 max-w-7xl mx-auto mt-24 md:mt-32">
      <div className="border-2 border-border-default rounded-3xl bg-neutral-white relative overflow-hidden">
        <div className="absolute inset-0 bg-diagonal-line opacity-30" />
        <div className="relative pt-12 md:pt-20 px-5 md:px-10 pb-12 md:pb-20">
          <div className="-mx-5 md:-mx-10 border-b-2 px-5 md:px-10 border-border-default mb-10 pb-12 md:pb-16">
            <div className="mx-auto w-fit">
              <LogoPill text="Siap Untuk Mencoba?" />
            </div>
            <h1 className="h1-heading text-text-heading text-center py-6 md:py-8 max-w-3xl mx-auto">
              Deteksi penyakit daun tomat Anda sekarang dan dapatkan diagnosis
              dalam hitungan detik
            </h1>
            <div className="flex flex-col md:flex-row md:justify-center gap-4 pt-6">
              <Button text="Mulai Deteksi" inv={true} href="/register" />
              <Button text="Pelajari Lebih Lanjut" inv={false} href="#fitur" />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="w-12 h-12 mx-auto rounded-2xl bg-surface-default text-icon-default border border-border-default flex items-center justify-center mb-3">
                <Image
                  src="/images/logo.svg"
                  alt="logo"
                  width={24}
                  height={24}
                  className="h-6 w-auto"
                />
              </div>
              <h1 className="md-semibold text-text-heading">100% Otomatis</h1>
              <p className="sm-default text-text-placeholder mt-1">
                Tanpa perlu pengetahuan teknis
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 mx-auto rounded-2xl bg-surface-default text-icon-default border border-border-default flex items-center justify-center mb-3">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M12 6V12L16 14M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </div>
              <h1 className="md-semibold text-text-heading">{"< 5 Detik"}</h1>
              <p className="sm-default text-text-placeholder mt-1">
                Respons cepat setiap deteksi
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 mx-auto rounded-2xl bg-surface-default text-icon-default border border-border-default flex items-center justify-center mb-3">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </div>
              <h1 className="md-semibold text-text-heading">80%+ Akurat</h1>
              <p className="sm-default text-text-placeholder mt-1">
                Berdasarkan dataset PlantVillage
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}