"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/auth-context";
import { SidebarNav } from "@/components/navigation/sidebar-nav";
import { Skeleton } from "@/components/ui/skeleton";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return (
      <div className="flex h-screen w-full bg-slate-950">
        <div className="w-64 border-r border-slate-800 p-6 space-y-4">
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-6 w-3/4" />
          <Skeleton className="h-6 w-5/6" />
          <Skeleton className="h-6 w-2/3" />
        </div>
        <div className="flex-1 p-8 space-y-6">
          <Skeleton className="h-12 w-1/3" />
          <div className="grid grid-cols-3 gap-6">
            <Skeleton className="h-32 w-full" />
            <Skeleton className="h-32 w-full" />
            <Skeleton className="h-32 w-full" />
          </div>
          <Skeleton className="h-64 w-full" />
        </div>
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100">
      <SidebarNav />
      <main className="flex-1 p-8 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}
