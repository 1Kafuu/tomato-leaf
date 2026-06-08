"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Navbar from "../components/landing/Navbar";
import Footer from "../components/landing/Footer";
import { useAuth } from "../hooks/useAuth";

export default function AppLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const router = useRouter();
  const { user, hydrated, logout } = useAuth();

  useEffect(() => {
    if (hydrated && !user) {
      router.replace("/login");
    }
  }, [hydrated, user, router]);

  return (
    <>
      <Navbar variant="auth" user={user} onLogout={logout} />
      {hydrated ? (
        user ? (
          <main className="flex-1">{children}</main>
        ) : (
          <div className="flex-1 flex items-center justify-center py-20">
            <div className="flex flex-col items-center gap-3">
              <svg
                className="animate-spin text-icon-action"
                width="32"
                height="32"
                viewBox="0 0 24 24"
                fill="none"
              >
                <circle
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="3"
                  className="opacity-25"
                />
                <path
                  d="M4 12a8 8 0 018-8"
                  stroke="currentColor"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
              </svg>
              <p className="md-default text-text-placeholder">
                Mengalihkan ke halaman masuk...
              </p>
            </div>
          </div>
        )
      ) : (
        // SSR / pre-hydration: render shell kosong agar markup server match client
        <main className="flex-1" />
      )}
      <Footer variant="auth" />
    </>
  );
}
