# D1-B (against): include DataForSEO from day one

## Thesis
Launching blind on "demand" is the wrong default. The free stack measures what developers are excited about, not what YouTube viewers search for, and the YT supply check is quota-capped. DataForSEO costs about $1-5/month at our volume, so deferring it saves almost nothing and delays the one signal that validates the formula. Enable it from day one at standard-queue rates with a hard cap.

## Arguments
1. **The cost is small; the real barrier is the deposit.** Standard YouTube SERP is $0.0006 per 20 results, live $0.002 ([pricing](https://dataforseo.com/pricing/serp/youtube-serp-api)). 60 checks/day at the standard rate is about $1.1/month. The report's "~$27/month" worst case assumes 100 live checks/day and Trends on top ([report](01-trends.md) section 3). The minimum payment is $50, funds never expire ([DataForSEO FAQ via search](https://dataforseo.com/help-center/minimum-payment)). That is one prepayment, and it covers over a year at the standard rate. Verified this session. The report listed it as UNVERIFIED.
2. **The free YT supply check is thinner than the report assumes.** The quota page (fetched this session, small-model summary, so re-check) says search.list has its own bucket of 100 calls/day and that videos.insert has a separate 100/day bucket ([quota doc](https://developers.google.com/youtube/v3/determine_quota_cost)). That conflicts with the report's "100 units per search". Either reading leaves a hard ceiling of roughly 100 topic checks/day with no volume figure.
3. **Heat is not demand.** HN points and GitHub stars measure developer attention. The formula's `gap` term only counts existing videos (supply) and has no demand side. A topic with zero videos and zero searches scores as an opportunity. The report concedes `search_volume` is null in option X.
4. **Free Trends is the weak link.** pytrends is archived (2025-04-17) and the official Trends API is gated and has no Trending Now ([report](01-trends.md) table). DataForSEO Trends is $0.00225 per 5-keyword task, so it is the only stable path.
5. **The weights are guesses until data arrives.** The report says "weights are assumptions (UNVERIFIED), tune after 20 videos". Fixing a wrong formula after 20 flops costs far more in channel momentum than $1/month. Collect volume from the first run so the tuning data exists.

## Strongest point FOR D1, and my answer
Point: $0 cost, a smaller dependency surface, and no prepayment before the pipeline is proven. My answer: the schema already has the `signals.search_volume` slot. Wire the client and a budget guard now, and run it capped at $3/month. This keeps the plug-in architecture and still collects volume from day one. The $50 prepayment is the only real cost, and it lasts years.

## What would change my mind
- Evidence that DataForSEO YouTube SERP returns no usable volume. It returns SERP rank/results, so true search volume may need the Keywords Data API (UNVERIFIED, not checked).
- Evidence that channels in this niche win on news-velocity, not search demand.
- A cost below $50 to get a key, or the $1 trial credit covering a month of testing (~800+ SERPs).

## Scores for my alternative (free stack + capped DataForSEO from day 1)
- Cost: 4 (about $1-5/month plus the $50 prepayment)
- Output quality: 4
- Policy risk: 5 (commercial API)
- Implementation effort: 3 (one extra client and budget guard)
- Maintainability: 4
