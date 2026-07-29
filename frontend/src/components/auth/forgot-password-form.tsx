"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Alert } from "@/components/ui/alert";
import { Mail, ArrowLeft, Send } from "lucide-react";

const forgotSchema = z.object({
  email: z.string().email("Invalid email address").toLowerCase().trim(),
});

type ForgotSchemaType = z.infer<typeof forgotSchema>;

export function ForgotPasswordForm() {
  const [isSuccess, setIsSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ForgotSchemaType>({
    resolver: zodResolver(forgotSchema),
  });

  const onSubmit = async (values: ForgotSchemaType) => {
    // Simulate password reset email send
    await new Promise((res) => setTimeout(res, 1200));
    setIsSuccess(true);
  };

  return (
    <div className="w-full space-y-6">
      {isSuccess ? (
        <Alert variant="success" className="space-y-2">
          <p className="font-semibold">Reset instructions sent!</p>
          <p className="text-xs">Check your inbox for password reset instructions.</p>
        </Alert>
      ) : (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Work Email Address
            </label>
            <Input
              {...register("email")}
              type="email"
              placeholder="you@company.com"
              icon={<Mail className="h-4 w-4" />}
              error={errors.email?.message}
            />
          </div>

          <Button
            type="submit"
            variant="default"
            size="lg"
            className="w-full font-semibold"
            isLoading={isSubmitting}
          >
            <Send className="mr-2 h-4 w-4" />
            Send Password Reset Link
          </Button>
        </form>
      )}

      <div className="text-center pt-2">
        <Link
          href="/login"
          className="inline-flex items-center text-xs text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="mr-1.5 h-3.5 w-3.5" />
          Back to Login
        </Link>
      </div>
    </div>
  );
}
