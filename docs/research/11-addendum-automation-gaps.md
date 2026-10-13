# Plan Addendum: closing the automation gaps

Date: 2026-10-14. Companion to `Plan.md`. Evidence tags: **[S]** = read this session in search-result excerpts (mostly secondary pages, not full primary docs), **UNVERIFIED** = not checked. Verify the **[S]** items you depend on before building.

---

## 1. Gaps found in the current plan

| # | Gap | Where | Why it blocks full automation |
|---|---|---|---|
| G1 | **Nothing generates the visuals.** `visual.spec` is a free-form object that no stage fills. Task 11's `scene_html` handles only `code` and `stat`; type `diagram` falls into the final `else` branch and renders as plain title text. Figures come only from a hand-curated library of 3-6 Anatomy figures. | Tasks 6, 10, 11 | Most of every video would be static text on a dark background plus narration. This is the main hole, and also the main "inauthentic content" risk (R1). |
| G2 | **Visuals are not synced to narration.** Stage order is visuals (04) before subtitles (05), clips are fixed-length static HTML, and `words.json` is never given to the visual stage. | Sections 2, 6; Tasks 9, 11 | A reveal cannot land on the spoken word, so it plays as a slideshow. |
| G3 | **No QA that looks at pixels.** `qa.py` catches black, frozen and silent output only. | Task 12 | Clipped text, overflow and unreadable slides pass every gate. |
| G4 | **No image or B-roll source.** | Task 11 | Nothing between "text slide" and "hand-built figure". |
| G5 | **Thumbnail is title text only.** | Task 12 | Weak click-through, and it is the one asset viewers judge before anything else. |
| G6 | **Music is manual.** `assets/music/` is hand-curated. | Task 12 | One human chore, but it is a human chore. |
| G7 | **Research input is thin.** Task 6 fetches only the page linked from one trend item, and the claim check is only as good as that text. | Task 6 step 6 | Paywalled or JS-only pages give weak sources and many `review_queue` stops. |
| G8 | **Human tap before publish**, with autopilot deferred to Phase 2 Task 18. | D10, Tasks 13, 16, 18 | By design, but it is the only non-automated step left once G1-G7 are fixed. |
| G9 | **Hardware.** The plan says GTX 1650 Ti. I believe that card has 4 GB VRAM (check with `nvidia-smi`). The open video models below list about 8 GB minimum. | Global constraints | Local AI video generation is not an option on this PC. |

Not gaps (already covered): TTS (Kokoro, Task 8), captions (stable-ts, Task 9), assembly (FFmpeg, Task 12), upload (Task 13), analytics (Task 14). Your instinct about audio and subtitles was right to ask, but those two are the best-specified parts of the plan. The visuals are the weak part.

---

## 2. What the free options actually give you

### NVIDIA NIM (build.nvidia.com)
- Free hosted endpoints through an OpenAI-compatible API (`https://integrate.api.nvidia.com/v1`), key prefix `nvapi-`, about 40 requests/minute, no card. [S]
- Free endpoints exist for FLUX.1-schnell, FLUX.1-dev, FLUX.2-klein-4B, Stable Diffusion 3.5, TRELLIS (text-to-3D), speech models (Riva/Magpie TTS, Fugatto, Parakeet-type ASR) and many chat models. [S]
- Cosmos video models were still enterprise-gated for free keys as of 2026-04. [S]
- **Licence limit that matters:** NVIDIA's FAQ says Developer Program access is for "prototyping, research, development and testing purposes only", and defines production as any non-testing activity including serving real end users. [S, docs.api.nvidia.com/nim FAQ] A daily pipeline feeding a public, monetizable channel is very likely "production". Use NIM for building and testing the pipeline, not as a dependency of the live daily run, unless you accept that risk.

### Hugging Face
- Hosted inference is not free in any useful way: Free accounts get about $0.10/month of Inference Provider credit, PRO $2/month. [S] ZeroGPU gives free users roughly 5 minutes of GPU per day. [S]
- Use HF as a **weights host** (download Kokoro, FLUX.2-klein, ACE-Step, Whisper), not as an inference service.

