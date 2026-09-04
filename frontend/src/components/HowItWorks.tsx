import { BarChart3, BrainCircuit, DatabaseZap, GitBranch } from "lucide-react";
import { HOW_IT_WORKS } from "@/lib/mock-data";
import { SectionHeading } from "./SectionHeading";

const ICONS = [BrainCircuit, GitBranch, DatabaseZap, BarChart3];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="relative py-20 sm:py-28">
      <div className="mx-auto max-w-7xl px-5 sm:px-8">
        <SectionHeading eyebrow="PIPELINE" title="How It Works" />

        <div className="relative mt-14">
          <div
            className="absolute left-0 right-0 top-9 hidden h-px lg:block"
            style={{ backgroundImage: "var(--gradient-brand)", opacity: 0.4 }}
            aria-hidden="true"
          />
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {HOW_IT_WORKS.map((s, i) => {
              const Icon = ICONS[i] ?? BrainCircuit;
              return (
                <div key={s.step} className="relative">
                  <div
                    className="relative z-10 flex h-[72px] w-[72px] items-center justify-center rounded-2xl border border-border bg-background"
                    style={{ boxShadow: "0 0 40px -14px var(--violet)" }}
                  >
                    <Icon className="h-6 w-6" style={{ color: i % 2 ? "var(--cyan)" : "var(--violet)" }} />
                  </div>
                  <div className="gradient-border hover-lift glass mt-5 rounded-3xl p-6">
                    <span className="font-mono text-sm text-muted-foreground">{s.step}</span>
                    <h3 className="mt-2 font-display text-lg font-bold tracking-[0.06em]">{s.title}</h3>
                    <p className="mt-2 text-sm text-muted-foreground">{s.body}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
