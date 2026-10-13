# D8-B: Against "Analytics API + Reporting API job for CTR"

## Thesis
At launch, use the Analytics API only (retention, engagedViews, traffic source). Defer the Reporting API job and every CTR rule until the channel has enough impressions to make CTR statistically usable. The cost of waiting is small and bounded.

## Arguments
1. **The report's own rules make CTR mostly inert.** Rule 9 allows CTR comparisons only between variants with >= 2,000 impressions each, and rule 3 needs n >= 8 videos per value. A brand-new channel will not reach either for months. The job would be ingesting data that no rule can act on (08-analytics.md, section 8).
2. **Deferral is cheap: backfill exists.** The report says new jobs get a 30-day historical backfill (08-analytics.md s1; https://developers.google.com/youtube/reporting/v1/reports). So adding the job on day ~60 loses at most the oldest weeks, and those weeks hold the smallest samples. Skipping it now is a reversible choice.
3. **Thumbnail changes confound CTR on tiny samples.** The reach report (`channel_reach_basic_a1`, https://developers.google.com/youtube/reporting/v1/reports/channel_reports) gives video/day impressions and CTR. At a few hundred impressions, a CTR swing is noise, and it also depends on audience mix and traffic source. Rules that rotate thumbnails or titles on it overfit. This is the failure mode the report warns about.
4. **Extra moving parts for a $30/month automation.** A second API surface, job lifecycle, ~48 h first delivery, 60-day expiry, CSV parse, upsert, gap detection, and acceptance tests 3, 6 and 10 (08-analytics.md s9). Every one is a new failure that can silently starve the weekly report.
5. **The real launch bottlenecks are visible without CTR.** Retention cliffs, `engagedViews` and traffic mix already drive the hook, length and topic decisions (report s8 rules 2, 7). Studio shows CTR for free in a manual weekly check, with no code.

## Strongest point FOR, and my answer
For: CTR is the only signal for thumbnail/title quality; without it, view velocity is a weak proxy, and the 60-day expiry means data not archived is lost forever.
Answer: that loss is real, but it is capped by the 30-day backfill and by the Studio fallback. Thumbnail testing at this scale is underpowered either way. Add the job when the 2,000-impression gate is reachable.

## What would change my mind
- Evidence that backfill is shorter than 30 days or not applied to reach reports (UNVERIFIED for reach reports specifically).
- The channel clearing ~2,000 impressions per video within the first month.
- The ingest being shown to be about 40 lines and already needed for other reports.
- Studio CTR being unreadable or unavailable.

## Scores for my alternative (Analytics API only, manual Studio CTR glance)
Cost 5 | Output quality 3 | Policy risk 5 | Implementation effort 5 | Maintainability 5

Caveat: the 30-day backfill figure comes from the report, not independently re-fetched; I confirmed only that the reach report and its metrics exist.
