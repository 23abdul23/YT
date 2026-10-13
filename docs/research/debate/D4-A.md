# D4-A: FOR a curated reusable Anatomy library + ~70-80% fallback visuals

(Source key: R = research/04-visuals-anatomy.md; S = repos/an-SKILL.md. Web re-verification attempted, firecrawl rate-limited: no new web facts; all below from local files.)

## Thesis
Anatomy figures are expensive to author and cheap to render. Pay authoring once, offline and supervised, then reuse by parametrization. Fresh-per-video generation fails on budget, reliability and topic fit.

## Arguments
1. **Authoring cost is hostile to a daily cadence.** A Figure is 40-80 parts, "budget up to an hour", with audit-to-zero, line check and 4x close-ups in both themes (S lines 59, 68-76). Token cost is UNVERIFIED, estimated 0.5-2 M per figure (R line 31). At <= $30/month that is unaffordable per video.
2. **Render is nearly free once built.** Eight MIT figures ship (S lines 14-23). Build ran instantly, drive ran 4.4 s with clean console, capture ~110 ms/frame measured (R lines 6-8). Reuse stage = 0 LLM tokens (R acceptance test 8).
3. **The skill itself resists unattended generation.** Step 3 demands a new invented object per concept (S line 65); Epic tier refuses to start; audit "must end passed" (S line 73). An unattended run can stall (R DECISION X.2). Curated figures are audited once by a human.
4. **Topic fit is partial, so fallbacks are mandatory anyway.** Figures suit one mechanism with numeric states (caches, queues, locks, rate limiters; S lines 29-39). News, people, charts, benchmarks do not fit (R line 36). A library plus fallbacks (code screens, GSAP diagrams, charts, all deterministic HTML on the same capture rig) never blocks the pipeline.
5. **Determinism is achievable once.** A seekable wrapper (`__anim.step/set`, virtual clock) is written in the build template, not per video (R lines 21-26). Tests: identical frame hashes, seek equality (R acceptance 1-2).

## Strongest opposing point and answer
Opposition: reuse makes channels look repetitive, and the skill says "never copy" (S line 65); a 6-12 library can't cover trending topics. Answer: parametrization (numbers, labels, params injection, crop/pan per scene, R line 57) changes the content; figures appear only as 10-25 s hero beats in selected videos (R line 36), so repetition is bounded. Generic mechanisms (gauge, queue, lock, spring, cache) recur across tech topics. Repetition is a smaller risk than a broken or missing figure. Also, "fresh per video" does not avoid the 70-80% fallback share; it only adds cost.

## What would change my mind
- Measured token/minute data for a Figure-tier build showing < ~100k tokens and < 10 min (publish.mjs gallery records minutes/tokens: https://github.com/wheresryan22/anatomy-community; UNVERIFIED, not fetched).
- Evidence the user has flat-rate agent capacity for hourly builds.
- Evidence that forks of a nearest example reliably pass audit unattended (cheap "mutate" tier between library and fresh).
- Audience retention data showing reused figures hurt watch time, or a platform "reused/repetitive content" policy hit (UNVERIFIED either way).

## Scores (1-5; 5 = best / easiest)
- Cost: 5
- Output quality: 4 (curated, audited; limited variety)
- Policy risk: 3 (repetitive-content risk mitigated by varied scripted content; UNVERIFIED)
- Implementation effort: 3 (seekable wrapper + render-figure.mjs + library build; portrait 9:16 untested)
- Maintainability: 4 (pin Chrome version; SVG-only figures preferred, R line 42)
