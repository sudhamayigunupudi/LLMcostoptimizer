import { Zap } from "lucide-react";
import { TRUST_TAGS } from "@/lib/mock-data";

export function Footer() {
  return (
    <footer className="border-t border-border/70 py-12">
      <div className="mx-auto flex max-w-7xl flex-col items-center gap-6 px-5 text-center sm:px-8 md:flex-row md:justify-between md:text-left">
        <div className="flex items-center gap-2.5">
          <span
            className="flex h-8 w-8 items-center justify-center rounded-lg"
            style={{ backgroundImage: "var(--gradient-brand)" }}
          >
            <Zap className="h-4 w-4 text-primary-foreground" strokeWidth={2.5} />
          </span>
          <span className="font-display text-sm font-bold">LLM Cost Optimizer</span>
        </div>

        <div className="flex flex-wrap justify-center gap-2">
          {TRUST_TAGS.map((t) => (
            <span key={t} className="rounded-full border border-border px-3 py-1.5 text-[10px] tracking-[0.14em] text-muted-foreground">
              {t}
            </span>
          ))}
        </div>

        <p className="text-xs text-muted-foreground">Demo interface · mock data</p>
      </div>
    </footer>
  );
}
