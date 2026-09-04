import { Activity, Coins, DatabaseZap, Gauge, PiggyBank, Sparkles, TrendingDown } from "lucide-react";
import { MetricCard } from "./MetricCard";
import { SectionHeading } from "./SectionHeading";
import { CostComparison } from "./CostComparison";
import type { PerformanceSummary } from "@/services/optimizerApi";

export function PerformanceDashboard({ summary }: { summary: PerformanceSummary }) {
  return (
    <section id="performance" className="relative py-20 sm:py-28">
      <div
        className="glow-orb right-[-6%] top-[10%] h-[360px] w-[360px]"
        style={{ background: "var(--magenta)", opacity: 0.2 }}
        aria-hidden="true"
      />
      <div className="relative mx-auto max-w-7xl px-5 sm:px-8">
        <SectionHeading
          eyebrow="ANALYTICS"
          title="Optimization Performance"
          subtitle="Demo data from a simulated 1,248-request workload."
        />

        <div className="mt-6 flex justify-center">
          <span
            className="rounded-full border px-4 py-1.5 font-mono text-[11px] font-semibold tracking-[0.18em]"
            style={{
              borderColor: "color-mix(in oklab, var(--cyan) 45%, transparent)",
              color: "var(--cyan)",
            }}
          >
            DEMO DATA
          </span>
        </div>

        <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <MetricCard label="TOTAL REQUESTS" value={summary.totalRequests.toLocaleString()} icon={<Activity className="h-4 w-4" />} hint="Demo workload" />
          <MetricCard label="BASELINE COST" value={`$${summary.baselineCost.toFixed(2)}`} icon={<Coins className="h-4 w-4" />} accent="magenta" hint="Always powerful model" />
          <MetricCard label="OPTIMIZED COST" value={`$${summary.optimizedCost.toFixed(2)}`} icon={<TrendingDown className="h-4 w-4" />} accent="cyan" hint="With smart routing" />
          <MetricCard label="COST SAVED" value={`$${summary.costSaved.toFixed(2)}`} icon={<PiggyBank className="h-4 w-4" />} accent="lime" hint="Same workload" />
          <MetricCard label="SAVINGS" value={`${summary.savingsPct.toFixed(1)}%`} icon={<Sparkles className="h-4 w-4" />} hint="Cost reduction" />
          <MetricCard label="QUALITY SCORE" value={`${summary.qualityScore}%`} icon={<Gauge className="h-4 w-4" />} accent="lime" hint="Within 1pt of baseline" />
          <MetricCard label="CACHE HIT RATE" value={`${summary.cacheHitRate}%`} icon={<DatabaseZap className="h-4 w-4" />} accent="cyan" hint="Reused context blocks" />
          <MetricCard label="AVG LATENCY" value="420 ms" icon={<Activity className="h-4 w-4" />} accent="magenta" hint="38% faster than baseline" />
        </div>

        <div className="mt-6">
          <CostComparison />
        </div>
      </div>
    </section>
  );
}
