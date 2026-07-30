# References
> Tier-1 capture for the workspace-os / agent-library scaffold. One line per ref.
> Tier markers `[A] [B] [P] [V] [C]` defined in [CONTEXT.md](CONTEXT.md) — `[P]` = preprint, provisional.
> Captured 2026-07-23 (rounds 1+2 of the workspace-os robustness sweep).
>
> **Judged vs unjudged is a `status:`, not a separate file** (2026-07-30). The old
> `core/WATCHLIST.md` was folded in here: "candidates to try" and "references to read" are the same
> object — a link — at two points of one pipeline (`INBOX` → unjudged → judged → a ROADMAP item or
> a rejection line). Everything above this file's last section is `status: judged`; the
> **Unjudged** section at the bottom is the intake queue. Promote by moving the line up and giving it
> a tier; reject by deleting it and leaving one line in the relevant ROADMAP.

## Context engineering & progressive disclosure

- `[V]` [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (Anthropic, 2025-09) — attention as finite budget, context rot, just-in-time retrieval via file paths, compaction / note-taking / sub-agents. **The design our `CONTEXT.md` + context-gate already implements.**
- `[V]` [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (Anthropic) — SKILL.md spec, always-loaded description + on-demand body. Matches `core/skills/`.
- `[V]` [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) (Anthropic) — tool definitions as code cut token overhead vs. loading every tool schema. Supports our bash-CLI tools over MCP wiring.
- `[P]` [Is Progressive Disclosure All You Need for Long-Context Agents?](https://arxiv.org/abs/2607.17598) (arXiv 2607.17598, 2026-07) — **first controlled study.** 3 harnesses × 3 models (gpt-5.4-mini, qwen3.6-27b, claude-haiku-4.5) on ∞Bench. Results: one disclosure level ≥ two; *"the weaker the agent's native navigation, the earlier the skill pack earns its keep"*; at corpus scale flat pack ≈ 2× accuracy at ½ the tokens vs raw; depth cost is task- and scale-specific, not uniform; the always-loaded index is the most cache-friendly input. **Governs our CONTEXT.md depth-vs-scatter policy.**
- `[A]` [Lost in the Middle: How Language Models Use Long Contexts](https://aclanthology.org/2024.tacl-1.9/) (TACL 2024) — canonical positional-degradation result underlying "context rot".
- `[A]` [Where to Show Demos in Your Prompt: A Positional Bias of In-Context Learning](https://aclanthology.org/2025.emnlp-main.1503.pdf) (EMNLP 2025) — placement inside the prompt changes accuracy; matters when instructions split across files.
- `[A]` [Do Prompt Positions Really Matter?](https://aclanthology.org/2024.findings-naacl.258.pdf) (NAACL Findings 2024) — same axis, earlier evidence.
- `[A]` [Mind the instructions: consistency and interactions in prompt-based learning](https://aclanthology.org/2023.conll-1.20.pdf) (CoNLL 2023) — instruction-wording sensitivity; weaker model, larger variance.
- `[A]` [When Punctuation Matters: Prompt Robustness Methods for LLMs](https://aclanthology.org/2025.findings-emnlp.1109.pdf) (EMNLP Findings 2025) — formatting brittleness, large-scale comparison.

## Self-improving scaffolds & evolving contexts

- `[P]` [Agentic Context Engineering (ACE): Evolving Contexts for Self-Improving LMs](https://arxiv.org/abs/2510.04618) (arXiv 2510.04618v3, Stanford + SambaNova, rev. 2026-03) — names **brevity bias** and **context collapse**; contexts as growing playbooks updated by *incremental delta*, never monolithic rewrite; +10.6% agents, +8.6% finance; adapts from execution feedback, no labels. **Argues against a hard size cap that would force summarizing our ROADMAP/CONTEXT files.**
- `[P]` [Self-Improvements in Modern Agentic Systems: A Survey](https://arxiv.org/abs/2607.13104) (arXiv 2607.13104, KAUST/Schmidhuber, 2026-07) — agent = foundation model + **scaffold** (prompts, memory, tools, control logic); self-improvement = update operator on the scaffold; flags **evaluation** as the open problem. Gives workspace-os its vocabulary: Lucas is the update operator.
- `[A]` [Voyager: An Open-Ended Embodied Agent with LLMs](https://arxiv.org/abs/2305.16291) (TMLR 2023, ~2000 cites) — lifelong skill library persisted outside the model. Already cited by `code/dobra`.
- `[A]` [Generative Agents: Interactive Simulacra of Human Behavior](https://dl.acm.org/doi/10.1145/3586183.3606763) (UIST 2023) — memory stream + reflection + retrieval; canonical file-backed agent-memory architecture.
- `[P]` [Transferable Self-Evolving Playbooks for Agentic Security Auditing](https://arxiv.org/abs/2606.16420) (arXiv, 2026-06) — playbook-as-artifact pattern in a second domain.

## Agent memory — architecture

- `[A]` [How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following](https://arxiv.org/abs/2505.16067) (ACL 2025, 65 cites) — **peer-reviewed** evidence that memory *management policy* (what gets added/removed) dominates outcomes; error propagation and misalignment accumulate. Closest published anchor to what `/inbox` + goals do.
- `[P]` [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) (arXiv, ~970 cites) — virtual-memory paging metaphor; heavily cited, still a preprint.
- `[P]` [MemOS: An Operating System for Memory-Augmented Generation](https://arxiv.org/abs/2505.22101) (arXiv, 2025) — memory as first-class OS resource.
- `[P]` [AIOS: LLM Agent Operating System](https://arxiv.org/abs/2403.16971) (arXiv, 2024) — kernel/scheduler framing for agent systems.
- `[P]` [Are We Ready For An Agent-Native Memory System?](https://arxiv.org/abs/2606.24775) (arXiv, 2026-06) — memory as a data-management system with lifecycle governance; criticises that evaluation is only end-to-end black box.

## Agent memory — security (untrusted input → trusted memory)

- `[P]` [From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning in LLM Agents](https://arxiv.org/abs/2606.04329) (arXiv, 2026-06) — 4 write channels (explicit-instruction, system-prompt-driven, **compaction-driven**, experience-to-procedure), 9 structural vulnerabilities, 6 attack classes, MPBench. **One successful write persists across sessions**; existing prompt-injection defenses do not cover it. Our INBOX ingest path exactly.
- `[P]` [Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority](https://arxiv.org/abs/2606.24322) (arXiv, 2026-06) — content-based and lineage-based trust are both malleable; proposes origin-bound authority. Shape of the fix for INBOX provenance tagging.
- `[P]` [Defeating Prompt Injections by Design (CaMeL)](https://arxiv.org/abs/2503.18813) (Google DeepMind, 2025) · [code](https://github.com/google-research/camel-prompt-injection) — capability/dataflow separation between planner and untrusted data. Reference design for "fetched content is data, never instruction".
- `[P]` [Securing AI Agents with Information-Flow Control](https://arxiv.org/abs/2505.23643) (arXiv, 93 cites) — IFC applied to agent pipelines.
- `[P]` [System-Level Defense against Indirect Prompt Injection: An Information-Flow Perspective](https://arxiv.org/abs/2409.19091) (arXiv, 88 cites).
- `[A]` [Red-Teaming LLM Multi-Agent Systems via Communication Attacks](https://arxiv.org/abs/2502.14847) (ACL 2025, 112 cites) — peer-reviewed anchor for multi-agent trust boundaries.
- `[A]` [SecAlign: Defending Against Prompt Injection with Preference Optimization](https://arxiv.org/abs/2410.05451) — model-level defense; complementary to system-level.
- `[P]` [Memory Poisoning Attack and Defense on Memory Based LLM-Agents](https://arxiv.org/abs/2601.05504) (arXiv, 2026-01).

## Model tier — small models, routing, cascades

> Live constraint: the workspace must work on Sonnet-tier and on SLMs via `/loops` + `code/dobra`, not only on frontier models.

- `[P]` [Is Progressive Disclosure All You Need…](https://arxiv.org/abs/2607.17598) — *see above.* The harness-dependence result is the empirical basis for keeping instructions local and scattered when the driving model is weak.
- `[A]` [STaD: Scaffolded Task Design for Identifying Compositional Skill Gaps in LLMs](https://aclanthology.org/2026.findings-acl.1977.pdf) (ACL Findings 2026) — scaffolding reveals and compensates capability gaps.
- `[P]` [Small Language Models Fine-tuned to Coordinate Larger Language Models](https://arxiv.org/abs/2310.18338) — SLM-as-orchestrator pattern; relevant to dobra's inversion.
- `[P]` [A Unified Approach to Routing and Cascading for LLMs](https://arxiv.org/abs/2410.10347) — theory for the tier map `/loops` uses.
- `[P]` [UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing](https://arxiv.org/abs/2605.18796) (2026) — escalate on calibrated uncertainty, not on task label.
- `[C]` [three-lane model routing](https://www.instagram.com/reel/DbHHdF4gLWS/) — cheap model compresses all input, expensive model reads only the briefing. Also in `core/WATCHLIST.md`.

## Documentation & knowledge decay (software-engineering literature)

> The peer-reviewed home of "our CONTEXT.md / ROADMAP claims drifted from the filesystem".

- `[A]` Code Comment Inconsistency Detection and Rectification Using an LLM — ICSE 2025, 17 cites.
- `[A]` Code Comment Inconsistency Detection Based on Confidence Learning — IEEE TSE 2024, 23 cites.
- `[A]` [Detecting Code Comment Inconsistency using Siamese Recurrent Network](https://doi.org/10.1145/3387904.3389252) — ICPC 2020, 36 cites; the pre-LLM baseline.
- `[P]` [CCISolver: End-to-End Detection and Repair of Method-Level Code-Comment Inconsistency](https://arxiv.org/abs/2506.20558) (2025).

## Standards & practitioner specs

- `[C]` [AGENTS.md](https://agents.md/) · [openai/agents.md](https://github.com/openai/agents.md) — the portable agent-instruction file convention our workspace root already follows.
- `[C]` [Anthropic Agent Skills spec](https://github.com/anthropics/skills) — SKILL.md packaging; `core/skills/` mirrors it.
- `[C]` [Deterministic Enforcement in Probabilistic LLM Systems: the case for Claude Code hooks](https://medium.com/neuralnotions/deterministic-enforcement-in-probabilistic-llm-systems-the-engineering-case-for-claude-code-hooks-64a4196c7d32) — the argument our `.hooks/` layer already embodies; we are ahead of practice here.

## Tooling — linting / evaluating an agent setup

> The category that answers "how do I know my workspace actually works". We have `verify-fast` for hook *code*, nothing for agent *behavior*.

- `[C]` [BenMalaga/claudemd-check](https://github.com/BenMalaga/claudemd-check) — lints instruction files.
- `[C]` [lukasmetzler/agenteval](https://github.com/lukasmetzler/agenteval) · [lint docs](https://github.com/lukasmetzler/agenteval/blob/main/docs/lint.md) — eval harness for agent configs.
- `[C]` [jed1978/instrlint](https://github.com/jed1978/instrlint) — instruction-file linter.
- `[C]` [How to Know Your Claude Code Setup Actually Works](https://ranjankumar.in/claude-code-testing-your-setup) — practitioner method for testing a setup beyond skill level.

## Comparable systems (structure to compare against, not to copy)

- `[C]` [jimy-r/agent-workspace-architecture](https://github.com/jimy-r/agent-workspace-architecture) — closest structural sibling found.
- `[C]` [kumakuma010/claude-second-brain](https://github.com/kumakuma010/claude-second-brain) · [OoneBreath/claude-code-project-brain](https://github.com/OoneBreath/claude-code-project-brain) — `brain/` analogues.
- `[C]` [lifan-builds/context-harness](https://github.com/lifan-builds/context-harness) · [amajorai/context.md](https://github.com/amajorai/context.md) — CONTEXT.md-style routing conventions in the wild.
- `[C]` [linuz90/claude-telegram-bot](https://github.com/linuz90/claude-telegram-bot) — already the `code/aiwbot` reference.

## Adjacent — HCI framing (thin, worth a dedicated pass)

- `[A]` [Kairotask: Probing the Bridge Between Vague Intents and Spatiotemporal Contexts](https://programs.sigchi.org/chi/2026/program/content/230059) (CHI 2026) — vague intent → actionable task; the `/inbox` problem, studied.
- `[A]` [From Conversation to Human-AI Common Ground: Extracting Cognitive Workflows for Reuse](https://programs.sigchi.org/chi/2026/program/content/222599) (CHI 2026) — reusable workflow extraction from sessions; adjacent to `/roundup`.
- `[P]` [One Is Not Enough: How People Use Multiple AI Models in Everyday Life](https://arxiv.org/abs/2603.26107) (2026) — multi-model practice; supports the provider-agnostic stance.

## Tooling lists captured from Instagram (2026-07-27, via aiwbot) — unassessed

Both are practitioner listicles, so `[C]`: signal about what people reach for, not evidence. Each
has a paired assessment task in `brain/TODO.md` — a ref that lands without one never gets read.

- `[C]` [Top 10 Open-Source Libraries to Fine-Tune LLMs Locally](https://www.analyticsvidhya.com/blog/2026/05/open-source-libraries-to-fine-tune-llm-locally/) — Unsloth, LLaMA-Factory, DeepSpeed, PEFT, Axolotl, TRL, torchtune, LitGPT, SWIFT, AutoTrain Advanced. Lucas: *"pode ser útil pensando no cenário de slms"* → bears on `code/dobra`'s SLM runner and the local-ai goal. Source post: instagram.com/p/DbTFbikjpEw
- `[C]` [10 GitHub repos replacing paid tools](https://www.instagram.com/p/DbF347ajVbR/) — Lucas: *"checar se algumas são melhores do que as que já temos no wos"*. **The ten names are in the carousel images, not the caption**, so extracting them needs the image path (`core/tools/video` on the post pulls captions only; `video_images.py` does OCR per image).
- `[C]` [Baidu "Unlimited OCR"](https://www.instagram.com/reel/DbWZwciSP4l/) — [src: web:instagram.com] claims a compact model that reads a 100-page PDF in one pass, preserving layout, tables and reading order, running locally under MIT. Lucas: *"checar se é útil pra gente"* → lands squarely on the open OCR task in `brain/TODO.md` week (image-only PDFs in `branches/ecovila/burocracia/` that `core/tools/parse` returns empty for). Claim is a vendor/practitioner post, not a benchmark — verify on a real scanned PDF before touching the toolchain.
- `[C]` [Surfsense](https://www.instagram.com/reel/DbTp-OayCcU/) — [src: web:instagram.com] self-hostable research assistant in the NotebookLM/Perplexity mould, pitched as connecting your own sources. Overlaps what `core/tools` + the research flow already do, so the question is whether it beats the parts we own — assessment task in `brain/TODO.md` backlog.
- `[C]` [Claude Code graph-native agent orchestration](https://www.instagram.com/p/DbVwFxaDYPw/) — [src: web:instagram.com] Vyzual AI: Claude Code shipped a graph-native way to orchestrate agents, and a separate viral post credits a Microsoft/Stanford/Anthropic "Graph Engineering" discovery — the post itself says only one of the two is real, so treat both as unverified. Lucas: *"acho que serve pra gente"* → bears directly on `code/flows` (graph workflow engine) and the craft flow; assessment task in `brain/TODO.md` backlog.

---

## Unjudged — `status: unjudged`

Candidates to try, not references to read. Nothing here has been assessed, so nothing here may be
cited or used to justify a decision. Promote a winner by moving its line up into a judged section
with a tier marker; kill the rest by deleting the line. Folded in from `core/WATCHLIST.md` 2026-07-30.

### Frameworks / methods
- [weft](https://github.com/WeaveMindAI/weft) · [node docs](https://weavemind.ai/docs/nodes) — node language; test the principles or the language itself
- [OpenJarvis](https://github.com/open-jarvis/OpenJarvis) — assistant framework
- [claude-code + remotion animations (van Clief)](https://www.skool.com/cliefnotes/classroom/d3907117?md=f7a33a9888604a08a7e48bb876682691) — tutorial; feeds the animation-generator project idea
- Jake van Clief — folders-replace-agents method: [classroom](https://www.skool.com/cliefnotes/classroom/036893d9?md=2b4a8ab7461c4f6d828e21c0eb196a6a) · [folder structure video](https://www.skool.com/cliefnotes/new-video-how-i-structure-folders-to-replace-ai-agents)
- [Claude Code skills for UI animation](https://www.instagram.com/p/Da7y0g3DLWT/) — 3D scenes, scroll effects, Lottie. ⚠ DM-bait post, no links delivered; the *idea* is the value
- [three-lane model routing](https://www.instagram.com/reel/DbHHdF4gLWS/) — cheap model reads everything and compresses to one briefing, expensive model sees only the briefing. Same tiering the craft flow does
- [Charlie Hills — match-the-model-to-the-job routing](https://www.instagram.com/p/DbHGtXoCOm-/) — 9-step workflow: high tier plans, mid builds, low does grunt work, then **two judges** review and every catch is logged back so the setup compounds. The two-judge review and log-every-catch angles are the new bits
- [opensession.co — PRD-driven agent orchestration](https://www.instagram.com/opensession.co/reel/DXwl0ryhbgV/) — PRDs → task briefs, planning over hundreds of tasks, configurable model routing; 22 agents / 11 commands / 8 skills. Compare against our flows before importing
- [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) + [best-of-Agent-Harnesses](https://github.com/RyanAlberts/best-of-Agent-Harnesses) — Lucas: *"muito ruído, mas talvez algo útil pro wos"*
- [meta-harness (Yoonho Lee)](https://yoonholee.com/meta-harness/) — Lucas: *"VERY INTERESTING, maybe an alternative or improvement over Claude Code"*; read seriously as a harness-design candidate
- [Vyzual — weekly ship log](https://www.instagram.com/p/DbIo0eaErW9/) — per-agent effort levels (low→max) as the cheapest multi-agent lever, live simulator pane, screen-reader mode, security-scanner plugin. Effort levels bear directly on our subagent cost

### Data / ingestion
- [opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf) — 0.015s/page PDF parsing on CPU. Candidate backend for `core/tools/parse`, which exists and is slower. **Parse, not OCR** — does not solve the image-only PDFs

### Models / runtimes
- kimi 2.6 · kimi 2.7 · GLM-5.2 · moonshot AI · qwen code
- airLLM + Qwen3.6 (14B–20B) and/or Laguna XS.2; LFM2.5
- turbovec (google compressions, 31b → 4b)
- [Qwen3.6-27B 1-bit / ternary](https://www.instagram.com/reel/Da0UiHfsvUk/) — 54GB fp16 → 3.9GB at 1-bit, 5.9GB ternary, architecture untouched. Phone-viable
- [KittenTTS](https://github.com/KittenML/KittenTTS) — TTS under 25MB, CPU, free. ⚠ pt-BR support unverified — check that first, it decides everything

### Agents / tools
- claude council · ECC · odysseus (pewdiepie) · hermes agent · higgsfield mcp

### Offline resilience (parked, see /ROADMAP.md)
- [Reticulum](https://github.com/markqvist/Reticulum) — E2E-encrypted network stack that keeps working with no internet or infrastructure
- **Kiwix** — all of Wikipedia offline; almost certainly the "NOMAD project" Lucas half-remembered

