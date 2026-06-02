import Link from "next/link";
import Image from "next/image";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b-2 border-border-default bg-neutral-white/90 backdrop-blur">
      <div className="max-w-7xl mx-auto px-5 md:px-10 h-16 md:h-20 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5">
          <Image
            src="/images/logo.svg"
            alt="TomaCheck"
            width={28}
            height={28}
            className="h-7 w-auto"
          />
          <span className="md-semibold text-text-heading">TomaCheck</span>
        </Link>

        <nav className="hidden md:flex items-center gap-8">
          <a
            href="#fitur"
            className="sm-default text-text-label hover:text-text-action transition-colors"
          >
            Fitur
          </a>
          <a
            href="#cara-kerja"
            className="sm-default text-text-label hover:text-text-action transition-colors"
          >
            Cara Kerja
          </a>
          <a
            href="#penyakit"
            className="sm-default text-text-label hover:text-text-action transition-colors"
          >
            Penyakit
          </a>
          <a
            href="#faq"
            className="sm-default text-text-label hover:text-text-action transition-colors"
          >
            FAQ
          </a>
        </nav>

        <div className="flex items-center gap-2 md:gap-3">
          <Link
            href="/login"
            className="hidden md:inline-flex h-10 items-center justify-center px-4 sm-semibold text-text-action hover:text-text-action-hover transition-colors"
          >
            Masuk
          </Link>
          <Link
            href="/register"
            className="inline-flex h-10 items-center justify-center px-4 md:px-5 rounded-2xl bg-surface-primary text-neutral-white sm-semibold hover:bg-surface-primary-hover transition-colors"
          >
            Daftar
          </Link>
        </div>
      </div>
    </header>
  );
}
