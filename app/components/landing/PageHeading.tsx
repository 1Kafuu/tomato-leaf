import Button from "./Button";
import LogoPill from "./LogoPill";

export default function PageHeading() {
  return (
    <div className="flex flex-col gap-6 md:gap-8 max-w-3xl mx-auto mt-12 md:mt-20 desktop:mt-32 mb-12 md:mb-20 desktop:mb-24 px-5">
      <div className="flex justify-center">
        <LogoPill text="TomaCheck Health Detection" />
      </div>

      <h1 className="h1-heading font-bold text-text-heading text-center max-w-3xl mx-auto">
        Diagnosis Penyakit Daun Tomat dalam Hitungan Detik
      </h1>

      <p className="md-default text-text-placeholder text-center max-w-2xl mx-auto leading-relaxed">
        Unggah foto daun tomat Anda, sistem akan melakukan segmentasi citra,
        ekstraksi fitur visual, dan inferensi Fuzzy Sugeno untuk memberikan
        diagnosis yang cepat, konsisten, dan dapat diandalkan.
      </p>

      <div className="flex flex-col md:flex-row gap-4 md:mx-auto">
        <Button text="Mulai Deteksi" inv={true} href="/register" />
        <Button text="Lihat Demo" inv={false} href="#cara-kerja" />
      </div>

      <div className="mt-8 md:mt-12 relative">
        <div className="border-2 border-border-default rounded-3xl bg-diagonal-line p-8 md:p-16 overflow-hidden">
          <div className="relative z-10 flex justify-center">
            <div className="bg-neutral-white border-2 border-border-default rounded-2xl p-6 md:p-8 max-w-md w-full">
              <div className="flex items-center gap-3 pb-5 mb-5 border-b border-border-default">
                <div className="w-10 h-10 rounded-2xl bg-surface-default text-icon-default border border-border-default flex items-center justify-center shrink-0">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path
                      d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
                <div>
                  <p className="xs-semibold text-text-placeholder uppercase tracking-wider mb-1">
                    Hasil Diagnosis
                  </p>
                  <h1 className="md-semibold text-text-heading">Early Blight</h1>
                </div>
              </div>

              <div className="pb-5 mb-5 border-b border-border-default">
                <div className="flex justify-between items-end mb-4">
                  <div>
                    <p className="xs-default text-text-placeholder mb-1">
                      Skor Fuzzy
                    </p>
                    <h1 className="text-[40px] leading-none font-bold text-text-action">
                      71.25
                    </h1>
                  </div>
                  <span className="px-3 py-1.5 rounded-full bg-neutral-100 text-text-label border border-border-default xs-semibold">
                    Ringan
                  </span>
                </div>
                <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-surface-primary rounded-full"
                    style={{ width: "71.25%" }}
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div className="text-center py-2">
                  <p className="xs-default text-text-placeholder mb-1">Spot</p>
                  <p className="sm-semibold text-text-heading">12.3%</p>
                </div>
                <div className="text-center py-2 border-x border-border-default">
                  <p className="xs-default text-text-placeholder mb-1">
                    Kuning
                  </p>
                  <p className="sm-semibold text-text-heading">15.2%</p>
                </div>
                <div className="text-center py-2">
                  <p className="xs-default text-text-placeholder mb-1">
                    Coklat
                  </p>
                  <p className="sm-semibold text-text-heading">2.8%</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
