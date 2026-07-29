"use client";

import { useQuery } from "@tanstack/react-query";
import { Network, ShieldCheck, AlertTriangle, Layers, CheckCircle2, Code2 } from "lucide-react";

export default function ArchitectureDashboardPage() {
  const { data: arch, isLoading } = useQuery({
    queryKey: ["architecture-review-data"],
    queryFn: async () => ({
      repoName: "acme/billing-microservice",
      techDebtScore: 28.5,
      cleanArchComplianceScore: 85.0,
      circularDependenciesCount: 0,
      godClassesCount: 1,
      godClassesDetails: [
        { file: "src/services/billing_monolith.py", loc: 450, reason: "Exceeds SRP threshold (>400 LOC)" },
      ],
      recommendations: [
        "Refactor identified God Class into distinct BillingStrategy domain handlers.",
        "Extract repository interfaces to satisfy Dependency Inversion (DIP).",
      ],
    }),
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Network className="h-6 w-6 text-indigo-400" />
          Architecture Graph & Code Smell Assessment
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          LangGraph Architecture Review Agent evaluating microservice coupling, SOLID principles, and Clean Architecture adherence.
        </p>
      </div>

      {/* Metrics Banner */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span className="text-xs font-medium text-slate-400">Technical Debt Score</span>
          <h2 className="text-3xl font-bold text-emerald-400">{arch?.techDebtScore} / 100</h2>
          <p className="text-xs text-slate-500">Low Technical Debt Rating</p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span className="text-xs font-medium text-slate-400">Clean Architecture Adherence</span>
          <h2 className="text-3xl font-bold text-indigo-400">{arch?.cleanArchComplianceScore}%</h2>
          <p className="text-xs text-slate-500">Domain Layer Well Isolated</p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span className="text-xs font-medium text-slate-400">God Classes & Smells</span>
          <h2 className="text-3xl font-bold text-amber-400">{arch?.godClassesCount} Detected</h2>
          <p className="text-xs text-slate-500">Circular Dependencies: {arch?.circularDependenciesCount}</p>
        </div>
      </div>

      {/* Code Smells & Refactoring Plan */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
          <h3 className="font-bold text-white text-base flex items-center gap-2">
            <Code2 className="h-5 w-5 text-amber-400" />
            Detected Code Smells & God Classes
          </h3>
          <div className="space-y-3 text-xs">
            {arch?.godClassesDetails.map((gc, i) => (
              <div key={i} className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <span className="text-indigo-300 font-mono font-semibold block">{gc.file}</span>
                <p className="text-slate-400">Lines of Code: <span className="font-bold text-white">{gc.loc} LOC</span></p>
                <p className="text-amber-400">{gc.reason}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
          <h3 className="font-bold text-white text-base flex items-center gap-2">
            <ShieldCheck className="h-5 w-5 text-emerald-400" />
            Refactoring Recommendations
          </h3>
          <ul className="space-y-2.5 text-xs text-slate-300">
            {arch?.recommendations.map((rec, i) => (
              <li key={i} className="flex items-start gap-2 p-3 rounded-xl bg-slate-950 border border-slate-800">
                <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
