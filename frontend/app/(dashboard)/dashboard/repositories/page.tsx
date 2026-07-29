"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { FolderGit2, Search, GitBranch, ShieldCheck, Cpu, Code2 } from "lucide-react";

export default function RepositoriesDashboardPage() {
  const [searchTerm, setSearchTerm] = useState("");

  const { data: repos, isLoading } = useQuery({
    queryKey: ["repositories-list"],
    queryFn: async () => [
      {
        id: "repo-1",
        name: "acme/payment-service",
        language: "Python (FastAPI)",
        branch: "main",
        activePRs: 6,
        healthScore: 94,
        microservice: "payment-service",
        lastSync: "5 mins ago",
      },
      {
        id: "repo-2",
        name: "acme/auth-service",
        language: "Go / TypeScript",
        branch: "main",
        activePRs: 2,
        healthScore: 88,
        microservice: "auth-service",
        lastSync: "12 mins ago",
      },
      {
        id: "repo-3",
        name: "acme/billing-engine",
        language: "Python",
        branch: "master",
        activePRs: 4,
        healthScore: 91,
        microservice: "billing-service",
        lastSync: "1 min ago",
      },
    ],
  });

  const filteredRepos = repos?.filter((r) =>
    r.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <FolderGit2 className="h-6 w-6 text-indigo-400" />
            Connected Repositories & Microservices
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time GitHub repository synchronization linked to Neo4j Knowledge Graph.
          </p>
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search repository..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-sm text-white placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 transition-all"
          />
        </div>
      </div>

      {/* Repo Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredRepos?.map((repo) => (
          <div
            key={repo.id}
            className="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 hover:border-indigo-500/50 transition-all group"
          >
            <div className="flex items-start justify-between">
              <div>
                <h3 className="font-bold text-white text-base group-hover:text-indigo-400 transition-colors">
                  {repo.name}
                </h3>
                <span className="text-xs text-slate-400 font-mono mt-0.5 block">
                  Microservice: {repo.microservice}
                </span>
              </div>
              <div className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                {repo.healthScore}% Health
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs pt-2 border-t border-slate-800/80">
              <div className="flex items-center gap-2 text-slate-400">
                <Code2 className="h-4 w-4 text-indigo-400" />
                <span>{repo.language}</span>
              </div>
              <div className="flex items-center gap-2 text-slate-400">
                <GitBranch className="h-4 w-4 text-purple-400" />
                <span>{repo.branch}</span>
              </div>
              <div className="flex items-center gap-2 text-slate-400">
                <Cpu className="h-4 w-4 text-emerald-400" />
                <span>{repo.activePRs} Active PRs</span>
              </div>
              <div className="flex items-center gap-2 text-slate-400">
                <ShieldCheck className="h-4 w-4 text-cyan-400" />
                <span>Synced {repo.lastSync}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
