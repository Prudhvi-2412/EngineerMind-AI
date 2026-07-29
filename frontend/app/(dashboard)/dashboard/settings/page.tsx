"use client";

import { useAuth } from "@/context/auth-context";
import { Settings, Shield, Key, Bell, Database, Radio, CheckCircle2 } from "lucide-react";

export default function SettingsDashboardPage() {
  const { user, org } = useAuth();

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Settings className="h-6 w-6 text-indigo-400" />
          Workspace & Integrations Settings
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Manage system configurations, webhook endpoints, and hybrid database persistences.
        </p>
      </div>

      {/* Connected Integrations Card */}
      <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-base flex items-center gap-2">
          <Radio className="h-5 w-5 text-indigo-400" />
          Multi-Source Telemetry Integrations
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
            <div>
              <h4 className="font-bold text-white">GitHub Integration</h4>
              <p className="text-slate-400">OAuth & Webhooks</p>
            </div>
            <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              CONNECTED
            </span>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
            <div>
              <h4 className="font-bold text-white">Jira Software</h4>
              <p className="text-slate-400">Issue Webhook Collector</p>
            </div>
            <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              CONNECTED
            </span>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
            <div>
              <h4 className="font-bold text-white">Slack App</h4>
              <p className="text-slate-400">Event Subscriptions</p>
            </div>
            <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              CONNECTED
            </span>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
            <div>
              <h4 className="font-bold text-white">Prometheus / Grafana</h4>
              <p className="text-slate-400">Alertmanager Webhook</p>
            </div>
            <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              CONNECTED
            </span>
          </div>
        </div>
      </div>

      {/* Persistence Drivers Status Card */}
      <div className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4">
        <h3 className="font-bold text-white text-base flex items-center gap-2">
          <Database className="h-5 w-5 text-emerald-400" />
          Persistence Infrastructure
        </h3>

        <div className="space-y-3 text-xs">
          <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-slate-300 font-mono">PostgreSQL / TimescaleDB</span>
            <span className="text-emerald-400 font-bold flex items-center gap-1">
              <CheckCircle2 className="h-4 w-4" /> Healthy (AsyncPG Pool Active)
            </span>
          </div>

          <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-slate-300 font-mono">Neo4j Enterprise Graph</span>
            <span className="text-emerald-400 font-bold flex items-center gap-1">
              <CheckCircle2 className="h-4 w-4" /> Bolt Protocol Active (bolt://localhost:7687)
            </span>
          </div>

          <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-slate-300 font-mono">Redis Distributed Cache & Queue</span>
            <span className="text-emerald-400 font-bold flex items-center gap-1">
              <CheckCircle2 className="h-4 w-4" /> Celery Workers Listening
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
