"use client";

import React, { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "@/context/theme-context";
import { AuthProvider } from "@/context/auth-context";
import "@/app/globals.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 1000 * 60 * 5,
        retry: 1,
      },
    },
  }));

  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen">
        <QueryClientProvider client={queryClient}>
          <ThemeProvider>
            <AuthProvider>
              {children}
            </AuthProvider>
          </ThemeProvider>
        </QueryClientProvider>
      </body>
    </html>
  );
}
