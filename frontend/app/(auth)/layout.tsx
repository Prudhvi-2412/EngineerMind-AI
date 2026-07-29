import React from "react";
import { Sparkles } from "lucide-react";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative min-h-screen w-full flex items-center justify-center bg-slate-950 p-4 overflow-hidden">
      {/* Dynamic Background Glows */}
      <div className="absolute -top-40 -left-40 h-96 w-96 rounded-full bg-indigo-600/20 blur-[128px] pointer-events-none" />
      <div className="absolute -bottom-40 -right-40 h-96 w-96 rounded-full bg-purple-600/20 blur-[128px] pointer-events-none" />

      {/* Main Container */}
      <div className="relative z-10 w-full max-w-md">
        {/* Logo Branding Header */}
        <div className="flex flex-col items-center text-center mb-8">
          <div className="h-12 w-12 rounded-2xl bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center shadow-xl shadow-indigo-500/25 mb-4">
            <Sparkles className="h-6 w-6 text-white" />
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">EngineeringOS AI</h1>
          <p className="text-xs text-slate-400 font-medium mt-1">
            Autonomous AI Management for Software Engineering
          </p>
        </div>

        {/* Form Card */}
        <div className="rounded-3xl border border-slate-800/80 bg-slate-900/60 p-8 backdrop-blur-2xl shadow-2xl shadow-indigo-950/40">
          {children}
        </div>
      </div>
    </div>
  );
}
