# 08 - Analytics, Reporting, Feedback Loop (verified 2026-10-14)

## 1. Key findings (with sources)
- Analytics API `reports.query` scopes: `yt-analytics.readonly` (views/retention) and `yt-analytics-monetary.readonly` (revenue); page also says requests now need `youtube.readonly`. https://developers.google.com/youtube/analytics/reference/reports/query
- Metrics page lists `views`, `engagedViews`, `estimatedMinutesWatched`, `averageViewDuration`, `averageViewPercentage`, and retention (`audienceWatchRatio`, `relativeRetentionPerformance` via dimension `elapsedVideoTimeRatio`; one video per query). `impressions` was renamed `adImpressions` (ad impressions, NOT thumbnail impressions); no general video CTR metric is listed. No Shorts-specific metrics listed (no "viewed vs swiped away" in the API; it is Studio-only - UNVERIFIED absence, nothing found). https://developers.google.com/youtube/analytics/metrics
- **Thumbnail impressions + CTR exist only in Reporting API bulk reports** `channel_reach_basic_a1` (dims date, channel_id, video_id; metrics `video_thumbnail_impressions`, `video_thumbnail_impressions_ctr`), added Jan 15 2026. https://developers.google.com/youtube/reporting/v1/reports/channel_reports ; https://developers.google.com/youtube/analytics/revision_history
- **Defect in claude-youtube:** `fetch_video_analytics.py` DEFAULT_METRICS requests `impressions` and `impressionClickThroughRate` from `reports.query`. Per the metrics page these are not valid there; I expect HTTP 400 "query is not supported" (not executed - UNVERIFIED). Its `analytics-guide.md` correctly mentions `channel_reach_basic_a1`, but the script never calls the Reporting API. Source: https://github.com/AgriciDaniel/claude-youtube (skills/claude-youtube/execution/fetch_video_analytics.py, references/analytics-guide.md).
- What claude-youtube already does: OAuth service via `utils/youtube_auth`; per-video metrics query (dimension=video, max 200 rows); traffic-source breakdown (`insightTrafficSourceType`); daily series; channel/recent-video fetch via Data API with a quota tracker (`fetch_channel_data.py`). `analyze.md` is an interpretation prompt (funnel diagnosis, retention classes cliff/valley/bump/steady) for screenshots/CSV. Reusable: auth, query wrappers, diagnostic matrix. Missing: storage, Reporting API, scheduler, feedback.
- Latency: 48-72 h processing; endDate truncated to last processed day; use Data API `videos.list` for near-real-time stats; low-traffic data may be withheld; non-monetized channels get HTTP 403 on monetary metrics. https://developers.google.com/youtube/analytics/data_model (and revision history entry Sep 9 2026).
- Quota: Analytics API each request = 1 unit against the quota in Cloud console (default number not on the page - UNVERIFIED); Reporting API: download once, quota "not a practical concern". https://developers.google.com/youtube/analytics/data_model ; https://developers.google.com/youtube/reporting/v1/reports
- Reporting API: `jobs.create` with reportTypeId; first report ~48 h later; 30-day historical backfill for new jobs; reports downloadable 60 days then gone, so archive to SQLite. https://developers.google.com/youtube/reporting/v1/reports
- Traffic-source queries error if videos x days > 50,000 (Nov 2024). Revision history link above.
- Shorts counting: since Apr 30 2025 `views` counts every start/replay; `engagedViews` preserves old min-watch semantics. On **Aug 27 2026** public view counting was aligned across long-form/Live/Shorts (view = playback begins) and `engagedViews` redefined; CTR and AVD stay anchored to engaged metrics. Use `engagedViews` for Shorts quality comparison. Revision history link above.

