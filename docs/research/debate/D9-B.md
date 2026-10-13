# D9-B (against): plain CLI + SQLite + Task Scheduler

## Thesis
The proposition is wrong as a *complete* answer. The report itself lists a 12-item feature set (retries with backoff, resume, stale-run heartbeat, lock row, hourly resume task, approval polling, status table, Telegram alerts, kill switch). That is a homegrown orchestrator. Prefect 3 gives most of these built in, and Task Scheduler on a home PC is a single point of failure with no external watchdog. Preferred: Prefect 3 server as a Windows service plus an off-box dead-man's-switch.

## Arguments
1. **Re-implementation is scoped in the report.** Section 5 specifies retries/backoff, run history, `status`, heartbeats, locks, resume and approval polling (report s5, "Runtime rules"). Prefect provides retries, run history and a UI natively. Vendor docs claim a Windows service recipe: https://docs.prefect.io/v3/how-to-guides/self-hosted/server-windows (the report cites this [V]; my re-fetch was rate-limited, so I have not re-read the recipe myself). Each homegrown piece is also a test burden: 12 acceptance tests, several covering orchestration rather than product.
2. **Sleep/wake is unreliable on consumer Windows 11.** Microsoft Q&A threads report "Wake the computer to run this task" ticked yet the PC not waking, and Modern Standby (DRIPs) blocking scheduled wakes: https://learn.microsoft.com/en-us/answers/questions/651690/windows-11-does-not-wake-computer-to-run-scheduled ; https://www.tenforums.com/performance-maintenance/132472-scheduled-wake-drips-modern-standby.html ; https://learn.microsoft.com/en-us/answers/questions/5721805/windows-11-scheduler-will-not-wake-up-computer . The report marks every Task Scheduler reliability claim [U]. The user's machine is Windows 11 Home Single Language (possibly a laptop; UNVERIFIED).
3. **Silent failure is the worst mode.** If the PC is off, no code runs, so no Telegram alert fires. The CLI design has no external heartbeat. An off-box dead-man's-switch (a cloud routine or GitHub Actions cron that checks "was a video uploaded in 26h?") closes this. Routines run on Anthropic cloud and "keep working when your laptop is closed": https://code.claude.com/docs/en/routines . They cannot render locally, but they can monitor.
4. **Upgrade path is not free.** The report's "mechanical change to wrap in `@task`" ignores that the hand-rolled SQLite state (manifest, ledger, locks) duplicates Prefect's state model, so migration means ripping out the runner, not wrapping it. Starting on Prefect avoids that.

## Strongest point FOR, and my answer
Prefect adds a resident server and DB on a PC that also renders video, and Airflow/Dagster are weak on Windows (report s1). Answer: only Prefect is in my proposal. Its server is lightweight next to ffmpeg/Chrome (UNVERIFIED, needs measuring), and a service is restart-managed by Windows. Honest concession: Prefect does not fix sleep, so power settings or an always-on box are still required. Task Scheduler remains a fine *trigger*.

## Would change my mind
- The Prefect Windows service idles under ~300 MB RAM and survives reboot and logoff in a 1-week test.
- The user's PC is a desktop with sleep disabled, so the wake risk goes away.
- Homegrown runner stays under ~300 LOC in a prototype.

## Scores for preferred alternative (Prefect 3 service + cloud watchdog)
cost 4 ($0; watchdog uses free tier/subscription) | output quality 4 (neutral; better ops visibility) | policy risk 4 (no extra YouTube/ToS exposure; secrets stay local) | implementation effort 2 (server, worker, deployment, watchdog) | maintainability 4 (fewer custom state bugs, but more moving parts to patch)
