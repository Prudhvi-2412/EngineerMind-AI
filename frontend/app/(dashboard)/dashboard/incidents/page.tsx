"use client";

import { useQuery } from "@tanstack/react-query";
import { ShieldAlert, Activity, Bot, CheckCircle2, Wrench, Flame } from "lucide-react";

export default function IncidentsDashboardPage() {
  const { data: incident, isLoading } = useQuery({
    queryKey: ["incident-prediction-data"],
    queryFn: async () => ({
      serviceName: "payment-service",
      predictedIncidentRisk: 88.5,
      predictedIncidentLevel: "HIGH",
      rootCauseAnalysis:
        "Elevated HTTP 5xx error rate (6.2%) and P99 latency spike (780ms) triggered by deployment dep-904 on payment-service. Database connection pool exhaustion detected on payment_db.",
      affectedServices: ["payment-service", "billing-service", "user-service"],
      mitigationSteps: [
        "Roll back Kubernetes deployment dep-904 on payment-service to previous stable container digest.",
        "Scale HPA deployment replicas from 3 to 8 pods.",
        "Increase PostgreSQL max_connections setting on payment_db instance.",
      ],
    }),
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Bot className="h-6 w-6 text-rose-400" />
          Incident Prediction & Root Cause SRE Intelligence
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          LangGraph SRE AI Agent evaluating Prometheus metrics, Grafana alerts, and Kubernetes deployment triggers.
        </p>
      </div>

      {/* Incident Risk Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-rose-950/60 via-slate-900 to-slate-950 border border-rose-500/30 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Flame className="h-4 w-4 text-rose-400 animate-pulse" />
            <span className="text-xs font-bold text-rose-400 uppercase tracking-wider">
              {incident?.predictedIncidentLevel} RISK INCIDENT PREDICTED
            </span>
          </div>
          <h2 className="text-xl font-bold text-white">Target Service: {incident?.serviceName}</h2>
          <p className="text-xs text-slate-400">Time Horizon: Next 30 minutes</p>
        </div>

        <div className="px-5 py-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-center">
          <span className="text-2xl font-bold text-rose-400">{incident?.predictedIncidentRisk}%</span>
          <span className="text-[10px] text-slate-400 block font-medium uppercase">Outage Probability</span>
        </div>
      </div>

      {/* Root Cause & Affected Scope */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-3">
          <h3 className="font-bold text-white text-base flex items-center gap-2">
            <Activity className="h-5 w-5 text-indigo-400" />
            AI Root Cause Analysis
          </h3>
          <p className="text-sm text-slate-300 leading-relaxed bg-slate-950 p-4 rounded-xl border border-slate-800">
            {incident?.rootCauseAnalysis}
          </p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-3">
          <h3 className="font-bold text-white text-base flex items-center gap-2">
            <ShieldAlert className="h-5 w-5 text-amber-400" />
            Affected Cascading Scope
          </h3>
          <ul className="space-y-2 text-xs font-mono text-slate-300">
            {incident?.affectedServices.map((svc) => (
              <li key={svc} className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between">
                <span>{svc}</span>
                <span className="text-amber-400 font-bold">At Risk</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* SRE Mitigation Steps */}
      <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-base flex items-center gap-2">
          <Wrench className="h-5 w-5 text-emerald-400" />
          Recommended Automated SRE Mitigation Plan
        </h3>
        <div className="space-y-2.5">
          {incident?.mitigationSteps.map((step, i) => (
            <div key={i} className="flex items-start gap-3 p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200">
              <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>{step}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
