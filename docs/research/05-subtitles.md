# 05 - Subtitles / Captions (long-form sidecar + Shorts burned-in)

Date: 2026-10-14. Items without a URL or marked UNVERIFIED were not confirmed this session.

## 1. YouTube captions.insert facts
- Quota: 400 units/call; scope `youtube.force-ssl`; file <=100 MB; needs videoId, language, name (<=150 chars); duplicate name+language gives 409 `captionExists`. Source: https://developers.google.com/youtube/v3/docs/captions/insert
- Other costs: list 50, update 450, delete 50. Source: https://developers.google.com/youtube/v3/determine_quota_cost
- Default quota 10,000 units/day, so about 25 caption uploads/day (my arithmetic). Plenty for 1-3 long-form/day. Shorts need no sidecar (burned in).
- Unverified-project lock: videos.insert from unverified projects created after 2020-07-28 is forced private until audit. Source: https://developers.google.cn/youtube/v3/docs/videos?hl=en . I found NO source saying captions.insert is restricted the same way. UNVERIFIED; test once. Note the real blocker is the video-upload lock, which affects the whole pipeline (flag to the upload-component owner).
- Cheaper alternative: set captions at upload time is not possible via videos.insert, so the call is separate. Fallback: YouTube auto-captions plus Studio manual upload.

## 2. Timing-source options (comparison)

| Option | Accuracy | CPU-only OK | Tech-term handling | License/commercial | Verdict |
|---|---|---|---|---|---|
| TTS-native word timings (Kokoro: per-token durations; Kokoro-FastAPI `/dev/captioned_speech`, Kokoros Rust) | Excellent (exact by construction, no ASR), English voices only | Yes | Perfect: script is the text, no recognition | Apache-2.0 model (UNVERIFIED for each wrapper) | Primary if TTS is Kokoro. Sources: https://github.com/moses-root/Kokoro-FastAPI , https://replicate.com/siegerts/kokoro-tts-82m |
| stable-ts `align(audio, script)` | Good (Whisper timestamp tokens), may drift on long files; chunk per paragraph | Yes (slow on large models; use small/base for alignment) | Exact script words used; no recognition errors | MIT (UNVERIFIED) | Best engine-agnostic fallback. Source: https://pypi.org/project/stable-ts/2.11.3 |
| WhisperX (wav2vec2 phoneme alignment) | Very good; uses VAD+alignment | Yes with `--compute_type int8 --device cpu`, heavier install on Windows | Transcribes first unless you feed transcript segments; numbers/symbols need normalizing to words | BSD-2 (UNVERIFIED) | Heavier than needed. Source: https://gotranscript.com/public/master-word-level-timestamping-with-whisperx-a-comprehensive-tutorial |
| faster-whisper `word_timestamps=True` + `initial_prompt` | Good, cross-attention DTW | Yes (int8) | Transcription can still mangle terms (kubectl, CUDA) | MIT (UNVERIFIED) | Use only as QA check, not as source of truth |
| whisper.cpp (`-ml 1`/`-owts`) | Okay, token-level | Yes, fast | Same as above | MIT | Skip (extra binary, no gain) |
| ctc-forced-aligner (MMS) | Good, low-RAM | Yes | Exact text | Model weights CC-BY-NC-4.0 = non-commercial. Trap for a monetized channel. | AVOID. Source: https://huggingface.co/Zmu/mms-300m-1130-forced-aligner and the paper https://arxiv.org/pdf/2609.21145 |
| Montreal Forced Aligner | Best phone-level | Yes but conda/Kaldi, painful on Windows | Needs pronunciation dictionary; tech terms are OOV, need G2P | MIT (UNVERIFIED) | Overkill. Source: https://montreal-forced-aligner.readthedocs.io/en/latest/first_steps/alignment_example.html |
| aeneas | Coarse (DTW on espeak TTS, ~0.1-0.5 s) | Yes | Fine | AGPL | Skip (stale, too coarse for word highlight) UNVERIFIED |
| HyperFrames / media-use (`hyperframes transcribe`, captions via media-use shared audio engine) | Unknown | Node 22+ and FFmpeg only stated | It transcribes (ASR), not script-aligned as far as docs say; UNVERIFIED | Open-source repo | Use as renderer/caption-style layer only if video is built in HyperFrames. Docs did not specify whisper model or output format. Sources: https://github.com/heygen-com/hyperframes , https://hyperframes.heygen.com/ |

## 3. THE crucial decision

**Option X: Use TTS-native word timings as the source of truth (Kokoro durations), run Whisper only as a QA gate.**
1. Timings come from the same model that produced the audio, so drift is bounded by frame resolution and tech terms never get misrecognized (the text is the script). Source: Kokoro predicts per-token durations, https://replicate.com/siegerts/kokoro-tts-82m
2. Zero extra compute or dependencies on CPU; word timestamps exist in Kokoro-FastAPI/Kokoros but reportedly English voices only (same Replicate source).
3. Locks the pipeline to Kokoro-class engines; if the TTS component picks a cloud/other engine (Edge TTS gives word boundaries; others may not), the aligner is gone. Timings must be post-corrected after any ffmpeg tempo/silence-trim of the wav (UNVERIFIED how the wrappers handle this).

**Option Y: Engine-agnostic forced alignment of narration.wav + script.txt with stable-ts (Whisper small/base, CPU).**
1. Works with any TTS and with human-recorded or post-processed audio; aligns the exact script text, so no ASR spelling errors. Source: https://pypi.org/project/stable-ts/2.11.3
2. Runs on CPU with Windows pip install; no commercial-license trap (unlike MMS, CC-BY-NC). Source for the trap: https://huggingface.co/Zmu/mms-300m-1130-forced-aligner
3. Whisper timestamps are not trained to be word-exact (stable-ts mitigates with silence suppression), so expect higher drift than X; must chunk per sentence on long videos. Source: same stable-ts page / https://github.com/linto-ai/whisper-timestamped

