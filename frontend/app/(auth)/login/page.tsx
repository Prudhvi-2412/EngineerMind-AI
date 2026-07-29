import { LoginForm } from "@/components/auth/login-form";

export default function LoginPage() {
  return (
    <div>
      <div className="text-center mb-6">
        <h2 className="text-xl font-bold text-white tracking-tight">Sign In to Workspace</h2>
        <p className="text-xs text-slate-400 mt-1">Enter your credentials to access your engineering dashboard</p>
      </div>
      <LoginForm />
    </div>
  );
}
