# 10 - Policy, Monetization & Legal Risk (researched 2026-10-14)

Labels: [V] = read on official page this session; [S] = credible secondary reporting; UNVERIFIED = not confirmed.

## 1. Current facts

**Inauthentic content (YPP).** Renamed from "repetitious content" on 2025-07-15 [V: https://support.google.com/youtube/answer/1311392]. Page text: content that "looks like it's made with a template", interchangeable/mass-produced videos, or AI content from generic templates without the creator's original insight is not monetizable; same intro/outro with differing main content is fine.
**July 16, 2026 clarification** [S: https://www.netinfluencer.com/youtube-trust-and-safety-chief-details-three-categories-of-content-barred-from-monetization/ (2026-07-21); TechCrunch/Nieman Lab coverage]: Matt Halprin (YouTube T&S) split it into 3 non-monetizable buckets: (1) generic/repetitive/template mass-produced videos, incl. tutorials repeating content already saturating the platform; (2) distressing/emotionally manipulative content made for views; (3) **AI personas on finance, legal, medical/health topics**. He said "no new policy"; AI itself is fine if original/high quality; rules apply whether made with "AI, CGI, or no additional tools". Evaluation is **channel-level** (too much of any bucket = no monetization), not per video. Suspended: 21 days to appeal, reapply after 90 days. YPP rules govern money, Community Guidelines govern presence. Flag counts don't affect YPP evaluation. I could not retrieve YouTube's own page for this split -> treat exact boundaries of "sensitive topics" as UNVERIFIED.
**Reports of enforcement:** claims of 16 channels / 35M subs wiped [S, AIR Media-Tech etc.]; UNVERIFIED against YouTube. Individual "faceless AI channel demonetized, appeal pending" case studies exist, anecdotal.

**Altered/synthetic disclosure** [V: https://support.google.com/youtube/answer/14328491, no effective date shown, (c)2026]: Disclose via Studio "AI use" when realistic content is generated/altered: real person saying/doing what they didn't; altered real event/place; realistic scene that didn't occur; generated music as main focus. NOT required: non-realistic/animated/fantastical content; minor edits (captions, upscaling, audio repair, cloning your own voice for voiceover); **AI-assisted scripts, outlines, titles, thumbnails**. Labels may be auto-applied (YouTube AI tools, C2PA metadata). Repeated non-disclosure -> manual label, removal, or YPP suspension. Disclosure doesn't limit reach/monetization. => Animated explainer with TTS likely needs no label, but a conservative gate sets it anyway when any photoreal image/synthetic-human voice imitating a real person is used.

**YPP thresholds** [V: https://support.google.com/youtube/answer/72851]: 1,000 subs + 4,000 public long-form watch hours (12 mo), OR 1,000 subs + 10M public Shorts views (90 days). Shorts-feed watch hours don't count toward 4,000h. **Changes effective 2027-02-01** (existing partners accept new modules by 2027-01-31) [V page mentions dates; details S: https://www.newsshooter.com/2026/08/10/youtube-updates-its-partner-program/ , https://www.searchenginejournal.com/youtube-updates-partner-program-terms-shorts-payout-rules/585331]: new applicants 8,000 h/365 d or 20M Shorts views/90 d (500-sub fan-funding tier unchanged); existing partners need 10M Shorts views/90 d to earn Shorts ad revenue. Plan for the stricter bar; pending-application transition UNVERIFIED.

**Copyright of AI visuals:** US Copyright Office Part 2 (2025-01-29): prompts alone don't confer authorship; human selection/arrangement/modification can [S: https://www.jonesday.com/de/insights/2025/02/copyrightability-of-ai-outputs-us-copyright-office-analyzes-human-authorship-requirement]. Programmatically generated vector/code animation (own code, own design) is human-authored work; raw generative-model images are not protectable (others may copy them). Favor code-drawn visuals.
**Music:** YouTube Audio Library: most tracks no attribution; CC BY tracks need credit in description; license scope outside YouTube unclear [S: https://support.google.com/youtube/answer/3376882]. Safer: CC0 or self-generated/synthesized music (check generator ToS), log license per track.
**TTS license:** Kokoro-82M advertised as Apache-2.0, but the model card showed conflicting "Creative Commons" heading; repo not checked -> UNVERIFIED, check LICENSE and voice-pack terms before shipping. Cloud TTS (ElevenLabs etc.): paid plan needed for commercial use (UNVERIFIED, check plan ToS). Never clone a real person's voice.
**Fonts/assets:** use OFL/Apache fonts (Google Fonts) and store license file; no logos/screenshots of brands beyond fair use (UNVERIFIED legal view; not legal advice).
**Content ID/quoting:** quoting news text, code with restrictive licenses, or screenshots risks claims/takedowns; Content ID rarely hits own-drawn visuals. Re-render code snippets in own style, attribute and respect repo licenses (MIT/Apache attribution), short quotes only.
**Shorts:** same YPP/inauthentic rules; threshold is 10M views (20M from 2027), so Shorts are a discovery tool, not a quick income path.
**Claude subscription for automation (flag only):** Consumer Terms reportedly bar automated access except via API key or explicit permission; from 2026-06-15 programmatic/headless use reportedly draws from a separate credit pool; OAuth subscription auth is meant only for Claude Code/Claude.ai [S: https://www.theregister.com/ai-ml/2026/05/14/anthropic-tosses-agents-into-the-api-billing-pool/5240748]. Primary Anthropic terms not retrieved -> UNVERIFIED. Recommend API key for an always-on pipeline; ask Anthropic/read current terms.

## 2. Risk register

| # | Risk | Likelihood | Impact | Mitigation | Source |
|---|---|---|---|---|---|
| 1 | YPP denied/removed as inauthentic (templated, AI voice, interchangeable) | High if fully autonomous | Critical (no revenue) | Original angle/analysis per video, varied structure, human review, unique visual identity, limit upload cadence | support.google.com/youtube/answer/1311392 |
| 2 | Medical/financial/legal topics with AI voice persona | Medium | High | Avoid those niches; tech only; no "advice"; no personified AI host on sensitive topics | netinfluencer (Jul 2026) |
| 3 | Missing synthetic label | Low (animated) / Med (photoreal) | Medium | Auto flag + conservative default | answer/14328491 |
| 4 | Factual errors in technical content | High | High (trust, strikes for misinformation) | Source list, claim-check vs cited sources, human sign-off | UNVERIFIED general |
| 5 | Copyright claim (music, quoted code/news/screenshots) | Medium | Medium | CC0/own music, license log, own-rendered code, short quotes | answer/3376882 |
| 6 | TTS/model license violation | Low-Med | Medium | Verify LICENSE; record in manifest | HF model card (conflicting) |
| 7 | Spam/mass-upload pattern, duplicate titles | Medium | High | Cap uploads (e.g. <=1 long/day), similarity gate | inauthentic policy |
| 8 | Threshold shift 2027 (8,000h / 20M) slows monetization | High | Medium | Plan on long-form, accept terms by 2027-01-31 | newsshooter 2026-08-10 |
| 9 | AI visuals not copyrightable / copied | Medium | Low | Code-drawn assets | Jones Day 2025 |
| 10 | Anthropic ToS on subscription automation | Medium | Medium | Use API key | The Register 2026-05-14 |
| 11 | Reused-content flag from scraping trending news | Medium | High | Transform + add analysis; never paste article text | answer/1311392 |

## 3. Pre-publish gates (codeable)

1. `ai_disclosure` field in upload (status.containsSyntheticMedia via API; verify field name in current API docs - UNVERIFIED): true if any photoreal image/real-person-likeness audio.
2. Description must contain: source URLs (>=3 primary), music/asset credits (CC BY text), "AI-assisted script, human reviewed" line.
3. Sensitive-topic classifier: if medical/financial/legal -> block publish (or route human + no AI persona).
4. Script similarity: embedding/n-gram cosine vs all prior scripts < 0.8; title dedupe (edit distance/semantic); structure-variation check (no >3 consecutive same outline template).
5. Originality checks: script contains >=1 author-stated opinion/comparison/own demo; ratio of source-quoted text < 10%; every factual claim has a source id.
6. Asset ledger: every music/font/image/model has license in allowlist (CC0, OFL, Apache, MIT, YT Audio Library no-attribution).
7. TTS: voice not on real-person blocklist; license file present.
8. Cadence limiter: max N uploads/day/channel; Shorts derived must have distinct hook, not clip-spam.
9. Human approval token present (see decision).
10. Render QA: duration > min, no black frames, captions present, loudness normalized.

## 4. Crucial decision

**Option X: Fully autonomous publish.**
- Facts: YPP evaluates the whole channel for template/mass-produced content (netinfluencer, 2026-07); no human step makes variety hard to prove.
- Unreviewed technical claims have no stopper; misinformation risk.
- Enforcement is immediate with no phase-in (S), appeal wait 21 days, reapply after 90 days.

**Option Y: Human approves each video (publish as private/unlisted until approved) - RECOMMENDED.**
- Facts: YouTube states AI-assisted videos with original value stay monetizable; human value-add is the defense (answer/1311392).
- Approval takes ~2-5 min with an automated checklist report; pipeline remains 95% automatic.
- Creates audit trail for appeals and disclosure correctness.

## 5. Acceptance tests
- Upload with photoreal asset and no disclosure flag -> pipeline blocks.
- Medical/finance topic -> blocked or routed to human, never auto-published.
- Two scripts with >0.8 similarity -> second rejected.
- Asset with unknown license -> build fails.
- Description missing sources -> publish rejected.
- Without approval token, video stays private.
- 30-day sample of 10 videos: outlines differ structurally (manual audit), none flagged by YouTube.
- Quarterly re-fetch of answer/1311392, 14328491, 72851 and diff for changes.
