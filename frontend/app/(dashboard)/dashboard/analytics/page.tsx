"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  BarChart3,
  Download,
  FileSpreadsheet,
  FileText,
  TrendingUp,
  Zap,
  Activity,
  Clock,
  Bug,
  Sparkles,
} from "lucide-react";

export default function AnalyticsDashboardPage() {
  const [timeframe, setTimeframe] = useState<"30d" | "90d" | "1y">("30d");

  const { data: analytics, isLoading } = useQuery({
    queryKey: ["analytics-trends-data", timeframe],
    queryFn: async () => ({
      timeframe,
      velocityTrend: [
        { date: "Jul 01", pts: 38 },
        { date: "Jul 05", pts: 42 },
        { date: "Jul 10", pts: 45 },
        { date: "Jul 15", pts: 40 },
        { date: "Jul 20", pts: 48 },
        { date: "Jul 25", pts: 52 },
        { date: "Jul 30", pts: 50 },
      ],
      deploymentFrequencyTrend: [
        { date: "Jul 01", deps: 3 },
        { date: "Jul 05", deps: 4 },
        { date: "Jul 10", deps: 5 },
        { date: "Jul 15", deps: 2 },
        { date: "Jul 20", deps: 6 },
        { date: "Jul 25", deps: 4 },
        { date: "Jul 30", deps: 5 },
      ],
      mttrTrend: [
        { date: "Jul 01", mins: 35 },
        { date: "Jul 05", mins: 28 },
        { date: "Jul 10", mins: 22 },
        { date: "Jul 15", mins: 19 },
        { date: "Jul 20", mins: 18 },
        { date: "Jul 25", mins: 16 },
        { date: "Jul 30", mins: 15 },
      ],
      leadTimeTrend: [
        { date: "Jul 01", hrs: 3.2 },
        { date: "Jul 05", hrs: 2.8 },
        { date: "Jul 10", hrs: 2.5 },
        { date: "Jul 15", hrs: 2.1 },
        { date: "Jul 20", hrs: 1.9 },
        { date: "Jul 25", hrs: 1.8 },
        { date: "Jul 30", hrs: 1.7 },
      ],
      bugTrends: [
        { date: "Jul 01", opened: 5, resolved: 6 },
        { date: "Jul 05", opened: 4, resolved: 5 },
        { date: "Jul 10", opened: 3, resolved: 4 },
        { date: "Jul 15", opened: 6, resolved: 7 },
        { date: "Jul 20", opened: 2, resolved: 4 },
        { date: "Jul 25", opened: 1, resolved: 3 },
        { date: "Jul 30", opened: 2, resolved: 4 },
      ],
      engineeringScoreTrend: [
        { date: "Jul 01", score: 81.0 },
        { date: "Jul 05", score: 83.5 },
        { date: "Jul 10", score: 85.0 },
        { date: "Jul 15", score: 84.2 },
        { date: "Jul 20", score: 87.0 },
        { date: "Jul 25", score: 88.5 },
        { date: "Jul 30", score: 89.2 },
      ],
    }),
  });

  const handleExportCSV = () => {
    window.open(`/api/v1/analytics/export/csv?timeframe=${timeframe}`, "_blank");
  };

  const handleExportPDF = () => {
    window.open(`/api/v1/analytics/export/pdf?timeframe=${timeframe}`, "_blank");
  };

  return (
    <div className="space-y-8">
      {/* Top Header & Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <BarChart3 className="h-6 w-6 text-indigo-400" />
            Engineering Analytics & Historical Trends
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Historical time-series graphs for Velocity, DORA Metrics, Bug Trends, and Health Scores.
          </p>
        </div>

        <div className="flex items-center gap-3">
          {/* Timeframe Filter Buttons */}
          <div className="flex items-center bg-slate-900 border border-slate-800 p-1 rounded-xl">
            {(["30d", "90d", "1y"] as const).map((tf) => (
              <button
                key={tf}
                onClick={() => setTimeframe(tf)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold uppercase transition-all ${
                  timeframe === tf
                    ? "bg-indigo-600 text-white shadow-md"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                {tf}
              </button>
            ))}
          </div>

          {/* Export Actions */}
          <button
            onClick={handleExportCSV}
            className="px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-emerald-500/40 text-emerald-400 hover:text-emerald-300 text-xs font-semibold flex items-center gap-1.5 transition-all"
          >
            <FileSpreadsheet className="h-4 w-4" />
            Export CSV
          </button>
          <button
            onClick={handleExportPDF}
            className="px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-1.5 transition-all shadow-lg shadow-indigo-600/20"
          >
            <FileText className="h-4 w-4" />
            Export PDF
          </button>
        </div>
      </div>

      {/* 6 Analytics Charts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Chart 1: Velocity Trend */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 hover:border-indigo-500/40 transition-all">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-sm flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-indigo-400" />
              Sprint Velocity (Story Points)
            </h3>
            <span className="text-xs font-bold text-emerald-400">+18% Velocity</span>
          </div>

          <div className="space-y-2 pt-2">
            {analytics?.velocityTrend.map((v) => (
              <div key={v.date} className="space-y-1">
                <div className="flex justify-between text-xs font-mono text-slate-400">
                  <span>{v.date}</span>
                  <span className="text-white font-bold">{v.pts} pts</span>
                </div>
                <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"
                    style={{ width: `${(v.pts / 60) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Chart 2: Deployment Frequency */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 hover:border-indigo-500/40 transition-all">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-sm flex items-center gap-2">
              <Zap className="h-4 w-4 text-emerald-400" />
              Deployment Frequency (Per Day)
            </h3>
            <span className="text-xs font-bold text-emerald-400">Elite Cadence</span>
          </div>

          <div className="space-y-2 pt-2">
            {analytics?.deploymentFrequencyTrend.map((d) => (
              <div key={d.date} className="space-y-1">
                <div className="flex justify-between text-xs font-mono text-slate-400">
                  <span>{d.date}</span>
                  <span className="text-white font-bold">{d.deps} deploys</span>
                </div>
                <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-emerald-500 to-teal-400 rounded-full"
                    style={{ width: `${(d.deps / 8) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Chart 3: Mean Time to Recovery (MTTR) */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 hover:border-indigo-500/40 transition-all">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-sm flex items-center gap-2">
              <Activity className="h-4 w-4 text-purple-400" />
              Mean Time to Recovery (MTTR)
            </h3>
            <span className="text-xs font-bold text-emerald-400">-57% MTTR</span>
          </div>

          <div className="space-y-2 pt-2">
            {analytics?.mttrTrend.map((m) => (
              <div key={m.date} className="space-y-1">
                <div className="flex justify-between text-xs font-mono text-slate-400">
                  <span>{m.date}</span>
                  <span className="text-white font-bold">{m.mins} mins</span>
                </div>
                <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"
                    style={{ width: `${(m.mins / 40) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Chart 4: Lead Time for Changes */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 hover:border-indigo-500/40 transition-all">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-sm flex items-center gap-2">
              <Clock className="h-4 w-4 text-cyan-400" />
              Lead Time for Changes (Hours)
            </h3>
            <span className="text-xs font-bold text-emerald-400">-46% Lead Time</span>
          </div>

          <div className="space-y-2 pt-2">
            {analytics?.leadTimeTrend.map((l) => (
              <div key={l.date} className="space-y-1">
                <div className="flex justify-between text-xs font-mono text-slate-400">
                  <span>{l.date}</span>
                  <span className="text-white font-bold">{l.hrs} hrs</span>
                </div>
                <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full"
                    style={{ width: `${(l.hrs / 4.0) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Chart 5: Bug Trends (Opened vs Resolved) */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 hover:border-indigo-500/40 transition-all">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-sm flex items-center gap-2">
              <Bug className="h-4 w-4 text-rose-400" />
              Bug Trends (Opened vs Resolved)
            </h3>
            <span className="text-xs font-bold text-emerald-400">Net Negative Bugs</span>
          </div>

          <div className="space-y-2 pt-2">
            {analytics?.bugTrends.map((b) => (
              <div key={b.date} className="space-y-1 text-xs font-mono">
                <div className="flex justify-between text-slate-400">
                  <span>{b.date}</span>
                  <span>
                    <span className="text-rose-400 font-bold">{b.opened} Opened</span> /{" "}
                    <span className="text-emerald-400 font-bold">{b.resolved} Resolved</span>
                  </span>
                </div>
                <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden flex">
                  <div className="h-full bg-rose-500" style={{ width: `${(b.opened / 10) * 100}%` }} />
                  <div className="h-full bg-emerald-500" style={{ width: `${(b.resolved / 10) * 100}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Chart 6: Composite Engineering Score */}
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 hover:border-indigo-500/40 transition-all">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-white text-sm flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-amber-400" />
              Engineering Health Score Trend
            </h3>
            <span className="text-xs font-bold text-emerald-400">89.2 Score</span>
          </div>

          <div className="space-y-2 pt-2">
            {analytics?.engineeringScoreTrend.map((s) => (
              <div key={s.date} className="space-y-1">
                <div className="flex justify-between text-xs font-mono text-slate-400">
                  <span>{s.date}</span>
                  <span className="text-white font-bold">{s.score} / 100</span>
                </div>
                <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-amber-400 to-emerald-400 rounded-full"
                    style={{ width: `${s.score}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