## 2. YPP milestones
- Official: 1,000 subs + 4,000 qualified watch hours (12 mo) OR 1,000 subs + 10M qualified Shorts views (90 d); Shorts-feed watch hours do not count toward the 4,000. Updated YPP terms start **Feb 1 2027** (accept in Studio by Jan 31 2027). https://support.google.com/youtube/answer/72851
- 500-sub early tier (3 uploads/90 d, 3,000 h or 3M Shorts views/90 d) and a rise to 8,000 h / 20M on Feb 1 2027 are reported only by vidIQ; the official page fetched did not mention them -> **UNVERIFIED**. https://vidiq.com/blog/post/monetize-youtube-guide/ . Hedge: track against the stricter numbers.
- Track `watch_hours_12m` and `shorts_views_90d` in the DB (table `milestone`).

## 3. "Reused / mass-produced / inauthentic" warnings
- Policy renamed "repetitious" to "inauthentic content" Jul 15 2025: mass-produced/repetitive, template-like with little variation, enforced channel-wide; test is whether the average viewer can tell videos differ; not AI-specific. https://support.google.com/youtube/answer/1311392 (seen through search summary, not fetched in full).
- Notices appear in Studio. **No API endpoint found for monetization/policy status** (UNVERIFIED absence), so treat as manual: weekly report carries a checklist "Studio notifications / Earn tab / email". Appeal window and 90-day reapply figures come only from third-party blogs - UNVERIFIED.
- Proactive proxy: similarity guard (script n-gram + visual-template overlap vs last 20 videos) blocks publish above a threshold.

## 4. Comparison table
| Signal | Source | Granularity | Latency | Notes |
|---|---|---|---|---|
| views, engagedViews, minutes, AVD, avgViewPct, subs | Analytics API | video/day | 48-72 h | 1 unit/request |
| Retention curve | Analytics API `elapsedVideoTimeRatio` | 1 video/query | 48-72 h | cliff/valley detection |
| Traffic sources | Analytics API | video/day | 48-72 h | videos x days <= 50k |
| Thumbnail impressions + CTR | Reporting API reach report | video/day CSV | ~2 d | 60-day expiry |
| Near-real-time views | Data API `videos.list` | video | minutes | stats only |
| Shorts swiped-away % | Studio UI only | - | - | UNVERIFIED not in API |
| Policy warnings | Studio/email | - | - | no API found |
| Revenue | Analytics monetary scope | day | 48-72 h | 403 until monetized |

## 5. ONE crucial decision: where does CTR come from?
**Option X - Analytics API only (skip CTR).** (1) One scope `yt-analytics.readonly`, 1 unit per request; (2) retention, `engagedViews`, traffic source all available; (3) no thumbnail CTR, so title/thumbnail rules run blind, using view velocity as a weak proxy.
**Option Y - Analytics API + Reporting API reach job (RECOMMENDED).** (1) `channel_reach_basic_a1` gives thumbnail impressions and CTR per video/day (since Jan 2026); (2) one `jobs.create`, 30-day backfill, first data ~48 h; (3) extra work is a nightly CSV download-and-upsert, mandatory anyway because reports expire after 60 days.

## 6. SQLite schema (`analytics.db`)
```sql
CREATE TABLE video (video_id TEXT PRIMARY KEY, kind TEXT CHECK(kind IN('long','short')),
  published_at TEXT, topic TEXT, topic_score REAL, title TEXT, hook_type TEXT,
  length_sec INT, visual_type TEXT, voice TEXT, thumb_variant TEXT, script_hash TEXT, run_id TEXT);
CREATE TABLE daily (video_id TEXT, day TEXT, views INT, engaged_views INT, minutes REAL,
  avg_view_sec REAL, avg_view_pct REAL, subs_gained INT, subs_lost INT, likes INT, comments INT, shares INT,
  PRIMARY KEY(video_id, day));
CREATE TABLE reach (video_id TEXT, day TEXT, impressions INT, ctr REAL, PRIMARY KEY(video_id, day));
CREATE TABLE traffic (video_id TEXT, day TEXT, source TEXT, views INT, minutes REAL, PRIMARY KEY(video_id,day,source));
CREATE TABLE retention (video_id TEXT, fetched_on TEXT, ratio REAL, watch_ratio REAL, rel_perf REAL, PRIMARY KEY(video_id,fetched_on,ratio));
CREATE TABLE milestone (day TEXT PRIMARY KEY, subs INT, watch_hours_12m REAL, shorts_views_90d INT);
CREATE TABLE feature_stat (feature TEXT, value TEXT, n INT, mean_metric REAL, shrunk REAL, updated TEXT, PRIMARY KEY(feature,value));
```
"Settled" = published + 7 d (long) / + 3 d (short) and endDate <= today-3. Re-pull the last 7 days each run to catch revisions.

