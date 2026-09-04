import { BrainCircuit, Cpu, GitBranch, User } from "lucide-react";
import type { OptimizationResult } from "@/services/optimizerApi";
import { SectionHeading } from "./SectionHeading";

function Node({
  icon,
  title,
  sub,
  active,
  color = "var(--violet)",
}: {
  icon: React.ReactNode;
  title: string;
  sub?: string;
  active?: boolean;
  color?: string;
}) {
  return (
    <div
      className="flex w-full flex-col items-center gap-1.5 rounded-2xl border px-4 py-4 text-center transition-all duration-500"
      style={{
        borderColor: active ? `color-mix(in oklab, ${color} 70%, transparent)` : "var(--border)",
        background: active ? `color-mix(in oklab, ${color} 12%, transparent)` : "color-mix(in oklab, var(--surface) 60%, transparent)",
        boxShadow: active ? `0 0 40px -8px color-mix(in oklab, ${color} 65%, transparent)` : "none",
      }}
    >
      <span style={{ color: active ? color : "var(--muted-foreground)" }}>{icon}</span>
      <span className="font-display text-xs font-bold tracking-[0.14em]">{title}</span>
      {sub && <span className="text-[10px] text-muted-foreground">{sub}</span>}
    </div>
  );
}

export function RoutingVisualizer({ result }: { result: OptimizationResult | null }) {
  const cheap = result?.modelTier === "cheap";
  const powerful = result?.modelTier === "powerful";

  return (
    <section className="relative py-20 sm:py-24">
      <div className="mx-auto max-w-4xl px-5 sm:px-8">
        <SectionHeading eyebrow="ROUTING VISUALIZER" title="Watch the decision happen" />

        <div className="gradient-border glass mt-10 rounded-4xl p-6 sm:p-9">
          <div className="mx-auto max-w-md">
            <Node icon={<User className="h-5 w-5" />} title="USER REQUEST" active={!!result} />
            <svg viewBox="0 0 200 40" className="h-9 w-full" fill="none" aria-hidden="true">
              <path d="M100 0 V40" stroke="var(--violet)" strokeWidth="1.8" className={result ? "animate-dash" : ""} opacity={result ? 0.9 : 0.3} />
            </svg>
            <Node icon={<BrainCircuit className="h-5 w-5" />} title="DIFFICULTY CLASSIFIER" sub={result ? `${result.difficulty} · ${Math.round(result.confidence * 100)}%` : "idle"} active={!!result} />
            <svg viewBox="0 0 200 40" className="h-9 w-full" fill="none" aria-hidden="true">
              <path d="M100 0 V40" stroke="var(--violet)" strokeWidth="1.8" className={result ? "animate-dash" : ""} opacity={result ? 0.9 : 0.3} />
            </svg>
            <Node icon={<GitBranch className="h-5 w-5" />} title="ROUTING ENGINE" active={!!result} />
            <svg viewBox="0 0 200 48" className="h-11 w-full" fill="none" aria-hidden="true">
              <path
                d="M100 0 V14 Q100 24 84 24 H34 Q20 24 20 36 V48"
                stroke="var(--cyan)"
                strokeWidth={cheap ? 2.4 : 1.4}
                className={cheap ? "animate-dash" : ""}
                opacity={cheap ? 1 : 0.25}
              />
              <path
                d="M100 0 V14 Q100 24 116 24 H166 Q180 24 180 36 V48"
                stroke="var(--magenta)"
                strokeWidth={powerful ? 2.4 : 1.4}
                className={powerful ? "animate-dash" : ""}
                opacity={powerful ? 1 : 0.25}
              />
            </svg>
            <div className="grid grid-cols-2 gap-4">
              <Node icon={<Cpu className="h-5 w-5" />} title="CHEAP MODEL" active={cheap} color="var(--cyan)" />
              <Node icon={<Cpu className="h-5 w-5" />} title="POWERFUL MODEL" active={powerful} color="var(--magenta)" />
            </div>
          </div>

          <p className="mt-8 text-center text-sm text-muted-foreground">
            {result ? (
              <>
                Your request was classified as{" "}
                <strong className="text-foreground">{result.difficulty.toUpperCase()}</strong>, so the
                optimizer selected the{" "}
                {cheap ? "lower-cost model." : "powerful model to protect answer quality."}
              </>
            ) : (
              "Run the optimizer above to light up the selected path."
            )}
          </p>
        </div>
      </div>
    </section>
  );
}