### Google Gemini API (free tier)
- Text models (Flash, Flash-Lite) and Flash TTS models were listed as free as of 2026-09-30. Imagen and Veo were listed as not free. Free-tier content may be used to improve Google products. [S]
- Reports on Flash Image free quota conflict (some say about 500/day, others say paid only). Treat image generation here as unavailable until you test it. [S, conflicting]
- Good as a free fallback LLM for cheap steps (claim check, scene QA). Not a visuals source.

### Free GPUs
- Kaggle: about 30 GPU-hours/week on T4/P100, 12 h sessions, quota floats and is not documented as a number. [S] Colab free: T4, limits not published, 90 min idle timeout, about 12 h cap. [S]
- Both are usable for **one-off batch jobs** (generate a music library, a set of stock figures). Both are brittle for a daily unattended pipeline. Headless triggering of Kaggle kernels is UNVERIFIED here.

### Open-weight video models (for completeness)
- Wan 2.x (Apache 2.0), LTX 2.x (Apache 2.0 with conditions; read its licence), HunyuanVideo 1.5 (Tencent community licence, not Apache). Min VRAM quoted about 8-14 GB. [S] None fit a 4 GB card, and none give reliable technical diagrams or readable on-screen text. **Skip generative video for the daily loop.** For a technical-explainer niche, code-drawn animation is both cheaper and more accurate.

### Pexels API (stock B-roll and photos)
- Free key, 200 requests/hour and 20,000/month default, limits can be lifted free if you show attribution. Free for commercial use. Terms ask for a visible link back to Pexels when using the API. [S] Whether a credit line in the YouTube description satisfies that is UNVERIFIED; ask api@pexels.com once.

### Music
- ACE-Step 1.5 (MIT per its model card, "commercial-ready" claim) generates background music; the older v1 is listed as Apache 2.0. [S] An open GitHub question asks the authors to clarify output rights and has no reply. [S] It needs a real GPU, so generate a **library once** on Kaggle, not per video. Keep a licence ledger.

### TTS
- Kokoro (Apache 2.0) stays the default. Chatterbox (MIT), CosyVoice2 (Apache 2.0), Dia (Apache 2.0) are the upgrade candidates. [S] This agrees with Task 8's bake-off.

### Claude plugins and skills relevant to video
| Item | What it is | Fit |
|---|---|---|
| Remotion agent skill (`npx skills add remotion`) | Teaches Claude Code to write React/Remotion video code, `npx remotion render` to MP4. [S] | Good for kinetic text and charts. Remotion's licence is free only for 3-person-or-smaller companies (your own plan says this), so fine solo. |
| Manim skill (`Yusuke710/manim-skill`, Claude Code plugin) | Plans scenes, writes Manim code, renders, iterates. [S] | **Best fit for technical explainers** (algorithms, data structures, graphs, step-by-step math). Skill licence UNVERIFIED; Manim itself is MIT (from my knowledge, not checked here). |
| Claude Code Video Toolkit (`digitalsamba/claude-code-video-toolkit`) | Bundle of Remotion, FFmpeg, Playwright and TTS skills. [S] | Useful as a prompt and tooling reference. |
| Youtube Clipper skill | Downloads and clips existing videos. [S] | **Do not use.** Re-using other people's footage is the opposite of what the policy risk section asks for. |

Important: these skills are built for an interactive Claude Code session. Your plan (D2) correctly runs the pipeline on the **API key**, not a subscription login. So do not call the skills at runtime. **Vendor their prompts and reference notes** into `prompts/` (check each licence first), exactly as you already do for claude-youtube.

---

## 3. Recommended design: LLM-authored scene code with a render, inspect, repair loop

This replaces "pick a figure from a library, else show a title" as the default.

```
 storyboard (scenes + narration + cues)
        |
        v
 03 TTS -> 05 SUBTITLES (words.json)      <- moved BEFORE visuals
        |
        v   per scene: narration text + word times for that scene
 04a SCENE AUTHOR (Sonnet)  -- picks renderer, writes scene code with reveals at word times
        |
        +--> Manim scene .py        (algorithms, graphs, math, step animations)
        +--> HTML/SVG/CSS scene     (architecture, code walkthrough, charts)  [reuse render-figure.mjs virtual clock]
        +--> Pexels B-roll + caption card  (abstract or intro scenes)
        |
        v
 04b RENDER (deterministic, per scene, 1080p and 9:16)
        |
        v
 04c VISUAL QA: ffprobe gates + 3 sampled frames -> Haiku vision check
        |        (legible? clipped? matches narration?)  -> up to 2 repairs
        |        still failing -> fallback: Pexels B-roll + captions
        v
 06 RENDER/MIX (unchanged)
```

