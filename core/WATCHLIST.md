# Watchlist
> AI / agent / model tooling to evaluate — candidates to try, not references to read. Promote a winner into a project or a `/research` pass when it earns a real look.
> On-demand doc — never CONTEXT.md.

## Frameworks / methods
- [weft](https://github.com/WeaveMindAI/weft) · [node docs](https://weavemind.ai/docs/nodes) — node language; test the principles or the language itself
- [OpenJarvis](https://github.com/open-jarvis/OpenJarvis) — assistant framework
- [claude-code + remotion animations (van Clief)](https://www.skool.com/cliefnotes/classroom/d3907117?md=f7a33a9888604a08a7e48bb876682691) — tutorial; feeds the animation-generator project idea
- Jake van Clief — folders-replace-agents method: [classroom](https://www.skool.com/cliefnotes/classroom/036893d9?md=2b4a8ab7461c4f6d828e21c0eb196a6a) · [folder structure video](https://www.skool.com/cliefnotes/new-video-how-i-structure-folders-to-replace-ai-agents)
- [Claude Code skills for UI animation](https://www.instagram.com/p/Da7y0g3DLWT/) — 3D scenes, scroll effects, Lottie. ⚠ DM-bait post, no links delivered; the *idea* is the value. Feeds `teaching-materials` [research-tools]
- [three-lane model routing](https://www.instagram.com/reel/DbHHdF4gLWS/) — cheap model reads all mail/docs and compresses to one briefing, expensive model only on the briefing. Same tiering `/loops` autorouting does; see `craft-flows` [tier-briefing]
- [Reticulum](https://github.com/markqvist/Reticulum) — E2E-encrypted network stack that keeps working with no internet/infrastructure. Feeds `workspace-os` [offline-resilience]
- [Charlie Hills — match-the-model-to-the-job routing](https://www.instagram.com/p/DbHGtXoCOm-/) — 9-step CLAUDE.md workflow: Opus/Fable plan, Sonnet builds, Haiku+subagents grunt, then two judges (Claude reads the transcript + a second model reviews), every catch logged back to CLAUDE.md so the setup compounds. Same tiering `/loops` does; the *two-judge review* + *log-every-catch* angles are the new bits worth stealing
- [opensession.co — PRD-driven agent orchestration (Claude plugin)](https://www.instagram.com/opensession.co/reel/DXwl0ryhbgV/) — open-sourced framework: turns PRDs into task briefs, extended planning over hundreds of tasks, context-efficient, configurable model routing + branching; 22 agents / 11 commands / 8 skills. Comment "OS" to get it. Compare against our flows before importing
- [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) + [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses) — two curated collections of agent-harness engineering (Lucas: "muito ruído, mas talvez algo útil pro wos"); mine for anything our craft flow lacks
- [meta-harness (Yoonho Lee)](https://yoonholee.com/meta-harness/) — Lucas: "VERY INTERESTING, maybe an alternative or improvement over Claude Code"; read seriously as a harness-design candidate
- [Vyzual — Claude Code weekly ship log](https://www.instagram.com/p/DbIo0eaErW9/) — per-agent effort levels (low→max) on Managed Agents (cheapest multi-agent lever: routing agents→low, high/max only for real reasoning), live iOS Simulator pane, `--ax-screen-reader` mode, security scanner plugin. Lucas: "considerar com cuidado pro workspace" — effort-levels especially relevant to our subagent cost

## Data / ingestion
- [opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf) — 0.015s/page PDF parsing on CPU. Candidate backend for `core/tools/parse`, which exists and is slower

## Models / runtimes
- kimi 2.6, kimi 2.7
- GLM-5.2
- airLLM + Qwen3.6 (14B–20B) and/or Laguna XS.2; LFM2.5
- turbovec (google compressions, 31b → 4b)
- moonshot AI · qwen code
- [Qwen3.6-27B 1-bit / ternary](https://www.instagram.com/reel/Da0UiHfsvUk/) — 54GB fp16 → 3.9GB at 1-bit, 5.9GB ternary, architecture untouched. Phone-viable; see `local-ai` [tiny-quant]
- [KittenTTS](https://github.com/KittenML/KittenTTS) — TTS under 25MB, runs on CPU, free. ⚠ pt-BR support unverified — check that first, it decides everything

## Agents / tools
- claude council
- ECC
- odysseus (pewdiepie)
- hermes agent — "ver o que é o hermes pra IA"
- higgsfield mcp
