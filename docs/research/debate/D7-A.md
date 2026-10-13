# D7-A (FOR): test first, audit only if forced private

## Thesis
Skip the audit. The day-1 test costs about 1 quota unit plus a 20 s video, and it settles an empirical question the docs contradict. The audit demands an organisation, a site and demo credentials, and has no published turnaround. That is a poor first move for a solo channel.

## Arguments
1. **The reference page was refreshed 8 days ago and says no restriction.** videos.insert ("Last updated 2026-10-08 UTC") says: "Videos uploaded from unverified API projects are not restricted to private viewing mode." (https://developers.google.com/youtube/v3/docs/videos/insert). It also says unset privacy defaults to public, and that some uploads default to private by creator account settings. Google touched this page recently with that sentence intact, so it is probably not a stale leftover.
2. **The contrary evidence is old or secondhand.** The 2020-07-28 revision-history entry and a 2020 StackOverflow answer (https://stackoverflow.com/questions/64079139) are from 2020. The Help page (https://support.google.com/youtube/answer/7300965) is a generic "locked as private" page. Its unverified-API line sits in a bulleted "not a complete list". Outstand's 2026 blog repeats the 2020 text (https://www.outstand.so/blog/youtube-api-pricing-quota), but it sells a relay, so it has an incentive. I found no 2026 first-hand failure report. UNVERIFIED that none exist.
3. **A failed test costs almost nothing.** Per the report, a private-lock appears as a videoId plus a locked state on a throwaway video. Re-upload is "required" only for that one test file. Loss: a few minutes.
4. **The audit is heavy and may not fit.** It needs org legal name, HTTPS site, privacy policy, ToS and demo credentials (report, section 1). One StackOverflow answer claims private-use apps "won't approve it" (UNVERIFIED, anecdote). Filing first risks a rejection without evidence it was needed.
5. **Quota is not a constraint.** About 500 shared units per video against 10,000/day (report), so no extension is needed either.

## Strongest opposing point and answer
Opposing: Google's own sources conflict. If the Help page and revision history are right, every production video is locked private with no appeal, and the owner finds out only after the pipeline is built.
Answer: that is why the test runs on day 1, before any content investment, with `status.privacyStatus` set to public or unlisted. The probe uses videos.update 50 units, then a logged-out view (report, section 7, step 4). Also, "locked" here means the video is private with no appeal, and the fallback is manual upload of one test file. It does not hurt the channel: Help says no strike is applied.

## Evidence that would change my mind
- The test video snaps to locked/private, or a 2026 first-hand report of lock on a Production consent screen.
- Google confirming the lock applies at project creation date, not at upload.
- Locks appearing only after N uploads (so one test passes falsely). Run 3 uploads over 3 days.

## Scores (5 = best / easiest)
- Cost: 5
- Output quality: 4
- Policy risk: 3 (docs conflict, official API otherwise)
- Implementation effort: 4
- Maintainability: 4
