"use client";

import { useQuery } from "@tanstack/react-query";
import { Layers, TrendingUp, AlertOctagon, CheckCircle2, Lightbulb, ArrowUpRight } from "lucide-react";

export default function SprintDashboardPage() {
  const { data: sprint, isLoading } = useQuery({
    queryKey: ["sprint-prediction-data"],
    queryFn: async () => ({
      sprintId: "SPRINT-42",
      sprintName: "Sprint 42 - Q3 Payment Engine Upgrade",
      totalStoryPoints: 80.0,
      completedStoryPoints: 32.0,
      daysRemaining: 4,
      historicalVelocity: 45.0,
      requiredDailyVelocity: 12.0,
      sprintSuccessPercentage: 62.5,
      delayProbability: 37.5,
      blockedTasksCount: 2,
      blockedTasksDetails: [
        { key: "ENG-104", summary: "Redis Cluster migration block", points: 5 },
        { key: "ENG-109", summary: "Stripe API Webhook Signature validation", points: 8 },
      ],
      reasons: [
        "Required daily velocity (12.0 pts/day) exceeds historical team baseline (4.5 pts/day).",
        "Active blockages on 2 high-priority Jira tickets total 13 blocked story points.",
      ],
      recommendations: [
        "Descope non-essential ticket ENG-112 to preserve core sprint release commitment.",
        "Unblock Redis Cluster migration in SRE standup tomorrow.",
      ],
    }),
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Layers className="h-6 w-6 text-indigo-400" />
          Active Sprint Completion Prediction
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          AI Agent evaluating Jira burndown trajectory, velocity deficit ratio, and ticket blockages.
        </p>
      </div>

      {/* Progress Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span className="text-xs font-medium text-slate-400">Sprint Success Probability</span>
          <h2 className="text-3xl font-bold text-emerald-400">{sprint?.sprintSuccessPercentage}%</h2>
          <p className="text-xs text-slate-500">Days Remaining: {sprint?.daysRemaining} days</p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span className="text-xs font-medium text-slate-400">Delay Probability</span>
          <h2 className="text-3xl font-bold text-amber-400">{sprint?.delayProbability}%</h2>
          <p className="text-xs text-slate-500">Velocity Deficit: +7.5 pts/day needed</p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span className="text-xs font-medium text-slate-400">Story Points Completion</span>
          <h2 className="text-3xl font-bold text-white">
            {sprint?.completedStoryPoints} / {sprint?.totalStoryPoints}
          </h2>
          <p className="text-xs text-slate-500">Blocked Story Points: 13 pts</p>
        </div>
      </div>

      {/* AI Reasons & Recommendations */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
          <h3 className="font-bold text-white text-base flex items-center gap-2">
            <AlertOctagon className="h-5 w-5 text-amber-400" />
            AI Root Reasons for Risk
          </h3>
          <ul className="space-y-2.5 text-xs text-slate-300">
            {sprint?.reasons.map((reason, i) => (
              <li key={i} className="flex items-start gap-2 p-3 rounded-xl bg-slate-950 border border-slate-800/80">
                <span className="h-1.5 w-1.5 rounded-full bg-amber-400 mt-1.5 shrink-0" />
                <span>{reason}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
          <h3 className="font-bold text-white text-base flex items-center gap-2">
            <Lightbulb className="h-5 w-5 text-indigo-400" />
            AI Descoping & Action Plan
          </h3>
          <ul className="space-y-2.5 text-xs text-slate-300">
            {sprint?.recommendations.map((rec, i) => (
              <li key={i} className="flex items-start gap-2 p-3 rounded-xl bg-slate-950 border border-slate-800/80">
                <ArrowUpRight className="h-4 w-4 text-emerald-400 shrink-0" />
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
