# 04 - Visuals via the Anatomy skill (research, 2026-10-14)

Repo: https://github.com/wheresryan22/anatomy (MIT). Cloned and tested locally: scratchpad/anrepo/a. Doc copies: scratchpad/repos/an-SKILL.md, an-README.md, scratchpad/repos/an/ (motion.md, verify.md, capture.mjs, drive.mjs, dial build.mjs). Note: `examples/dial-indicator/live.js` does not exist (404); the live code is an inline template string at the bottom of `examples/dial-indicator/build.mjs` (~lines 190-290).

## Measured on THIS PC (Windows 11, Node 22.13, Chrome 154 at C:\Program Files\Google\Chrome)
- `node examples/dial-indicator/build.mjs` wrote the standalone HTML instantly.
- `node scripts/drive.mjs dial-indicator.html ...` ran in 4.4 s, console clean, a WebGL2 context was obtained (renderer string masked as "WebKit WebGL"). drive.mjs launches with `--headless=new --enable-unsafe-swiftshader --ignore-gpu-blocklist`, plus `--do-not-de-elevate` on win32 (scripts/drive.mjs line 120). NOT tested: a heavy shader figure (raptor-engine, ripple-tank): UNVERIFIED perf.
- 30 consecutive 1920x1080 screenshots of the dial figure: 3.29 s, ~110 ms/frame (SVG only). My extrapolation: 60 s at 30 fps = 1800 frames ~ 3.5 min; at 60 fps ~ 7 min. Dense/WebGL figures will be several times slower; the docs say a capture takes 60-200 ms, "more on heavy WebGL pages" (references/verify.md).

## Q1. Deterministic frame capture
How figures animate (dial build.mjs live code): one `requestAnimationFrame` loop, `dt = min((now-last)/1000, 1/30)`, exponential follow plus a 4-substep spring, an idle "tour" on an internal `clock`, an `IntersectionObserver` gate, `matchMedia(reduced-motion)`. The model is separate but the state is stateful (springs), so it is NOT a pure function of t out of the box (motion.md says only "gestures and clips" are pure functions of time).

Options:
1. drive.mjs: has `["slow", f]`, which wraps rAF and `performance.now` (line 168), plus `sheet`/`shot`. Real-time sleeps, so spacing = `every` + 60-200 ms capture (verify.md). Good for QA, not final capture.
2. **Own virtual clock + CDP `Page.captureScreenshot` (RECOMMENDED).** A preload script replaces rAF/performance.now with a manual clock (same trick as drive.mjs, stepped instead of scaled). Per frame: advance exactly 1/fps, flush rAF callbacks, wait for paint, screenshot, pipe to ffmpeg. dt is clamped to 1/30 and motion is time-based, so fixed steps are deterministic on the same Chrome. `setTimeout` stays on wall clock (verify.md line 57), so stub the 3.6 s idle-tour timer in the preload.
3. CDP `Emulation.setVirtualTimePolicy`: plausible, not tested with the IntersectionObserver gate: UNVERIFIED. Option 2 is simpler.
4. CDP screencast / Playwright recordVideo: real-time capture, dropped frames, variable fps. Reject for determinism (general knowledge; Playwright docs not re-fetched: UNVERIFIED).
5. HyperFrames (HeyGen): Apache-2.0, Node 22+, FFmpeg; renders by seeking `window.__timelines` per frame (sources disagree whether Puppeteer-seek or BeginFrame; nothing on Windows): https://deepwiki.com/heygen-com/hyperframes , https://blog.nidhin.dev/video-as-code-a-deep-dive-into-heygen-s-hyperframes . An arbitrary rAF/spring page is not seekable by it without the adapter below. Useful as the final compositor (figure + captions + audio) only if the other components pick HyperFrames; the figure capture itself does not need it.
6. Remotion + iframe `?t=`: workable (iframe must apply `?t=` synchronously and signal ready) but adds a React toolchain; its licence terms for commercial use were not checked: UNVERIFIED.

Changes needed to make a figure seekable (a wrapper in the build template, not edits per figure):
- Expose `window.__anim = { reset(), step(dt), set(cmd), pose() }`: factor `tick(now)` into `advance(dt)` (dial: ~15 lines); `set` replaces the pointer/key `steer(target)` calls with commands from script.json.
- Force `touring=false`, `visible=true` (skip the IntersectionObserver gate) and `still.matches=false`.
- `__setTime(t)` = `reset()` then replay `step(1/60)` to t, cached for sequential capture. Springs cost < 1 ms/frame (motion.md line 80).
- Figures hard-code their numbers (BLOCKS, STOPS...). Move them to a JSON `PARAMS` object so script.json can inject values.
- `?bare=1` CSS hiding the card chrome (Fig label, hint, caption), keeping the readout (true model output) for caption use.

