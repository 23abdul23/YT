# D3-A (FOR): Kokoro-82M local default, swappable, A/B-validated

## Thesis
Default to Kokoro locally behind one interface. It is the only option that is $0, quota-free, and commercially licensed. The blind A/B on jargon scripts decides whether to escalate. This is a gated default, not a bet on quality.

## Arguments
1. **License settled (mostly).** The official HF model card says "Apache-licensed weights ... deployed anywhere from production environments to personal projects", and states training used only permissive or non-copyrighted audio (https://huggingface.co/hexgrad/Kokoro-82M). The "Creative Commons" heading that worried 10-policy.md is only the CC-BY attribution table for ~12h of training data (Koniwa, SIWIS), not the model licence. GitHub LICENSE file fetch was rate-limited: UNVERIFIED, so record the LICENSE hash in tts_meta.json (03-tts.md T9).
2. **Cost.** $0 vs ElevenLabs Creator $22 (~13 ten-minute videos/mo, ~70% of the $30 budget) or Starter $6 (~3 videos) (03-tts.md s.3). Daily cadence is impossible on ElevenLabs within budget. Hosted Kokoro costs only ~$0.65-0.80/M chars (HF card), i.e. pennies as a cloud fallback.
3. **Engine is already wired.** `npx hyperframes tts` is local Kokoro; Whisper alignment already supplies word timestamps for Kokoro and ElevenLabs alike (03-tts.md s.2), so ElevenLabs' char-level timestamps add little.
4. **Jargon is a fixable, testable problem.** misaki supports inline IPA overrides (`[Kokoro](/kˈOkəɹO/)`, HF card), and the lexicon plus T5 round-trip test (>=95% match) makes failures into permanent fixes.
5. **No lock-in.** Interface spec (03-tts.md s.4) makes ElevenLabs or Google Chirp 3 HD (1M free chars/mo) a config change. Downside of being wrong is one setting.

## Strongest opposing point and answer
Quality: Artificial Analysis lists Kokoro at Elo ~1063 vs Eleven v4 ~1328 and Eleven v3 ~1176 (https://artificialanalysis.ai/text-to-speech/leaderboard/provider-voice). That is a real gap, and "Kokoro is #1" claims (texttolab.com) are secondary and conflict with it, so I discard them. Answer: Kokoro is the top open-weight model there (Inworld benchmark page), the gap matters less for a clean English explainer narrator, and retention is driven by script and visuals (my judgment). The A/B test T7 turns this into a measurement: if Kokoro loses 2/3, escalate.

## What would change my mind
- Blind A/B (>=10 listeners, jargon scripts) where Kokoro loses clearly, or listeners cite fatigue on 8+ min narration.
- Measured RTF on the GTX 1650 Ti PC > 0.5 (T8; currently UNVERIFIED).
- A LICENSE file or voice-pack terms that restrict commercial use.
- Early analytics showing voice-linked drop-off.

## Scores (1-5, 5 = best/easiest)
- Cost: 5
- Output quality: 3
- Policy risk: 4 (Apache weights; synthetic-voice disclosure generally not triggered, my inference per 03-tts.md s.6)
- Implementation effort: 4 (already in HyperFrames; lexicon upkeep)
- Maintainability: 4
