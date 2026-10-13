# 06 - Video Composition + Render (researched 2026-10-14)

## Local machine facts (verified by running commands)
Node v22.13.0 (HyperFrames needs 22+), ffmpeg gyan.dev build 2024-05-27 (old, upgrade advisable), GPU = NVIDIA GTX 1650 Ti (NVENC available, so `--gpu` usable). Skills hyperframes, hyperframes-cli, -core, -audio, -animation, -keyframes, -registry, media-use are installed in ~/.claude/skills.

## Key facts
- HyperFrames: Apache-2.0, "no per-render fees or commercial-use thresholds"; needs Node 22+ and FFmpeg; renderer seeks each frame in headless Chrome and encodes with FFmpeg (deterministic). https://github.com/heygen-com/hyperframes
- Local `render` needs no HeyGen account per README (cloud = HeyGen-hosted / Lambda / Cloud Run are optional). Whether `publish`/`cloud` need login: UNVERIFIED. Local doc: ~/.claude/skills/hyperframes-cli/references/preview-render.md
- Windows: README is silent, but release notes show Windows fixes (v0.7.27 npx spawn, v0.7.42 symlink EPERM, v0.7.54 npx, v0.7.59 paths, v0.7.60 "more deterministic across software-GPU, Windows") https://newreleases.io/project/github/heygen-com/hyperframes/release/v0.7.60 . Newer releases exist (v0.8.34 seen). Known pitfall: Chromium 147+ removed HeadlessExperimental.beginFrame; fix = `npx hyperframes upgrade -y` or `PRODUCER_FORCE_SCREENSHOT=true` (third-party mirror: https://download.hermesedi.duckdns.org/.hermes/hermes-agent/optional-skills/creative/hyperframes/references/troubleshooting.md).
- Render flags (local skill doc): `--fps 24|30|60` (60 = 2x time), `--quality draft|looks|delivery` (looks = CRF 16 x264 standard), `--crf` or `--video-bitrate` (exclusive), `--resolution`, `--workers N|auto` (each ~256 MB Chrome), `--gpu` (NVENC), `--browser-gpu` (host GPU for WebGL capture), `--variables-file` (parametrised renders from JSON), formats mp4/webm/mov/png-sequence/hls, `--docker` byte-identical. Also `benchmark`, `doctor`, `lint`, `check`, `snapshot`. Mirror of CLI docs: https://openskillindex.com/skills/heygen-com-hyperframes-hyperframes-cli
- Audio/captions: `<audio data-volume>` in HTML; `/hyperframes-audio` covers fades, ducking, EQ/compressor/limiter, buses; `/media-use` covers TTS, transcription, captions, BGM/SFX (README). CLI has `tts` and `transcribe`.
- Remotion license: free for individuals and for-profit orgs of <=3 people (commercial OK); 4+ needs Company License: Creators $25/seat/month, Automators $0.01/render with $100/month minimum. https://www.remotion.pro/license , https://github.com/remotion-dev/remotion/blob/main/LICENSE.md . Solo channel = free.
- Anatomy skill: MIT; figures are SVG + WebGL (+ beta 3D) standalone HTML, mainly user-driven (hover/drag/keyboard), no video export; own capture.mjs makes PNGs for verification. Timing model undocumented, so figures are NOT known to be seekable. https://github.com/wheresryan22/anatomy
- YouTube upload spec: MP4, moov at front, H.264 High, CABAC, progressive, 4:2:0, 2 B-frames, closed GOP = half frame rate, VBR; 1080p SDR 8 Mbps (24/25/30 fps), 12 Mbps (48-60); AAC-LC 48 kHz, 384 kbps stereo; BT.709. https://support.google.com/youtube/answer/1722171
- Loudness: YouTube publishes no official upload target; community norm -14 LUFS integrated, TP -1 to -1.5 dBTP, two-pass loudnorm with linear=true (non-official: https://instagit.com/browser-use/video-use/social-media-loudness-normalization-targets/). My proposal -14 LUFS / -1.5 dBTP is a design choice, UNVERIFIED as a YouTube requirement.

## Comparison

| Tool | License / cost | Windows CPU-only | Seekable / deterministic | Captions / audio | Fit for interactive HTML/SVG/WebGL | Verdict |
|---|---|---|---|---|---|---|
| HyperFrames | Apache-2.0, free | Yes with fixes (>=v0.7.60; run `doctor`) | Yes, per-frame seek in headless Chrome; figures need a paused-timeline wrapper | Skills for captions, TTS, transcribe, mixing, ducking | Native; WebGL via `--browser-gpu` or software GL | Primary; skills already installed |
| Remotion | Free <=3 people, else $25/seat or $0.01/render | Yes | Yes (React frame-based) | Captions pkg; basic audio | Needs React rewrite of every figure | Backup; license risk if team grows |
| FFmpeg only | LGPL/GPL, free | Yes, fastest | Yes | libass, loudnorm, sidechaincompress | Cannot render HTML | Post-process (mux, loudnorm, 9:16, stills) |
| MoviePy | MIT | Yes, slow | Yes | Basic | PNG sequences only | Skip |
| Manim | MIT (Community) | Yes | Yes | None | Math/algorithm scenes only | Optional: pre-render mp4 clips as inputs |
| Playwright/Puppeteer + ffmpeg | Apache-2.0 | Yes | Only if page has seek hook; else real-time, flaky | You build it | Works, but re-implements HyperFrames | Per-scene fallback |

## Render-speed estimate (UNVERIFIED, reasoning only, not benchmarked)
10 min x 30 fps = 18,000 frames. Headless-Chrome screenshot capture is roughly 5-20 fps per worker for 1080p light SVG on CPU; with ~4 workers expect ~15-40 min per long video, WebGL-heavy scenes slower (software GL). x264 encode overlaps capture; NVENC (`--gpu`) only speeds encode. A 60 s Short (1,800 frames) is about 2-4 min. Run `npx hyperframes benchmark` before committing; 24 fps is YouTube-legal if time is tight.

## ONE crucial decision: engine for the anatomy-style interactive visuals

**Option X: HyperFrames as the single compositor (HTML to mp4); wrap each anatomy figure as a time-driven scene (GSAP / paused timeline sets its state).**
1. Apache-2.0, no per-render fees; local render needs only Node 22 + FFmpeg (README).
2. Deterministic per-frame seek, built-in caption/TTS/audio-ducking skills (already installed), and `--variables-file` lets one template plus storyboard.json produce both long and Short (portrait).
3. Risk: Windows support is inferred from release-note fixes only, project is young (0.8.x), and anatomy figures are user-driven so each needs an adapter exposing seek(t).

**Option Y: Playwright/Puppeteer capture of anatomy pages + FFmpeg assembly (libass, loudnorm).**
1. Mature, tiny dependency surface; FFmpeg is the most controllable muxer/normalizer.
2. Anatomy ships capture.mjs/drive.mjs but only for verification; no documented seek, so you need real-time recording or custom virtual-time hooks (frame-pacing flaky).
3. You hand-build caption animation, transitions, audio mix and templating; no timeline or preview tooling.

**Recommendation: X, with FFmpeg as the post-process stage (loudnorm, faststart, thumbnails) and Y capture only as a per-scene fallback.** Prototype one anatomy figure first.

## Interface spec
```
INPUT  job_dir/
  storyboard.json
    { "id","title","fps":30,
      "narration":"assets/narration.wav", "words":"assets/words.json",   // [{w,start,end}] seconds
      "music":"assets/music.mp3|null","music_gain_db":-22,
      "scenes":[{ "id","start","end","visual":"assets/scenes/s01.html|.mp4|.png",
                  "caption_mode":"words|lines|none","transition":"cut|fade",
                  "shorts":{"include":true,"start":0,"end":55} }] }
  assets/  narration.wav, words.json, scenes/*.html, sfx/, music, brand/
OUTPUT job_dir/out/
  final_long.mp4   1920x1080 30fps, H.264 High yuv420p BT.709, 8-12 Mbps VBR, faststart, AAC-LC 48k 384k stereo, -14 LUFS
  final_short.mp4  1080x1920 30fps, same codec, ~<=60 s, burned-in captions
  thumbnail.png    1280x720, <2 MB (limit UNVERIFIED)
  render_report.json  { ffprobe fields, LUFS, durations, black_frames, pass }
STAGES
  1 storyboard -> index.html (template + variables)   2 hyperframes lint / check
  3 hyperframes render --fps 30 --quality delivery --workers auto [--gpu]
  4 ffmpeg 2-pass loudnorm, then -movflags +faststart -bf 2 -g 15 -b:v 8M -maxrate 12M -bufsize 16M
    with colorspace/primaries/trc = bt709
  5 Short: separate portrait composition from the same storyboard (re-layout, NOT center-crop: a 16:9 crop cuts off diagrams)
  6 Thumbnail: HTML->PNG (hyperframes snapshot or Playwright) for typography control;
    ffmpeg frame grab (-ss T -frames:v 1) is the zero-effort fallback
```

## Acceptance tests (script; any failure fails the job)
1. Video: `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,codec_name,profile,pix_fmt,r_frame_rate,color_space` gives long 1920x1080, short 1080x1920; h264 / High / yuv420p / bt709; 30/1.
2. Audio: aac, 48000 Hz, 2 channels.
3. Loudness: `ffmpeg -i f -af ebur128=peak=true -f null -` gives integrated -14 +/-1 LUFS, true peak <= -1.0 dBTP.
4. Duration: |video - narration.wav - intended pad| <= 0.5 s (long) / 0.25 s (short); audio vs video stream duration differ <= 0.1 s.
5. Black frames: `ffmpeg -i f -vf blackdetect=d=0.5:pix_th=0.10 -an -f null -` finds none >0.5 s except first/last 1 s. Add `freezedetect=n=-60dB:d=8` as a warning for frozen visuals.
6. Silence: `silencedetect=n=-45dB:d=3` finds none inside the narration span.
7. Container: `ffprobe -show_entries format=format_name,bit_rate` is mp4, 6-14 Mbps; moov precedes mdat.
8. Caption sync: spot-check 5 words, caption appears within +/-1 frame of word.start.
9. Thumbnail: 1280x720 PNG, <2 MB.

## Gaps / UNVERIFIED
Windows end-to-end WebGL render with `--browser-gpu` on GTX 1650 Ti; real fps; seekability of anatomy figures; Shorts max length and thumbnail size limits; adequacy of the 2024 ffmpeg build (update recommended).