Why this works for the "everything automatic" goal:
- Every output is code or API data, so it is deterministic, free to render, and auditable.
- Reveals are driven by `words.json`, which fixes G2.
- The vision check fixes G3 without a human.
- Anatomy figures stay as optional hero beats (D4), no longer the backbone.

**Cost tension (honest):** this raises LLM spend. My rough estimate, not measured: about 25 scenes x 3k output tokens at $10/MTok is about $0.75 per long video, plus input and about 30% repairs, so $1.2-1.8 per long video. That crosses the current $1.50 per-run cap and pushes the month near the $25 cap. Levers: Haiku for simple scenes, prompt caching on the static system prompts, Gemini free-tier Flash for QA checks, and raising `per_run_cap_usd` to about 2.5. Measure real tokens in the Task 16 pilot before settling.

### Thumbnail (G5)
Generate a background image with FLUX.2-klein-4B (Apache 2.0 weights, about 8 GB VRAM per vendor note, so not local on 4 GB) via Kaggle for a pre-made background pack, or via NIM during development only. Overlay the title with the existing HTML capture tool. Fallback stays the frame-grab already in Task 12.

### Music (G6)
One-off job: generate 20-30 instrumental loops with ACE-Step on Kaggle, record prompt, model hash and licence text in `assets/music/LICENSES.md`, then pick by mood tag per run. Do this only after you are comfortable with the ACE-Step output-rights wording; otherwise download a one-time CC0 pack manually (a single chore, not recurring).

### Research (G7)
Add a research step before script: for the chosen trend item, fetch the primary page plus 2-3 related sources (paper, repo README, docs) with a local extractor (for example `trafilatura`, UNVERIFIED on Windows) and store cleaned text as `sources[].quote` material. Claim check then runs against more than one page.

### Approval (G8)
Technically the whole pipeline can run unattended after the fixes above. I would not remove the human step on day one: monetization is judged at channel level and the claim check cannot prove facts. The smallest honest version of "fully automatic" is Task 18 (auto-schedule 24 h out, owner veto by Telegram), enabled after 10 clean approvals. If you want it sooner, lower the bar to 5 clean approvals with an explicit written acceptance of the risk. That is your call, not a technical limit.

---

## 4. Tool choices per gap

| Gap | Tool | Licence / limit | Runs where | Status |
|---|---|---|---|---|
| G1 diagrams, algorithms | Manim | MIT (unchecked) | Local CPU; needs Cairo, ffmpeg, LaTeX for math text | Spike E |
| G1 architecture, code, charts | HTML/SVG + existing `render-figure.mjs` (works on any HTML, not only Anatomy) | yours | Local | Reuse Task 10 |
| G1 authoring | Anthropic API (Sonnet/Haiku) with vendored Remotion/Manim skill prompts | per plan | API | Task 11a |
| G2 sync | `words.json` cues passed to scene author | n/a | n/a | Reorder stages |
| G3 pixel QA | Haiku vision on 3 frames per scene | API cost | API | Task 11c |
| G4 B-roll | Pexels API | free, attribution | API | Task 11d |
| G5 thumbnail | FLUX.2-klein-4B or FLUX.1-schnell | Apache 2.0 (klein); NIM only for dev | Kaggle batch or NIM (dev) | Task 12 change |
| G6 music | ACE-Step 1.5 once, or CC0 pack | MIT claim, rights unclarified | Kaggle batch | Task 20 |
| G7 research | local extractor + 2-3 sources | n/a | Local | Task 6 change |
| G9 compute | Kokoro on CPU; heavy jobs on Kaggle in batches | Kaggle quota floats | mixed | Spike F |

Rejected for the daily loop: NIM as a runtime dependency (licence), Hugging Face hosted inference (credits too small), Gemini image and Veo (not free), open video diffusion models (VRAM, text accuracy), the Clipper skill (policy).

