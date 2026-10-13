# 07 - Upload + Publish (YouTube Data API v3), verified 2026-10-14

## 1. Verified facts
| Topic | Fact | Source |
|---|---|---|
| videos.insert quota | 1 unit/call, own bucket, default 100 calls/day. (Dec 4 2025 cost fell ~1,600 -> ~100; Jun 1 2026 split into granular buckets) | https://developers.google.com/youtube/v3/determine_quota_cost ; https://developers.google.com/youtube/v3/revision_history |
| Other costs | thumbnails.set 50; captions.insert 400; playlistItems.insert 50; videos.update 50. Shared bucket 10,000/day, reset midnight Pacific | determine_quota_cost (above) |
| Per video total | 1 (own bucket) + 50 + 400 + 50 = 500 units of shared bucket -> ~20 full videos/day max; we need 1-3/day. Quota is NOT a constraint | derived |
| Quota extension | Needs compliance audit via https://support.google.com/youtube/contact/yt_api_form (org legal name, HTTPS site, privacy policy, ToS, demo creds, per-endpoint justification). Not needed for us | https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits |
| PRIVATE-LOCK RULE | **CONFLICTING.** Introduced 2020-07-28: videos from unverified API projects created after that date are forced private until audit (revision_history). BUT the current videos.insert reference (fetched today) says: "Videos uploaded from unverified API projects are not restricted to private viewing mode." The YouTube Help page (~4 yrs old) still lists "uploaded by an unverified third party API service" as a lock trigger, no appeal, re-upload required. | https://developers.google.com/youtube/v3/docs/videos/insert ; https://support.google.com/youtube/answer/7300965 |
| containsSyntheticMedia | Exists since Oct 30 2024; settable in videos.insert/update (`status.containsSyntheticMedia`) | revision_history |
| Other status fields | privacyStatus, publishAt (invalidPublishAt error if bad), selfDeclaredMadeForKids, license, embeddable, publicStatsViewable | videos/insert page |
| Scopes | upload needs youtube.upload (or youtube / force-ssl). Thumbnails/captions/playlists need `youtube` or `youtube.force-ssl` (UNVERIFIED per method; check each method page) | https://developers.google.com/youtube/v3/guides/uploading_a_video |
| Thumbnails | Max size raised 2MB -> 50MB on Sep 14 2026. Custom thumbnails need phone verification (higher daily limit needs channel history/ID verification) | revision_history; https://support.google.com/youtube/answer/9890437 |
| >15 min videos | Need phone verification (intermediate access); daily upload limit exists without verification, number not published | https://support.google.com/youtube/answer/9890437 |
| OAuth Testing mode | Authorizations and refresh tokens expire after 7 days in "Testing"; max 100 test users. "In production" removes expiry; unverified production app shows warning and caps at 100 users for sensitive scopes - fine for 1 owner | https://support.google.com/cloud/answer/15549945 |
| Resumable upload | Official sample: MediaFileUpload(resumable=True), chunksize=-1, exponential backoff, MAX_RETRIES=10 on 500/502/503/504 | https://developers.google.com/youtube/v3/guides/uploading_a_video |
| Shorts | Up to 3 min, vertical. No API "is Short" flag; Shorts is inferred from file shape. Square support and #Shorts requirement UNVERIFIED (page silent) -> use 9:16, <=180s, add #Shorts in title/description anyway | https://support.google.com/youtube/answer/10059070 |
| AI disclosure | Required for realistic synthetic content (real person doing/saying things, fake events). Not needed for AI scripts, voice cloning of yourself, non-realistic animation. Auto-labelled if C2PA present. Policy: repeat non-disclosure -> penalties | https://support.google.com/youtube/answer/14328491 |
| Audit form for appeal | Failed-audit appeal form exists | revision_history |

