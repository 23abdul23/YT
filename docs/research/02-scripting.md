# 02 - Scripting component (research -> factual script -> storyboard)
Date 2026-10-14. Items without a source are marked UNVERIFIED.

## 1. What claude-youtube outputs (read locally + raw GitHub)
- Repo: https://github.com/AgriciDaniel/claude-youtube (skill = Markdown prompts + 6 Python YouTube-API scripts; install = copy into `~/.claude/skills/`) [README].
- Orchestrator (SKILL.md) REQUIRES three context inputs before any sub-skill: niche, size tier, goal. If missing it "asks". This is the interactivity problem.
- `script`: inputs topic, length, channel type, audience, key points, tone, CTA. Output = free-form Markdown (hook Grab/Promise/Stakes, intro, content blocks, mid-CTA ~25%, re-hook ~60%, outro, pattern-interrupt log, retention-risk map). Rules: ~150 wpm (+-10%), interrupt every 60-90 s, bracket tags `[B-ROLL CUE] [GRAPHIC] [SOUND EFFECT] [CAMERA CHANGE] [UNEXPECTED STAT]`. It assumes an on-camera creator (CAMERA CHANGE) and has NO fact/citation step. Not machine-readable.
- `shorts`: inputs niche, idea/long-form, goal, audience. Output = Markdown table (timestamp | visual | audio | notes), visual change every 3 s, loop ending, title 4-6 words, 3-5 hashtags, viewed-vs-swiped prediction. Length guidance: 13 s or 60 s.
- `hook`: 5 variants x ~75 words, each with mechanism + drop-off risk. `metadata`: 3 titles, description, tags, chapters, thumbnail brief, checklist. `thumbnail`: brief + 3 A/B concepts; can call NanoBanana (Gemini) MCP if present.
- Non-interactive use: skill is just prompt text, so (a) pre-fill the 3 context answers in the prompt/CLAUDE.md ("niche=trending tech explainers; size=New; goal=Growth; do not ask questions") and (b) demand JSON output. Cleaner: vendor the sub-skill .md files + retention guide into our own repo as system-prompt files and call them from API/CLI; skip the router and DataForSEO/Agent bits. Sources: local copies of cy-SKILL.md / cy-script.md / cy-shorts.md; raw files hook.md, metadata.md, thumbnail.md, retention-scripting-guide.md.

## 2. Headless Claude Code, auth, ToS (official)
- `claude -p` runs non-interactively; `CLAUDE_CODE_OAUTH_TOKEN` via `claude setup-token` is documented for CI/scripts: https://code.claude.com/docs/en/authentication
- If `ANTHROPIC_API_KEY` is set, `-p` uses it over the subscription (silent pay-per-token): same page.
- ToS: OAuth is "intended exclusively" for subscribers for ordinary use of Claude Code; developers building products/services (incl. Agent SDK) "should use API key authentication"; no routing other users through subscription credentials; limits "assume ordinary, individual usage": https://code.claude.com/docs/en/legal-and-compliance . Reading: a personal single-user cron on your own machine is defensible but a gray zone (24/7 automated pipeline is not "ordinary individual usage"); Anthropic may enforce "without prior notice". Not legal advice.
- Billing status: help article says the June-15 Agent SDK credit change was paused, then an Oct 7 2026 update says `claude -p`/Agent SDK still work with subscription limits and Max/Team plans include monthly API credits; amounts not given: https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan (two fetches described it slightly differently -> treat details as UNSTABLE, re-check before launch).

## 3. Prices (official, https://platform.claude.com/docs/en/about-claude/pricing)
| Model | Input $/MTok | Output $/MTok | Cache hit | Batch (-50%) |
|---|---|---|---|---|
| Sonnet 5.5 | 2 | 10 | 0.10 | 1 / 5 (computed) |
| Haiku 5.5 (<=100k prompt) | 0.10 | 0.50 | 0.01 | 0.05 / 0.25 (computed) |
| Haiku 4.5 | 1 | 5 | 0.10 | 0.50 / 2.50 |
| Opus 5.5 | 4 | 20 | 0.20 | - |
Web search tool: $10 / 1,000 searches + tokens (same page). Cache write 5m = 1.25x input. Batch = 50% off, stacks with caching (same page).

