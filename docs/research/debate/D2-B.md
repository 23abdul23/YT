# D2-B: Against "API key, not headless Claude Code" (adversary B)

## Thesis
At launch, run LLM stages with `claude -p` on the user's existing subscription, skills used as-is, behind a thin `llm/` adapter so an API backend can be swapped in later. The proposition spends dev effort and cash to remove a risk that Anthropic's own pages do not describe as a prohibition for this use.

## Arguments
1. **Anthropic documents this use as supported.** The support article (fetched 2026-10-14, https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan) says "You can still use the Claude Agent SDK, `claude -p`, and third-party apps with your subscription limits." It says the June 15 change is paused ("nothing has changed") and that Max/Team plans add monthly API credits as of Oct 7. It does not prohibit scripts.
2. **The ToS restrictions target a different scenario.** The legal page (https://code.claude.com/docs/en/legal-and-compliance) bars developers "building products or services" and "route requests through ... plan credentials on behalf of their users." It expressly allows "an end user [to sign] in to the unmodified Claude Code binary with their own Claude subscription." A one-user channel pipeline on the user's own PC, unmodified binary, own login, fits that carve-out. The report's "gray zone" is real only for "ordinary, individual usage" of limits. UNVERIFIED: whether a daily batch counts as "ordinary".
3. **Cost.** Marginal cash is $0 versus about $9/month for the API (02-scripting.md section 8). That is 30% of the $30 cap, and it competes with TTS, stock assets and retries. The report's $0.6-1.0 per video is its own estimate, not measured.
4. **Effort and quality.** The skills are Markdown prompts that `claude -p` loads natively. The API path needs vendored prompts, a hand-built research loop and web_search at $10 per 1k searches (02 section 1, section 3). Agentic WebSearch/WebFetch comes built in, which is the report's own "best quality on technical facts" rating (02 section 4).
5. **Controls exist.** `--max-turns`, `--allowedTools`, JSON output and, per a third-party source, `--max-budget-usd` (09 section 1, V-weak). The `OAuth token` route for scripts is documented (authentication doc, cited in 02 section 2).

## Strongest point FOR the proposition, and my answer
Enforcement "without prior notice" could break the pipeline or hit the personal account, and policy flipped twice in four months. Answer: the failure mode is a stage error, not channel loss. Stage idempotency and the cache (09 section 5) make it resumable. A backend switch is a config change if the adapter is built on day one. Also, the 4-month policy swing cuts both ways: the API price table could also change.

## What would change my mind
- Anthropic text saying scheduled or unattended `claude -p` is outside "ordinary individual usage", or limits too tight for about 40 runs per month (measure this week).
- A rate-limit collision with interactive use that causes missed uploads.
- Per-video API cost measured under $0.30.
- Any report of accounts banned for personal cron use (none found by me, but I searched little).

## Scores for my alternative (headless `claude -p` + API fallback adapter)
- Cost: 5
- Output quality: 4
- Policy risk: 2
- Implementation effort: 4
- Maintainability: 3 (CLI flags and JSON fields drift; 09 section 8)
