export function MetricCard({
  label,
  value,
  hint,
  icon,
  accent = "violet",
}: {
  label: string;
  value: string;
  hint?: string;
  icon?: React.ReactNode;
  accent?: "violet" | "cyan" | "magenta" | "lime";
}) {
  const color = `var(--${accent})`;
  return (
    <div className="gradient-border hover-lift glass relative overflow-hidden rounded-3xl p-5 sm:p-6">
      <div
        className="glow-orb -right-10 -top-12 h-28 w-28"
        style={{ background: color, opacity: 0.28 }}
        aria-hidden="true"
      />
      <div className="relative flex items-start justify-between gap-3">
        <span className="text-[11px] font-semibold tracking-[0.16em] text-muted-foreground">
          {label}
        </span>
        {icon && <span style={{ color }}>{icon}</span>}
      </div>
      <div className="relative mt-4 font-display text-[clamp(1.8rem,3vw,2.4rem)] font-bold leading-none">
        {value}
      </div>
      {hint && <p className="relative mt-2 text-xs text-muted-foreground">{hint}</p>}
    </div>
  );
}
