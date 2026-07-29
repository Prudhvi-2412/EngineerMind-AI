import { ForgotPasswordForm } from "@/components/auth/forgot-password-form";

export default function ForgotPasswordPage() {
  return (
    <div>
      <div className="text-center mb-6">
        <h2 className="text-xl font-bold text-white tracking-tight">Reset Password</h2>
        <p className="text-xs text-slate-400 mt-1">Enter your work email to receive password reset instructions</p>
      </div>
      <ForgotPasswordForm />
    </div>
  );
}