---

## 5. Patches to `Plan.md`

1. **Stage order (Sections 2, 6, Task 15):** run 03 TTS and 05 Subtitles before 04 Visuals. Task 11 then consumes `words.json`.
2. **Schema (Task 6):** add `scenes[].cues: [{"t": float, "text": str}]` (filled after alignment, not by the writer) and `scenes[].broll_query: str`. Add `renderer: "manim" | "html" | "stock"` to `visual`.
3. **Fix the `diagram` bug in Task 11 immediately:** until 11a exists, route `diagram` to a real handler or to the stock fallback, not the title branch. Add a test that `scene_html({"type":"diagram",...})` is not a plain text card.
4. **New Task 11a, scene author.** Interface: `author_scene(scene, cues, llm, cfg) -> SceneCode(kind, source, params)`. Tests with `FakeLLM`: bad code triggers at most 2 repairs; hostile strings never reach a shell or filter string; Manim source is run in a subprocess with a timeout, no network, working directory limited to the run folder.
5. **New Task 11b, Manim renderer.** `render_manim(source, out_mp4, size, fps)` plus ffprobe gates. Test with a fixed two-line scene.
6. **New Task 11c, visual QA.** `inspect_frames(mp4, narration, llm) -> {ok, problems}` on 3 sampled frames. Test with a deliberately clipped-text fixture.
7. **New Task 11d, B-roll.** `pexels.search(query, orientation)`, local cache for 24 h, credit lines appended to the description. Test with a recorded API fixture.
8. **Task 12:** thumbnail from generated background plus overlay; keep the frame-grab fallback.
9. **Task 6 step 6:** multi-source research as in section 3.
10. **New Spikes in Task 4:**
    - **E:** Manim on this Windows PC (install, render a 5 s scene, time it). Fallback: run Manim in WSL or Docker, or drop to HTML scenes only.
    - **F:** Trigger one Kaggle notebook run headlessly and fetch its output. If it fails, music and thumbnail backgrounds become a once-a-month manual batch.
    - **G:** Ask Pexels whether a description credit meets their attribution rule; test one real query.
11. **Task 18 (autopilot):** keep the gate, but move it ahead of Task 17 if you want maximum automation.
12. **Budget:** add a pilot measurement of scene-authoring tokens to Task 16 and set `per_run_cap_usd` from the result, not from my estimate.

---

## 6. Still unverified

- Manim and `trafilatura` installation on Windows 11 here.
- Kaggle headless kernel runs and the real weekly GPU quota.
- Whether NVIDIA would treat your channel as "production" (the FAQ language says probably; only NVIDIA can say).
- ACE-Step output-rights wording; the authors have not answered the open question.
- Licence terms of each Claude skill repo before vendoring its prompts.
- Free image generation on the Gemini API (sources conflict).
- Actual per-video LLM cost of the scene-authoring loop.

## Sources

- NVIDIA NIM FAQ: https://docs.api.nvidia.com/nim/docs/product and https://forums.developer.nvidia.com/t/nvidia-nim-faq/300317
- NVIDIA Build catalog: https://build.nvidia.com/models and https://pypi.org/project/genblaze-nvidia/
- Hugging Face Inference Providers pricing: https://huggingface.co/docs/inference-providers/pricing
- Gemini free tier: https://yingtu.ai/en/blog/google-gemini-api-free-tier-limits-2026 and https://ai.google.dev/gemini-api/docs/rate-limits
- Free GPUs: https://gpuperhour.com/blog/free-cloud-gpus-and-credits
- Pexels API: https://help.pexels.com/hc/en-us/articles/900005852323
- ACE-Step: https://huggingface.co/ACE-Step/acestep-5Hz-lm-4B and https://github.com/ace-step/ACE-Step-1.5/discussions/1256
- Open video models: https://ltx.io/blog/best-open-source-video-generation-models and https://www.thundercompute.com/blog/best-open-source-ai-video-generation-models
- Open TTS: https://tts.ai/blog/open-source-text-to-speech-guide-2026/
- Claude video skills: https://github.com/wilwaldon/Claude-Code-Video-Toolkit
