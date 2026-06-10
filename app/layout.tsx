import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import icon from "../public/images/logo.svg";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "TomaCheck - Deteksi Penyakit Daun Tomat",
  description:
    "Aplikasi berbasis web untuk mendeteksi kesehatan daun tomat melalui analisis citra digital menggunakan metode Fuzzy Sugeno Orde 0.",
  icons: {
    icon: icon.src,
  },
  openGraph: {
    title: "TomaCheck - Deteksi Penyakit Daun Tomat",
    description:
      "Aplikasi berbasis web untuk mendeteksi kesehatan daun tomat melalui analisis citra digital menggunakan metode Fuzzy Sugeno Orde 0.",
    url: "https://whiny-botanist-fax.ngrok-free.dev",
    siteName: "TomaCheck",
    images: [
      {
        url: "/images/og-thumbnail.png",
        width: 1200,
        height: 630,
      },
    ],
    locale: "id_ID",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "TomaCheck - Deteksi Penyakit Daun Tomat",
    description:
      "Aplikasi berbasis web untuk mendeteksi kesehatan daun tomat melalui analisis citra digital menggunakan metode Fuzzy Sugeno Orde 0.",
    images: ["/images/og-thumbnail.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="id"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-neutral-white">
        {children}
      </body>
    </html>
  );
}
