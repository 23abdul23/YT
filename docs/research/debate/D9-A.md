# D9-A (FOR): plain Python CLI + SQLite + Task Scheduler

## Thesis
For ~1 linear run/day on one Windows PC, a stdlib-only pipeline (sqlite3 + schtasks) is the cheapest, most debuggable option. Orchestrators add resident servers, not capability. LLM calls stay inside the script stage only.

## Arguments
1. **Alternatives are worse here.** Airflow has no native Windows support (maintainers: WSL2/Docker only) [github.com/apache/airflow/issues/10388, via report s1]. Prefect is viable on Windows but needs a server + DB + worker [docs.prefect.io/v3/how-to-guides/self-hosted/server-windows], which is extra processes on a box that also renders video.
2. **The real risks are solved by the ledger, not a DAG engine.** Paid-API re-calls and YouTube quota are handled by content-hash cache + cost ledger, which any orchestrator would still need custom code for (report s2; Prefect's cache keys don't hash rendered media natively [U]).
3. **Missed runs and laptop sleep are first-class Task Scheduler settings.** "Run task as soon as possible after a scheduled start is missed" runs the task at the next opportunity; "Wake the computer" wakes from sleep. Caveat: Power Options wake timers must not be Disabled [learn.microsoft.com Q&A "Scheduled task not waking computer"; Macrium KB, both surfaced in search]. The hourly `resume` task is a second safety net, because it is idempotent by hash.
4. **Secrets.** `keyring` uses Windows Credential Manager (WinVaultKeyring) [PyPI/keyring source, Windows.py]. Limit: blob is about 2560 bytes (some older sources say 512) [third-party PR comment; UNVERIFIED at Microsoft]. An OAuth refresh token is short enough, and a DPAPI fallback exists (keyrings.alt EncryptedKeyring).
5. **Smallest blast radius.** Stages as `run(ctx)` pure functions can be wrapped in Prefect `@task` later mechanically (report s2), so the choice is reversible. The `claude -p` stage worker is bounded by `--max-turns`/`--max-budget-usd` [headless docs; flags are V-weak].

## Strongest opposing point
Hand-rolled resume/locking/retry code will accumulate bugs, and an orchestrator provides a UI, retries and run history free. Answer: the logic is about 300 lines (stage loop, hash key, lock row, atomic rename), covered by the 12 acceptance tests in the report (crash resume, overlap lock, cache hit). Prefect's retry/UI do not remove the need for the ledger and the approval gate. `ytauto status` over SQLite covers the UI need for a single operator.

## What would change my mind
- Task Scheduler failing the logged-off, wake-from-sleep test on the actual PC (report test 12), repeatedly.
- Pipeline growing to many concurrent channels or parallel GPU jobs.
- Measured bugs in custom resume logic after about 30 live runs.
- Evidence Prefect's Windows service runs reliably with under 300 MB RAM overhead [UNVERIFIED].

## Scores (1-5)
- Cost: 5 ($0, no daemon)
- Output quality: 4 (neutral; pipeline-agnostic)
- Policy risk: 4 (no extra third-party data flow; approval gate is independent)
- Implementation effort: 4 (more code than Prefect, but small)
- Maintainability: 4 (one repo, stdlib, easy swap to Prefect)