## Q2. Cost, time, tokens per figure
- SKILL tiers (an-SKILL.md lines 58-62): Figure 40-80 parts, "often well under an hour", budget up to an hour; Hero 80-150 parts, 2-4 h; Epic 6 h+ (skill refuses to start). CHANGELOG [Unreleased] says the old 30-90 min Figure estimate was often far longer than the build. README "Limits": "slow on purpose"; 3D orbit audit 15-20 min.
- Per figure the skill demands: parts list, geometry, painter's order, `--audit` to zero for pipes/round parts, `lines.mjs` check, 4x close-ups in both themes, reading every PNG.
- Token cost: no published number found for the Figure tier. My ESTIMATE (UNVERIFIED): 20-60 min and roughly 0.5-2 M non-cached tokens, plus large reference reads (craft.md, kit.md). publish.mjs records minutes and tokens per figure in the community gallery (https://github.com/wheresryan22/anatomy-community), which would give real data. This is too expensive for a daily cadence at <= $30/month unless run on a flat-rate subscription.
- Faster: (a) library of finished figures (the repo ships 8: dial-indicator, desk-computer, arcade-cabinet, raptor-engine, ripple-tank, test-rig, spot-plate, turning-dial); (b) Figure tier only; (c) fork the nearest example and change numbers/labels (estimate minutes, 20-80k tokens, UNVERIFIED); (d) author new figures offline in supervised sessions, not in the pipeline.
- Limit of reuse: SKILL step 3 says invent a new object per concept, never copy; reuse only works when the topic maps onto an existing machine (gauge, threshold, lock, spring, queue).

## Q3. Topic fit and fallbacks
Fits: one mechanism with a few numeric states: caches, rate limiters, pools, queues, locks, springs, memory layouts, hardware (SKILL concept->object table lines 29-39). Poor: charts, people, maps, news, benchmarks, multi-actor stories (the skill description is about physical mechanisms), which describes most trending news. Fallbacks, all deterministic HTML so the same capture rig works: (1) code/terminal screens with typed lines, (2) SVG/HTML diagrams with GSAP timelines (natively seekable), (3) animated charts, (4) AI/stock imagery with Ken Burns (other components). Suggested mix: ~70-80% fallback visuals; an Anatomy figure as a 10-25 s "hero beat" in selected videos.

## Q4. Vertical 9:16
Figures are SVG in a fixed viewBox; the camera is fitted at build time by `fitProjection(points, width, height, {pad, azimuth})` (SKILL step 5), and the card is landscape. Cheapest: 1080x1920 viewport with `?bare=1`: the SVG scales to width, so the figure fills only ~30% of height; place the title above and captions below in the compositor. Better: scripted crop/pan/zoom (CSS transform on the SVG) per scene, or add a portrait fit parameter to the build template. SKILL line 122 requires it to read at 390 px wide, so narrow layouts are a supported test. Feasible with moderate rework; portrait render not tested: UNVERIFIED.

## Q5. WebGL in headless Windows Chrome
Worked here with SwiftShader flags (context created, console clean). Plain SVG figures need no WebGL. Risks: SwiftShader is CPU-bound (heavy shader figures slow: UNVERIFIED), output may differ slightly across Chrome versions/CPUs, so pin the Chrome version. The repo's own CHANGELOG has a Windows fix for elevated terminals (`--do-not-de-elevate`). The SKILL says the SVG must still read with `--no-webgl`, so prefer SVG-only figures in the pipeline.

## DECISION
**Option X - generate a fresh Anatomy figure per video.**
1. Figure tier is 40-80 parts and up to an hour of agent work with audit/close-up checks (an-SKILL.md line 59); my token estimate 0.5-2 M per figure (UNVERIFIED).
2. The skill must invent a new object per concept (step 3), so quality varies and an unattended run can stall on the audit.
3. Most trending technical topics lack a single mechanism (charts, people, news), so many videos would get a poor figure or none.

**Option Y - curated reusable library (6-12 figures, built offline and supervised) + parametrized reuse + fallback visuals. RECOMMENDED.**
1. Eight MIT-licensed figures already ship; building takes seconds (tested) and capture is ~0.11 s/frame measured, so marginal cost per video is minutes of CPU and ~0 LLM tokens.
2. A seekable wrapper (`__anim.step/set`) is written once per figure; then `figure.html + script.json -> mp4` is deterministic and unattended.
3. Fallback visuals cover topics with no mechanism, so the pipeline never blocks; new figures are added only when a recurring theme justifies a supervised session.

## Proposed capture interface
`node render-figure.mjs --figure figs/dial.html --script script.json --fps 30 --size 1920x1080|1080x1920 --theme dark --out out/fig.mp4 [--frames dir]`
script.json: `{ "duration": 14, "params": {"BLOCKS":[18,14,10]}, "events":[{"t":0,"cmd":"set","target":120},{"t":4,"cmd":"set","target":-60}], "crop":[{"t":0,"rect":[x,y,w,h]},{"t":6,"rect":[...]}] }`
Flow: launch pinned Chrome with the flags above -> preload virtual clock -> load `figure.html?bare=1` -> per frame i: apply events with t <= i/fps, `__anim.step(1/fps)`, apply crop transform, `Page.captureScreenshot` -> ffmpeg stdin (libx264, yuv420p). Also write a sidecar `fig.json` with the model readout per frame for captions.

## Acceptance tests
1. Determinism: same script rendered twice gives identical per-frame PNG hashes on the same machine.
2. Seek equality: `__setTime(t)` screenshot equals sequential frame t (pixel diff 0).
3. Speed: 14 s @30 fps 1080p dial figure < 90 s (basis ~46 s measured-rate); 9:16 likewise.
4. Zero console errors; `--no-webgl` render identical for SVG-only figures.
5. ffprobe confirms size, fps, duration, yuv420p; no blank first frame; sidecar readout matches the model.
6. 9:16: figure box inside the safe area, nothing clipped.
7. A topic with no mapped figure routes to a code/diagram fallback rather than failing.
8. Render stage uses 0 LLM tokens when reusing a library figure.

Not checked: heavy-WebGL frame rates, portrait render, HyperFrames on Windows, Remotion licensing, real token cost per figure.
