"use client";

import { useQuery } from "@tanstack/react-query";
import {
  TrendingUp,
  GitPullRequest,
  ShieldAlert,
  Zap,
  Activity,
  CheckCircle2,
  AlertTriangle,
  Clock,
} from "lucide-react";

export default function OverviewDashboardPage() {
  const { data: doraMetrics, isLoading: loadingDora } = useQuery({
    queryKey: ["dora-metrics-overview"],
    queryFn: async () => {
      // Simulated live query response
      return {
        deploymentFrequency: { value: "4.2 / day", status: "ELITE", change: "+14%" },
        leadTimeForChanges: { value: "1.8 hours", status: "ELITE", change: "-22%" },
        meanTimeToRecovery: { value: "18 mins", status: "HIGH", change: "-35%" },
        changeFailureRate: { value: "2.1%", status: "ELITE", change: "-1.2%" },
      };
    },
  });

  const { data: activeAlerts } = useQuery({
    queryKey: ["active-risk-alerts"],
    queryFn: async () => [
      {
        id: "ALT-101",
        title: "High Blast Radius PR Merged in auth-service",
        severity: "HIGH",
        timestamp: "10 mins ago",
        affected: "auth-service, user-service",
      },
      {
        id: "ALT-102",
        title: "Sprint 42 Burndown Deficit (+2.4 pts/day needed)",
        severity: "MEDIUM",
        timestamp: "25 mins ago",
        affected: "Sprint 42 - Q3 Engine",
      },
    ],
  });

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-indigo-950/60 via-purple-950/40 to-slate-900 border border-indigo-500/20 p-6 rounded-2xl shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping" />
            <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">AI Engine Active</span>
          </div>
          <h1 className="text-2xl font-bold text-white mt-1">Engineering Executive Overview</h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time telemetry synthesis across GitHub, Jira, Prometheus, Grafana, and Neo4j Knowledge Graph.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="px-4 py-2 rounded-xl bg-slate-900/80 border border-slate-800 text-xs font-mono text-slate-300">
            Org: <span className="text-indigo-400 font-bold">Acme-Corp</span>
          </div>
        </div>
      </div>

      {/* DORA Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-3 relative overflow-hidden group hover:border-indigo-500/50 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Deployment Frequency</span>
            <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
              <Zap className="h-4 w-4" />
            </div>
          </div>
          <div className="flex items-baseline justify-between">
            <h2 className="text-2xl font-bold text-white">{doraMetrics?.deploymentFrequency.value || "---"}</h2>
            <span className="text-xs font-bold text-emerald-400">{doraMetrics?.deploymentFrequency.change}</span>
          </div>
          <div className="inline-flex px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            {doraMetrics?.deploymentFrequency.status || "ELITE"}
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-3 relative overflow-hidden group hover:border-indigo-500/50 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Lead Time for Changes</span>
            <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400">
              <Clock className="h-4 w-4" />
            </div>
          </div>
          <div className="flex items-baseline justify-between">
            <h2 className="text-2xl font-bold text-white">{doraMetrics?.leadTimeForChanges.value || "---"}</h2>
            <span className="text-xs font-bold text-emerald-400">{doraMetrics?.leadTimeForChanges.change}</span>
          </div>
          <div className="inline-flex px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            {doraMetrics?.leadTimeForChanges.status || "ELITE"}
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-3 relative overflow-hidden group hover:border-indigo-500/50 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Mean Time to Recovery (MTTR)</span>
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
              <Activity className="h-4 w-4" />
            </div>
          </div>
          <div className="flex items-baseline justify-between">
            <h2 className="text-2xl font-bold text-white">{doraMetrics?.meanTimeToRecovery.value || "---"}</h2>
            <span className="text-xs font-bold text-emerald-400">{doraMetrics?.meanTimeToRecovery.change}</span>
          </div>
          <div className="inline-flex px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            {doraMetrics?.meanTimeToRecovery.status || "HIGH"}
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-3 relative overflow-hidden group hover:border-indigo-500/50 transition-all">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Change Failure Rate (CFR)</span>
            <div className="p-2 rounded-lg bg-rose-500/10 text-rose-400">
              <ShieldAlert className="h-4 w-4" />
            </div>
          </div>
          <div className="flex items-baseline justify-between">
            <h2 className="text-2xl font-bold text-white">{doraMetrics?.changeFailureRate.value || "---"}</h2>
            <span className="text-xs font-bold text-emerald-400">{doraMetrics?.changeFailureRate.change}</span>
          </div>
          <div className="inline-flex px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            {doraMetrics?.changeFailureRate.status || "ELITE"}
          </div>
        </div>
      </div>

      {/* Active AI Risk Alerts & Feeds */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-base flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-400" />
              Active AI Risk Intelligence Feed
            </h3>
            <span className="text-xs text-slate-400 font-mono">Live Sync</span>
          </div>

          <div className="space-y-3">
            {activeAlerts?.map((alert) => (
              <div
                key={alert.id}
                className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 flex items-start justify-between gap-4 hover:border-slate-700 transition-all"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded text-[9px] font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">
                      {alert.severity} RISK
                    </span>
                    <span className="text-xs text-slate-400">{alert.timestamp}</span>
                  </div>
                  <h4 className="text-sm font-semibold text-white">{alert.title}</h4>
                  <p className="text-xs text-slate-400">Affected Scope: <span className="font-mono text-indigo-300">{alert.affected}</span></p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* System Persisted Knowledge Graph Health */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
          <h3 className="font-bold text-white text-base flex items-center gap-2">
            <CheckCircle2 className="h-5 w-5 text-indigo-400" />
            Knowledge Graph Health
          </h3>
          <div className="space-y-3 text-xs">
            <div className="flex justify-between p-3 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-slate-400">Neo4j Nodes Synchronized</span>
              <span className="font-bold text-white font-mono">1,420 Nodes</span>
            </div>
            <div className="flex justify-between p-3 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-slate-400">Relationships Index</span>
              <span className="font-bold text-white font-mono">4,890 Edge Paths</span>
            </div>
            <div className="flex justify-between p-3 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-slate-400">Redis Queue Latency</span>
              <span className="font-bold text-emerald-400 font-mono">1.2 ms</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
