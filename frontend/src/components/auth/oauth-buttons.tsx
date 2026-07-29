"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/lib/api-client";
import { Github, Mail, ShieldAlert } from "lucide-react";

export function OAuthButtons() {
  const [loadingProvider, setLoadingProvider] = useState<string | null>(null);

  const handleOAuthClick = async (provider: "github" | "google" | "microsoft") => {
    try {
      setLoadingProvider(provider);
      const state = Math.random().toString(36).substring(7);
      const { data } = await apiClient.get<{ url: string }>(`/auth/oauth/${provider}/url?state=${state}`);
      window.location.href = data.url;
    } catch (error) {
      console.error(`Failed to initiate ${provider} OAuth:`, error);
      alert(`OAuth login with ${provider} is currently unavailable.`);
      setLoadingProvider(null);
    }
  };

  return (
    <div className="grid grid-cols-3 gap-3 w-full">
      <Button
        type="button"
        variant="outline"
        className="w-full flex items-center justify-center gap-2 border-slate-800 bg-slate-900/80 hover:bg-slate-800"
        isLoading={loadingProvider === "github"}
        onClick={() => handleOAuthClick("github")}
      >
        <Github className="h-4 w-4" />
        <span className="hidden sm:inline text-xs font-semibold">GitHub</span>
      </Button>

      <Button
        type="button"
        variant="outline"
        className="w-full flex items-center justify-center gap-2 border-slate-800 bg-slate-900/80 hover:bg-slate-800"
        isLoading={loadingProvider === "google"}
        onClick={() => handleOAuthClick("google")}
      >
        <Mail className="h-4 w-4 text-rose-400" />
        <span className="hidden sm:inline text-xs font-semibold">Google</span>
      </Button>

      <Button
        type="button"
        variant="outline"
        className="w-full flex items-center justify-center gap-2 border-slate-800 bg-slate-900/80 hover:bg-slate-800"
        isLoading={loadingProvider === "microsoft"}
        onClick={() => handleOAuthClick("microsoft")}
      >
        <ShieldAlert className="h-4 w-4 text-blue-400" />
        <span className="hidden sm:inline text-xs font-semibold">Microsoft</span>
      </Button>
    </div>
  );
}
