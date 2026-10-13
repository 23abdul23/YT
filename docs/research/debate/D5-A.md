# D5-A (FOR): words.json via stable-ts forced alignment, TTS-native fast path, ASS burn (Shorts) + SRT sidecar (long-form)

## Thesis
One engine-agnostic file, words.json, decouples captions from TTS and renderer. stable-ts is MIT, runs on CPU, and aligns the exact script text. Kokoro's native timings are an optional shortcut that emits the same schema.

## Arguments
1. **Survives engine swaps.** The TTS pick is still open: Kokoro has no native timestamps in the reported schema, and the report's shared audio engine gets Kokoro/ElevenLabs/Gemini timings from a Whisper pass (03-tts.md, lines 26-27). Forced alignment is the only path that works for every engine, plus post-processed audio (05-subtitles.md s3).
2. **License is clean.** stable-ts is MIT (verified: https://raw.githubusercontent.com/jianfch/stable-ts/main/LICENSE). Kokoro is Apache-2.0 (verified: https://raw.githubusercontent.com/hexgrad/kokoro/main/LICENSE). The alternative aligner, MMS, is CC-BY-NC, a trap for a monetized channel (05-subtitles.md s2).
3. **Free output formats.** The stable-ts README shows `result.to_srt_vtt('audio.srt')` and `result.to_ass('audio.ass')` (https://github.com/jianfch/stable-ts). It also runs on CPU, with docs for CPU-only options. That cuts the code to write and costs $0.
4. **The fast path is real but wrapper-bound.** Kokoro's `KPipeline.join_timestamps` sets per-token `start_ts`/`end_ts` from predicted durations (https://raw.githubusercontent.com/hexgrad/kokoro/main/kokoro/pipeline.py). So "optional fast path" is accurate, and it can emit the same words.json.
5. **Decoupled burn-in.** ffmpeg `ass=` with a bundled OFL font keeps captions independent of the renderer (05-subtitles.md s6). A SRT sidecar for long-form is cheap: 400 quota units per upload, about 25 per day (https://developers.google.com/youtube/v3/docs/captions/insert).

## Strongest opposing point and answer
Opposition: "Whisper timestamps are not word-exact, so drift beats TTS-native timing; why add an aligner when Kokoro already knows durations?" Answer: native timing locks you to one engine, and the wrappers' handling of tempo/trim post-processing is UNVERIFIED (05-subtitles.md s3). The contract is the schema, not the aligner. Drift is bounded by a gate: median |delta| <= 80 ms and p95 <= 150 ms, with per-paragraph chunking (05 s8). If Kokoro is chosen, the fast path is used and the aligner stays as a fallback.

## What would change my mind
- A 2-minute bake-off on the GTX 1650 Ti machine showing stable-ts median drift > 150 ms, or runtime above about 1x realtime on a 10-minute narration, with WhisperX or native timing clearly better.
- The TTS decision locks to a single engine with exact native timings and zero audio post-processing, which makes the aligner dead weight.
- A stable-ts regression on Windows or on the newest PyTorch (UNVERIFIED this session).

## Scores (1-5; 5 = best / easiest)
- Cost: 5 (all local, MIT)
- Output quality: 4 (good, with a drift gate)
- Policy risk: 4 (an SRT sidecar is standard; captions.insert on an unverified project is UNVERIFIED)
- Implementation effort: 4 (README shows align plus srt/ass export, but a thin words.json adapter is still needed)
- Maintainability: 5 (single schema, engine-agnostic)

Not verified this session: stable-ts CPU speed (no benchmark; the report also lacks one) and its exact `align()` signature (firecrawl was rate-limited, so I checked only the README).
