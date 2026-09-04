# SmartRoute AI

Build ONLY the frontend UI for a premium AI SaaS product called:

"LLM Cost Optimizer"

IMPORTANT:

- FRONTEND ONLY.

- Do not build or modify any backend.

- Do not create databases.

- Do not create authentication.

- Do not implement real LLM/API logic.

- Use realistic mock data and placeholder API functions for now.

- The frontend will later connect to an existing FastAPI backend.

DESIGN DIRECTION

Create a visually impressive, professional, modern AI product interface suitable for an IEEE-level hackathon demonstration.

The design should feel:

- premium

- futuristic

- energetic

- intelligent

- polished

- technically sophisticated

- memorable at first glance

Use vibrant colors, but keep the interface professional.

Take inspiration from the QUALITY and visual polish of modern curated SaaS/product websites such as One Page Love, but DO NOT copy its layout, branding, components, or visual design.

Create our own distinctive visual identity.

COLOR SYSTEM

Use a sophisticated vibrant palette such as:

- deep navy / near-black base

- electric purple

- vivid violet

- cyan

- blue

- subtle pink/magenta accents

- white/light text

Use gradients carefully for:

- hero highlights

- important buttons

- metric cards

- selected states

- charts

- subtle background glows

Avoid making the entire interface rainbow-colored.

Use strong contrast and plenty of whitespace.

VISUAL STYLE

Use:

- large bold typography

- clean modern sans-serif font

- rounded cards

- subtle glassmorphism where appropriate

- soft shadows

- gradient borders

- subtle background glow/orbs

- elegant hover effects

- smooth transitions

- tasteful micro-interactions

- modern charts

- clean iconography

Do NOT make it look like a generic Bootstrap dashboard.

Do NOT make it look like a basic student project.

It should look like a real AI startup product.

==================================================

PAGE STRUCTURE

==================================================

1. HERO / LANDING SECTION

Create a striking hero section.

Headline:

"Route Intelligence.

Lower AI Costs."

Supporting text:

"Automatically choose the right LLM for every request — reducing cost without sacrificing quality."

Include a primary CTA:

"Try the Optimizer →"

Include a secondary CTA:

"View Performance"

Add a visually interesting animated representation of:

USER REQUEST

      ↓

INTELLIGENCE

      ↓

SMART ROUTING

   ↙        ↘

CHEAP      POWERFUL

 MODEL       MODEL

Make this visual distinctive and polished.

Add small trust/technology indicators such as:

"AI MODEL ROUTING"

"PROMPT CACHING"

"COST ANALYTICS"

"QUALITY AWARE"

==================================================

2. LIVE OPTIMIZER SECTION

==================================================

Create the main interactive application area.

Title:

"Optimize a Request"

Subtitle:

"See how our routing engine chooses the most cost-efficient model."

Large prompt textarea:

"Ask anything..."

Include example prompt chips:

"What is the capital of Japan?"

"Write a Python function..."

"Analyze a microservices architecture..."

Primary button:

"Optimize Request"

When clicked using mock data, display a polished result.

==================================================

3. REQUEST ANALYSIS RESULT

==================================================

Show a beautiful result card.

Display:

DIFFICULTY

Easy / Medium / Hard

CONFIDENCE

94%

SELECTED MODEL

Cheap Model

ROUTING DECISION

"Low-complexity request routed to the cost-efficient model."

CACHE STATUS

CACHE HIT / CACHE MISS

COST

$0.0008

TOKENS

245

LATENCY

420 ms

Use visual badges and icons.

Make the selected model tier visually obvious.

==================================================

4. ROUTING VISUALIZER

==================================================

Create an interactive visual pipeline:

User Request

      ↓

Difficulty Classifier

      ↓

Routing Engine

   ↙        ↘

CHEAP      POWERFUL

MODEL        MODEL

The selected path should glow/highlight after optimization.

Include a small explanation:

"Your request was classified as EASY, so the optimizer selected the lower-cost model."

==================================================

