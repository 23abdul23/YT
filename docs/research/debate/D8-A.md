# D8-A (FOR): Analytics API + Reporting API job `channel_reach_basic_a1`

## Thesis
Thumbnail CTR is the one signal that separates "bad packaging" from "bad content". Only the Reporting API exposes it. The extra cost is one nightly CSV loop that we must write anyway because reports expire. Reusing claude-youtube only for OAuth/quota is correct, because its script requests metrics the API rejects.

## Arguments
1. **CTR exists only here.** Fetched page https://developers.google.com/youtube/reporting/v1/reports/channel_reports: `channel_reach_basic_a1` has dimensions date, channel_id, video_id and metrics `video_thumbnail_impressions` and `video_thumbnail_impressions_ctr`. The Analytics `reports.query` metrics list has no thumbnail CTR (`impressions` became `adImpressions`; report 08, https://developers.google.com/youtube/analytics/metrics). Without it, title/thumbnail rules run blind (report 08 s5, Option X).
2. **Low cost and low effort.** Reports are free CSV downloads (report 08: quota "not a practical concern"). One `jobs.create`. New jobs get 30 days of historical reports, mostly posted within a couple of days, and first data arrives in about 48 h (https://developers.google.com/youtube/reporting/v1/reports, fetched). Cost is $0 against the $30 budget.
3. **Archiving is mandatory regardless.** Non-historical reports last 60 days and historical ones 30 days (same page). A SQLite `reach` table (report 08 s6) is therefore already required, and the schema is a two-metric table.
4. **Idempotent by design.** The docs say YouTube issues backfill reports with a new report ID but the same start/end time, and tell clients to replace stored data for that period (same page). That matches the plan's upsert on PRIMARY KEY(video_id, day) and its "re-pull last 7 days" rule.
5. **Reuse is scoped to what works.** report 08 s1 says `fetch_video_analytics.py` requests `impressions` and `impressionClickThroughRate` from `reports.query`, which is likely a 400 error (UNVERIFIED, not executed). Taking only its OAuth/quota helpers avoids inheriting that defect.

## Strongest opposing point and answer
**"Small-channel CTR is noisy, and it adds a second scope and API surface for little decision value."** Answer: the plan already gates on it. Feedback rules require at least 2,000 impressions per variant for CTR comparisons (report 08 s8 #9). Below that, the data is ignored, so the cost of noise is zero and the cost of omission is blindness once volume exists. The Reporting API uses the same OAuth token. `yt-analytics.readonly` covers it (UNVERIFIED for this exact report; the docs fetched list no separate scope).

## What would change my mind
- A live test showing `channel_reach_basic_a1` returns no rows for a channel with fewer than about 1k impressions per day (anonymization thresholds; docs only say some dimension values are withheld).
- Google deprecating the report type, or a revision-history note moving CTR into `reports.query`, which would make the job redundant.
- 4 weeks of data showing the channel never reaches the 2,000-impression gate.

## Scores (1-5)
- Cost: 5 ($0)
- Output quality: 5 (only source of impressions/CTR)
- Policy risk: 4 (official API; storing derived metrics is fine; the 30-day metadata refresh rule applies to resource metadata, https://developers.google.com/youtube/reporting/v1/reports)
- Implementation effort (5 = easiest): 3 (job create, list, download, CSV upsert, gap handling)
- Maintainability: 4 (versioned `_a1` report IDs are stable; backfill handled by upsert)
