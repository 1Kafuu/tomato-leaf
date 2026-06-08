import Link from "next/link";
import Image from "next/image";

type Variant = "marketing" | "auth";

type Props = {
  variant: Variant;
};

export default function Footer({ variant }: Props) {
  const isAuthed = variant === "auth";

  return (
    <footer className="border-t-2 border-border-default bg-surface-default mt-20">
      <div className="max-w-7xl mx-auto px-5 md:px-10 py-10 md:py-12">
        {isAuthed ? (
          <div className="flex flex-col md:flex-row gap-3 items-center justify-between">
            <p className="xs-default text-text-placeholder">
              &copy; {new Date().getFullYear()} TomaCheck. All rights reserved.
            </p>
            <p className="xs-default text-text-placeholder">
              Dibuat dengan cinta untuk petani Indonesia.
            </p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
              <div>
                <Link href="/" className="flex items-center gap-2.5 mb-4">
                  <Image
                    src="/images/logo.svg"
                    alt="TomaCheck"
                    width={28}
                    height={28}
                    className="h-7 w-auto"
                  />
                  <span className="md-semibold text-text-heading">TomaCheck</span>
                </Link>
                <p className="sm-default text-text-placeholder leading-relaxed max-w-sm">
                  Deteksi penyakit daun tomat otomatis berbasis kecerdasan buatan
                  dengan metode Fuzzy Sugeno Orde 0. Cepat, akurat, dan mudah
                  digunakan siapa saja.
                </p>
              </div>

              <div>
                <h1 className="label-semibold text-text-heading mb-4 uppercase tracking-wider">
                  Produk
                </h1>
                <ul className="space-y-3">
                  <li>
                    <Link
                      href="/#fitur"
                      className="sm-default text-text-label hover:text-text-action transition-colors"
                    >
                      Fitur
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/#cara-kerja"
                      className="sm-default text-text-label hover:text-text-action transition-colors"
                    >
                      Cara Kerja
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/#penyakit"
                      className="sm-default text-text-label hover:text-text-action transition-colors"
                    >
                      Penyakit
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/#faq"
                      className="sm-default text-text-label hover:text-text-action transition-colors"
                    >
                      FAQ
                    </Link>
                  </li>
                </ul>
              </div>

              <div>
                <h1 className="label-semibold text-text-heading mb-4 uppercase tracking-wider">
                  Akun
                </h1>
                <ul className="space-y-3">
                  <li>
                    <Link
                      href="/login"
                      className="sm-default text-text-label hover:text-text-action transition-colors"
                    >
                      Masuk
                    </Link>
                  </li>
                  <li>
                    <Link
                      href="/register"
                      className="sm-default text-text-label hover:text-text-action transition-colors"
                    >
                      Daftar
                    </Link>
                  </li>
                </ul>
              </div>
            </div>

            <div className="mt-12 pt-6 border-t border-border-default flex flex-col md:flex-row gap-3 items-center justify-between">
              <p className="xs-default text-text-placeholder">
                &copy; {new Date().getFullYear()} TomaCheck. All rights reserved.
              </p>
              <p className="xs-default text-text-placeholder">
                Dibuat dengan cinta untuk petani Indonesia.
              </p>
            </div>
          </>
        )}
      </div>
    </footer>
  );
}
