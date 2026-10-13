# D6-B: Against "HyperFrames is the single compositor"

## Thesis
Do not make a fast-moving, vendor-owned renderer the single point of failure for an unattended channel. Use plain FFmpeg for assembly, captions (libass), loudnorm and Shorts. Use a small custom Playwright/CDP virtual-clock capture for Anatomy figures (already recommended in 04-visuals-anatomy.md). Add Manim optionally. Remotion is the fallback (free for solo, 06-render.md).

## Arguments
1. **Churn is extreme.** The report saw v0.8.34; the releases page now shows v0.8.150 (https://github.com/heygen-com/hyperframes/releases), and the main page lists 5,537 commits (https://github.com/heygen-com/hyperframes). A single-compositor pipeline would absorb roughly 115 releases of change in one report cycle. The versions are not strictly comparable, since the report's "v0.8.34 seen" may be incidental. A pinned version avoids drift, but then you do not get the fixes.
2. **Silent corruption exists in the render path.** Issue #3591 (Sep 2026): an HDR-tagged clip makes the render ignore scene windows. It "exits 0, lint/check pass, preview correct" and the output is wrong (https://github.com/heygen-com/hyperframes/issues/3591). An unattended channel can only catch this with the ffprobe/blackdetect gates, which we need anyway.
3. **Windows is still a second-class platform.** Open or recent Windows items: a console window flashes on every render (#3430), and a webm alpha bug closed "not planned" (#2824). v0.8.144 fixes Windows renders cancelling when a parent pid is reused (https://github.com/heygen-com/hyperframes/releases). The report itself calls Windows support "inferred from release-note fixes only".
4. **It does not solve the hard part.** Anatomy figures are stateful rAF/spring pages and are not seekable (04, Q1). Each needs a `__anim.step()` adapter plus a paused-timeline wrapper. That is the same work our own virtual-clock capture needs, so HyperFrames adds a layer without removing the adapter.
5. **Vendor and runtime dependence.** The project is HeyGen-owned, with core maintainers on the HeyGen payroll (UNVERIFIED headcount). Its Apache-2.0 licence limits the legal risk but not the roadmap risk. Rendering also depends on Chromium behaviour; the report notes Chromium 147+ removed BeginFrame, which needed a tool upgrade. FFmpeg and Chrome CDP are the stable layer under it. Our own capture is about 100 lines, and the dial figure captured at about 0.11 s/frame on this PC (04).

## Strongest point FOR, and my answer
For: 62.7k stars, 5.6k forks and a daily commit pace (GitHub page, scraped 2026-10-14) mean it is not obscure or abandoned, and it ships captions, TTS, ducking and a lint/check CLI that would take weeks to rebuild. Answer: popularity does not give version stability or Windows depth. The captions and mixing it ships are thin wrappers over what FFmpeg (libass, sidechaincompress) already does. Use HyperFrames, if at all, as an optional per-scene HTML renderer behind the storyboard interface, so it can be swapped out.

## What would change my mind
- A 30-day-pinned HyperFrames version rendering 10 consecutive 10-minute 1080p videos on this GTX 1650 Ti with zero silent defects and a measured render time at or below the custom pipeline.
- An Anatomy figure working through HyperFrames with no per-figure adapter.
- The Windows bug backlog staying flat for 3 months.

## Scores for my alternative (FFmpeg + custom CDP capture, Remotion backup), 1-5
- Cost: 5 (all free; Remotion free at 3 people or fewer)
- Output quality: 3 (captions and transitions are hand-built, so they look more basic)
- Policy risk: 5 (no vendor ToS or telemetry, no policy exposure beyond YouTube's)
- Implementation effort (5 = easiest): 2
- Maintainability: 4 (small, stable surface: FFmpeg, CDP)
