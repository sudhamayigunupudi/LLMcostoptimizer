import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { Navbar } from "@/components/Navbar";
import { Hero } from "@/components/Hero";
import { Optimizer } from "@/components/Optimizer";
import { OptimizationResult } from "@/components/OptimizationResult";
import { RoutingVisualizer } from "@/components/RoutingVisualizer";
import { PerformanceDashboard } from "@/components/PerformanceDashboard";
import { QualityComparison } from "@/components/QualityComparison";
import { CacheAnalytics } from "@/components/CacheAnalytics";
import { HowItWorks } from "@/components/HowItWorks";
import { FinalCTA } from "@/components/FinalCTA";
import { Footer } from "@/components/Footer";
import {
  getPerformanceSummary,
  optimizeRequest,
  type OptimizationResult as Result,
  type PerformanceSummary,
} from "@/services/optimizerApi";

const TITLE = "LLM Cost Optimizer — Route Intelligence, Lower AI Costs";
const DESCRIPTION =
  "Automatically choose the right LLM for every request — cutting AI spend by 47% with difficulty-aware routing, prompt caching and cost analytics.";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: TITLE },
      { name: "description", content: DESCRIPTION },
      { property: "og:title", content: TITLE },
      { property: "og:description", content: DESCRIPTION },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

function Index() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Result | null>(null);
  const [summary, setSummary] = useState<PerformanceSummary | null>(null);
  const resultRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getPerformanceSummary().then(setSummary).catch(() => setSummary(null));
  }, []);

  const handleOptimize = async (prompt: string) => {
    setLoading(true);
    try {
      const res = await optimizeRequest(prompt);
      setResult(res);
      requestAnimationFrame(() =>
        resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }),
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen overflow-x-hidden bg-background">
      <Navbar />
      <main>
        <Hero />
        <Optimizer onOptimize={handleOptimize} loading={loading} />
        <div ref={resultRef} className="scroll-mt-28 px-5 sm:px-8">
          {result && <OptimizationResult result={result} />}
        </div>
        <RoutingVisualizer result={result} />
        {summary && <PerformanceDashboard summary={summary} />}
        <QualityComparison />
        <CacheAnalytics />
        <HowItWorks />
        <FinalCTA />
      </main>
      <Footer />
    </div>
  );
}
