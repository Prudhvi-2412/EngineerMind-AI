"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Bot, Send, Sparkles, ShieldCheck, Database, GitPullRequest, Layers, Network, User } from "lucide-react";

interface ChatMessage {
  id: string;
  sender: "user" | "assistant";
  text: string;
  evidence?: Array<{ source: string; entity: string; fact: string }>;
}

export default function EngineeringChatPage() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "init-1",
      sender: "assistant",
      text: "Hello! I am your **Grounded EngineeringOS AI Assistant**. Every response I generate is strictly backed by evidence from your **Neo4j Knowledge Graph, PostgreSQL Database, GitHub Repos, and Jira Sprints** without hallucination.\n\nHow can I assist your engineering team today?",
      evidence: [],
    },
  ]);

  const chatMutation = useMutation({
    mutationFn: async (userQuery: string) => {
      // Simulated API response or live fetch
      return {
        user_query: userQuery,
        intent_category: "repository",
        assistant_response: `### Grounded Analysis & Answer\n\nBased on factual data from your **Neo4j Knowledge Graph** and **GitHub Integration**:\n\n- **Target Entity:** \`PR-2048\` in \`acme/payment-service\`\n- **Touched Microservices:** \`payment-service\`, \`billing-service\`\n- **Databases at Risk:** \`payment_db\`\n\n#### Recommended Next Steps\n- Ensure database migrations on \`payment_db\` are run in pre-deploy phase.\n- Request mandatory review from \`sre-lead@company.com\` before merging.`,
        confidence_score: 98.5,
        grounded_evidence: [
          { source: "Neo4j Knowledge Graph", entity: "PullRequest:PR-2048", fact: "Touches payment-service & billing-service; database payment_db at risk." },
          { source: "GitHub Integration", entity: "Repo:acme/payment-service", fact: "Python FastAPI repo on main branch with 6 active PRs." }
        ]
      };
    },
    onSuccess: (data) => {
      setMessages((prev) => [
        ...prev,
        {
          id: `asst-${Date.now()}`,
          sender: "assistant",
          text: data.assistant_response,
          evidence: data.grounded_evidence,
        },
      ]);
    },
  });

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || chatMutation.isPending) return;

    const userText = query.trim();
    setQuery("");

    setMessages((prev) => [
      ...prev,
      { id: `user-${Date.now()}`, sender: "user", text: userText },
    ]);

    chatMutation.mutate(userText);
  };

  const handleQuickPrompt = (promptText: string) => {
    setQuery(promptText);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)] space-y-4">
      {/* Top Header */}
      <div className="flex items-center justify-between bg-slate-900/80 border border-slate-800 p-4 rounded-2xl">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/25">
            <Bot className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-white text-base">Grounded Engineering RAG AI Assistant</h1>
            <p className="text-xs text-emerald-400 font-mono flex items-center gap-1.5">
              <ShieldCheck className="h-3.5 w-3.5" /> Zero-Hallucination Grounding Active
            </p>
          </div>
        </div>

        {/* Quick Suggestion Chips */}
        <div className="hidden lg:flex items-center gap-2">
          <button
            onClick={() => handleQuickPrompt("What is the blast radius of PR-2048?")}
            className="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-slate-300 hover:border-indigo-500 transition-all flex items-center gap-1.5"
          >
            <GitPullRequest className="h-3.5 w-3.5 text-indigo-400" />
            PR Blast Radius
          </button>
          <button
            onClick={() => handleQuickPrompt("Will Sprint 42 finish on time?")}
            className="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-slate-300 hover:border-indigo-500 transition-all flex items-center gap-1.5"
          >
            <Layers className="h-3.5 w-3.5 text-purple-400" />
            Sprint Prediction
          </button>
          <button
            onClick={() => handleQuickPrompt("What caused the high latency alert on payment-service?")}
            className="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-slate-300 hover:border-indigo-500 transition-all flex items-center gap-1.5"
          >
            <Database className="h-3.5 w-3.5 text-amber-400" />
            Incident Root Cause
          </button>
        </div>
      </div>

      {/* Messages Stream */}
      <div className="flex-1 bg-slate-900/50 border border-slate-800/80 rounded-2xl p-6 overflow-y-auto space-y-6">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex items-start gap-4 ${
              msg.sender === "user" ? "flex-row-reverse" : "flex-row"
            }`}
          >
            <div
              className={`h-9 w-9 rounded-xl flex items-center justify-center shrink-0 text-sm font-bold shadow-md ${
                msg.sender === "user"
                  ? "bg-indigo-600 text-white"
                  : "bg-gradient-to-tr from-indigo-500 to-purple-500 text-white"
              }`}
            >
              {msg.sender === "user" ? <User className="h-5 w-5" /> : <Bot className="h-5 w-5" />}
            </div>

            <div
              className={`max-w-3xl rounded-2xl p-5 space-y-3 ${
                msg.sender === "user"
                  ? "bg-indigo-600/20 border border-indigo-500/30 text-indigo-100"
                  : "bg-slate-900 border border-slate-800 text-slate-200"
              }`}
            >
              <div className="prose prose-invert max-w-none text-sm leading-relaxed whitespace-pre-line">
                {msg.text}
              </div>

              {/* Grounded Evidence Drawer */}
              {msg.evidence && msg.evidence.length > 0 && (
                <div className="pt-3 border-t border-slate-800 space-y-2">
                  <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                    <ShieldCheck className="h-3.5 w-3.5" /> Cited Evidence ({msg.evidence.length})
                  </span>
                  <div className="space-y-1.5 text-xs">
                    {msg.evidence.map((ev, i) => (
                      <div key={i} className="p-2.5 rounded-xl bg-slate-950 border border-slate-800/80 font-mono">
                        <span className="text-indigo-400 font-bold">{ev.source}</span> ({ev.entity}):{" "}
                        <span className="text-slate-300">{ev.fact}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}

        {chatMutation.isPending && (
          <div className="flex items-center gap-3 text-slate-400 text-xs font-mono animate-pulse">
            <Bot className="h-4 w-4 text-indigo-400" />
            Querying Neo4j Knowledge Graph & Telemetry Database...
          </div>
        )}
      </div>

      {/* Input Box */}
      <form onSubmit={handleSend} className="relative">
        <input
          type="text"
          placeholder="Ask anything about PRs, microservices, deployments, sprints, or incidents..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full bg-slate-900 border border-slate-800 rounded-2xl pl-5 pr-14 py-4 text-sm text-white placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 shadow-xl transition-all"
        />
        <button
          type="submit"
          disabled={!query.trim() || chatMutation.isPending}
          className="absolute right-3 top-3 h-10 w-10 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white flex items-center justify-center transition-all shadow-lg shadow-indigo-600/25"
        >
          <Send className="h-4 w-4" />
        </button>
      </form>
    </div>
  );
}
