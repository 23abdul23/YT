# D7-B (against): do not rely on unaudited API upload for launch

## Thesis
The forced-private rule is unsettled, and the evidence that it still applies is stronger than the single contrary sentence. A day-1 test cannot prove it is gone. So launch with a semi-manual Studio upload of a pre-built package (Option Z), and file the audit in parallel only if full automation is wanted later.

## Arguments
1. Three official sources still describe the lock; one says otherwise. The revision history (2020-07-28) says videos from unverified projects created after that date "will be restricted to private viewing mode" (https://developers.google.com/youtube/v3/revision_history). The Help page still says there is no appeal and the video must be re-uploaded (https://support.google.com/youtube/answer/7300965). The developers.google.cn mirror of the videos reference carries a restriction banner (found via search; page not fetched, UNVERIFIED). The sole contrary sentence is in the privacyStatus field description: "not restricted to private viewing mode" (videos/insert). The revision history has no entry that reverses the 2020 rule (page read only to char 100000 of 240024; UNVERIFIED beyond that).
2. A pass on day 1 does not settle it. The lock is applied per project and reported only to the creator by email (search summary, UNVERIFIED). The API returns success either way. Enforcement can also change after a short test. A 20-second private test video may not trigger anything.
3. A failure costs real money and credibility. Locked videos cannot be appealed and must be re-uploaded (Help page above). A scheduled public release can silently turn into private videos. In a fully automated channel nobody may notice for days.
4. The audit is not trivial, but it is not needed for Z. The form needs an org name, HTTPS site, privacy policy, ToS and demo credentials (report 07 section 1, https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits). No turnaround time is published. So do not block launch on it; use Z first.
5. Policy exposure exists. Developer Policies I.2 bars automating "uploads" without express user consent. An owner's own upload is consented, so this is low risk, but any audit would look at it (https://developers.google.com/youtube/terms/developer-policies).

## Strongest point FOR D7, and my answer
Point: the current reference text explicitly says unverified projects are not restricted, the test costs $0, and a failure can be fixed by filing the audit afterwards.
Answer: the fix is slow and has no published turnaround, and the test result is not durable. Z costs only a few minutes of owner time per upload. Z also gives a clean fallback if the audit fails or is slow.

## What would change my mind
- A dated Google changelog entry that removes the 2020 rule.
- A recent first-hand report (2026) of a post-2020 unverified project publishing public videos for weeks.
- Google staff confirmation.

## Scores for Option Z (1-5, 5 = easiest/best)
- Cost: 5
- Output quality: 4
- Policy risk (5 = lowest): 5
- Implementation effort (5 = easiest): 4
- Maintainability: 4 (this is not full automation; the pipeline stays modular, so the API upload can be added once the lock question is settled)
