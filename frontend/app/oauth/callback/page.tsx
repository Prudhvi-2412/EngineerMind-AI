"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/auth-context";
import { apiClient } from "@/lib/api-client";
import { TokenResponse } from "@/types/auth";
import { Sparkles, AlertCircle } from "lucide-react";

export default function OAuthCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { setAuthTokens } = useAuth();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const code = searchParams.get("code");
    const provider = searchParams.get("provider") || "github";

    if (!code) {
      setError("Authorization code is missing from OAuth callback.");
      return;
    }

    const exchangeCode = async () => {
      try {
        const { data } = await apiClient.get<TokenResponse>(
          `/auth/oauth/${provider}/callback?code=${code}`
        );
        await setAuthTokens(data.access_token, data.refresh_token);
        router.push("/dashboard");
      } catch (err: any) {
        console.error("OAuth callback error:", err);
        setError(err.response?.data?.detail || "OAuth login failed. Please try again.");
      }
    };

    exchangeCode();
  }, [searchParams, setAuthTokens, router]);

  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-center bg-slate-950 p-4">
      {error ? (
        <div className="max-w-md w-full rounded-2xl border border-rose-800/60 bg-rose-950/40 p-6 text-center space-y-4">
          <AlertCircle className="h-10 w-10 text-rose-400 mx-auto" />
          <h2 className="text-lg font-bold text-rose-200">OAuth Authentication Failed</h2>
          <p className="text-xs text-rose-300">{error}</p>
          <button
            onClick={() => router.push("/login")}
            className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold text-white hover:bg-slate-800"
          >
            Back to Login
          </button>
        </div>
      ) : (
        <div className="flex flex-col items-center text-center space-y-4">
          <div className="h-14 w-14 rounded-2xl bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center shadow-xl shadow-indigo-500/25 animate-pulse">
            <Sparkles className="h-8 w-8 text-white" />
          </div>
          <h2 className="text-xl font-bold text-white tracking-tight">Authenticating with OAuth...</h2>
          <p className="text-xs text-slate-400">Verifying security token and loading workspace context</p>
        </div>
      )}
    </div>
  );
}
