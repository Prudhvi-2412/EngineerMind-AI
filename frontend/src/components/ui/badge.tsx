import { cn } from "@/lib/utils"
import { Role } from "@/types/auth"

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  role?: Role;
}

export function Badge({ className, role, children, ...props }: BadgeProps) {
  const roleStyles: Record<Role, string> = {
    ADMIN: "bg-purple-950/60 border-purple-700/60 text-purple-300",
    ENGINEERING_MANAGER: "bg-indigo-950/60 border-indigo-700/60 text-indigo-300",
    LEAD_ENGINEER: "bg-blue-950/60 border-blue-700/60 text-blue-300",
    ENGINEER: "bg-emerald-950/60 border-emerald-700/60 text-emerald-300",
    VIEWER: "bg-slate-900 border-slate-800 text-slate-400",
  };

  const badgeClass = role ? roleStyles[role] : "bg-slate-900 border-slate-800 text-slate-300";

  return (
    <div
      className={cn(
        "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold tracking-wider transition-colors uppercase",
        badgeClass,
        className
      )}
      {...props}
    >
      {role || children}
    </div>
  );
}
