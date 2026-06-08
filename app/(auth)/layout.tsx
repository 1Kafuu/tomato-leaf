import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "TomaCheck - Masuk & Daftar",
  description: "Masuk atau daftar untuk mulai mendeteksi penyakit daun tomat.",
};

export default function AuthLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // <html> dan <body> di-render oleh app/layout.tsx (root).
  // Halaman login/register (centered card) dibungkus div dengan min-h agar
  // konten tetap di tengah layar penuh.
  return <div className="min-h-full flex-1 flex flex-col">{children}</div>;
}
