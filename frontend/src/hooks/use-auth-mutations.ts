import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { TokenResponse, User, Organization } from "@/types/auth";

export interface LoginParams {
  org_slug: string;
  email: string;
  password: str;
}

export interface RegisterParams {
  org_name: string;
  org_slug: string;
  admin_email: string;
  admin_name: string;
  password: str;
}

export function useAuthMutations() {
  const queryClient = useQueryClient();

  const loginMutation = useMutation<TokenResponse, Error, LoginParams>({
    mutationFn: async (params) => {
      const response = await apiClient.post<TokenResponse>("/auth/login", params);
      return response.data;
    },
  });

  const registerMutation = useMutation<TokenResponse, Error, RegisterParams>({
    mutationFn: async (params) => {
      const response = await apiClient.post<TokenResponse>("/auth/register", params);
      return response.data;
    },
  });

  const logoutMutation = useMutation<void, Error, void>({
    mutationFn: async () => {
      const refreshToken = localStorage.getItem("refresh_token");
      if (refreshToken) {
        await apiClient.post("/auth/logout", { refresh_token: refreshToken });
      }
    },
    onSuccess: () => {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      queryClient.clear();
      window.location.href = "/login";
    },
  });

  return {
    loginMutation,
    registerMutation,
    logoutMutation,
  };
}
