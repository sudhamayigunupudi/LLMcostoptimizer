/**
 * Isolated API layer.
 *
 * Everything here currently returns MOCK data. When the FastAPI backend is
 * ready, replace the bodies of these functions with `fetch(`${API_BASE}/...`)`
 * calls — the component layer does not need to change.
 */

export const API_BASE = import.meta.env["VITE_API_BASE_URL"] ?? "/api";

export type Difficulty = "Easy" | "Medium" | "Hard";
export type ModelTier = "cheap" | "powerful";

export interface OptimizationResult {
  prompt: string;
  difficulty: Difficulty;
  confidence: number;
  modelTier: ModelTier;
  modelName: string;
  routingDecision: string;
  cacheHit: boolean;
  cost: number;
  baselineCost: number;
  tokens: number;
  latencyMs: number;
}

export interface PerformanceSummary {
  totalRequests: number;
  baselineCost: number;
  optimizedCost: number;
  costSaved: number;
  savingsPct: number;
  qualityScore: number;
  cacheHitRate: number;
}

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

function classify(prompt: string): { difficulty: Difficulty; confidence: number } {
  const text = prompt.trim().toLowerCase();
  const words = text.split(/\s+/).filter(Boolean).length;
  const hardHints = ["architect", "microservice", "distributed", "trade-off", "prove", "optimize", "design a", "scal"];
  const mediumHints = ["write", "function", "code", "refactor", "explain", "summarize", "sql"];

  if (hardHints.some((h) => text.includes(h)) || words > 45) {
    return { difficulty: "Hard", confidence: 0.91 };
  }
  if (mediumHints.some((h) => text.includes(h)) || words > 14) {
    return { difficulty: "Medium", confidence: 0.88 };
  }
  return { difficulty: "Easy", confidence: 0.94 };
}

/** MOCK — replace with POST `${API_BASE}/optimize` */
export async function optimizeRequest(prompt: string): Promise<OptimizationResult> {
  await delay(1100);
  const { difficulty, confidence } = classify(prompt);
  const tier: ModelTier = difficulty === "Hard" ? "powerful" : "cheap";
  const tokens = Math.max(96, Math.round(prompt.length * 1.6) + (difficulty === "Hard" ? 640 : 180));
  const cacheHit = prompt.trim().length % 3 !== 0;
  const unit = tier === "cheap" ? 0.0000032 : 0.000029;
  const cost = Number((tokens * unit * (cacheHit ? 0.62 : 1)).toFixed(4));

  return {
    prompt,
    difficulty,
    confidence,
    modelTier: tier,
    modelName: tier === "cheap" ? "Cheap Model" : "Powerful Model",
    routingDecision:
      tier === "cheap"
        ? "Low-complexity request routed to the cost-efficient model."
        : "High-complexity reasoning detected — routed to the powerful model.",
    cacheHit,
    cost: cost || 0.0008,
    baselineCost: Number((tokens * 0.000029).toFixed(4)),
    tokens,
    latencyMs: tier === "cheap" ? 420 : 1180,
  };
}

/** MOCK — replace with GET `${API_BASE}/performance` */
export async function getPerformanceSummary(): Promise<PerformanceSummary> {
  await delay(200);
  return {
    totalRequests: 1248,
    baselineCost: 18.42,
    optimizedCost: 9.76,
    costSaved: 8.66,
    savingsPct: 47.0,
    qualityScore: 94.2,
    cacheHitRate: 38,
  };
}

export interface CacheAnalytics {
  cacheStatus: "HIT" | "MISS";
  cacheHitRate: number;
  tokensReused: number;
  estimatedSavings: number;
}

/** MOCK — replace with GET `${API_BASE}/cache-analytics` */
export async function getCacheAnalytics(): Promise<CacheAnalytics> {
  await delay(200);
  return { cacheStatus: "HIT", cacheHitRate: 38, tokensReused: 24850, estimatedSavings: 3.21 };
}

/** Alias kept for the documented service-layer name. */
export const getPerformanceMetrics = getPerformanceSummary;
