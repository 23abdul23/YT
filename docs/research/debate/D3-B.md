# D3-B (AGAINST): Kokoro should not be the default voice

## Thesis
Make a cloud voice (Google Chirp 3 HD free tier, Azure Neural free tier; ElevenLabs only if it earns its price) the default. Keep Kokoro as the offline fallback. The report's own figures show the cloud free tiers cost $0 as well, so Kokoro's cost advantage is nil, while voice quality is the one input a viewer notices in the first 10 seconds.

## Arguments
1. **Kokoro's "$0" edge does not exist.** Report 03 lists Google's free allowance as 1M chars/mo for Chirp 3 HD, about 110 ten-minute videos, and Azure F0 at 0.5M chars/mo, about 55 videos (03-tts.md table, citing cloud.google.com/text-to-speech/pricing and azure.microsoft.com pricing). Both are enough for a daily channel. I could not re-verify these live (the fetch was rate-limited), so they rest on the report.
2. **The report itself doubts Kokoro's quality.** It calls Kokoro's prosody "slightly flat on long text" (03 s.1). Explainer videos are long-form narration. It also makes a blind A/B (T7) the final judge, so the default should be whichever side is more likely to pass.
3. **Retention and monetization risk.** The July 2026 YouTube clarification targets generic, template-like, mass-produced content (10-policy.md s.1, secondary source netinfluencer.com). A flat synthetic voice makes a channel sound templated. Voice is the channel's most recognizable trait, and changing it later after an audience forms is costly. A "config swap" later is not free.
4. **Kokoro costs engineering time the cloud engines don't.** It has no SSML, no native timestamps, and Windows needs espeak-ng. It also needs a hand-kept IPA lexicon and a Whisper alignment pass (03 s.1, s.4). Azure gives WordBoundary events plus full SSML, and ElevenLabs gives character-level alignment (03 table). The Whisper/forced-alignment step is also an unmeasured accuracy risk (T3).
5. **Unmeasured performance.** Kokoro's CPU real-time factor on this PC is UNVERIFIED (03 "Not verified"; T8). The model card also says training used synthetic audio from "closed TTS models from large providers" (huggingface.co/hexgrad/Kokoro-82M). I read this as a minor provenance footnote, not a legal finding.

**License, settled in part:** the HF model card says "Apache-licensed" weights and "welcome the deployment ... in real use cases" (huggingface.co/hexgrad/Kokoro-82M). The "Creative Commons Attribution" heading only lists CC BY training data. I did not retrieve GitHub's LICENSE file (UNVERIFIED), but I concede Kokoro's license is not a real weakness. I am dropping that attack.

## Strongest point FOR, and my answer
Local Kokoro has no quota, no outage, no API key and no ToS drift, and it is already bundled in HyperFrames (03 s.2). Answer: that argues for Kokoro as the automatic fallback, not the default. Cloud-first with local fallback keeps both benefits. Free tiers can change, but a config swap back to Kokoro is equally cheap.

## What would change my mind
- A blind A/B (T7) where listeners can't prefer Chirp 3 HD or Azure over Kokoro in at least 2 of 3 scripts.
- Google or Azure free quotas shrinking below the daily cadence, or the card requirement being a hard blocker.
- Kokoro CPU RTF below 0.5 plus Whisper alignment above 95% within 80 ms, with the jargon test (T5) passing at 95% or better.

## Scores for my alternative (Google Chirp 3 HD free tier default, Azure as backup, Kokoro as fallback)
Higher is better; for cost and policy risk, 5 means cheaper or safer.
- Cost: 5 (inside free tiers); 3 if ElevenLabs is added
- Output quality: 4 (Chirp 3 HD quality is UNVERIFIED by me, not tested)
- Policy risk: 4 (commercial-use service terms; no cloning)
- Implementation effort: 3 (account and card setup; alignment still needed for Google, since its SSML timepoints are UNVERIFIED)
- Maintainability: 3 (vendor API and quota drift, offset by the Kokoro fallback)
