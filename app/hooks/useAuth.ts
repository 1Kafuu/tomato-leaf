"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { api, getApiError } from "@/app/lib/api";
import type { User } from "@/app/types";

const TOKEN_KEY = "toma_token";
const USER_KEY = "toma_user";

function readSession(): { token: string | null; user: User | null } {
  if (typeof window === "undefined") return { token: null, user: null };
  try {
    const token = localStorage.getItem(TOKEN_KEY);
    const userStr = localStorage.getItem(USER_KEY);
    if (token && userStr) {
      return { token, user: JSON.parse(userStr) as User };
    }
  } catch {
    /* ignore */
  }
  return { token: null, user: null };
}

export function useAuth() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [hydrated, setHydrated] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Hydrate session dari localStorage saat komponen mount di client.
  // Ini adalah use-case sah untuk useEffect: sinkronisasi React state
  // dengan external system (localStorage). Set state di sini akan trigger
  // re-render TERBATAS — bukan loop, karena dipanggil sekali saat mount.
  useEffect(() => {
    const { token: t, user: u } = readSession();
    setToken(t);
    setUser(u);
    setHydrated(true);
  }, []);

  const login = useCallback(
    async (email: string, password: string) => {
      setLoading(true);
      setError(null);
      try {
        const { data } = await api.post<{
          access_token: string;
          token_type: string;
          user: User;
        }>("/auth/login", { email, password });
        localStorage.setItem(TOKEN_KEY, data.access_token);
        localStorage.setItem(USER_KEY, JSON.stringify(data.user));
        setToken(data.access_token);
        setUser(data.user);
        router.push("/dashboard");
      } catch (err) {
        const e = getApiError(err);
        setError(
          e.detail === "Incorrect email or password"
            ? "Email atau kata sandi salah"
            : e.detail
        );
      } finally {
        setLoading(false);
      }
    },
    [router]
  );

  const register = useCallback(
    async (email: string, password: string, full_name: string) => {
      setLoading(true);
      setError(null);
      try {
        await api.post("/auth/register", { email, password, full_name });
        const { data } = await api.post<{
          access_token: string;
          token_type: string;
          user: User;
        }>("/auth/login", { email, password });
        localStorage.setItem(TOKEN_KEY, data.access_token);
        localStorage.setItem(USER_KEY, JSON.stringify(data.user));
        setToken(data.access_token);
        setUser(data.user);
        router.push("/dashboard");
      } catch (err) {
        const e = getApiError(err);
        setError(e.detail || "Registrasi gagal");
      } finally {
        setLoading(false);
      }
    },
    [router]
  );

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    setToken(null);
    setUser(null);
    router.push("/login");
  }, [router]);

  return {
    user,
    token,
    hydrated,
    loading,
    error,
    login,
    register,
    logout,
  };
}
