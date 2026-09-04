import { DatabaseZap, Layers, Recycle } from "lucide-react";
import { CACHE_STATS } from "@/lib/mock-data";
import { MetricCard } from "./MetricCard";
import { SectionHeading } from "./SectionHeading";

export function CacheAnalytics() {
  return (
    <section className="relative py-20 sm:py-28">
      <div
        className="glow-orb left-[-8%] top-[20%] h-[340px] w-[340px]"
        style={{ background: "var(--cyan)", opacity: 0.18 }}
        aria-hidden="true"
      />
      <div className="relative mx-auto max-w-6xl px-5 sm:px-8">
        <SectionHeading
          eyebrow="PROMPT CACHE"
          title="Prompt Intelligence"
          subtitle="Repeated system and context blocks are reused instead of being repeatedly processed."
        />

        <div className="mt-12 grid gap-5 lg:grid-cols-[1fr_1.1fr]">
          <div className="gradient-border glass rounded-3xl p-6 sm:p-8">
            <svg viewBox="0 0 320 180" className="h-48 w-full" fill="none" aria-hidden="true">
              <defs>
                <linearGradient id="cacheEdge" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="var(--cyan)" />
                  <stop offset="100%" stopColor="var(--violet)" />
                </linearGradient>
              </defs>
              {[40, 90, 140].map((y, i) => (
                <g key={y}>
                  <path
                    d={`M40 ${y} H160`}
                    stroke="url(#cacheEdge)"
                    strokeWidth="1.6"
                    className="animate-dash"
                    style={{ animationDelay: `${i * 0.4}s` }}
                    opacity="0.85"
                  />
                  <circle cx="40" cy={y} r="7" fill="color-mix(in oklab, var(--cyan) 30%, transparent)" stroke="var(--cyan)" />
                </g>
              ))}
              <rect x="160" y="52" width="86" height="76" rx="16" fill="color-mix(in oklab, var(--violet) 14%, transparent)" stroke="var(--violet)" />
              <text x="203" y="86" textAnchor="middle" fontSize="11" fill="var(--foreground)" fontFamily="monospace">
                CACHE
              </text>
              <text x="203" y="104" textAnchor="middle" fontSize="13" fill="var(--cyan)" fontFamily="monospace">
                38%
              </text>
              <path d="M246 90 H296" stroke="url(#cacheEdge)" strokeWidth="1.8" className="animate-dash" />
              <circle cx="300" cy="90" r="8" fill="color-mix(in oklab, var(--lime) 25%, transparent)" stroke="var(--lime)" />
            </svg>

            <div className="mt-4 flex flex-wrap gap-3">
              <span
                className="inline-flex items-center gap-2 rounded-full border px-4 py-2 text-xs font-semibold tracking-[0.12em]"
                style={{ borderColor: "color-mix(in oklab, var(--lime) 50%, transparent)", color: "var(--lime)" }}
              >
                <Recycle className="h-3.5 w-3.5" /> CACHE HIT
              </span>
              <span className="inline-flex items-center gap-2 rounded-full border border-border px-4 py-2 text-xs font-semibold tracking-[0.12em] text-muted-foreground">
                <Layers className="h-3.5 w-3.5" /> CACHE MISS
              </span>
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:content-center">
            <MetricCard label="CACHE HIT RATE" value={`${CACHE_STATS.hitRate}%`} accent="cyan" icon={<DatabaseZap className="h-4 w-4" />} />
            <MetricCard label="TOKENS REUSED" value={CACHE_STATS.tokensReused.toLocaleString()} accent="violet" icon={<Recycle className="h-4 w-4" />} />
            <MetricCard
              label="ESTIMATED SAVINGS"
              value={`$${CACHE_STATS.estimatedSavings.toFixed(2)}`}
              accent="lime"
              icon={<Layers className="h-4 w-4" />}
              hint="From cached context alone"
            />
            <div className="gradient-border glass rounded-3xl p-6 text-sm text-muted-foreground">
              Long system prompts, tool schemas and retrieved context are hashed once and reused across
              requests — cutting both tokens and latency.
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
