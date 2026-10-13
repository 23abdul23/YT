# 09 Orchestration, Scheduling, State, Secrets, Observability (2026-10-14)

Evidence labels: [V] = source fetched/searched this session; [U] = UNVERIFIED (from my background knowledge or only third-party hearsay).

## 1. Comparison table

| Option | Windows 11 native | Fit for 1 PC, <=$30/mo | Verdict |
|---|---|---|---|
| **Python CLI + SQLite job table + Task Scheduler** | Yes (stdlib `sqlite3`, `schtasks`) [U, standard] | $0, zero daemons, debuggable | **Pick** |
| Prefect 3 (self-hosted server) | Vendor docs claim first-class Windows, PowerShell, can run server as a Windows service [V: https://docs.prefect.io/v3/how-to-guides/self-hosted/server-windows] | $0 but adds a server + DB for one linear DAG | Good upgrade path, overkill now |
| Dagster | Installs on Windows (pywin32/psutil deps); no explicit statement found that webserver+daemon are supported natively; Python-version range sources disagree [V: https://docs.dagster.io/getting-started/install] | $0, heavy asset model | Skip |
| Airflow | No native Windows support; maintainers said no plans, WSL2/Docker only, WSL2 "not recommended for production" [V: https://github.com/apache/airflow/issues/10388] | Heavy (scheduler+webserver+DB) | Reject |
| n8n self-hosted | Runs via npm/Docker [U]; fair-code licence [U] | Good for webhooks/Telegram glue, poor for hash-cached media stages, JSON-in-GUI is hard to version | Optional only for approval webhook; not core |
| Temporal | Dev server binary exists for Windows [U]; needs worker + server | Overkill for ~1 run/day | Reject |
| Make / Zapier | SaaS; cannot run ffmpeg/Chrome locally | Per-operation pricing, ~free tiers too small [U] | Reject |
| Claude Code `claude -p` as the LLM-step runner | Works on Windows. Headless via `-p/--print`, `--output-format text|json|stream-json`, `--permission-mode`, `--allowedTools` [V: https://docs.claude.com/en/docs/claude-code/headless]; `--max-budget-usd` and `--max-turns` cap spend/turns per run (third-party reference, verify with `claude --help`) [V-weak: https://www.mintlify.com/VineeTagarwaL-code/claude-code/reference/commands/cli-flags]; JSON result carries cost + session_id, field name differs by source (`total_cost_usd` vs `cost_usd`) so parse defensively [V: same headless docs search] | Uses the existing subscription/API; LLM steps only | **Use as a stage worker, not as the orchestrator** |
| Claude Code desktop scheduled tasks (`mcp__scheduled-tasks__*` tools: create/list/run/update/delete, `list_task_runs`) and cloud `/schedule` routines | Local scheduled tasks exist in this app (tools present in this session). Whether they fire when the app is closed or PC asleep: [U] | Spends model tokens just to trigger a script; non-deterministic | Not for the trigger; fine as a weekly "review analytics" LLM job |
| GitHub Actions | Hosted job limit 6 h; free private-repo minutes 2,000/mo on Free plan; Windows 2x multiplier (secondary sources) [V: https://docs.github.com/en/actions/reference/usage-limits-billing-and-administration] | No GPU; Chrome headless works on runners [U]; secrets leave the PC; TTS/model caches must be re-downloaded each run | Use only for CI tests of the pipeline code, not production renders |

## 2. THE crucial decision: who owns scheduling + state?

**Option X: Plain Python CLI (`ytauto run`) + SQLite + Windows Task Scheduler (recommended).**
1. Task Scheduler is built into Windows 11, supports "run whether user logged on or not", "wake the computer", and restart-on-failure [U, standard feature]. Zero extra processes, so nothing to patch or crash.
2. Airflow is explicitly unsupported natively [V: github.com/apache/airflow/issues/10388] and Prefect/Dagster need a resident server on a PC that also renders video; one-run-per-day with ~9 linear stages gains nothing from a DAG engine.
3. The expensive failure modes here are not scheduling but (a) paid-API re-calls and (b) YouTube quota. Both are solved by a content-hash cache + cost ledger in SQLite, which any orchestrator would still require you to write.

**Option Y: Prefect 3 self-hosted as a Windows service.**
1. Documented Windows support with a service recipe [V: docs.prefect.io server-windows], so it is viable, not just theoretical.
2. Gives UI, retries, run history and cron-like deployments out of the box.
3. But it adds a server, its own DB and a worker, and its caching key model still needs custom hashing of rendered media; vendor "full parity" claim is unverified in practice [U].

Decision: **X now**; write stages as pure functions with `run(ctx)` so wrapping each in a Prefect `@task` later is a mechanical change.

Notes: YouTube `videos.insert` costs 1,600 quota units vs a 10,000/day default (about 6 uploads/day), sources disagree, confirm in Cloud Console [V-weak: https://www.ayrshare.com/solutions/how-to-bypass-the-youtube-10k-unit-limit-fixing-the-403-quota-exceeded-error/]. Videos uploaded from unverified API projects created after July 2020 are forced private until the project passes an audit [V-weak: https://www.ayrshare.com/solutions/google-api-error-403-unverified-app-how-to-fix-the-audit-pipeline/]. This makes "upload as private, human flips to public" both the safest approval gate and possibly unavoidable; plan the audit form early (the sources are from a vendor with a commercial interest; verify at Google's own docs).

## 3. Repo layout

```
YT-Automation/
  pyproject.toml
  config/ channel.yaml  budgets.yaml  stages.yaml   # model ids, per-stage budget, voice, template ids
  src/ytauto/
    cli.py            # ytauto run|resume|stage|approve|status|kill|cost
    runner.py         # stage loop, hashing, retries, kill-switch check
    db.py             # sqlite: runs, stages, ledger, quota
    ledger.py  secrets.py  notify.py  log.py
    stages/ trend.py script.py tts.py visuals.py subtitles.py render.py upload.py analytics.py
    llm/claude_cli.py # wraps `claude -p --output-format json --max-budget-usd --max-turns`
  state/ ytauto.db  KILL            # presence of KILL file = stop before next stage
  runs/2026-10-14-<slug>/
    manifest.json
    01_trend/ out.json
    02_script/ script.json  prompt.txt  claude_result.json
    03_tts/ narration.wav  timings.json
    04_visuals/ scenes/*.html  frames/ (or clips/)
    05_subtitles/ captions.srt  words.json
    06_render/ video.mp4  short.mp4  thumb.png
    07_upload/ response.json     # videoId, privacyStatus
    08_analytics/ d1.json d7.json
    logs/ run.jsonl  stage-<name>.log
  tests/
  .github/workflows/ci.yml        # lint + unit tests + dry-run only
```

## 4. `manifest.json` schema

```json
{
  "schema": 1,
  "run_id": "2026-10-14-kv-cache-explained",
  "created_at": "2026-10-14T06:00:00Z",
  "mode": "live | dry-run",
  "topic": {"title": "", "source_urls": [], "score": 0.0},
  "config_hash": "sha256:...",
  "status": "running | awaiting_approval | done | failed | killed",
  "budget_usd": {"cap": 1.50, "spent": 0.42},
  "stages": {
    "02_script": {
      "status": "pending|running|done|failed|skipped_cached",
      "input_hash": "sha256:...",
      "code_version": "git-sha-or-file-hash",
      "outputs": [{"path": "02_script/script.json", "sha256": "..."}],
      "attempts": 1, "started_at": "", "ended_at": "",
      "cost_usd": 0.12, "tokens": {"in": 0, "out": 0},
      "error": null
    }
  },
  "approval": {"required": true, "state": "pending|approved|rejected", "by": "", "at": ""},
  "upload": {"video_id": null, "privacy": "private", "quota_units": 1600}
}
```
The SQLite `runs/stages/ledger` tables mirror this (the manifest is the portable truth per run; DB is for cross-run queries like daily quota and monthly spend).

## 5. Stage contract

Idempotency key for every stage = `sha256(stage_name + code_version + stage_config + sorted(input artifact sha256s))`. If the key equals the manifest's `input_hash` and all output files exist with matching hashes, status = `skipped_cached`. Outputs are written to `*.tmp` then atomically renamed, so a crash never leaves a half file that looks complete.

| Stage | Inputs | Outputs | Idempotency key adds | Test |
|---|---|---|---|---|
| 01_trend | config topics/sources | `out.json` (ranked topic) | date + source snapshot hash | fixture feed gives deterministic top-1 |
| 02_script | topic, style guide | `script.json` (scenes, narration, on-screen text, citations) | prompt text + model id | JSON-schema validates; every claim has a source URL; word count in range |
| 03_tts | script narration | `narration.wav`, `timings.json` | voice id + text hash | duration within +-15% of words/WPM estimate; no clipping |
| 04_visuals | script scenes, timings | HTML scenes + frames/clips | template version + scene hash | each scene renders non-blank, correct resolution |
| 05_subtitles | wav + script text | `captions.srt`, `words.json` | wav hash + aligner version | all script words aligned; max drift < 300 ms vs timings |
| 06_render | visuals, wav, srt | `video.mp4`, `short.mp4`, `thumb.png` | ffmpeg args + inputs | `ffprobe` duration = audio duration +-0.3 s; codec/res as spec |
| 07_upload | video, metadata, approval | `response.json` | video sha256 + title | dry-run only hits a mock; live refuses without approval=approved; refuses if a video with same sha already uploaded (dedupe in DB) |
| 08_analytics | video_id | metrics json | video_id + day offset | mock API returns fixed JSON; ledger updated |

Runtime rules:
- **Retries**: 3 attempts with exponential backoff (10 s, 60 s, 300 s) for network/5xx/429; zero retries for schema-validation failures after the first LLM repair attempt (cap LLM re-asks at 2 so cost is bounded). Upload is never retried blindly: first query the channel for the sha-tagged title/description to avoid duplicate uploads.
- **LLM steps**: `claude -p ... --output-format json --max-turns N --max-budget-usd X`, with a restrictive `--allowedTools` (none for pure script generation). Parse `result` and cost fields defensively; store the raw JSON next to the artifact.
- **Cost ledger**: table `ledger(ts, run_id, stage, provider, units, usd, note)`. Runner aborts if month-to-date > cap in `budgets.yaml` (set at $25 to leave margin under $30) or per-run cap exceeded.
- **Kill switch**: `state/KILL` file (or `ytauto kill`) checked before each stage and before any upload; also kills child ffmpeg/Chrome by Job-object/PID tracking [U implementation detail]. Also a daily upload count cap and a quota-units cap in the DB.
- **Dry-run**: `--dry-run` stubs every paid or externally visible call (Claude returns a canned fixture, TTS emits a silent wav of the right length, upload writes a fake response). It exercises hashing, caching and manifest paths for free; CI runs this.
- **Human approval gate**: after `06_render`, runner sets `awaiting_approval`, uploads nothing yet, and sends a Telegram bot message (bot API is free [U]) with the thumbnail, script summary and the local command `ytauto approve <run_id>` (or two inline buttons polled by long-polling; no inbound port needed, which avoids exposing the PC). Fallback/alternative after the audit issue: upload as `private` and notify; the human flips to public in Studio. Default to this until N (say 10) consecutive videos are approved without edits, then optionally auto-publish scheduled.
- **Secrets**: use the `keyring` Python library which on Windows uses Windows Credential Manager [U, standard]; store the YouTube OAuth refresh token and bot token there, never in `.env` or in `runs/`. `.env` only for non-secret config. Claude Code auth stays in its own store. Redact tokens in logs with a filter. Alternative if keyring is blocked: `.env` encrypted with DPAPI via `win32crypt` [U].
- **Logging**: JSON Lines (`logs/run.jsonl`, fields: ts, run_id, stage, level, event, cost_usd) plus a rotating human log. One `ytauto status` command prints a table from SQLite. Failure notification to Telegram with the last 20 log lines.
- **Task Scheduler**: one daily task triggers `ytauto run --today`; a second hourly task runs `ytauto resume` which finishes any `failed|running-stale` run (stale = no heartbeat for 30 min) and polls approvals. A lock row in SQLite prevents overlapping runs. Enable "Run task as soon as possible after a scheduled start is missed" and "wake to run" [U, standard Task Scheduler options].

## 6. Where Claude Code scheduling fits
- Use `claude -p` only as a worker inside `02_script` (and optionally a weekly analytics-review job). Reason: deterministic OS scheduling, no tokens burned to decide "run now", simple failure semantics.
- Desktop-app scheduled tasks/CronCreate/routines: behavior when the app is closed or the PC sleeps is not documented in what I verified [U]; do not put the daily trigger on them. Cloud `/schedule` routines run remotely, so they cannot touch the local GPU/ffmpeg/files; at most they could do read-only trend research and push a `topics.json` to a repo [U].

## 7. Acceptance tests
1. **Fresh dry-run**: `ytauto run --dry-run` produces a full `runs/<date>-<slug>/` with all stages `done`, zero ledger USD, no network calls (verified by blocking sockets in the test).
2. **Cache hit**: a second run with identical inputs marks every stage `skipped_cached` and finishes in <5 s.
3. **Selective invalidation**: change one script sentence; only `02_script` onward re-run, `01_trend` stays cached; change only the subtitle style, only `05_subtitles`/`06_render` re-run.
4. **Crash resume**: kill the process during `06_render`; `ytauto resume` redoes only that stage; no `.tmp` files left, manifest valid JSON.
5. **Atomicity**: truncated output file (hash mismatch) is detected and the stage re-runs.
6. **Retry bounds**: injected 429s retry exactly 3 times then fail the stage with `status=failed` and a Telegram alert; schema failure causes at most 2 LLM repair calls.
7. **Budget cap**: set cap to $0.01; run halts before the first paid call that would exceed it; month cap blocks new runs.
8. **Kill switch**: creating `state/KILL` mid-run stops before the next stage and never reaches upload.
9. **Approval gate**: live run without approval makes zero calls to the upload endpoint; after `approve`, exactly one `videos.insert` happens; re-running does not upload twice (sha dedupe).
10. **Secrets**: grep of `runs/`, logs, and manifest for the token strings returns nothing; secrets are only readable via keyring.
11. **Overlap lock**: two concurrent `ytauto run` invocations result in one running, one exiting cleanly.
12. **Task Scheduler**: task fires at the configured time with the user logged off and exits with code 0 (manual check once; recorded in docs).

## 8. Open items / UNVERIFIED
- Exact current `claude -p` JSON cost field name and `--max-budget-usd` semantics on the installed version (run `claude --help`, `claude -p "x" --output-format json`).
- Whether Claude Code desktop scheduled tasks run with the app closed.
- YouTube upload quota cost and whether this project falls under the forced-private rule (check Cloud Console + Google's audit page).
- Headless Chrome on GitHub Actions and n8n licence terms were not verified.

Sources: https://docs.prefect.io/v3/how-to-guides/self-hosted/server-windows ; https://github.com/apache/airflow/issues/10388 ; https://docs.dagster.io/getting-started/install ; https://docs.claude.com/en/docs/claude-code/headless ; https://www.mintlify.com/VineeTagarwaL-code/claude-code/reference/commands/cli-flags ; https://docs.github.com/en/actions/reference/usage-limits-billing-and-administration ; https://www.ayrshare.com/solutions/how-to-bypass-the-youtube-10k-unit-limit-fixing-the-403-quota-exceeded-error/ ; https://www.ayrshare.com/solutions/google-api-error-403-unverified-app-how-to-fix-the-audit-pipeline/
