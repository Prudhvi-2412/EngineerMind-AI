"use client";

import { useQuery } from "@tanstack/react-query";
import {
  Sparkles,
  TrendingUp,
  ShieldCheck,
  Zap,
  Activity,
  DollarSign,
  Users,
  Clock,
  CheckCircle2,
  AlertTriangle,
  ArrowDownRight,
  ArrowUpRight,
} from "lucide-react";

export default function EngineeringHealthDashboardPage() {
  const { data: health, isLoading } = useQuery({
    queryKey: ["engineering-health-dashboard-data"],
    queryFn: async () => ({
      engineeringScore: 88.5,
      deploymentSuccessRate: 97.8,
      sprintHealthScore: 84.2,
      incidentRiskScore: 12.4,
      technicalDebtScore: 24.0,
      cloudCostMonthly: 14250.0,
      cloudCostChangePercent: -4.5,
      topContributors: [
        { name: "Alex Rivera", email: "alex.lead@company.com", commitsCount: 48, prsMerged: 12, impactScore: 94.5 },
        { name: "Sarah Chen", email: "sarah.dev@company.com", commitsCount: 36, prsMerged: 9, impactScore: 89.0 },
        { name: "Marcus Vance", email: "marcus.eng@company.com", commitsCount: 29, prsMerged: 7, impactScore: 82.0 },
      ],
      recentEvents: [
        { eventId: "evt-101", source: "github", eventType: "pull_request.merged", timestamp: "10 mins ago", summary: "PR-2048 merged into payment-service main branch" },
        { eventId: "evt-102", source: "prometheus", eventType: "alert.resolved", timestamp: "25 mins ago", summary: "HighMemoryUsage alert resolved on auth-service" },
        { eventId: "evt-103", source: "jira", eventType: "issue.updated", timestamp: "42 mins ago", summary: "ENG-104 moved to In Progress by Sarah Chen" },
      ],
    }),
  });

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-indigo-950/80 via-purple-950/50 to-slate-900 border border-indigo-500/30 p-6 rounded-2xl shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-indigo-400" />
            <span className="text-xs font-bold text-indigo-400 uppercase tracking-widest">Composite AI Executive Health</span>
          </div>
          <h1 className="text-2xl font-bold text-white mt-1">Engineering Organization Health Matrix</h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time scorecards across deployment velocity, sprint health, SRE incident risk, technical debt, and cloud spend.
          </p>
        </div>

        <div className="px-6 py-3 rounded-2xl bg-slate-900/90 border border-indigo-500/40 text-center shadow-inner">
          <span className="text-xs text-slate-400 font-medium block">Overall Engineering Score</span>
          <span className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-indigo-400">
            {health?.engineeringScore} / 100
          </span>
        </div>
      </div>

      {/* 6 Core Metric Widgets Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-5">
        {/* Widget 1: Deployment Success */}
        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-3 hover:border-indigo-500/40 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Deployment Success</span>
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
              <Zap className="h-4 w-4" />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-white">{health?.deploymentSuccessRate}%</h2>
          <div className="inline-flex px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            OPTIMAL PIPELINE
          </div>
        </div>

        {/* Widget 2: Sprint Health */}
        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-3 hover:border-indigo-500/40 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Sprint Health</span>
            <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
              <Activity className="h-4 w-4" />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-white">{health?.sprintHealthScore}%</h2>
          <div className="inline-flex px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            ON TRACK
          </div>
        </div>

        {/* Widget 3: Incident Risk */}
        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-3 hover:border-indigo-500/40 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Incident Risk</span>
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
              <ShieldCheck className="h-4 w-4" />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-emerald-400">{health?.incidentRiskScore}%</h2>
          <div className="inline-flex px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            LOW RISK
          </div>
        </div>

        {/* Widget 4: Technical Debt */}
        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-3 hover:border-indigo-500/40 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Technical Debt Score</span>
            <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
              <AlertTriangle className="h-4 w-4" />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-white">{health?.technicalDebtScore} / 100</h2>
          <div className="inline-flex px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            MANAGEABLE DEBT
          </div>
        </div>

        {/* Widget 5: Cloud Cost */}
        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-3 hover:border-indigo-500/40 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Cloud Infra Cost</span>
            <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400">
              <DollarSign className="h-4 w-4" />
            </div>
          </div>
          <div className="flex items-baseline justify-between">
            <h2 className="text-2xl font-bold text-white">${health?.cloudCostMonthly.toLocaleString()}</h2>
            <span className="text-xs font-bold text-emerald-400 flex items-center">
              <ArrowDownRight className="h-3 w-3" />
              {health?.cloudCostChangePercent}%
            </span>
          </div>
          <div className="inline-flex px-2 py-0.5 rounded text-[10px] font-bold bg-purple-500/10 text-purple-400 border border-purple-500/20">
            ESTIMATED MONTHLY
          </div>
        </div>
      </div>

      {/* Top Contributors & Recent Telemetry Events Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Widget 6: Top Contributors Leaderboard */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-base flex items-center gap-2">
              <Users className="h-5 w-5 text-indigo-400" />
              Top Contributors Leaderboard
            </h3>
            <span className="text-xs text-slate-400">Last 30 Days</span>
          </div>

          <div className="space-y-3">
            {health?.topContributors.map((c, i) => (
              <div
                key={c.email}
                className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between hover:border-slate-700 transition-all"
              >
                <div className="flex items-center gap-3">
                  <div className="h-8 w-8 rounded-full bg-indigo-950 border border-indigo-700/50 flex items-center justify-center font-bold text-indigo-400 text-xs">
                    #{i + 1}
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-white">{c.name}</h4>
                    <p className="text-xs text-slate-400 font-mono">{c.email}</p>
                  </div>
                </div>

                <div className="flex items-center gap-4 text-xs">
                  <span className="text-slate-300 font-mono">{c.commitsCount} Commits</span>
                  <span className="text-purple-300 font-mono">{c.prsMerged} PRs</span>
                  <span className="px-2 py-0.5 rounded font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                    Impact: {c.impactScore}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Widget 7: Recent Events Feed */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-base flex items-center gap-2">
              <Clock className="h-5 w-5 text-emerald-400" />
              Real-time Ingested Telemetry Feed
            </h3>
            <span className="text-xs text-emerald-400 font-mono animate-pulse">● Live Stream</span>
          </div>

          <div className="space-y-3">
            {health?.recentEvents.map((evt) => (
              <div
                key={evt.eventId}
                className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1 hover:border-slate-700 transition-all"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider bg-slate-800 text-indigo-300 border border-slate-700">
                      {evt.source}
                    </span>
                    <span className="text-xs font-mono text-slate-400">{evt.eventType}</span>
                  </div>
                  <span className="text-xs text-slate-500">{evt.timestamp}</span>
                </div>
                <p className="text-xs text-slate-200 font-medium">{evt.summary}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
