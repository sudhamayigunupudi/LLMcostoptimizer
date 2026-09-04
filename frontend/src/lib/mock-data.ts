export const EXAMPLE_PROMPTS = [
  "What is the capital of Japan?",
  "Write a Python function...",
  "Analyze a microservices architecture...",
];

export const COST_COMPARISON = [
  { label: "Always Powerful", cost: 18.42 },
  { label: "Optimized Routing", cost: 9.76 },
];

export const MODEL_DISTRIBUTION = [
  { name: "Cheap Model", value: 71 },
  { name: "Powerful Model", value: 29 },
];

export const SAVINGS_TREND = Array.from({ length: 13 }, (_, i) => {
  const requests = i * 100;
  return {
    requests,
    saved: Number((requests * 0.00694 * (1 + i * 0.012)).toFixed(2)),
    baseline: Number((requests * 0.01476).toFixed(2)),
  };
});

export const QUALITY_COMPARISON = [
  { metric: "Cost per 1K requests", powerful: "$18.42", optimized: "$9.76", better: "optimized" as const },
  { metric: "Quality score", powerful: "95.1%", optimized: "94.2%", better: "tie" as const },
  { metric: "Median latency", powerful: "680 ms", optimized: "420 ms", better: "optimized" as const },
  { metric: "Escalation to powerful", powerful: "100%", optimized: "29%", better: "optimized" as const },
];

export const CACHE_STATS = {
  hitRate: 38,
  tokensReused: 24850,
  estimatedSavings: 3.21,
};

export const HOW_IT_WORKS = [
  { step: "01", title: "UNDERSTAND", body: "Analyze request difficulty." },
  { step: "02", title: "ROUTE", body: "Choose the cheapest capable model." },
  { step: "03", title: "CACHE", body: "Reuse repeated context." },
  { step: "04", title: "MEASURE", body: "Track cost, quality and performance." },
];

export const TRUST_TAGS = ["AI MODEL ROUTING", "PROMPT CACHING", "COST ANALYTICS", "QUALITY AWARE"];
