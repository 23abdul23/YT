# 01 - Trend / Topic Discovery (verified 2026-10-14)

## 1. Comparison table

| Source | Cost | Limits | Windows | Signal for "trending AND under-served on YT" | ToS risk |
|---|---|---|---|---|---|
| YouTube Data API v3 (search.list, videos.list, mostPopular) | Free | 10,000 units/day default; search.list = 100 units, videos.list = 1 unit (50 ids/call); failed calls still cost 1; reset midnight PT ([quota doc](https://developers.google.com/youtube/v3/determine_quota_cost), [overview](https://developers.google.com/youtube/v3/getting-started)) | Pure HTTPS, trivial | The ONLY source for the "under-served" half: count/recency/views of existing videos on a topic. ~50-90 search calls/day max. mostPopular is generic, weak for tech | Low (own project key; already required for upload) |
| Hacker News Firebase API | Free | No published rate limit ([HackerNews/API](https://github.com/HackerNews/API)); 1 request per item, so cache | Trivial | Strong "tech-trending now" (points, comments, age) | Low |
| HN Algolia search | Free | ~10k req/h/IP is community-reported, not official; UNVERIFIED current setting ([source](https://unpkg.com/hacker-news-api@2.0.0/README.md)) | Trivial | Good for "how much discussion in last 7d for keyword X" | Low |
| Reddit Data API | Free tier = non-commercial only, ~100 QPM per OAuth client; commercial pricing not public (figures $0.24/1k and $12k/yr-or-month conflict) ([techloy](https://www.techloy.com/reddit-api-pricing-in-2026-complete-guide-for-developers-and-businesses/), [socialcrawl](https://www.socialcrawl.dev/blog/reddit-api-key-limits-alternatives-2026)); self-serve approval reportedly slow (2-4 wks, UNVERIFIED) | see left | Fine | Good signal (r/programming, r/MachineLearning) but monetized channel = commercial use | HIGH for a monetized channel |
| Google Trends via pytrends | Free | Repo archived 2025-04-17; Explore reportedly works, trending-searches returned 404 in a Sep 2026 test (single third-party report, UNVERIFIED) ([dev.to](https://dev.to/esteban_ortega/pytrends-is-dead-heres-how-to-get-google-trends-data-in-2026-1a18), [scrapebadger](https://scrapebadger.com/blog/does-google-trends-have-an-api-what-to-use-in-2026)) | pip works | Good for "is interest rising" on a keyword; flaky, 429s | Medium (unofficial scraping of google.com) |
| Official Google Trends API (alpha) | Unknown | Application-gated; 5-yr consistent-scaled data; NO Trending Now ([Google blog](https://developers.google.com/search/blog/2025/07/trends-api), [ppc.land](https://ppc.land/google-opens-alpha-testing-for-new-trends-api-targeting-developers-and-journalists/)) | n/a | Excellent if granted, but cannot be planned on | None |
| GitHub Trending | Free | No official API; scrape page or community wrappers. Official REST search 30 req/min authed, 4,000-result cap ([docs](https://docs.github.com/en/rest/search/search)) | Fine | Strong for tools/libraries (stars/day) | Low-medium (HTML scrape). Safer: REST search `created:>date sort:stars` |
| arXiv API | Free | Respect rate limits; community: 3 req/s, 503 on abuse; metadata CC0 ([TOU](https://info.arxiv.org/help/api/tou.html)) | Fine | Papers lag; good for AI explainers only | Low |
| HF Daily Papers `/api/daily_papers` | Free | Endpoint documented only by third-party skill pages, no official doc found: UNVERIFIED ([listing](https://mcpservers.org/vi/agent-skills/huggingface/huggingface-papers)) | Fine | Community-upvoted AI papers: better curated than arXiv | Low |
| RSS tech news (Verge, Ars, TechCrunch, vendor blogs, Hugging Face blog, etc.) | Free | Polite polling (hourly) | `feedparser` works | Confirms mainstream coverage; cross-source count boosts confidence | Low (headlines/links only; do not copy text) |
| DataForSEO (YouTube SERP, Trends, keyword volume) | Pay-as-you-go. YouTube SERP $0.0006 standard / $0.002 live per 20 results (Video Info/Subtitles x3); Google Trends $0.00225/task (5 kw) standard, $0.009 live ([SERP pricing](https://dataforseo.com/pricing/serp/youtube-serp-api), [Trends pricing](https://dev_wp.dataforseo.com/pricing/keywords-data/google-trends)). Minimum top-up deposit: UNVERIFIED | Generous | npm MCP, needs Node | Best single "demand vs supply" signal incl. volume; no quota juggling | Low (commercial API) |
| claude-youtube `ideate` | Free skill; ~$0.01/run via DataForSEO, else WebSearch fallback ([ideate.md](https://raw.githubusercontent.com/AgriciDaniel/claude-youtube/main/skills/claude-youtube/sub-skills/ideate.md)) | needs Claude Code session | Markdown prompts, needs LLM | Outputs 10 ideas scored Demand x CTR x Feasibility x Niche Fit (/40), markdown only, scales undefined | Low |
| claude-youtube `competitor` | ~$0.02 DataForSEO or 100 units/search YT API fallback ([competitor.md](https://raw.githubusercontent.com/AgriciDaniel/claude-youtube/main/skills/claude-youtube/sub-skills/competitor.md)) | up to 3 channels | same | Gap maps and 3x-outlier detection: useful monthly, not daily | Low |

## 2. Scoring formula, dedupe, novelty

Pipeline: collect candidates (HN, GitHub, HF papers, RSS) -> normalize to a topic key -> cluster -> enrich top ~15 with YouTube supply check -> score -> pick top N.

```
heat      = 0.35*z(HN_points_per_hour_capped) + 0.25*z(gh_stars_per_day) + 0.20*z(hf_upvotes) + 0.20*min(rss_distinct_outlets,5)/5
momentum  = clamp(heat_now / (heat_7d_avg + eps), 0, 3) / 3          # fresh spike vs. steady
supply    = log10(1 + yt_videos_last_14d_on_topic) + 0.5*log10(1 + top3_views_last14d/1e4)
gap       = 1 - clamp(supply / 4, 0, 1)                               # 1 = nobody covered it
fit       = LLM/keyword rubric 0..1: explainable in 6-10 min with visuals, evergreen angle, not pure news
risk      = 1 if policy-sensitive (security exploit details, unreleased leaks, legal), else 0

score = 100 * (0.30*heat + 0.20*momentum + 0.30*gap + 0.20*fit) * (1 - 0.8*risk)
```
Rules: hard gate `gap >= 0.25` (else "saturated") unless you have a distinct angle; Shorts take any score >= 55, long-form >= 65. The weights are assumptions (UNVERIFIED), tune after 20 videos using analytics views-per-impression.

Dedupe: key = lowercased canonical entity (repo full_name, arXiv id, product+version) else normalized title tokens. Merge if URL domain+path equal, or title Jaccard >= 0.6, or embedding cosine >= 0.85 (local small model; Jaccard-only is enough to start). Keep a persistent `history.jsonl` of all produced topic keys.

Novelty: reject if the same key was published in the last 90 days, unless `new_event=true` (new version, new benchmark, >=3x heat) in which case allow once per 30 days, tagged `followup`. Cap 1 topic per entity per week and at most 2 of the same category per day.

## 3. THE crucial decision

Decision: how do we measure "under-served on YouTube"?

**Option X: free-only stack, YouTube Data API supply check, no DataForSEO.**
- Cost is $0; the YouTube key is needed for upload anyway, and 10,000 units/day allows about 60-80 topic checks/day after reserving upload/analytics quota ([quota doc](https://developers.google.com/youtube/v3/determine_quota_cost)).
- No search-volume number exists, so "demand" is inferred from HN/GitHub/HF heat only; pytrends is flaky and archived since 2025-04-17 ([scrapebadger](https://scrapebadger.com/blog/does-google-trends-have-an-api-what-to-use-in-2026)).
- Everything is deterministic Python on Windows with no extra service; the quota is a hard cap on candidates per day.

**Option Y: add DataForSEO (pay-as-you-go) for YouTube SERP + Trends + volume.**
- Roughly $0.002-0.009 per check ([pricing](https://dataforseo.com/pricing/serp/youtube-serp-api)): 100 checks/day is about $0.2-0.9/day, i.e. up to ~$27/month at the live rate, so standard queue or fewer checks is needed to stay far under $30 (budget math, my estimate).
- Gives search-volume and Trends validation that the free stack cannot, which is what the claude-youtube ideate/competitor skills assume ([ideate.md](https://raw.githubusercontent.com/AgriciDaniel/claude-youtube/main/skills/claude-youtube/sub-skills/ideate.md)).
- Adds an account, an npm MCP/REST dependency and a prepaid balance; minimum deposit UNVERIFIED.

Recommendation: start with X (the formula above uses only X-available inputs); add Y as an optional `demand` plug-in behind the same schema field (`signals.search_volume`, null in X) once a month of data shows heat alone mispredicts winners. Use claude-youtube `competitor` monthly (manual) to seed the niche gap list, and borrow `ideate`'s brief fields (hook angle, urgency flag) but not its LLM-only scoring.

Cut: Reddit (commercial-use ToS risk for a monetized channel), official Trends API (gated), arXiv direct (HF daily papers suffices).

## 4. Interface: `topics.json` producer

CLI: `python -m trends.run --config trends.yaml --out data/topics.json --history data/history.jsonl`. Exit 0 even if some sources fail (recorded in `source_status`); exit 2 only if zero candidates.

Config (input): 
```json
{"niche_keywords":["ai","llm","rust","kubernetes","gpu"],"exclude":["crypto price","celebrity"],
 "max_topics":10,"min_score":{"long":65,"short":55},"yt_checks_budget":60,
 "sources":{"hn":true,"github":true,"hf_papers":true,"rss":["https://..."],"dataforseo":false}}
```
Output `topics.json`:
```json
{
 "schema_version": 1,
 "generated_at": "2026-10-14T06:00:00Z",
 "source_status": {"hn":"ok","github":"ok","hf_papers":"fail:HTTP 404","yt_search":"ok","yt_units_used":6100},
 "topics": [{
   "id": "sha1-of-topic_key[:12]",
   "topic_key": "repo:owner/name | arxiv:2410.01234 | title:normalized tokens",
   "title": "string (<=100 chars, working title)",
   "category": "ai|dev-tools|security|hardware|web|other",
   "format": "long|short|both",
   "angle": "one sentence differentiator",
   "sources": [{"type":"hn","url":"https://...","points":812,"age_h":5}],
   "signals": {"heat":0.0,"momentum":0.0,"supply_videos_14d":3,"top3_views_14d":45000,"gap":0.0,"search_volume":null},
   "fit": 0.0, "risk": false,
   "score": 0.0,
   "novelty": {"status":"new|followup|duplicate","last_published":null},
   "keywords": ["..."], "expires_at": "2026-10-21T00:00:00Z"
 }]
}
```
Contract for downstream (script stage): read `topics[0]` after sorting by `score` desc; must not mutate; pipeline writes chosen `id` to `history.jsonl` on successful upload only.

## 5. Acceptance tests

1. Schema: output validates against JSON Schema; `schema_version`, unique `id`s, score in [0,100], sorted descending.
2. Offline fixture run (recorded HN/GitHub/YT responses) produces byte-identical `topics.json` twice (determinism).
3. Source failure: kill each source in turn (mock 404/timeout); run still exits 0, `source_status` shows failure, other topics returned.
4. Quota guard: with `yt_checks_budget=60`, `yt_units_used` <= 6,100 (60 searches x 100 + enrichment), never exceeding 8,000 so uploads/analytics keep headroom.
5. Dedupe: two items "Show HN: Foo 2.0" and the GitHub repo foo/foo merge into one topic with both sources listed.
6. Novelty: topic key present in history <90 days is `duplicate` and excluded; with `new_event=true` it appears as `followup`.
7. Saturation gate: topic with supply_videos_14d >= 40 and top3 views high is excluded or `gap < 0.25`.
8. Risk gate: title containing exploit/leak terms yields score reduced by 80%.
9. Rate-limit behavior: injected 429/503 triggers exponential backoff (max 3 tries), no crash; GitHub scrape layout failure falls back to REST search.
10. Windows: runs under PowerShell with Python 3.11+, no WSL, no reliance on `/tmp`; UTF-8 output.
11. Cost: a full run with dataforseo=false makes no paid call (assert via network allowlist).

Not verified: Google's current Trends alpha page, DataForSEO minimum deposit, HF Daily Papers official docs, Reddit's current official terms page, arXiv's Oct 2026 rate policy claim.
