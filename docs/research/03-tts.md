# 03 - Text-to-Speech Voiceover (researched 2026-10-14)

Assumptions: Windows 11, possibly no NVIDIA GPU, budget <= $30/mo. 10-min video ~ 1,500 words ~ 9,000 chars (my estimate at ~150 wpm; HyperFrames docs also use 145-155 wpm, local `media-use/audio/references/tts.md`).

## 1. Comparison table

| Engine | Commercial license | Windows CPU/GPU | Word timestamps | Pronunciation / SSML | Cost / 10-min video | Notes |
|---|---|---|---|---|---|---|
| **Kokoro-82M** (+kokoro-onnx) | Weights Apache-2.0; kokoro-onnx MIT ([kokoro](https://github.com/hexgrad/kokoro), [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx)) | CPU OK; ~80MB quantized/~300MB ONNX; README claims only "near real-time on M1". Windows CPU RTF: UNVERIFIED (a Russian fine-tune reports RTF 0.10 on a laptop CPU, [HF](https://huggingface.co/da1353/kokoro-ru)). Needs espeak-ng MSI on Windows. | Not in README; a "timestamped" ONNX export exists ([mixpeek](https://mixpeek.com/model/onnx-community/Kokoro-82M-v1.0-ONNX-timestamped)). Plan: forced alignment (s.4). | No SSML. Inline IPA override `[Kokoro](/kˈOkəɹO/)` via misaki ([PyPI](https://www.pypi.org/project/misaki)) | $0 | Best free quality/speed; 54 voices, 8 langs. Prosody slightly flat on long text (my judgment). |
| **Piper** | GPL-3.0 code now at OHF-Voice ([repo](https://github.com/OHF-Voice/piper1-gpl)); per-voice licenses UNVERIFIED | CPU, fast (UNVERIFIED) | No native | espeak phonemes; no SSML | $0 | More robotic than Kokoro. Skip. |
| **Coqui XTTS-v2** | **Non-commercial only (CPML)**; Coqui closed, nobody sells a license ([summary](https://scour.ing/@minezone/p/https://github.com/artcore-c/AI-Voice-Clone-with-Coqui-XTTS-v2), [GH #4145](https://github.com/coqui-ai/TTS/discussions/4145)) | Slow on CPU | No | Limited | n/a | **Reject** for a monetized channel. |
| **F5-TTS** | Code MIT; **weights CC-BY-NC** ([repo](https://github.com/SWivid/F5-TTS)) | README lists NVIDIA/AMD/Intel/Apple only; no CPU path | No | No | n/a | **Reject** (NC weights). |
| **Chatterbox** (Turbo/Nano/Multilingual V3) | MIT; every output carries Resemble Perth watermark ([repo](https://github.com/resemble-ai/chatterbox)) | Nano (110M) claims "3x faster than realtime on 8 CPU cores" (vendor claim); larger want GPU | No | `[laugh]` tags only | $0 | Candidate if a GPU appears; otherwise Kokoro. |
| **Orpheus** | Apache-2.0 (Llama-3B backbone) ([repo](https://github.com/canopyai/Orpheus-TTS)) | vLLM GPU; llama.cpp no-GPU route, no speed given | No | Emotion tags | $0 | 3B params: too heavy for CPU (my judgment). |
| **Dia** (Dia2 exists) | Apache-2.0 ([repo](https://github.com/nari-labs/dia)) | ~4.4GB VRAM bf16, ~2x realtime on RTX 4090; **CPU "to be added soon"** | No | Dialogue tags | n/a | Dialogue-oriented; no GPU = unusable. |
| **Edge-TTS** (unofficial) | **No license grant**: undocumented Edge endpoint ([repo](https://github.com/rany2/edge-tts)); repo license appears GPL-3.0 (UNVERIFIED) | Cloud, any PC | Boundary metadata + subtitle output (README); per-word detail UNVERIFIED here | One `<voice>` + one `<prosody>` only; rate/pitch/volume args | $0 | Great voices but can break or be blocked; commercial grey zone. Emergency fallback only. |
| **Azure Neural TTS** | Yes (service terms) | Cloud | **Yes**: SDK `WordBoundary` (offset + char position) ([docs](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-structure); [reliability caveat](https://learn.microsoft.com/en-us/answers/questions/2260104/how-to-reliably-get-all-word-boundary-events-from)) | **Full SSML** (not on HD/personal voices) | Free F0: 0.5M chars/mo ≈ 55 videos ([pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/)); paid ~$15-16/1M chars UNVERIFIED ≈ $0.15 | Best legit + timestamps + SSML; needs Azure account/card. |
| **Google Cloud TTS** | Yes | Cloud | SSML `<mark>` timepoints (UNVERIFIED here) | SSML | Free/mo: 4M chars Standard & WaveNet; 1M Neural2/Studio/Chirp 3 HD; Chirp 3 HD $30/1M after ([pricing](https://cloud.google.com/text-to-speech/pricing)) → $0 within free tier | 1M chars ≈ 110 videos/mo. |
| **ElevenLabs** | Commercial from Starter ([pricing](https://elevenlabs.io/pricing)); free tier non-commercial ([3rd party](https://www.happyrobot.ai/hub/elevenlabs-pricing)) | Cloud | **Char-level** alignment via `/with-timestamps` ([docs](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps)); HyperFrames engine does not use it (local `tts.md`: "No") | Pronunciation dictionaries (UNVERIFIED) | 1 credit/char → ~9k credits. Starter $6 / 30k = ~3 videos/mo; Creator $22 / 121k = ~13 videos/mo | Most natural; volume capped. |
| **OpenAI TTS** | Yes (AI-voice disclosure to users per OpenAI policy: UNVERIFIED) | Cloud | No | `instructions` style (gpt-4o-mini-tts); no SSML | gpt-4o-mini-tts ≈ $0.015/min est. ≈ $0.15 (tokens: $0.60/1M in, $12/1M audio out) ([model page](https://developers.openai.com/api/docs/models/gpt-4o-mini-tts), [forum](https://community.openai.com/t/understanding-gpt-4o-mini-tts-pricing-input-characters-cost/1151816)); tts-1 $15/1M chars ≈ $0.14 | Cheap, good; needs alignment pass. Official pricing page returned 403. |
| **HeyGen (via hyperframes)** | UNVERIFIED | Cloud | **Yes** native `word_timestamps[]` | n/a | OAuth web-plan free allowance 10 min/mo ≈ 1 video; API billed normally (local `tts.md`) | Not a base layer. |

## 2. What the local HyperFrames skill offers (verified on disk)
Source: `C:\Users\Azeem\.agents\skills\media-use\audio\references\tts.md`.
- `npx hyperframes tts "text" -o narration.wav` = **local Kokoro only**; no `--provider`/`--words` flags; default voice `af_heart`; documentation picks `bf_emma`, `bm_george`; tutorial `am_adam`.
- Shared engine `audio.mjs --request audio_request.json --only tts` writes `audio_meta.json` with `voices[].{path,duration_s,words[]}`. Provider order: HeyGen (native timestamps) > ElevenLabs > Kokoro; Gemini TTS opt-in (`gemini-3.8-flash-tts`, needs API key; timings from a transcription pass, not native).
- Word timestamps for Kokoro/ElevenLabs/Gemini come from a Whisper transcription pass (estimated alignment). Flat schema `[{id,text,start,end}]` feeds captions.
- `hyperframes` is not on PATH (use `npx`); ffmpeg 2024-05-27 gyan build is installed (verified).

## 3. THE crucial decision: Kokoro local vs ElevenLabs cloud as primary voice

**Option X - Kokoro-82M local + forced alignment**
1. $0/month, Apache-2.0 weights, CPU-only on Windows, no key/quota/outage ([kokoro](https://github.com/hexgrad/kokoro)).
2. Already shipped in the installed HyperFrames CLI/engine as the always-available route (local `tts.md`).
3. No native timestamps and no SSML; jargon is fixed with IPA overrides plus a text normalizer (cost: maintaining a pronunciation lexicon).

**Option Y - ElevenLabs Creator ($22/mo)**
1. Most natural prosody (my judgment; third-party consensus) with char-level alignment from `/with-timestamps` ([docs](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps)).
2. Commercial rights begin at Starter ([pricing](https://elevenlabs.io/pricing)).
3. 1 credit/char: Creator ≈ 13 ten-minute videos/month, Starter ≈ 3 ([pricing](https://elevenlabs.io/pricing)); a daily cadence overruns it and consumes ~70% of budget.

**Recommendation:** X as primary. Keep the engine behind one interface so a "hero voice" (Google Chirp 3 HD free tier, or ElevenLabs Starter) is a config swap. Decide finally after blind A/B test T7.

## 4. Interface spec
```
tts(script_path, out_dir, voice="af_heart", lexicon="lexicon.json") ->
  out_dir/narration.wav         # PCM16 mono 44.1 kHz, loudness-normalized
  out_dir/narration.words.json  # [{"id":0,"text":"GPU","start":0.00,"end":0.41,"line":"s01"}, ...]
  out_dir/tts_meta.json         # engine, voice, version, duration_s, lufs_in/out, true_peak, sha256(script)
```
Input: UTF-8 script, one scene per line `id|text` (ids join back to scenes, as the HyperFrames engine does).
Steps: (1) normalize via lexicon (acronyms "GPU" → spelled letters, "kubectl" → IPA override, "v1.2" → "version one point two", strip code spans); (2) chunk at sentence boundaries ≤ ~300 chars, synthesize, join with 150-250 ms silence; (3) word times: engine-native if available (Azure/ElevenLabs, merge chars → words), else forced-align audio against the *original script* (Whisper word timestamps via `hyperframes transcribe`, or CTC) and snap to script words; (4) loudness normalize; (5) write JSON with `text` taken from the script (captions show "kubectl", not its spoken form). Same `{id,text,start,end}` schema as HyperFrames captions.

## 5. Loudness: -14 LUFS, true peak <= -1 dBTP
YouTube normalizes playback toward about -14 LUFS (secondary-source consensus; YouTube's own statement not re-verified: UNVERIFIED). Narration alone to -16 LUFS so music (about -31 LUFS under voice per HyperFrames docs) doesn't push the mix over; final export -14 LUFS. Two-pass loudnorm:
```
ffmpeg -hide_banner -i narration_raw.wav -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null NUL
ffmpeg -i narration_raw.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=<I>:measured_TP=<TP>:measured_LRA=<LRA>:measured_thresh=<T>:offset=<O>:linear=true" -ar 44100 -ac 1 -c:a pcm_s16le narration.wav
```
Final video: same filter with I=-14. Linear mode applies gain only, so word times stay valid.

## 6. YouTube synthetic-voice disclosure
- Disclosure is required for realistic altered/synthetic content (real person made to say things, realistic fabricated scenes); AI-assisted scripts, audio repair and cloning your own voice for voiceover are listed as minor ([YouTube Help](https://support.google.com/youtube/answer/14328491)). A generic TTS narrator impersonating no one is therefore generally not a trigger (my inference; the page does not name stock TTS).
- Bigger risk is monetization: the July 2025 "inauthentic content" policy targets mass-produced, low-transformation videos; AI voice itself is allowed ([secondary summary](https://typecast.ai/learn/youtube-ai-monetization-july-15-ypp-update/); YouTube's own text not fetched: UNVERIFIED). Mitigate with original script/analysis and varied visuals.
- Never clone real people's voices without consent.
- Claims of a new mandatory 2026 upload checklist come from single blogs ([minimatters](https://minimatters.com/youtube-ai-content-labeling-update-in-may-2026/)): UNVERIFIED; check Studio at upload.

## 7. Acceptance tests
- T1 Schema: wav PCM16 mono 44.1k; words.json validates; word count equals script token count.
- T2 Timing: `start<end<=next start`; last `end` within 150 ms of wav duration (ffprobe).
- T3 Alignment: on 3 hand-marked scripts, >= 95% of words within ±80 ms.
- T4 Loudness: narration -16 ±0.5 LUFS, true peak <= -1.0 dBTP (ffmpeg `ebur128`); final mix -14 ±1 LUFS.
- T5 Jargon: 30-term glossary (GPU, CUDA, kubectl, nginx, SQL, PyTorch, YAML, OAuth, gRPC, WASM...) synthesized, round-tripped through Whisper, >= 95% match; misses become lexicon entries; rerun on every lexicon change.
- T6 Robustness: 12-min script, no clipped chunks, no unplanned gap > 400 ms, tail silence < 1 s, deterministic output or documented tolerance.
- T7 Quality gate: blind A/B Kokoro vs Option Y (3 scripts); if Kokoro loses ≥ 2/3, escalate voice tier.
- T8 Performance: measure CPU RTF on this PC (UNVERIFIED until measured); fail if RTF > 0.5.
- T9 Compliance: `tts_meta.json` records engine/voice/license; pre-upload check rejects voices tagged `cloned_real_person`.

## Not verified
Kokoro CPU RTF on this PC; Piper/Dia2 numbers; Azure paid rate; Google word timepoints; ElevenLabs/OpenAI commercial terms beyond pricing pages; YouTube's official -14 LUFS and inauthentic-content wording.
