import { ArrowRight, BrainCircuit, Cpu, GitBranch, Sparkles, User } from "lucide-react";
import { TRUST_TAGS } from "@/lib/mock-data";

function FlowNode({
  icon,
  label,
  sub,
  tone = "base",
}: {
  icon: React.ReactNode;
  label: string;
  sub?: string;
  tone?: "base" | "cheap" | "powerful";
}) {
  const toneStyle =
    tone === "cheap"
      ? "border-[color-mix(in_oklab,var(--cyan)_50%,transparent)] bg-[color-mix(in_oklab,var(--cyan)_10%,transparent)]"
      : tone === "powerful"
        ? "border-[color-mix(in_oklab,var(--magenta)_45%,transparent)] bg-[color-mix(in_oklab,var(--magenta)_10%,transparent)]"
        : "border-border bg-surface/70";
  return (
    <div
      className={`flex w-full flex-col items-center gap-1.5 rounded-2xl border px-4 py-3.5 text-center backdrop-blur-md ${toneStyle}`}
    >
      <span className="text-accent">{icon}</span>
      <span className="font-display text-[11px] font-bold tracking-[0.16em] sm:text-xs">{label}</span>
      {sub && <span className="text-[10px] tracking-wide text-muted-foreground">{sub}</span>}
    </div>
  );
}

function Connector({ split = false }: { split?: boolean }) {
  return (
    <svg viewBox="0 0 200 48" className="h-10 w-full" fill="none" aria-hidden="true">
      {split ? (
        <>
          <path d="M100 0 V14 Q100 24 84 24 H34 Q20 24 20 36 V48" stroke="var(--cyan)" strokeWidth="1.6" className="animate-dash" opacity="0.8" />
          <path d="M100 0 V14 Q100 24 116 24 H166 Q180 24 180 36 V48" stroke="var(--magenta)" strokeWidth="1.6" className="animate-dash" opacity="0.8" />
        </>
      ) : (
        <path d="M100 0 V48" stroke="var(--violet)" strokeWidth="1.8" className="animate-dash" opacity="0.85" />
      )}
    </svg>
  );
}

export function Hero() {
  return (
    <section id="overview" className="relative overflow-hidden pt-28 pb-16 sm:pt-36 sm:pb-24">
      <div className="grid-bg absolute inset-0" aria-hidden="true" />
      <div
        className="glow-orb animate-float-slow left-[-8%] top-[-6%] h-[420px] w-[420px]"
        style={{ background: "var(--violet)" }}
        aria-hidden="true"
      />
      <div
        className="glow-orb animate-float-slow right-[-10%] top-[18%] h-[380px] w-[380px]"
        style={{ background: "var(--cyan)", animationDelay: "3s" }}
        aria-hidden="true"
      />

      <div className="relative mx-auto grid max-w-7xl items-center gap-14 px-5 sm:px-8 lg:grid-cols-[1.05fr_0.95fr]">
        <div className="animate-rise">
          <span className="inline-flex items-center gap-2 rounded-full border border-border bg-surface/60 px-3.5 py-1.5 text-[11px] font-semibold tracking-[0.18em] text-muted-foreground backdrop-blur">
            <Sparkles className="h-3.5 w-3.5 text-accent" />
            COST-AWARE LLM ROUTING
          </span>

          <h1 className="mt-6 font-display text-[clamp(2.6rem,6.4vw,4.6rem)] font-bold leading-[0.98]">
            Route Intelligence.
            <br />
            <span className="text-gradient">Lower AI Costs.</span>
          </h1>

          <p className="mt-6 max-w-xl text-base leading-relaxed text-muted-foreground sm:text-lg">
            Automatically choose the right LLM for every request — reducing cost without sacrificing
            quality.
          </p>

          <div className="mt-9 flex flex-wrap gap-3">
            <a
              href="#optimizer"
              className="group inline-flex items-center gap-2 rounded-full px-7 py-3.5 text-sm font-semibold text-primary-foreground shadow-[var(--shadow-glow)] transition-transform hover:scale-[1.03]"
              style={{ backgroundImage: "var(--gradient-brand)" }}
            >
              Try the Optimizer
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
            </a>
            <a
              href="#performance"
              className="inline-flex items-center rounded-full border border-border bg-surface/60 px-7 py-3.5 text-sm font-semibold backdrop-blur transition-colors hover:border-accent/60 hover:bg-surface"
            >
              View Performance
            </a>
          </div>

          <div className="mt-10 flex flex-wrap gap-2.5">
            {TRUST_TAGS.map((t) => (
              <span
                key={t}
                className="rounded-full border border-border/80 px-3 py-1.5 text-[10px] font-semibold tracking-[0.16em] text-muted-foreground"
              >
                {t}
              </span>
            ))}
          </div>
        </div>

        <div className="gradient-border glass animate-rise rounded-4xl p-6 sm:p-8" style={{ animationDelay: "120ms" }}>
          <div className="mx-auto max-w-sm">
            <FlowNode icon={<User className="h-4.5 w-4.5" />} label="USER REQUEST" />
            <Connector />
            <FlowNode icon={<BrainCircuit className="h-4.5 w-4.5" />} label="INTELLIGENCE" sub="difficulty classifier" />
            <Connector />
            <FlowNode icon={<GitBranch className="h-4.5 w-4.5" />} label="SMART ROUTING" />
            <Connector split />
            <div className="grid grid-cols-2 gap-3">
              <FlowNode icon={<Cpu className="h-4.5 w-4.5" />} label="CHEAP" sub="MODEL" tone="cheap" />
              <FlowNode icon={<Cpu className="h-4.5 w-4.5" />} label="POWERFUL" sub="MODEL" tone="powerful" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
