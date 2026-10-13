# D5-B (against): TTS-native timings should be the primary contract

## Thesis
words.json should be produced at synthesis time by the TTS engine (Kokoro durations, ElevenLabs/Azure alignment). Whisper/stable-ts is a QA gate and a fallback adapter. Making forced alignment the contract adds a second ML model, a second failure mode and CPU minutes per video to answer a question the TTS already knows.

## Arguments
1. Exact by construction. The report rates Kokoro-native "Excellent (exact by construction, no ASR)" and expects drift <=40 ms vs ~80/150 ms median/p95 for stable-ts (05-subtitles.md s.2, s.8 gate 3). Whisper timestamps "are not trained to be word-exact" and need per-sentence chunking on long files (05 s.3 Y3).
2. Native timing exists in the stack we would use. Kokoro-FastAPI ships word-level `/dev/captioned_speech` and a `return_timing` chunk option (https://github.com/remsky/Kokoro-FastAPI). Azure has WordBoundary events; ElevenLabs has /with-timestamps (03-tts.md rows). The 05 report concedes: if Kokoro, "implement X first".
3. Engine-agnostic is a weak argument. The pipeline will pick ONE engine (Kokoro, $0). Paying alignment cost on every video to hedge a swap that may never happen is premature generality. A thin adapter per engine writing the same words.json schema keeps the interface agnostic without making Whisper mandatory.
4. Whisper QA already exists in the plan (05 s.8 gate 2), so the aligner is redundant compute. Keep Whisper as the independent check that catches mispronunciation.
5. WhisperX is a better aligner than stable-ts if alignment is kept. Its paper reports 93.2% vs 85.4% word precision (200 ms tolerance) against Whisper timestamps (https://www.forasoft.com/learn/ai-for-video-engineering/articles-ai/whisperx-diarization-word-level-timestamps), but this is on transcription, not script-forced alignment. UNVERIFIED head-to-head vs stable-ts align().

## Strongest point FOR the proposition, and my answer
Native timings are fragile in practice: Kokoro-FastAPI issue #249 shows a sentence missing from timestamps and the second chunk's times restarting at ~0.4 s (https://github.com/remsky/Kokoro-FastAPI/issues/249; closed "stale, believe resolved" Sep 2026, not confirmed fixed). Also the 03-tts pipeline concatenates chunks with 150-250 ms silence and loudness-normalizes, and the report says HyperFrames' "Kokoro" word times actually come from a Whisper pass (03-tts.md line 27). Answer: this argues for validating native timings, not for replacing them. Our own pipeline owns the chunk join, so we offset each chunk's times by cumulative sample count (deterministic, a few lines), and gates T1/T2 (word count == script count, monotonic, last end within 150 ms of wav duration) catch exactly the #249 failure. On failure, fall back to stable-ts: the "fast path" and "fallback" roles swap. Contract stays words.json either way.

## What would change my mind
- A 2-minute bake-off on this PC (05 s.9 already proposes one) where Kokoro-native fails the +/-80 ms test on >5% of words, or #249-style drops recur on the pinned version.
- Kokoro not being run through a wrapper that emits timings (raw kokoro-onnx README has none: 03-tts.md row 1), making us write the duration extraction ourselves.
- The chosen engine turning out to be OpenAI TTS or another with no timings.

## Scores for my alternative (native primary + Whisper QA + stable-ts fallback)
- Cost: 5 (no extra compute on happy path)
- Output quality: 4 (exact when it works)
- Policy risk: 5 (no license issues; Apache-2.0 model, UNVERIFIED per wrapper)
- Implementation effort: 3 (chunk offsets, wrapper pinning, plus fallback still built)
- Maintainability: 3 (wrapper bugs, per-engine adapters)