## 7. weekly_report.md template
```
# Weekly Report {week_start}..{week_end} (data through {last_settled_day})
## Headline
Subs {subs} ({d_subs:+}) | 12m watch hrs {wh}/4000 | Shorts 90d views {sv}/10M | Published {n_long}L/{n_short}S
## Per-video (last 28 d, settled only)
| video | kind | views | engViews | avg view % | CTR | impressions | subs+ | top source |
## Retention flags (cliff <30s / valley at t / steady)
## Winners & losers (vs trailing median, shrunk)
## Feature leaderboard (hook_type, length bucket, visual_type): n, shrunk score, status {explore|keep|drop}
## Topic-scoring changes applied this week
## Health: top-source share (>60% flag), max script similarity, cadence
## Manual checks (not in API): [ ] Studio notifications [ ] Earn tab status [ ] copyright claims
## Ops: API units used, failed jobs, report gaps
```
Delivery: write `reports/YYYY-Www.md` (render to HTML optional); email via SMTP only if desired (no cost; UNVERIFIED setup). Trigger via Windows Task Scheduler: nightly ingest, weekly report.

## 8. Feedback rules (avoid overfitting)
1. Judge only settled videos with >= 500 impressions (long) or >= 1,000 engagedViews (short).
2. Normalize each metric by trailing median of the same kind (long vs short separate). Long primary: avg_view_pct and minutes per impression. Shorts primary: engaged_views and avg_view_pct. Ignore likes.
3. Per feature value (hook type, 3 length buckets, visual type) use shrinkage: shrunk = (n*mean + k*global)/(n+k), k=5. Change policy only when n >= 8 per value AND shrunk differs from global by > 1 SD.
4. Exploration floor: 25% of videos pick the least-tried or random feature value; never drop a value with n < 8.
5. One rule change per week, one dimension at a time, logged in `feature_stat`.
6. Topic score = trend/demand score + w * shrunk(category performance), w capped at 0.3.
7. Retention rule: >40% drop in first 30 s on 3 of the last 5 videos -> rotate hook template; recurring mid-valley at the same ratio -> shorten that section type.
8. Anti-template guard: no feature value > 60% of last 20 videos (protects against the inauthentic-content policy).
9. CTR comparisons only between variants each with >= 2,000 impressions.
10. Do not read RPM/seasonal CPM swings as quality changes.

## 9. Acceptance tests
1. OAuth with `yt-analytics.readonly` + `youtube.readonly` returns rows for a known video; token refresh works after 7 days (Google OAuth apps in "Testing" status reportedly expire refresh tokens in 7 days - UNVERIFIED; move consent screen to production).
2. Query `views,engagedViews,estimatedMinutesWatched,averageViewPercentage` succeeds; adding `impressionClickThroughRate` fails with HTTP 400 (confirms the claude-youtube defect).
3. Reporting job created; within 72 h the reach CSV is downloaded and loaded; row count matches uploaded videos.
4. Ingest idempotent: running twice leaves identical row counts.
5. Ingest never writes unsettled days as final; last 7 days re-pulled.
6. Deleting local CSVs does not lose data older than 55 days (already in SQLite).
7. Weekly report renders with 0, 1 and 30 videos; shows "insufficient data" below thresholds.
8. Feedback unit test: n=3 per hook never changes policy; n=12 with clear gap does, and the 25% exploration still picks the loser.
9. Similarity guard blocks a duplicate script above threshold.
10. Quota ledger shows < 50 requests/day and appears in the report.
