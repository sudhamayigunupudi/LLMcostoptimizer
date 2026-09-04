import { Check, Minus } from "lucide-react";
import { QUALITY_COMPARISON } from "@/lib/mock-data";
import { SectionHeading } from "./SectionHeading";

function Bar({ label, pct, color }: { label: string; pct: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-muted-foreground">
        <span>{label}</span>
        <span className="font-mono">{pct}%</span>
      </div>
      <div className="mt-2 h-2.5 overflow-hidden rounded-full bg-secondary">
        <div className="h-full rounded-full transition-all duration-700" style={{ width: `${pct}%`, background: color }} />
      </div>
    </div>
  );
}

export function QualityComparison() {
  return (
    <section className="relative py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <SectionHeading
          eyebrow="QUALITY VS COST"
          title={
            <>
              Lower Cost. <span className="text-gradient">Same Intelligence.</span>
            </>
          }
          subtitle="Routing only downgrades a request when the cheaper model can answer it just as well."
        />

        <div className="mt-12 grid gap-5 lg:grid-cols-2">
          <div className="glass rounded-3xl border-[color-mix(in_oklab,var(--magenta)_35%,transparent)] p-6 sm:p-7">
            <span className="text-[11px] font-semibold tracking-[0.18em] text-muted-foreground">
              ALWAYS POWERFUL MODEL
            </span>
            <div className="mt-2 font-display text-3xl font-bold">$18.42</div>
            <div className="mt-6 space-y-4">
              <Bar label="Cost" pct={100} color="var(--magenta)" />
              <Bar label="Quality" pct={95} color="color-mix(in oklab, var(--magenta) 60%, var(--foreground))" />
              <Bar label="Latency" pct={100} color="color-mix(in oklab, var(--magenta) 45%, transparent)" />
            </div>
          </div>

          <div className="gradient-border glass rounded-3xl p-6 sm:p-7" style={{ boxShadow: "var(--shadow-glow)" }}>
            <span className="text-[11px] font-semibold tracking-[0.18em] text-accent">
              OPTIMIZED ROUTING
            </span>
            <div className="mt-2 font-display text-3xl font-bold text-gradient">$9.76</div>
            <div className="mt-6 space-y-4">
              <Bar label="Cost" pct={53} color="var(--violet)" />
              <Bar label="Quality" pct={94} color="var(--lime)" />
              <Bar label="Latency" pct={62} color="var(--cyan)" />
            </div>
          </div>
        </div>

        <div className="glass mt-6 overflow-hidden rounded-3xl">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-border text-[11px] tracking-[0.14em] text-muted-foreground">
                <th className="px-5 py-4 font-semibold">METRIC</th>
                <th className="px-5 py-4 font-semibold">ALWAYS POWERFUL</th>
                <th className="px-5 py-4 font-semibold">OPTIMIZED</th>
              </tr>
            </thead>
            <tbody>
              {QUALITY_COMPARISON.map((row) => (
                <tr key={row.metric} className="border-b border-border/60 last:border-0">
                  <td className="px-5 py-4 text-muted-foreground">{row.metric}</td>
                  <td className="px-5 py-4 font-mono">{row.powerful}</td>
                  <td className="px-5 py-4 font-mono font-semibold">
                    <span className="inline-flex items-center gap-2">
                      {row.optimized}
                      {row.better === "optimized" ? (
                        <Check className="h-4 w-4" style={{ color: "var(--lime)" }} />
                      ) : (
                        <Minus className="h-4 w-4 text-muted-foreground" />
                      )}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <p className="mt-6 text-center text-sm text-muted-foreground">
          Optimize spend without silently sacrificing intelligence.{" "}
          <span className="font-mono text-xs">All values shown are demo data.</span>
        </p>
      </div>
    </section>
  );
}
