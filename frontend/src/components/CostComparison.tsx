import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { COST_COMPARISON, MODEL_DISTRIBUTION, SAVINGS_TREND } from "@/lib/mock-data";

const tooltipStyle = {
  background: "var(--surface-2)",
  border: "1px solid var(--border)",
  borderRadius: 12,
  fontSize: 12,
  color: "var(--foreground)",
};

function ChartCard({
  title,
  caption,
  children,
}: {
  title: string;
  caption: string;
  children: React.ReactNode;
}) {
  return (
    <div className="gradient-border glass rounded-3xl p-5 sm:p-6">
      <h3 className="font-display text-base font-bold">{title}</h3>
      <p className="mt-1 text-xs text-muted-foreground">{caption}</p>
      <div className="mt-5 h-56">{children}</div>
    </div>
  );
}

export function CostComparison() {
  return (
    <div className="grid gap-5 lg:grid-cols-3">
      <ChartCard title="Cost Comparison" caption="Baseline vs optimized spend per 1,248 requests">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={COST_COMPARISON} margin={{ top: 8, right: 8, left: -18, bottom: 0 }}>
            <defs>
              <linearGradient id="barBaseline" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="var(--magenta)" stopOpacity={0.95} />
                <stop offset="100%" stopColor="var(--magenta)" stopOpacity={0.25} />
              </linearGradient>
              <linearGradient id="barOptimized" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="var(--violet)" stopOpacity={0.95} />
                <stop offset="100%" stopColor="var(--cyan)" stopOpacity={0.4} />
              </linearGradient>
            </defs>
            <XAxis dataKey="label" tick={{ fontSize: 11, fill: "var(--muted-foreground)" }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 11, fill: "var(--muted-foreground)" }} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={tooltipStyle} cursor={{ fill: "color-mix(in oklab, var(--violet) 10%, transparent)" }} formatter={(v: number) => [`$${v}`, "Cost"]} />
            <Bar dataKey="cost" radius={[10, 10, 4, 4]} barSize={62}>
              {COST_COMPARISON.map((d, i) => (
                <Cell key={d.label} fill={i === 0 ? "url(#barBaseline)" : "url(#barOptimized)"} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard title="Model Distribution" caption="Share of requests handled per model tier">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={MODEL_DISTRIBUTION}
              dataKey="value"
              nameKey="name"
              innerRadius={54}
              outerRadius={82}
              paddingAngle={4}
              stroke="none"
            >
              <Cell fill="var(--cyan)" />
              <Cell fill="var(--magenta)" />
            </Pie>
            <Tooltip contentStyle={tooltipStyle} formatter={(v: number, n: string) => [`${v}%`, n]} />
          </PieChart>
        </ResponsiveContainer>
        <div className="mt-1 flex justify-center gap-4 text-xs text-muted-foreground">
          <span className="inline-flex items-center gap-1.5">
            <i className="h-2.5 w-2.5 rounded-full" style={{ background: "var(--cyan)" }} /> Cheap 71%
          </span>
          <span className="inline-flex items-center gap-1.5">
            <i className="h-2.5 w-2.5 rounded-full" style={{ background: "var(--magenta)" }} /> Powerful 29%
          </span>
        </div>
      </ChartCard>

      <ChartCard title="Cost Savings Trend" caption="Cumulative savings as request volume grows">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={SAVINGS_TREND} margin={{ top: 8, right: 8, left: -18, bottom: 0 }}>
            <defs>
              <linearGradient id="savedFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="var(--violet)" stopOpacity={0.6} />
                <stop offset="100%" stopColor="var(--violet)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis dataKey="requests" tick={{ fontSize: 11, fill: "var(--muted-foreground)" }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 11, fill: "var(--muted-foreground)" }} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [`$${v}`, "Saved"]} labelFormatter={(l) => `${l} requests`} />
            <Area type="monotone" dataKey="saved" stroke="var(--violet)" strokeWidth={2.5} fill="url(#savedFill)" />
          </AreaChart>
        </ResponsiveContainer>
      </ChartCard>
    </div>
  );
}