5. PERFORMANCE DASHBOARD

==================================================

Create a premium analytics section titled:

"Optimization Performance"

Show large metric cards:

TOTAL REQUESTS

1,248

BASELINE COST

$18.42

OPTIMIZED COST

$9.76

COST SAVED

$8.66

SAVINGS

47.0%

QUALITY SCORE

94.2%

CACHE HIT RATE

38%

Use mock data clearly as demo data.

Create charts:

A. Cost Comparison

Bar chart:

Always Powerful

vs

Optimized Routing

B. Model Distribution

Donut chart:

Cheap Model

Powerful Model

C. Cost Savings Trend

Line/area chart showing savings over requests.

Charts should look polished and presentation-ready.

==================================================

6. QUALITY VS COST

==================================================

Create a section titled:

"Lower Cost. Same Intelligence."

Visually compare:

Always Powerful Model

vs

Optimized Routing

Metrics:

Cost

Quality

Latency

Use a clean comparison visualization.

Important:

The design must communicate that the optimizer is NOT simply saving money by producing worse answers.

==================================================

7. PROMPT CACHE SECTION

==================================================

Create a dedicated section:

"Prompt Intelligence"

Show:

CACHE HIT

CACHE MISS

Cache Hit Rate

38%

Tokens Reused

24,850

Estimated Savings

$3.21

Add a short explanation:

"Repeated system and context blocks are reused instead of being repeatedly processed."

Use a subtle animated cache/network visualization.

==================================================

8. HOW IT WORKS

==================================================

Create a visually impressive 4-step section:

01

UNDERSTAND

Analyze request difficulty.

02

ROUTE

Choose the cheapest capable model.

03

CACHE

Reuse repeated context.

04

MEASURE

Track cost, quality and performance.

Use connected visual elements rather than plain text boxes.

==================================================

9. FINAL CTA

==================================================

Create a strong final section:

"Make Every Token Count."

Subtitle:

"Intelligent routing for cost-efficient AI."

Button:

"Launch Optimizer →"

==================================================

NAVIGATION

==================================================

Create a clean sticky navigation:

LLM Cost Optimizer

Overview

Optimizer

Performance

How It Works

Right side:

"Launch Optimizer"

==================================================

RESPONSIVENESS

==================================================

The UI must work beautifully on:

- desktop

- laptop

- tablet

- mobile

Desktop should be the primary presentation experience.

==================================================

TECHNICAL FRONTEND REQUIREMENTS

==================================================

Use:

- React

- Vite

- modern CSS

- reusable React components

- clean component structure

- chart library if needed

Create reusable components such as:

Navbar

Hero

Optimizer

OptimizationResult

RoutingVisualizer

MetricCard

PerformanceDashboard

CostComparison

QualityComparison

CacheAnalytics

HowItWorks

Footer

Keep API communication isolated in a separate service file so we can connect the existing FastAPI backend later.

Use mock data for now.

Do not expose API keys.

==================================================

IMPORTANT DESIGN RULES

==================================================

1. Make the first screen immediately impressive.

2. Avoid excessive text.

3. Prioritize visual hierarchy.

4. Use vibrant gradients strategically.

5. Use animations subtly and professionally.

6. Make numbers and metrics visually prominent.

7. Make the routing decision visually understandable within 2 seconds.

8. Make the cost-saving story obvious to hackathon judges.

9. Do not use generic AI robot imagery.

10. Do not copy One Page Love or any existing website.

11. Create a unique visual identity for LLM Cost Optimizer.

12. The final product should look like a serious commercial AI SaaS product, not a college template.

The most important goal:

When a judge opens the application, they should immediately understand:

"THIS SYSTEM LOOKS AT A REQUEST → DECIDES HOW DIFFICULT IT IS → CHOOSES THE CHEAPEST CAPABLE MODEL → USES CACHING → MEASURES COST AND QUALITY."

Make that story visually obvious.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/a980d133-af49-4afe-9570-5e9975595de0).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
