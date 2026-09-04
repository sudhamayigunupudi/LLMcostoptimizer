import { useState } from "react";
import { Loader2, Sparkles, Wand2 } from "lucide-react";
import { EXAMPLE_PROMPTS } from "@/lib/mock-data";
import { SectionHeading } from "./SectionHeading";

export function Optimizer({
  onOptimize,
  loading,
}: {
  onOptimize: (prompt: string) => void;
  loading: boolean;
}) {
  const [prompt, setPrompt] = useState("");

  return (
    <section id="optimizer" className="relative py-20 sm:py-28">
      <div
        className="glow-orb left-1/2 top-0 h-[320px] w-[520px] -translate-x-1/2"
        style={{ background: "var(--violet)", opacity: 0.22 }}
        aria-hidden="true"
      />
      <div className="relative mx-auto max-w-4xl px-5 sm:px-8">
        <SectionHeading
          eyebrow="LIVE DEMO"
          title="Optimize a Request"
          subtitle="See how our routing engine chooses the most cost-efficient model."
        />

        <div className="gradient-border glass mt-10 rounded-4xl p-5 sm:p-7">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Ask anything..."
            rows={5}
            className="w-full resize-none rounded-2xl border border-input bg-background/60 p-4 text-base outline-none transition-shadow placeholder:text-muted-foreground focus:border-ring focus:shadow-[0_0_0_4px_color-mix(in_oklab,var(--ring)_18%,transparent)]"
          />

          <div className="mt-4 flex flex-wrap gap-2">
            {EXAMPLE_PROMPTS.map((p) => (
              <button
                key={p}
                type="button"
                onClick={() => setPrompt(p)}
                className="rounded-full border border-border bg-surface/60 px-3.5 py-2 text-xs text-muted-foreground transition-all hover:-translate-y-0.5 hover:border-accent/60 hover:text-foreground"
              >
                {p}
              </button>
            ))}
          </div>

          <div className="mt-6 flex flex-wrap items-center justify-between gap-4">
            <span className="inline-flex items-center gap-1.5 text-xs text-muted-foreground">
              <Sparkles className="h-3.5 w-3.5 text-accent" />
              Demo data — no live model is called
            </span>
            <button
              type="button"
              disabled={loading || !prompt.trim()}
              onClick={() => onOptimize(prompt.trim())}
              className="inline-flex items-center gap-2 rounded-full px-7 py-3.5 text-sm font-semibold text-primary-foreground shadow-[var(--shadow-glow)] transition-transform hover:scale-[1.03] disabled:cursor-not-allowed disabled:opacity-45 disabled:hover:scale-100"
              style={{ backgroundImage: "var(--gradient-brand)" }}
            >
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Wand2 className="h-4 w-4" />}
              {loading ? "Routing..." : "Optimize Request"}
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
