# D4-B (AGAINST: library of 6-12 figures)

## Thesis
A fixed library makes every video share the same 6-12 visuals. That is the exact "template" signal YouTube demonetizes. A fresh concept-specific figure per video, at Figure tier only and scheduled weekly (not daily), is affordable and is the channel's one defensible differentiator.

## Arguments
1. Policy. YouTube's "inauthentic content" rule targets videos that look "made with a template" or are interchangeable, and is judged at channel level (10-policy.md s1, https://support.google.com/youtube/answer/1311392 [V]; netinfluencer Jul 2026 [S]). Fallback visuals for 70-80% of scenes (code screens, GSAP diagrams, charts) are the most generic assets in AI-channel land. The Anatomy figure is the only scene type a competitor can't copy cheaply. Cutting it to a recycled 6-12 removes the moat. Policy risk #1 is rated "High if fully autonomous" (10-policy.md s2).
2. Repetition is arithmetic. At weekly cadence, 52 videos/yr over 8 figures means each figure repeats about 6 times. The repo ships exactly 8 figures (04-visuals-anatomy.md Q2). Viewers, and a channel-level reviewer, will notice repeats.
3. The skill itself says reuse is the wrong mode: "invent a new object per concept, never copy" (an-SKILL.md step 3, per 04 Q2). The report concedes reuse "only works when the topic maps onto an existing machine". A mismatched gauge on an unrelated topic is worse than no figure.
4. The cost objection is overstated. SKILL.md says a Figure "often finishes in well under an hour" (an-SKILL.md l.59). Its own CHANGELOG says the old 30-90 min estimate was often too long (04 Q2). The 0.5-2M-token cost in 04 is the author's own UNVERIFIED guess. No measured figure exists, and the gallery that would have one (https://github.com/wheresryan22/anatomy-community) couldn't be fetched, so nobody has shown it is unaffordable. One Figure per week is about 4 builds/month, and the 04 report itself says the budget issue arises only for a "daily cadence".
5. Scope is controllable: use a Figure-only tier, SVG-only, no WebGL. Hero (2-4h) and Epic (refuses to start) are excluded. The "poor-fit" topics (charts, people, news) can take a fallback in that one video while still getting a bespoke figure when a mechanism exists.

## Strongest point FOR, and my answer
FOR: unattended agent runs may stall on the audit, and the per-figure token cost is unmeasured, so the library is the safe option (04 DECISION). Answer: add a human-supervised build step (the 10-policy.md Option Y approval anyway) and a timeout that falls back to the nearest library figure. That gives per-video freshness with a safety net, and a library becomes the fallback rather than the plan.

## What would change my mind
- Measured gallery data showing a Figure takes more than 2h or more than about 3M tokens.
- Evidence (policy text or a case study) that varied scripts and voice satisfy the channel-level check without bespoke visuals.
- A test of 4 weekly builds in which more than 1 fails the audit.

## Scores for my alternative (hybrid: fresh Figure-tier per weekly video, library as timeout fallback), 1-5, 5 = best/easiest
- Cost: 3 (flat-rate or API budget; the UNVERIFIED token estimate is the risk)
- Output quality: 5
- Policy risk: 4 (5 = lowest risk)
- Implementation effort: 2
- Maintainability: 3
Not verified: Firecrawl was rate-limited, so no new fetches succeeded; all facts come from the supplied files.
