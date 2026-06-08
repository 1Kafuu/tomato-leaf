"use client";

import Link from "next/link";
import Image from "next/image";
import { useState, useEffect, useRef } from "react";
import { useAuth } from "@/app/hooks/useAuth";
import type { User } from "@/app/types";

type Variant = "marketing" | "auth";

type Props = {
  variant: Variant;
  user?: User | null;
  onLogout?: () => void;
};

export default function Navbar({ variant, user: userProp, onLogout: onLogoutProp }: Props) {
  const auth = useAuth();
  // Pada SSR, snapshot user = null (server snapshot). Pada client, useSyncExternalStore
  // akan sinkronkan dengan localStorage. Untuk mencegah hydration mismatch, kita TIDAK
  // merender apa pun yang bergantung pada user sampai hydrated.
  const user = userProp !== undefined ? userProp : auth.user;
  const onLogout = onLogoutProp ?? auth.logout;
  const hydrated = auth.hydrated;
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Tutup menu saat klik di luar
  useEffect(() => {
    if (!menuOpen) return;
    const handler = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [menuOpen]);

  const isAuthed = variant === "auth";

  return (
    <header className="sticky top-0 z-50 w-full border-b-2 border-border-default bg-neutral-white/90 backdrop-blur">
      <div className="max-w-7xl mx-auto px-5 md:px-10 h-16 md:h-20 flex items-center justify-between">
        {/* Logo: TIDAK link ke mana pun setelah login (hanya branding).
            Untuk marketing, logo link ke landing page. */}
        {isAuthed ? (
          <div className="flex items-center gap-2.5">
            <Image
              src="/images/logo.svg"
              alt="TomaCheck"
              width={28}
              height={28}
              className="h-7 w-auto"
            />
            <span className="md-semibold text-text-heading">TomaCheck</span>
          </div>
        ) : (
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
        )}

        {/* Navigation - hidden on mobile (handled by hamburger) */}
        {isAuthed ? (
          <nav className="hidden md:flex items-center gap-8">
            <Link
              href="/dashboard"
              className="sm-default text-text-label hover:text-text-action transition-colors"
            >
              Dashboard
            </Link>
            <Link
              href="/history"
              className="sm-default text-text-label hover:text-text-action transition-colors"
            >
              Riwayat
            </Link>
          </nav>
        ) : (
          <nav className="hidden md:flex items-center gap-8">
            <Link
              href="/#fitur"
              className="sm-default text-text-label hover:text-text-action transition-colors"
            >
              Fitur
            </Link>
            <Link
              href="/#cara-kerja"
              className="sm-default text-text-label hover:text-text-action transition-colors"
            >
              Cara Kerja
            </Link>
            <Link
              href="/#penyakit"
              className="sm-default text-text-label hover:text-text-action transition-colors"
            >
              Penyakit
            </Link>
            <Link
              href="/#faq"
              className="sm-default text-text-label hover:text-text-action transition-colors"
            >
              FAQ
            </Link>
          </nav>
        )}

        {/* Right side: Desktop buttons / User info */}
        {isAuthed ? (
          <div className="hidden md:flex items-center gap-3">
            {hydrated && user && (
              <span className="sm-default text-text-label max-w-[160px] truncate">
                {user.full_name}
              </span>
            )}
            <button
              onClick={onLogout}
              className="inline-flex h-10 items-center px-5 rounded-2xl border-2 border-border-default hover:border-tomato-default text-tomato-700 sm-semibold transition-colors"
            >
              Keluar
            </button>
          </div>
        ) : (
          <div className="hidden md:flex items-center gap-3">
            <Link
              href="/login"
              className="inline-flex h-10 items-center justify-center px-4 sm-semibold text-text-action hover:text-text-action-hover transition-colors"
            >
              Masuk
            </Link>
            <Link
              href="/register"
              className="inline-flex h-10 items-center justify-center px-5 rounded-2xl bg-surface-primary text-neutral-white sm-semibold hover:bg-surface-primary-hover transition-colors"
            >
              Daftar
            </Link>
          </div>
        )}

        {/* Mobile: hamburger button (always rendered to avoid layout shift) */}
        <button
          onClick={() => setMenuOpen((v) => !v)}
          className="md:hidden w-10 h-10 rounded-2xl border-2 border-border-default text-text-label hover:border-border-action hover:text-text-action transition-colors flex items-center justify-center"
          aria-label="Buka menu"
          aria-expanded={menuOpen}
        >
          {menuOpen ? (
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path
                d="M6 6L18 18M6 18L18 6"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
          ) : (
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path
                d="M4 6H20M4 12H20M4 18H20"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
          )}
        </button>
      </div>

      {/* Mobile menu dropdown */}
      {menuOpen && (
        <div
          ref={menuRef}
          className="md:hidden border-t-2 border-border-default bg-neutral-white"
        >
          <div className="max-w-7xl mx-auto px-5 py-4 flex flex-col gap-1">
            {isAuthed ? (
              <>
                {hydrated && user && (
                  <div className="px-3 py-2 mb-2 border-b border-border-default">
                    <p className="xs-default text-text-placeholder">Login sebagai</p>
                    <p className="sm-semibold text-text-heading truncate">
                      {user.full_name}
                    </p>
                  </div>
                )}
                <MobileNavLink href="/dashboard" onClick={() => setMenuOpen(false)}>
                  Dashboard
                </MobileNavLink>
                <MobileNavLink href="/history" onClick={() => setMenuOpen(false)}>
                  Riwayat
                </MobileNavLink>
                <button
                  onClick={() => {
                    setMenuOpen(false);
                    onLogout();
                  }}
                  className="mt-2 h-11 rounded-2xl border-2 border-border-default text-tomato-700 sm-semibold transition-colors hover:border-tomato-default"
                >
                  Keluar
                </button>
              </>
            ) : (
              <>
                <MobileNavLink href="/#fitur" onClick={() => setMenuOpen(false)}>
                  Fitur
                </MobileNavLink>
                <MobileNavLink href="/#cara-kerja" onClick={() => setMenuOpen(false)}>
                  Cara Kerja
                </MobileNavLink>
                <MobileNavLink href="/#penyakit" onClick={() => setMenuOpen(false)}>
                  Penyakit
                </MobileNavLink>
                <MobileNavLink href="/#faq" onClick={() => setMenuOpen(false)}>
                  FAQ
                </MobileNavLink>
                <div className="flex flex-col gap-2 mt-3 pt-3 border-t border-border-default">
                  <Link
                    href="/login"
                    onClick={() => setMenuOpen(false)}
                    className="h-11 rounded-2xl border-2 border-border-default text-text-heading sm-semibold flex items-center justify-center transition-colors hover:border-border-action-hover"
                  >
                    Masuk
                  </Link>
                  <Link
                    href="/register"
                    onClick={() => setMenuOpen(false)}
                    className="h-11 rounded-2xl bg-surface-primary text-neutral-white sm-semibold flex items-center justify-center transition-colors hover:bg-surface-primary-hover"
                  >
                    Daftar
                  </Link>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
}

function MobileNavLink({
  href,
  onClick,
  children,
}: {
  href: string;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <Link
      href={href}
      onClick={onClick}
      className="h-11 px-3 rounded-2xl sm-default text-text-label hover:bg-surface-default hover:text-text-action transition-colors flex items-center"
    >
      {children}
    </Link>
  );
}
