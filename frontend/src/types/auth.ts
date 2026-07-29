export type Role = "ADMIN" | "ENGINEERING_MANAGER" | "LEAD_ENGINEER" | "ENGINEER" | "VIEWER";

export interface User {
  id: string;
  org_id: string;
  email: string;
  name: string;
  role: Role;
  avatar_url?: string | null;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  plan_tier: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface AuthState {
  user: User | null;
  org: Organization | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
