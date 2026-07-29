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
import { Building2, User as UserIcon, Mail, Lock, ArrowRight } from "lucide-react";

const signupSchema = z.object({
  org_name: z.string().min(2, "Organization name must be at least 2 characters"),
  org_slug: z
    .string()
    .min(2, "Slug must be at least 2 characters")
    .regex(/^[a-z0-9-]+$/, "Slug must contain only lowercase letters, numbers, and hyphens"),
  admin_name: z.string().min(2, "Your name is required"),
  admin_email: z.string().email("Invalid email address").toLowerCase().trim(),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type SignupSchemaType = z.infer<typeof signupSchema>;

export function SignupForm() {
  const router = useRouter();
  const { setAuthTokens } = useAuth();
  const { registerMutation } = useAuthMutations();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<SignupSchemaType>({
    resolver: zodResolver(signupSchema),
    defaultValues: {
      org_name: "",
      org_slug: "",
      admin_name: "",
      admin_email: "",
      password: "",
    },
  });

  const handleOrgNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    const slugified = val
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, "")
      .replace(/\s+/g, "-");
    setValue("org_name", val);
    setValue("org_slug", slugified, { shouldValidate: true });
  };

  const onSubmit = async (values: SignupSchemaType) => {
    setErrorMessage(null);
    try {
      const data = await registerMutation.mutateAsync(values);
      await setAuthTokens(data.access_token, data.refresh_token);
      router.push("/dashboard");
    } catch (err: any) {
      const msg = err.response?.data?.detail || "Registration failed. Slug or email may already exist.";
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
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Organization Name
            </label>
            <Input
              {...register("org_name")}
              onChange={handleOrgNameChange}
              placeholder="e.g. Acme Corp"
              icon={<Building2 className="h-4 w-4" />}
              error={errors.org_name?.message}
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Workspace Slug
            </label>
            <Input
              {...register("org_slug")}
              placeholder="acme-corp"
              error={errors.org_slug?.message}
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Full Name (Admin)
          </label>
          <Input
            {...register("admin_name")}
            placeholder="Jane Doe"
            icon={<UserIcon className="h-4 w-4" />}
            error={errors.admin_name?.message}
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Work Email
          </label>
          <Input
            {...register("admin_email")}
            type="email"
            placeholder="jane@acmecorp.com"
            icon={<Mail className="h-4 w-4" />}
            error={errors.admin_email?.message}
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
            Password (min 8 chars)
          </label>
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
          isLoading={registerMutation.isPending}
        >
          Create Enterprise Workspace
          <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
        </Button>
      </form>

      <div className="relative my-6">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-slate-800" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-slate-900 px-3 text-slate-500 font-medium">Or register with</span>
        </div>
      </div>

      <OAuthButtons />

      <p className="text-center text-xs text-slate-400 pt-2">
        Already have a workspace?{" "}
        <Link href="/login" className="text-indigo-400 font-semibold hover:underline">
          Sign In
        </Link>
      </p>
    </div>
  );
}
