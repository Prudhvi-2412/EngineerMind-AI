import { SignupForm } from "@/components/auth/signup-form";

export default function SignupPage() {
  return (
    <div>
      <div className="text-center mb-6">
        <h2 className="text-xl font-bold text-white tracking-tight">Create Workspace</h2>
        <p className="text-xs text-slate-400 mt-1">Set up your enterprise organization and admin account</p>
      </div>
      <SignupForm />
    </div>
  );
}
