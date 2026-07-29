"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Alert } from "@/components/ui/alert";
import { OAuthButtons } from "@/components/auth/oauth-buttons";
import { useAuthMutations } from "@/hooks/use-auth-mutations";
import { useAuth } from "@/context/auth-context";
import { Building2, Mail, Lock, ArrowRight } from "lucide-react";

const loginSchema = z.object({
  org_slug: z.string().min(2, "Organization slug is required").toLowerCase().trim(),
  email: z.string().email("Invalid email address").toLowerCase().trim(),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

type LoginSchemaType = z.infer<typeof loginSchema>;

export function LoginForm() {
  const router = useRouter();
  const { setAuthTokens } = useAuth();
  const { loginMutation } = useAuthMutations();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginSchemaType>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      org_slug: "acme-eng",
      email: "admin@acme.com",
      password: "",
    },
  });

  const onSubmit = async (values: LoginSchemaType) => {
    setErrorMessage(null);
    try {
      const data = await loginMutation.mutateAsync(values);
      await setAuthTokens(data.access_token, data.refresh_token);
      router.push("/dashboard");
    } catch (err: any) {
      const msg = err.response?.data?.detail || "Invalid credentials or organization slug.";
      setErrorMessage(msg);
    }
  };

  return (
    <div className="w-full space-y-6">
      {errorMessage && (
        <Alert variant="error">
          {errorMessage}
        </Alert>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Organization Slug
          </label>
          <Input
            {...register("org_slug")}
            placeholder="e.g. acme-eng"
            icon={<Building2 className="h-4 w-4" />}
            error={errors.org_slug?.message}
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Work Email
          </label>
          <Input
            {...register("email")}
            type="email"
            placeholder="you@company.com"
            icon={<Mail className="h-4 w-4" />}
            error={errors.email?.message}
          />
        </div>

        <div>
          <div className="flex items-center justify-between mb-1.5">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
              Password
            </label>
            <Link
              href="/forgot-password"
              className="text-xs text-indigo-400 hover:text-indigo-300 hover:underline transition-colors"
            >
              Forgot password?
            </Link>
          </div>
          <Input
            {...register("password")}
            type="password"
            placeholder="••••••••••••"
            icon={<Lock className="h-4 w-4" />}
            error={errors.password?.message}
          />
        </div>

        <Button
          type="submit"
          variant="gradient"
          size="lg"
          className="w-full font-semibold group mt-2"
          isLoading={loginMutation.isPending}
        >
          Sign In to Workspace
          <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
        </Button>
      </form>

      <div className="relative my-6">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-slate-800" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-slate-900 px-3 text-slate-500 font-medium">Or continue with</span>
        </div>
      </div>

      <OAuthButtons />

      <p className="text-center text-xs text-slate-400 pt-2">
        Don&apos;t have an organization workspace?{" "}
        <Link href="/signup" className="text-indigo-400 font-semibold hover:underline">
          Create Workspace
        </Link>
      </p>
    </div>
  );
}
