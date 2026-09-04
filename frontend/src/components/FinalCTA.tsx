import { ArrowRight } from "lucide-react";

export function FinalCTA() {
  return (
    <section className="relative py-20 sm:py-28">
      <div className="mx-auto max-w-5xl px-5 sm:px-8">
        <div className="gradient-border glass relative overflow-hidden rounded-4xl px-6 py-16 text-center sm:px-12">
          <div
            className="glow-orb left-1/2 top-[-30%] h-[380px] w-[520px] -translate-x-1/2"
            style={{ background: "var(--violet)", opacity: 0.32 }}
            aria-hidden="true"
          />
          <div className="relative">
            <h2 className="font-display text-[clamp(2rem,4.5vw,3.4rem)] font-bold leading-tight">
              Make Every <span className="text-gradient">Token</span> Count.
            </h2>
            <p className="mx-auto mt-4 max-w-md text-muted-foreground">
              Intelligent routing for cost-efficient AI.
            </p>
            <a
              href="#optimizer"
              className="group mt-9 inline-flex items-center gap-2 rounded-full px-8 py-4 text-sm font-semibold text-primary-foreground shadow-[var(--shadow-glow)] transition-transform hover:scale-[1.03]"
              style={{ backgroundImage: "var(--gradient-brand)" }}
            >
              Launch Optimizer
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
