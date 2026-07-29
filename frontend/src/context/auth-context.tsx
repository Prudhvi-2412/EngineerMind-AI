"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { User, Organization } from "@/types/auth";
import { apiClient } from "@/lib/api-client";

interface AuthContextType {
  user: User | null;
  org: Organization | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setAuthTokens: (accessToken: string, refreshToken: string) => Promise<void>;
  logout: () => void;
  refetchUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [org, setOrg] = useState<Organization | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const fetchUserData = async () => {
    try {
      const accessToken = localStorage.getItem("access_token");
      if (!accessToken) {
        setIsLoading(false);
        return;
      }

      const [userRes, orgRes] = await Promise.all([
        apiClient.get<User>("/auth/me"),
        apiClient.get<Organization>("/organizations/me"),
      ]);

      setUser(userRes.data);
      setOrg(orgRes.data);
    } catch (error) {
      console.error("Failed to load user profile:", error);
      setUser(null);
      setOrg(null);
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchUserData();
  }, []);

  const setAuthTokens = async (accessToken: string, refreshToken: string) => {
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);
    setIsLoading(true);
    await fetchUserData();
  };

  const logout = () => {
    const refreshToken = localStorage.getItem("refresh_token");
    if (refreshToken) {
      apiClient.post("/auth/logout", { refresh_token: refreshToken }).catch(() => {});
    }
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    setOrg(null);
    window.location.href = "/login";
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        org,
        isAuthenticated: !!user,
        isLoading,
        setAuthTokens,
        logout,
        refetchUser: fetchUserData,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
