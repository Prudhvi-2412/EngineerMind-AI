"use client";

import { useQuery } from "@tanstack/react-query";
import { Users, Flame, Award, Clock, AlertTriangle, ShieldCheck } from "lucide-react";

export default function DevelopersDashboardPage() {
  const { data: developers, isLoading } = useQuery({
    queryKey: ["developers-insight-list"],
    queryFn: async () => [
      {
        email: "alex.lead@company.com",
        name: "Alex Rivera",
        role: "Lead SRE / Backend Architect",
        ownership: "payment-service (65%), auth-service (25%)",
        workloadHours: 54.5,
        burnoutRisk: "HIGH",
        burnoutScore: 78.5,
        lateNightCommits: 14,
        reviewQuality: 92,
      },
      {
        email: "sarah.dev@company.com",
        name: "Sarah Chen",
        role: "Senior Fullstack Engineer",
        ownership: "frontend-app (80%), api-gateway (30%)",
        workloadHours: 41.0,
        burnoutRisk: "LOW",
        burnoutScore: 18.0,
        lateNightCommits: 2,
        reviewQuality: 88,
      },
      {
        email: "marcus.eng@company.com",
        name: "Marcus Vance",
        role: "DevOps / Platform Engineer",
        ownership: "k8s-helm (90%), prometheus-rules (75%)",
        workloadHours: 48.0,
        burnoutRisk: "MEDIUM",
        burnoutScore: 52.0,
        lateNightCommits: 7,
        reviewQuality: 85,
      },
    ],
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Users className="h-6 w-6 text-indigo-400" />
          Developer Analytics & Organizational Health
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          AI Developer Insight Agent tracking code ownership, review quality, bus factor, and burnout risk indicators.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {developers?.map((dev: { email: string; name: string; role: string; ownership: string; workloadHours: number; burnoutRisk: string; burnoutScore: number; lateNightCommits: number; reviewQuality: number }) => (
          <div
            key={dev.email}
            className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 hover:border-indigo-500/50 transition-all flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-full bg-indigo-950 border border-indigo-700/50 flex items-center justify-center font-bold text-indigo-400 text-sm">
                    {dev.name.charAt(0)}
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-base">{dev.name}</h3>
                    <p className="text-xs text-slate-400">{dev.role}</p>
                  </div>
                </div>

                <div
                  className={`px-2.5 py-1 rounded-full text-xs font-bold border ${
                    dev.burnoutRisk === "HIGH"
                      ? "bg-rose-500/10 text-rose-400 border-rose-500/30"
                      : dev.burnoutRisk === "MEDIUM"
                      ? "bg-amber-500/10 text-amber-400 border-amber-500/30"
                      : "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
                  }`}
                >
                  {dev.burnoutRisk} BURNOUT RISK
                </div>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1.5 text-xs">
                <span className="text-slate-400 block font-medium">Code Ownership:</span>
                <span className="text-indigo-300 font-mono font-semibold">{dev.ownership}</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs pt-3 border-t border-slate-800/80">
              <div className="flex items-center gap-2 text-slate-400">
                <Clock className="h-4 w-4 text-indigo-400" />
                <span>{dev.workloadHours} hrs/wk</span>
              </div>
              <div className="flex items-center gap-2 text-slate-400">
                <Flame className="h-4 w-4 text-amber-400" />
                <span>{dev.lateNightCommits} Late Commits</span>
              </div>
              <div className="flex items-center gap-2 text-slate-400">
                <Award className="h-4 w-4 text-emerald-400" />
                <span>Review QL: {dev.reviewQuality}/100</span>
              </div>
              <div className="flex items-center gap-2 text-slate-400">
                <ShieldCheck className="h-4 w-4 text-purple-400" />
                <span>Burnout Score: {dev.burnoutScore}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