## 4. Comparison table (LLM options)
| Option | Cash cost/long video | Quality on technical facts | Automation risk | Notes |
|---|---|---|---|---|
| A. Headless Claude Code on subscription (`claude -p`) | ~$0 marginal (Pro/Max already paid) | Best (agentic WebSearch/WebFetch + skills natively) | ToS gray zone; shared rate limits; limits drift (see above) | Zero dev for skill loading |
| B. Anthropic API, Sonnet 5.5 (+ web_search tool) | ~$0.6-1.0 | High | None (supported path) | Needs own orchestration code; cap via budget |
| C. API Haiku 5.5 only | ~$0.05-0.15 | Lower reasoning; fine for extraction/claim-check | None | Use as verifier, not as author |
| D. Local LLM (Ollama, 7-14B) | $0 + electricity | Worst on current tech facts (stale, hallucination-prone; no browsing without own RAG) | None | GPU unknown (UNVERIFIED); use only as fallback |
| E. Mixed (recommended): Sonnet 5.5 write + Haiku 5.5 verify + Batch for Shorts | ~$0.7 long / ~$0.08 Short | High | None | |

## 5. THE crucial decision
**Option X: Headless Claude Code on subscription.**
1. Marginal cost ~$0 and it loads the claude-youtube skill natively (`claude -p`, OAuth token documented for scripts) [authentication doc].
2. Anthropic says OAuth is for "ordinary use" and builds on Agent SDK "should use API key" [legal page]; enforcement "without prior notice".
3. Subscription limits are shared with your interactive use and the billing policy flipped twice in 4 months (June 15 announcement -> paused -> Oct 7 update) [support article].

**Option Y: Anthropic API key (Sonnet 5.5 writer + Haiku 5.5 verifier).**
1. ~$0.7/long video, ~$0.08/Short => ~$9/month at 8 long + 30 Shorts (my estimate below), inside the $30 cap.
2. Explicit sanctioned path for automation/products [legal page]; per-token billing gives hard budget caps and no account-ban risk to your personal Claude account.
3. Batch -50% and caching (hit 0.1x) apply [pricing]; web_search tool available at $10/1k searches.

