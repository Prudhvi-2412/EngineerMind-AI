"use client";

import { useQuery } from "@tanstack/react-query";
import { GitPullRequest, ShieldAlert, Cpu, CheckCircle2, UserCheck, AlertTriangle } from "lucide-react";

export default function PRsDashboardPage() {
  const { data: prs, isLoading } = useQuery({
    queryKey: ["prs-risk-list"],
    queryFn: async () => [
      {
        id: "PR-2048",
        title: "Refactor Payment Processor & DB Connection Pool Schema",
        repo: "acme/payment-service",
        author: "alex.lead@company.com",
        riskScore: 84.5,
        riskLevel: "HIGH",
        additions: 240,
        deletions: 45,
        changedFiles: 8,
        touchedServices: ["payment-service", "billing-service"],
        databasesAtRisk: ["payment_db"],
        suggestedReviewers: ["sre-lead@company.com", "architecture-owner@company.com"],
      },
      {
        id: "PR-2049",
        title: "Upgrade TailwindCSS styling on Landing page",
        repo: "acme/frontend-app",
        author: "sarah.dev@company.com",
        riskScore: 12.0,
        riskLevel: "LOW",
        additions: 45,
        deletions: 12,
        changedFiles: 3,
        touchedServices: ["frontend-app"],
        databasesAtRisk: [],
        suggestedReviewers: ["frontend-lead@company.com"],
      },
    ],
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <GitPullRequest className="h-6 w-6 text-indigo-400" />
          Pull Request Risk & Blast Radius Intelligence
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          LangGraph AI Agent synthesizing Neo4j Knowledge Graph blast radius, code churn, and reviewer matching.
        </p>
      </div>

      <div className="space-y-4">
        {prs?.map((pr) => (
          <div
            key={pr.id}
            className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 hover:border-indigo-500/50 transition-all"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="space-y-1">
                <div className="flex items-center gap-3">
                  <span className="text-xs font-bold text-indigo-400 font-mono">{pr.id}</span>
                  <span className="text-xs text-slate-400 font-mono">{pr.repo}</span>
                </div>
                <h3 className="font-bold text-white text-lg">{pr.title}</h3>
                <p className="text-xs text-slate-400">Author: <span className="text-slate-300 font-mono">{pr.author}</span></p>
              </div>

              <div className="flex items-center gap-3">
                <div
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold border flex items-center gap-1.5 ${
                    pr.riskLevel === "HIGH"
                      ? "bg-rose-500/10 text-rose-400 border-rose-500/30"
                      : "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
                  }`}
                >
                  <ShieldAlert className="h-4 w-4" />
                  {pr.riskScore} RISK ({pr.riskLevel})
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-3 border-t border-slate-800/80 text-xs">
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <span className="text-slate-400 font-semibold flex items-center gap-1.5">
                  <Cpu className="h-3.5 w-3.5 text-indigo-400" />
                  Neo4j Blast Radius
                </span>
                <p className="text-slate-300 font-mono">Services: {pr.touchedServices.join(", ")}</p>
                <p className="text-amber-400 font-mono">DBs at Risk: {pr.databasesAtRisk.join(", ") || "None"}</p>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <span className="text-slate-400 font-semibold flex items-center gap-1.5">
                  <GitPullRequest className="h-3.5 w-3.5 text-purple-400" />
                  Code Churn Metrics
                </span>
                <p className="text-emerald-400 font-mono">+{pr.additions} Additions</p>
                <p className="text-rose-400 font-mono">-{pr.deletions} Deletions across {pr.changedFiles} files</p>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <span className="text-slate-400 font-semibold flex items-center gap-1.5">
                  <UserCheck className="h-3.5 w-3.5 text-emerald-400" />
                  Suggested Reviewers
                </span>
                <p className="text-indigo-300 font-mono">{pr.suggestedReviewers.join(", ")}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
