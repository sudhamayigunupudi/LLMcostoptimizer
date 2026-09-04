import { Clock, Coins, Cpu, DatabaseZap, Gauge, Hash, Route, Target } from "lucide-react";
import type { OptimizationResult as Result } from "@/services/optimizerApi";

const DIFFICULTY_TONE: Record<string, string> = {
  Easy: "var(--lime)",
  Medium: "var(--cyan)",
  Hard: "var(--magenta)",
};

function Stat({
  icon,
  label,
  value,
  color,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  color?: string;
}) {
  return (
    <div className="rounded-2xl border border-border/80 bg-background/40 p-4">
      <div className="flex items-center gap-2 text-[10px] font-semibold tracking-[0.16em] text-muted-foreground">
        <span style={{ color: color ?? "var(--violet)" }}>{icon}</span>
        {label}
      </div>
      <div className="mt-2 font-display text-xl font-bold" style={color ? { color } : undefined}>
        {value}
      </div>
    </div>
  );
}

export function OptimizationResult({ result }: { result: Result }) {
  const tone = DIFFICULTY_TONE[result.difficulty];
  const savedPct = Math.max(
    0,
    Math.round(((result.baselineCost - result.cost) / result.baselineCost) * 100),
  );

  return (
    <div className="gradient-border glass animate-rise mx-auto max-w-4xl rounded-4xl p-5 sm:p-7">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <span className="text-[11px] font-semibold tracking-[0.2em] text-muted-foreground">
          REQUEST ANALYSIS
        </span>
        <span
          className="rounded-full px-3 py-1.5 text-[11px] font-bold tracking-[0.14em] text-primary-foreground"
          style={{ backgroundImage: "var(--gradient-heat)" }}
        >
          {savedPct}% CHEAPER THAN BASELINE
        </span>
      </div>

      <div className="mt-5 grid gap-4 md:grid-cols-[1.1fr_1fr]">
        <div className="rounded-3xl border p-5" style={{ borderColor: `color-mix(in oklab, ${tone} 45%, transparent)`, background: `color-mix(in oklab, ${tone} 8%, transparent)` }}>
          <div className="flex items-center justify-between">
            <div>
              <div className="text-[10px] font-semibold tracking-[0.18em] text-muted-foreground">
                DIFFICULTY
              </div>
              <div className="mt-1 font-display text-3xl font-bold" style={{ color: tone }}>
                {result.difficulty}
              </div>
            </div>
            <div className="text-right">
              <div className="text-[10px] font-semibold tracking-[0.18em] text-muted-foreground">
                CONFIDENCE
              </div>
              <div className="mt-1 font-display text-3xl font-bold">
                {Math.round(result.confidence * 100)}%
              </div>
            </div>
          </div>
          <div className="mt-4 h-2 overflow-hidden rounded-full bg-secondary">
            <div
              className="h-full rounded-full transition-all duration-700"
              style={{ width: `${result.confidence * 100}%`, backgroundImage: "var(--gradient-brand)" }}
            />
          </div>
        </div>

        <div
          className="rounded-3xl border p-5"
          style={{
            borderColor:
              result.modelTier === "cheap"
                ? "color-mix(in oklab, var(--cyan) 50%, transparent)"
                : "color-mix(in oklab, var(--magenta) 50%, transparent)",
            background:
              result.modelTier === "cheap"
                ? "color-mix(in oklab, var(--cyan) 9%, transparent)"
                : "color-mix(in oklab, var(--magenta) 9%, transparent)",
          }}
        >
          <div className="text-[10px] font-semibold tracking-[0.18em] text-muted-foreground">
            SELECTED MODEL
          </div>
          <div className="mt-1 flex items-center gap-2 font-display text-2xl font-bold">
            <Cpu className="h-5 w-5" style={{ color: result.modelTier === "cheap" ? "var(--cyan)" : "var(--magenta)" }} />
            {result.modelName}
          </div>
          <div className="mt-3 flex items-start gap-2 text-xs text-muted-foreground">
            <Route className="mt-0.5 h-3.5 w-3.5 shrink-0 text-accent" />
            <span>{result.routingDecision}</span>
          </div>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Stat
          icon={<DatabaseZap className="h-3.5 w-3.5" />}
          label="CACHE STATUS"
          value={result.cacheHit ? "CACHE HIT" : "CACHE MISS"}
          color={result.cacheHit ? "var(--lime)" : "var(--muted-foreground)"}
        />
        <Stat icon={<Coins className="h-3.5 w-3.5" />} label="COST" value={`$${result.cost.toFixed(4)}`} />
        <Stat icon={<Hash className="h-3.5 w-3.5" />} label="TOKENS" value={String(result.tokens)} color="var(--cyan)" />
        <Stat icon={<Clock className="h-3.5 w-3.5" />} label="LATENCY" value={`${result.latencyMs} ms`} color="var(--magenta)" />
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-4 text-xs text-muted-foreground">
        <span className="inline-flex items-center gap-1.5">
          <Target className="h-3.5 w-3.5 text-accent" /> Baseline cost ${result.baselineCost.toFixed(4)}
        </span>
        <span className="inline-flex items-center gap-1.5">
          <Gauge className="h-3.5 w-3.5 text-accent" /> Quality guardrail passed
        </span>
      </div>
    </div>
  );
}
