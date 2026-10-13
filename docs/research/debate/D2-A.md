# D2-A: FOR the Anthropic API key (Sonnet 5.5 write, Haiku 5.5 claim-check, JSON prompts)

## Thesis
Run every LLM stage on the API. It fits the $30 cap with about 3x headroom. It is the only path Anthropic's docs explicitly sanction for an unattended product. It also gives hard budget caps and schema-enforced output.

## Arguments
1. **Cost fits.** Verified prices: Sonnet 5.5 is $2 in / $10 out per MTok. Haiku 5.5 (prompts up to 100k) is $0.10 / $0.50. Cache hits on Sonnet 5.5 are $0.10 (https://platform.claude.com/docs/en/about-claude/pricing, fetched today). Report estimate: about $0.6-0.8 per long video and about $0.08 per Short, so about $9/month for 8 long + 30 Shorts (02-scripting.md s8, the report's own arithmetic). Batch (-50%) and caching cut this further.
2. **Policy.** The legal page says OAuth is "intended exclusively" for subscribers and supports "ordinary use". It says developers "building products or services... including those using the Agent SDK, should use API key authentication". It also says advertised limits "assume ordinary, individual usage" and enforcement may come "without prior notice" (https://code.claude.com/docs/en/legal-and-compliance, fetched today). A 24/7 channel pipeline sits outside that wording at best, and the risk is losing the personal account that also runs the user's interactive Claude Code. The API path has no such exposure.
3. **Billing is unstable on the subscription side.** The support article changed twice in 4 months (02-scripting.md s2, s5). A pipeline should not depend on a policy that moves.
4. **Reliability and quality.** API calls give deterministic budgets and per-call token logs. Rate limits are not shared with the user's interactive sessions. Structured JSON output suits the storyboard schema validation in 02 s7. Haiku 5.5 as a separate-context verifier costs about $0.01 per video (02 s8).
5. **Vendoring is easy.** The claude-youtube skill is plain Markdown prompts (02 s1). Vendoring them as system prompts loses nothing the pipeline needs.

## Strongest opposing point and answer
**Opposing:** subscription `claude -p` costs about $0 marginal, loads skills natively, and 09-orchestration.md already designs a `llm/claude_cli.py` wrapper.
**Answer:** The saving is about $9/month, under a third of the budget, and you pay for it in ToS exposure and rate-limit coupling. The "zero dev" claim is weak. The pipeline already needs its own orchestration, validation and JSON schema, so a thin SDK call replaces the wrapper. Skills are only Markdown. `claude -p` also has an extra failure mode: if `ANTHROPIC_API_KEY` is set, it silently bills per token (02 s2).

## What would change my mind
- Anthropic stating in writing that a single-owner personal cron on a subscription is permitted. UNVERIFIED: the support-article details are unstable and I could not re-fetch them (Firecrawl was rate-limited).
- Measured API cost above about $20/month after the first 10 videos.
- Evidence that Haiku 5.5 claim-checking misses errors a Claude Code agentic loop catches (no benchmark in the report).

## Scores (1-5)
- Cost: 4 (about $9 of $30)
- Output quality: 4 (Sonnet 5.5, schema-forced JSON; no agentic browsing unless the web_search tool is used at $10/1k searches)
- Policy risk: 5 (sanctioned path)
- Implementation effort (5 = easiest): 3 (own orchestration, but the SDK is simple)
- Maintainability: 5 (explicit budgets, pinned models, no CLI output parsing)
