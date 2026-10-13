# D1-A (FOR): free sources + YouTube supply check, no DataForSEO at launch

## Thesis
Launch with HN, GitHub, HF papers, RSS and the YouTube Data API supply check. Keep DataForSEO as a null-by-default `signals.search_volume` plug-in. Cost is $0, there are fewer moving parts, and we can't yet tell whether paid demand data adds anything.

## Arguments
1. **Upfront cost conflicts with the budget.** DataForSEO's pricing page states "The minimum account top-up is $50" (https://dataforseo.com/pricing, fetched today). That is above the whole $30/month cap on day one. The report lists the minimum as UNVERIFIED (report s1 table); it is now verified. Per-call prices are tiny ($0.0006-$0.002 per YouTube SERP, per the report) but the entry ticket isn't.
2. **The free stack covers both halves of the score.** "Heat" comes from HN (the repo says "There is currently no rate limit", https://github.com/HackerNews/API), GitHub stars/day, HF upvotes and RSS outlet count. "Gap" comes from the YouTube key we need for upload anyway (report s1, s3-X). The scoring formula in the report already uses only X-available inputs.
3. **Search volume is the one thing we lose, and it is the least reliable input for new topics.** A topic trending on HN today has near-zero historical volume. Heat plus "few videos in the last 14 days" is arguably a better proxy for a fresh-trend channel. UNVERIFIED opinion, but testable with the first 20 videos.
4. **Fewer dependencies and failure modes.** There is no extra account, prepaid balance or npm MCP. Windows runs plain Python. Acceptance test 11 (no paid call) is trivial to assert (report s5).
5. **Reversible.** The schema already reserves `search_volume: null`. Adding DataForSEO later means one adapter and no redesign.

## Strongest opposing point and answer
Opposition: the YouTube quota is a hard cap (the report estimates about 60-80 checks/day), and the free stack gives no demand number, so we may pick topics nobody searches for.
Answer: 60 checks/day is plenty when the output is 1-3 videos/day. Pre-filter to about 15 candidates by free heat and spend quota only on those. The demand blind spot is covered by heat plus momentum, and the plug-in exists for the case where analytics show heat mispredicts winners. Caveat: my own fetch of the quota page returned a garbled summary (search.list "100 calls/day bucket"), which conflicts with the report's 100 units per call and the 10,000-unit daily quota. The report's reading is more plausible, but we should re-verify this before building. If search.list were capped at 100 calls/day, the conclusion would be unchanged, since 60 checks fit inside it either way.

## What would change my mind
- Quota verified so that fewer than about 20 supply checks/day are possible.
- After about 20 videos, a backtest shows heat-only ranking has weak correlation with views-per-impression, while search volume would have fixed it.
- The $50 deposit being a one-off that lasts over 6 months at our call volume, with measurable lift. The one-off $50 would then be amortized across months (UNVERIFIED).

## Scores (1-5; 5 = best / easiest)
- Cost: 5
- Output quality: 3 (no volume data, but a strong freshness signal)
- Policy risk: 5 (official APIs and public feeds only)
- Implementation effort: 4
- Maintainability: 4