## 2. Comparison
| Route | Cost | Fully automatic | ToS risk | Notes |
|---|---|---|---|---|
| Own Data API (OAuth, google-api-python-client) | $0 | Yes | Low (official) | Private-lock risk unresolved; test on day 1 |
| Browser automation (Playwright/Chrome MCP on Studio) | $0 | Fragile | HIGH: YouTube ToS bans automated access without written permission (https://www.youtube.com/terms); session/CAPTCHA breaks | Fallback only |
| upload-post / similar relays | Paid tiers, UNVERIFIED price | Yes | Low-med; custom YouTube credentials use YOUR Google client (so same lock question); default audit status unconfirmed | https://docs.upload-post.com |
| Zapier/Make | Paid, UNVERIFIED | Yes | Low | Add-on cost eats $30 budget; limited thumbnails/captions |
| claude-youtube skill | $0 | n/a | n/a | READ-ONLY: youtube_auth.py = API key + OAuth for Analytics; quota_tracker.py lists videos.insert=100 (stale, now 1 in own bucket). Cannot upload. https://github.com/AgriciDaniel/claude-youtube |

## 3. Crucial decision
**Option X: Own API project, set to Production, no audit, test private-lock on day 1.**
- Current official reference says unverified projects are NOT forced private (videos/insert page).
- Quota need is ~500 units/video vs 10,000/day; no audit needed.
- Cost $0; full control of thumbnail, captions, publishAt, synthetic flag.

**Option Y: Apply for the compliance audit up front (or use relay).**
- Help Center still lists unverified API uploads as a lock trigger with no appeal (support.google.com/youtube/answer/7300965).
- Audit demands org name, HTTPS site, privacy policy/ToS, demo creds (audit form) - heavy for a solo channel, no turnaround time published.
- Locked videos must be re-uploaded; a relay with an audited project avoids it but adds cost/dependency.

**Recommendation: X.** A day-1 acceptance test (Section 5) settles it empirically. Only if the test video is forced private, file the audit (Y) and meanwhile publish manually or via relay.

## 4. One-time setup checklist
1. Channel: verify phone (https://www.youtube.com/verify) for thumbnails and >15 min; record ID verification if upload limit hit.
2. console.cloud.google.com -> new project "yt-automation".
3. APIs & Services -> Library -> enable "YouTube Data API v3".
4. OAuth consent screen: External, app name, your email; scopes: `youtube.upload`, `youtube` (needed for thumbnails/playlists/captions; UNVERIFIED which minimal set), add yourself as test user.
5. Credentials -> OAuth client ID -> type "Desktop app"; download client_secret.json.
6. **Publish app to "In production"** (consent screen -> Publish app) BEFORE first login so the refresh token does not expire in 7 days. Accept the "unverified app" warning on first auth (Advanced -> continue).
7. Run one local auth script (`InstalledAppFlow.run_local_server`, access_type=offline, prompt=consent); store token.json outside repo, ACL-restricted. Refresh tokens can still die if revoked, unused for 6 months, or password changed (general Google behavior, UNVERIFIED here); alert on `invalid_grant`.
8. `pip install google-api-python-client google-auth-oauthlib`.
9. Add Cloud quota alert (Quotas page) and check videos.insert bucket after test upload.

## 5. Interface spec
Input folder `out/<slug>/`: `final.mp4`, `thumbnail.png` (<=50MB, 16:9; skip for Shorts), `captions.srt` or `.vtt` (optional), `metadata.json`:
```
{ "slug":"...", "title":"<=100 chars", "description":"<=5000", "tags":[...],
  "categoryId":"28", "kind":"long|short", "madeForKids":false,
  "containsSyntheticMedia":false, "privacy":"private|public|unlisted",
  "publishAt":"2026-10-20T15:00:00Z|null", "playlistId":null,
  "defaultLanguage":"en" }
```
Output: `out/<slug>/upload.json` = `{videoId, url, state, uploadedAt, steps:{insert,thumb,captions,playlist}}`. Exit code 0 only if all requested steps done.
Rules: categoryId 28 = Science & Technology (UNVERIFIED id, check videoCategories.list, cost 1). If publishAt set, privacyStatus must be private (scheduling behavior, UNVERIFIED in this pass). Shorts: kind=short -> append #Shorts, enforce 9:16 and <=180s in a pre-check with ffprobe.
Flow: insert (resumable) -> poll videos.list(part=status,processingDetails) until uploadStatus=processed -> thumbnails.set -> captions.insert (400 units; or skip and rely on YouTube auto captions to save quota) -> playlistItems.insert -> videos.update only if flipping privacy.

## 6. Idempotency / retry
- State file `upload.json` written after each step; rerun resumes at first incomplete step. Never call insert again if videoId present.
- Pre-insert dedupe: if state lacks videoId but a crash may have occurred, query channel uploads playlist (playlistItems.list, 1 unit) for same title in the last 24h before re-inserting. Embed `slug` in description footer as a key.
- Resumable upload: persist the resumable session URI; on restart resume it (Google session URIs live ~1 week, UNVERIFIED) else restart. Use official pattern: chunked (e.g. 8MB, multiple of 256KB), backoff 2^n + jitter, max 10 retries on 500/502/503/504 and network errors; fail fast on 400/401/403.
- quotaExceeded (403) -> sleep until midnight Pacific, then retry; uploadLimitExceeded -> stop, alert, retry in 24h.
- invalid_grant -> halt and alert (needs manual re-auth).
- Windows: use pathlib, open file in binary, run through Task Scheduler with "run whether logged on or not"; keep token path absolute; set no sleep during upload (powercfg).

## 7. Acceptance tests
1. Auth: script lists channel (channels.list mine=true), token refresh works; token still valid after 8 days (proves Production mode).
2. Upload 20 s test video as `private` with thumbnail -> response videoId; poll until processed.
3. Verify via videos.list: privacyStatus=private, containsSyntheticMedia as sent, madeForKids as sent.
4. **Private-lock probe:** flip to `unlisted`/public via videos.update (50 units), open the URL in a logged-out browser. If it snaps back to private or Studio shows "locked", Option X failed -> audit.
5. Scheduling: insert with publishAt = now+10 min; verify it goes public.
6. Re-run script with same slug: zero new videos created (idempotency).
7. Kill process mid-upload; rerun resumes.
8. Short test: 9:16, 45 s, verify it appears under Shorts tab (UNVERIFIED how to query; check manually).
9. Delete test videos via Studio.

## Gaps
No explicit published number for new-channel daily upload limits. Square-Short and #Shorts requirement, method-level scope minimums, scheduling nuance, upload-post/Zapier pricing UNVERIFIED.