**Recommendation: Y as the pipeline contract (one interface, any TTS), with X as an optional fast-path that emits the same `words.json`.** Reason: the interface below is engine-agnostic, the QA gate (section 7) already needs a Whisper pass, and Y is the only path that survives TTS-engine swaps. If the TTS researcher picks Kokoro, implement X first and keep Y as fallback when X's drift test fails.

## 4. Interface spec

```
narration.wav (mono, 24-48 kHz) + script.txt (UTF-8, one sentence per line, spoken-form text)
   -> align  -> words.json
   -> captions.py -> captions.srt (long-form) + captions.vtt (optional) + captions.ass (Shorts)
```
words.json:
```json
{"version":1,"duration_s":612.4,"source":"tts|stable-ts","words":[
 {"i":0,"w":"Kubernetes","start":0.12,"end":0.71,"line":0,"conf":0.98}]}
```
Rules: monotonic, `end>start`, no overlaps, one entry per script token in order (alignment text == script, never ASR output). Punctuation stays attached to the word. Script must be spoken-form (numbers/symbols expanded) before TTS so text and audio agree; keep a display-form map for on-screen casing (e.g. "kubectl").
Tech-term accuracy: custom lexicon file `terms.txt` (display form + spoken form); also pass the terms as `initial_prompt` when running faster-whisper QA.

## 5. Line-breaking rules
- Long-form SRT: max 42 chars/line, max 2 lines, 1-7 s cue, target 17 cps, min 0.8 s duration, break at punctuation first, never split a term from its noun or a number from its unit. These are Netflix-style conventions (secondary; I did not fetch the style guide, UNVERIFIED), ok for YouTube.
- Shorts: 1-3 words per card (max ~16 chars/line, max 2 lines), active word highlighted (ASS `\k`/`\kf` karaoke tags or per-word Dialogue events with color override), bold sans, outline 6-8 px, no background box needed.
- Shorts safe zone (1080x1920): third-party estimates only, no official spec: bottom 300-380 px reserved (title/subscribe), top about 120 px, right about 100-200 px. Keep captions inside a centered ~900x1400 box and place baseline around y=1300-1450 (middle-lower, above 1540). Sources: https://www.aicarousels.com/free-tools/youtube-safe-zone-checker , https://adkit.so/tools/safe-zones/youtube , https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide . UNVERIFIED officially; preview on a real phone once.

## 6. Generation and burn-in
- SRT/VTT: plain text, trivially generated in Python (stdlib). Upload SRT via captions.insert (language `en`, name e.g. "English").
- ASS for Shorts: write PlayResX=1080, PlayResY=1920, one Style, per-word `Dialogue` lines with `{\c&H...&}` highlight override.
- Burn: `ffmpeg -i in.mp4 -vf "ass=captions.ass:fontsdir=fonts" -c:a copy out.mp4` (libass is in standard gyan.dev Windows ffmpeg builds; UNVERIFIED version). Windows gotchas: run from the working dir with relative paths, or escape `C:` as `C\:` and use forward slashes; keep the font file in `fontsdir` so no system install is needed.
- If rendering via HyperFrames, captions would be HTML/GSAP rather than libass (media-use skill docs not retrievable here; UNVERIFIED). Using ffmpeg+ASS keeps the caption layer independent of the video renderer, which is the lazier and more robust choice.

## 7. Fonts (OFL only)
Inter, Montserrat, Poppins, Roboto (Apache), Bangers, Luckiest Guy are on Google Fonts under OFL (confirm each on https://fonts.google.com/ before bundling; UNVERIFIED this session). Bundle the TTF plus the OFL.txt in `fonts/`; OFL permits commercial use and embedding in video. Avoid Impact, Arial, and Komika (not OFL).

## 8. Quality gates and acceptance tests
1. Script fidelity: aligned word sequence == script token sequence (exact match, 100%).
2. Independent ASR check: run faster-whisper (small, int8) on narration.wav; WER vs script <= 5% (<= 8% if many code identifiers; compare with `terms.txt` normalization). Fail means TTS mispronounced or wrong script.
3. Alignment drift: for 20 sampled words, compare word start vs faster-whisper word start; median |delta| <= 80 ms, p95 <= 150 ms (X expected <= 40 ms).
4. Structure: words.json monotonic, no overlap, last end <= audio duration + 0.05 s, no gap > 1.5 s inside a sentence unless script has a pause marker.
5. SRT lint: no line > 42 chars, <= 2 lines, cue 0.8-7 s, cps <= 20, no cue overlap, file parses (e.g. `ffmpeg -i captions.srt -f null -`), UTF-8 without BOM issues.
6. Shorts ASS: all text bounding boxes inside the 900x1400 centered box (render one frame at t of the longest card and check by pixel scan of non-background rows: no caption pixels at y > 1540 or y < 120).
7. Burn-in smoke test: ffmpeg exit 0, output duration within 0.1 s of input, extracted frame at a highlight time shows the highlight color (pixel sample).
8. Upload: captions.insert returns 200; then captions.list shows the track. Log quota spent (400).
9. Accessibility: contrast ratio caption text vs outline >= 4.5:1; sidecar SRT is always uploaded for long-form even if burned-in is also used (do not burn in long-form).

## 9. Open risks
- Unverified-project private lock on videos.insert (not captions) may force a compliance audit; see section 1.
- Safe-zone numbers are third-party estimates.
- Kokoro timestamp availability depends on the wrapper/version used; confirm in the TTS component.
- No benchmark of stable-ts vs WhisperX on this machine; run a 2-minute bake-off before locking.
