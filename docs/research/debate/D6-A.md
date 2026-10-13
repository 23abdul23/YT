# D6-A (FOR): HyperFrames as single compositor, FFmpeg post, Remotion backup

## Thesis
One HTML-to-video compositor, installed skills already present, zero license cost, with FFmpeg doing only what it is best at (loudnorm, faststart, thumbs). Splitting compositors adds glue code with no gain.

## Arguments
1. **License and cost.** Apache-2.0, no per-render fees (README: https://github.com/heygen-com/hyperframes; report 06). Remotion is free only for <=3 people, else $25/seat or $0.01/render (https://www.remotion.pro/license). HyperFrames has no growth cliff.
2. **Maturity and momentum (fetched today).** Repo shows 62.7k stars, 5.6k forks, release v0.8.154 (https://github.com/heygen-com/hyperframes). Maintainers fix bugs fast: issue #3591 (HDR scene bug) was closed with a fix PR within about a week (https://github.com/heygen-com/hyperframes/issues/3591).
3. **Windows is exercised in CI.** The search surfaced a "Windows render verification" GitHub Actions job (https://github.com/heygen-com/hyperframes/actions/runs/26729557803). Report 06 lists Windows fixes in v0.7.27, .42, .54, .59, .60 (https://newreleases.io/project/github/heygen-com/hyperframes/release/v0.7.60). Node 22.13 on this PC meets the requirement (report 06).
4. **Fit to the Anatomy problem.** Report 04 shows Anatomy figures are rAF/spring-driven, not seekable; its recommended fix is a hand-built virtual clock plus CDP capture plus ffmpeg pipe. That is a private re-implementation of what HyperFrames already does (per-frame seek, `__timelines`). Writing one `__anim.step` adapter and letting HyperFrames own capture, captions, audio and 9:16 via `--variables-file` is less code than a bespoke renderer.
5. **Built-in pipeline pieces.** CLI has `tts`, `transcribe`, `lint`, `check`, `benchmark`, `doctor`, `--gpu` NVENC, `--docker` byte-identical (report 06), and skills are already installed locally.

## Strongest opposing point and answer
Opposing: "Project is young and Windows is only inferred; a custom Playwright+ffmpeg rig is a tiny, controllable surface." Answer: the same report 04 admits a custom rig needs a stubbed clock, setTimeout hacks and hand-built captions/mix. HyperFrames risk is bounded: render is a CLI call, output is plain mp4, `doctor` and `PRODUCER_FORCE_SCREENSHOT=true` cover the known Chromium 147+ BeginFrame break (report 06, third-party mirror, so treat as UNVERIFIED). Remotion backup remains free for a solo channel.

## What would change my mind
- A Day-1 prototype on this PC where `hyperframes render` fails after `doctor`/upgrade, or 1080p30 SVG scenes render slower than ~3 fps/worker.
- Anatomy adapter output differing between seek and sequential frames (pixel diff > 0).
- Evidence of silent-corruption bugs recurring (as #3591 did) without lint/check catching them.

## Scores (1-5; effort 5 = easiest)
- Cost: 5
- Output quality: 4
- Policy risk: 4 (Apache-2.0; HeyGen owns project, so governance risk. YouTube policy unaffected by compositor)
- Implementation effort: 4 (skills installed, but adapter per figure needed)
- Maintainability: 3 (0.8.x churn, fast releases; pin version)

UNVERIFIED: real fps on GTX 1650 Ti, WebGL with `--browser-gpu`, whether local render ever needs a HeyGen login.