**Recommendation: Y** (the scripting stage is the pipeline's riskiest ToS surface; a channel running 24/7 should not depend on a subscription). Use X only for manual/dev prototyping. Do not leave `ANTHROPIC_API_KEY` set in shells where you intend subscription billing.

## 6. Pipeline: research -> script -> storyboard (non-interactive, API)
1. **Topic brief** (input from trend component): topic, angle, length class (long|short).
2. **Research pass** (Sonnet 5.5 + web_search/web_fetch): output `sources[]` (id, url, title, date fetched, quote <=25 words) from primary sources only (official docs, RFCs, repos, papers, release notes). Min 5 for long, 2 for Short.
3. **Script pass**: prompt = vendored script.md/shorts.md/hook.md rules + "every sentence carrying a factual claim must reference source ids; no claims outside sources; no on-camera tags; narration-only".
4. **Claim-check pass** (fresh context, Haiku 5.5 or Sonnet): extract atomic claims (numbers, versions, dates, names, causal statements) from narration; for each, mark SUPPORTED / CONTRADICTED / NOT_FOUND against the stored quotes (re-fetch the URL if needed). Any non-SUPPORTED -> rewrite sentence or delete (max 2 loops), else fail video to a review queue.
5. **Storyboard pass**: convert script to `storyboard.json` (below). Validate with JSON Schema; reject on failure.
6. Publish `sources` as a "Sources" block in the description (metadata sub-skill gets them) - doubles as trust signal. Hard rule: dates/version numbers must be re-verified (the model's knowledge is stale vs 2026-10).

## 7. `storyboard.json` schema (draft 2020-12 summarized)
```json
{
  "video_id": "string", "format": "long|short", "title": "string",
  "target_duration_s": 540, "wpm": 150, "language": "en",
  "sources": [{"id":"S1","url":"https://...","title":"","retrieved":"2026-10-14","quote":""}],
  "scenes": [{
    "scene_id": "s01",
    "section": "hook|intro|block|midcta|rehook|outro|loop",
    "narration": "plain TTS-ready text, no tags",
    "word_count": 38,
    "est_duration_s": 15.2,
    "claims": [{"text":"","source_ids":["S1"],"checked":"SUPPORTED"}],
    "visual": {
      "type": "anatomy_figure|code|terminal|diagram|chart|stock_text_card|screenshot",
      "spec": "what is on screen, 1-2 sentences",
      "on_screen_text": ["max 8 words per line"],
      "motion": "zoom|pan|reveal_steps|none",
      "changes_at_s": [0, 3, 6]
    },
    "anatomy_figure": {
      "needed": true,
      "brief": "components, labels, relationships, reveal order",
      "elements": [{"id":"e1","label":"","kind":"box|arrow|icon|code"}],
      "reveal_order": ["e1","e2"]
    },
    "sfx": "optional", "pattern_interrupt": true,
    "caption_emphasis": ["words to highlight"]
  }],
  "outro": {"cta":"", "next_video_tease":""},
  "meta": {"title_options":[], "description":"", "tags":[], "hashtags":[], "chapters":[{"t":0,"label":""}]}
}
```
Constraints in validator: sum(est_duration_s) within 10% of target; Short: 13-60 s (use 13 or 55-60 s), visual change <=3 s, last scene mirrors scene 1 (loop); long: pattern interrupt <=90 s apart, mid-CTA ~25%, re-hook ~60% [script.md quality criteria]. Duration is final only after TTS - the render stage overwrites `est_duration_s` with real audio length.

## 8. Per-video cost estimate (API, my arithmetic from the pricing table)
Long (8-12 min, ~1,500 words): research 60k in + 4k out + 8 searches ($0.08); script 25k in/4k out; claim-check 40k in/4k out (Haiku 5.5: ~$0.01); storyboard 10k in/12k out; ~1 retry. Sonnet 5.5 ~ 130k in x $2 + 25k out x $10 = $0.26 + $0.25 = ~$0.51; + searches 0.08 + Haiku 0.01 = **~$0.6-0.8**.
Short: 15k in/3k out -> **~$0.06-0.10** (about $0.04 via Batch).
Month (8 long + 30 Shorts): ~$5.6 + ~$3 = **~$9**; keep $5 headroom for retries. Subscription route: $0 marginal (but see ToS).

## 9. Acceptance tests
1. Non-interactive: pipeline runs with no stdin prompt; zero clarifying questions (grep output for "?" questions = fail).
2. Schema: storyboard validates against JSON Schema 100%.
3. Duration: long narration 1,350-1,650 words; sum of scene durations within +-10% of target; Short 13 s or 50-60 s.
4. Citations: every scene with a factual claim has >=1 `source_ids`; all URLs return HTTP 200; every quote appears in the fetched page text (string match).
5. Claim-check: 0 CONTRADICTED, 0 NOT_FOUND after loop; human spot-check of 10 random claims on first 5 videos: >=95% correct.
6. Staleness: all version numbers/dates in narration match a source fetched within 7 days.
7. Retention structure: hook has Grab/Promise/Stakes <=30 s; interrupt gap <=90 s (long) / visual change <=3 s (Short); Shorts loop scene present.
8. Cost: logged tokens x price <= $1.00 per long, <= $0.15 per Short; monthly alert at $20.
9. Safety: no copyrighted-text blocks >15 words quoted; no on-camera tags ([CAMERA CHANGE]) in narration.
