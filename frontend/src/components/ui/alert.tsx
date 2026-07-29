import * as React from "react"
import { AlertCircle, CheckCircle2, Info } from "lucide-react"
import { cn } from "@/lib/utils"

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "error" | "success";
}

export function Alert({ className, variant = "default", children, ...props }: AlertProps) {
  const styles = {
    default: "bg-slate-900 border-slate-800 text-slate-200",
    error: "bg-rose-950/40 border-rose-800/60 text-rose-300",
    success: "bg-emerald-950/40 border-emerald-800/60 text-emerald-300",
  };

  const icons = {
    default: <Info className="h-4 w-4 text-slate-400 shrink-0 mt-0.5" />,
    error: <AlertCircle className="h-4 w-4 text-rose-400 shrink-0 mt-0.5" />,
    success: <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />,
  };

  return (
    <div
      className={cn(
        "flex items-start gap-3 rounded-xl border p-4 text-sm font-medium animate-in fade-in-50 duration-200",
        styles[variant],
        className
      )}
      {...props}
    >
      {icons[variant]}
      <div className="flex-1">{children}</div>
    </div>
  );
}
