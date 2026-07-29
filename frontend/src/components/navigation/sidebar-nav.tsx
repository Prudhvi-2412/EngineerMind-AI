"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/context/auth-context";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  FolderGit2,
  Users,
  GitPullRequest,
  Layers,
  ShieldAlert,
  Network,
  Settings,
  LogOut,
  Sparkles,
} from "lucide-react";

export function SidebarNav() {
  const pathname = usePathname();
  const { user, org, logout } = useAuth();

  if (!user) return null;

  const userRole = user.role;

  const navItems = [
    {
      name: "Overview",
      href: "/dashboard",
      icon: LayoutDashboard,
      roles: ["ADMIN", "ENGINEERING_MANAGER", "LEAD_ENGINEER", "ENGINEER", "VIEWER"],
    },
    {
      name: "Analytics & Reports",
      href: "/dashboard/analytics",
      icon: BarChart3,
      roles: ["ADMIN", "ENGINEERING_MANAGER", "LEAD_ENGINEER", "ENGINEER", "VIEWER"],
    },
    {
      name: "AI Chat Assistant",
      href: "/dashboard/chat",
      icon: Bot,
      roles: ["ADMIN", "ENGINEERING_MANAGER", "LEAD_ENGINEER", "ENGINEER", "VIEWER"],
    },
    {
      name: "Engineering Health",
      href: "/dashboard/health",
      icon: Sparkles,
      roles: ["ADMIN", "ENGINEERING_MANAGER", "LEAD_ENGINEER", "ENGINEER", "VIEWER"],
    },
    {
      name: "Repositories",
      href: "/dashboard/repositories",
      icon: FolderGit2,
      roles: ["ADMIN", "ENGINEERING_MANAGER", "LEAD_ENGINEER", "ENGINEER", "VIEWER"],
    },
    {
      name: "Developers",
      href: "/dashboard/developers",
      icon: Users,
      roles: ["ADMIN", "ENGINEERING_MANAGER", "LEAD_ENGINEER", "ENGINEER", "VIEWER"],
    },
    {
      name: "Pull Requests",
      href: "/dashboard/prs",
      icon: GitPullRequest,
      roles: ["ADMIN", "ENGINEERING_MANAGER", "LEAD_ENGINEER", "ENGINEER", "VIEWER"],
    },
    {
      name: "Sprint Prediction",
      href: "/dashboard/sprint",
      icon: Layers,
      roles: ["ADMIN", "ENGINEERING_MANAGER", "LEAD_ENGINEER", "ENGINEER", "VIEWER"],
    },
    {
      name: "Incidents & Root Cause",
      href: "/dashboard/incidents",
      icon: ShieldAlert,
      roles: ["ADMIN", "ENGINEERING_MANAGER", "LEAD_ENGINEER", "ENGINEER"],
    },
    {
      name: "Architecture Graph",
      href: "/dashboard/architecture",
      icon: Network,
      roles: ["ADMIN", "ENGINEERING_MANAGER", "LEAD_ENGINEER", "ENGINEER"],
    },
    {
      name: "Settings",
      href: "/dashboard/settings",
      icon: Settings,
      roles: ["ADMIN", "ENGINEERING_MANAGER", "LEAD_ENGINEER", "ENGINEER", "VIEWER"],
    },
  ];

  const filteredNavItems = navItems.filter((item) => item.roles.includes(userRole));

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950/90 backdrop-blur-xl flex flex-col h-screen sticky top-0 shrink-0">
      {/* Header / Org Branding */}
      <div className="p-6 border-b border-slate-800/80 flex items-center gap-3">
        <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/25">
          <Sparkles className="h-5 w-5 text-white" />
        </div>
        <div>
          <h2 className="font-bold text-white tracking-tight leading-none text-base">EngineeringOS</h2>
          <p className="text-xs text-indigo-400 font-medium mt-1 truncate max-w-[130px]">
            {org?.slug || "workspace"}
          </p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
        <p className="px-3 text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">
          Dashboard Suite
        </p>
        {filteredNavItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all group",
                isActive
                  ? "bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 shadow-inner"
                  : "text-slate-400 hover:bg-slate-900 hover:text-white"
              )}
            >
              <Icon className={cn("h-4 w-4 transition-colors", isActive ? "text-indigo-400" : "text-slate-400 group-hover:text-white")} />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* User Profile Footer */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-900/40">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3 overflow-hidden">
            <div className="h-9 w-9 rounded-full bg-indigo-950 border border-indigo-700/50 flex items-center justify-center font-bold text-indigo-400 shrink-0 text-sm shadow-sm">
              {user.name.charAt(0).toUpperCase()}
            </div>
            <div className="overflow-hidden">
              <p className="text-xs font-semibold text-white truncate">{user.name}</p>
              <Badge role={user.role} className="mt-1 text-[9px] py-0 px-1.5" />
            </div>
          </div>
          <button
            onClick={logout}
            title="Logout"
            className="p-2 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-800 transition-colors"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}
