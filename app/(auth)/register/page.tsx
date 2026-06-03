"use client";

import { useState } from "react";
import Link from "next/link";
import LogoPill from "../../components/landing/LogoPill";
import Button from "../../components/landing/Button";

export default function RegisterPage() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [agree, setAgree] = useState(false);

  // Password strength calculation
  const getPasswordStrength = () => {
    if (!password) return { level: 0, label: "", color: "" };
    let score = 0;
    if (password.length >= 8) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;

    if (score <= 1)
      return { level: 1, label: "Lemah", color: "bg-tomato-default" };
    if (score === 2)
      return { level: 2, label: "Sedang", color: "bg-secondary-default" };
    if (score === 3)
      return { level: 3, label: "Kuat", color: "bg-green-300" };
    return { level: 4, label: "Sangat Kuat", color: "bg-green-default" };
  };

  const strength = getPasswordStrength();

  return (
    <div className="min-h-screen flex flex-col bg-neutral-white">
      {/* Top bar - Back to landing */}
      <div className="w-full px-5 md:px-10 py-5 md:py-6 flex items-center justify-between max-w-7xl mx-auto">
        <Link
          href="/"
          className="inline-flex items-center gap-2 sm-default text-text-label hover:text-text-action transition-colors group"
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            className="transition-transform group-hover:-translate-x-0.5"
          >
            <path
              d="M19 12H5M12 19L5 12L12 5"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          Kembali ke Beranda
        </Link>
        <Link
          href="/"
          className="inline-flex items-center gap-2.5"
        >
          <span className="md-semibold text-text-heading">TomaCheck</span>
        </Link>
      </div>

      {/* Centered form */}
      <div className="flex-1 flex items-center justify-center px-5 py-8">
        <div className="w-full max-w-md">
          <div className="mb-6 md:mb-8 flex justify-center">
            <LogoPill text="Bergabung Bersama Kami" />
          </div>

          <h1 className="h1-heading font-bold text-text-heading mb-3 text-center">
            Buat Akun Baru
          </h1>
          <p className="md-default text-text-placeholder mb-8 text-center leading-relaxed">
            Daftar untuk mulai mendeteksi penyakit daun tomat dan simpan
            riwayat diagnosis Anda.
          </p>

          <form className="space-y-5" onSubmit={(e) => e.preventDefault()}>
            <div>
              <label
                htmlFor="fullName"
                className="label-semibold text-text-heading block mb-2"
              >
                Nama Lengkap
              </label>
              <div className="relative">
                <div className="absolute left-4 top-1/2 -translate-y-1/2 text-icon-default pointer-events-none">
                  <svg
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    <path
                      d="M12 14C8.13401 14 5 17.134 5 21H19C19 17.134 15.866 14 12 14Z"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
                <input
                  id="fullName"
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Nama lengkap Anda"
                  className="w-full h-12 md:h-14 pl-12 pr-4 rounded-2xl border-2 border-border-default bg-neutral-white text-md-default text-text-heading placeholder:text-text-placeholder focus:outline-none focus:border-border-action transition-colors"
                />
              </div>
            </div>

            <div>
              <label
                htmlFor="email"
                className="label-semibold text-text-heading block mb-2"
              >
                Email
              </label>
              <div className="relative">
                <div className="absolute left-4 top-1/2 -translate-y-1/2 text-icon-default pointer-events-none">
                  <svg
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      d="M3 8L10.8906 13.2604C11.5624 13.7083 12.4376 13.7083 13.1094 13.2604L21 8M5 19H19C20.1046 19 21 18.1046 21 17V7C21 5.89543 20.1046 5 19 5H5C3.89543 5 3 5.89543 3 7V17C3 18.1046 3.89543 19 5 19Z"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="nama@email.com"
                  className="w-full h-12 md:h-14 pl-12 pr-4 rounded-2xl border-2 border-border-default bg-neutral-white text-md-default text-text-heading placeholder:text-text-placeholder focus:outline-none focus:border-border-action transition-colors"
                />
              </div>
            </div>

            <div>
              <label
                htmlFor="password"
                className="label-semibold text-text-heading block mb-2"
              >
                Kata Sandi
              </label>
              <div className="relative">
                <div className="absolute left-4 top-1/2 -translate-y-1/2 text-icon-default pointer-events-none">
                  <svg
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      d="M12 15V17M6 21H18C19.1046 21 20 20.1046 20 19V13C20 11.8954 19.1046 11 18 11H6C4.89543 11 4 11.8954 4 13V19C4 20.1046 4.89543 21 6 21ZM16 11V7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7V11H16Z"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Minimal 8 karakter"
                  className="w-full h-12 md:h-14 pl-12 pr-12 rounded-2xl border-2 border-border-default bg-neutral-white text-md-default text-text-heading placeholder:text-text-placeholder focus:outline-none focus:border-border-action transition-colors"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-icon-default hover:text-text-action transition-colors"
                  aria-label={
                    showPassword ? "Sembunyikan kata sandi" : "Tampilkan kata sandi"
                  }
                >
                  {showPassword ? (
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                    >
                      <path
                        d="M3 3L21 21M10.584 10.5874C10.2087 10.9627 9.99778 11.4654 9.99756 11.9892C9.99735 12.513 10.2079 13.0159 10.5829 13.3916C10.958 13.7673 11.4606 13.9787 11.9844 13.9794C12.5082 13.9802 13.0113 13.7702 13.387 13.3954M9.363 5.365C10.2204 5.11978 11.1082 4.99689 12 5C16 5 19.5 7.5 21 11C20.5038 12.1338 19.7878 13.1665 18.892 14.043M6.679 6.679C4.886 7.812 3.5 9.354 3 11C4.5 14.5 8 17 12 17C13.3271 17.0054 14.6405 16.7281 15.853 16.187"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  ) : (
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                    >
                      <path
                        d="M2 12C2 12 5 5 12 5C19 5 22 12 22 12C22 12 19 19 12 19C5 19 2 12 2 12Z"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                      <path
                        d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  )}
                </button>
              </div>

              {password && (
                <div className="mt-3">
                  <div className="flex gap-1.5 mb-2">
                    {[1, 2, 3, 4].map((i) => (
                      <div
                        key={i}
                        className={`h-1.5 flex-1 rounded-full transition-colors ${
                          i <= strength.level
                            ? strength.color
                            : "bg-neutral-200"
                        }`}
                      />
                    ))}
                  </div>
                  <p className="xs-default text-text-placeholder">
                    Kekuatan kata sandi:{" "}
                    <span className="xs-semibold text-text-label">
                      {strength.label}
                    </span>
                  </p>
                </div>
              )}
            </div>

            <div>
              <label
                htmlFor="confirmPassword"
                className="label-semibold text-text-heading block mb-2"
              >
                Konfirmasi Kata Sandi
              </label>
              <div className="relative">
                <div className="absolute left-4 top-1/2 -translate-y-1/2 text-icon-default pointer-events-none">
                  <svg
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <path
                      d="M12 15V17M6 21H18C19.1046 21 20 20.1046 20 19V13C20 11.8954 19.1046 11 18 11H6C4.89543 11 4 11.8954 4 13V19C4 20.1046 4.89543 21 6 21ZM16 11V7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7V11H16Z"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
                <input
                  id="confirmPassword"
                  type={showPassword ? "text" : "password"}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Ulangi kata sandi"
                  className="w-full h-12 md:h-14 pl-12 pr-12 rounded-2xl border-2 border-border-default bg-neutral-white text-md-default text-text-heading placeholder:text-text-placeholder focus:outline-none focus:border-border-action transition-colors"
                />
                {confirmPassword && password === confirmPassword && (
                  <div className="absolute right-4 top-1/2 -translate-y-1/2 text-icon-action">
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                    >
                      <path
                        d="M5 12L10 17L20 7"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>
                )}
              </div>
            </div>

            <label className="flex items-start gap-2 cursor-pointer group pt-1">
              <div className="relative mt-0.5">
                <input
                  type="checkbox"
                  checked={agree}
                  onChange={(e) => setAgree(e.target.checked)}
                  className="peer sr-only"
                />
                <div className="w-5 h-5 rounded-md border-2 border-border-default peer-checked:bg-surface-primary peer-checked:border-surface-primary transition-colors flex items-center justify-center">
                  {agree && (
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                      <path
                        d="M5 12L10 17L20 7"
                        stroke="white"
                        strokeWidth="3"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  )}
                </div>
              </div>
              <span className="sm-default text-text-label group-hover:text-text-action transition-colors leading-relaxed">
                Saya menyetujui{" "}
                <Link
                  href="/terms"
                  className="sm-semibold text-text-action hover:text-text-action-hover transition-colors"
                >
                  Syarat & Ketentuan
                </Link>{" "}
                dan{" "}
                <Link
                  href="/privacy"
                  className="sm-semibold text-text-action hover:text-text-action-hover transition-colors"
                >
                  Kebijakan Privasi
                </Link>{" "}
                TomaCheck
              </span>
            </label>

            <div className="pt-2">
              <Button text="Daftar" inv={true} icon={false} fullWidth={true} />
            </div>

            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-border-default" />
              </div>
              <div className="relative flex justify-center">
                <span className="bg-neutral-white px-4 xs-default text-text-placeholder">
                  atau
                </span>
              </div>
            </div>

            <button
              type="button"
              className="w-full h-12 md:h-14 rounded-2xl border-2 border-border-default bg-neutral-white text-md-semibold text-text-heading hover:border-border-action-hover transition-colors flex items-center justify-center gap-3"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path
                  d="M21.8055 10.0415H21V10H12V14H17.6515C16.827 16.3285 14.6115 18 12 18C8.6865 18 6 15.3135 6 12C6 8.6865 8.6865 6 12 6C13.5295 6 14.921 6.577 15.9805 7.5195L18.809 4.691C16.953 3.0265 14.577 2 12 2C6.4775 2 2 6.4775 2 12C2 17.5225 6.4775 22 12 22C17.5225 22 22 17.5225 22 12C22 11.3295 21.931 10.675 21.8055 10.0415Z"
                  fill="#FFC107"
                />
                <path
                  d="M3.15295 7.3455L6.43845 9.755C7.32745 7.554 9.48045 6 12 6C13.5295 6 14.921 6.577 15.9805 7.5195L18.809 4.691C16.953 3.0265 14.577 2 12 2C8.15895 2 4.82795 4.1685 3.15295 7.3455Z"
                  fill="#FF3D00"
                />
                <path
                  d="M12 22C14.6225 22 16.9545 21.0035 18.8105 19.3045L15.7345 16.6545C14.8115 17.4475 13.481 17.999 12 17.999C9.39895 17.999 7.19045 16.3415 6.35845 14.027L3.09795 16.5395C4.75245 19.778 8.11345 22 12 22Z"
                  fill="#4CAF50"
                />
                <path
                  d="M21.8055 10.0415H21V10H12V14H17.6515C17.2555 15.1185 16.536 16.083 15.7335 16.6545C15.7335 16.6545 15.734 16.6545 15.7345 16.6545L18.8105 19.3045C18.6185 19.479 22 17 22 12C22 11.3295 21.931 10.675 21.8055 10.0415Z"
                  fill="#1976D2"
                />
              </svg>
              Daftar dengan Google
            </button>

            <p className="sm-default text-text-placeholder text-center pt-2">
              Sudah punya akun?{" "}
              <Link
                href="/login"
                className="sm-semibold text-text-action hover:text-text-action-hover transition-colors"
              >
                Masuk di sini
              </Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
