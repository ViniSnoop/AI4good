# Tooling and comparable systems
> What lints an agent setup, what to compare against, and how to draw it.
> answers: agent-setup linters, systems worth comparing, generated diagrams

## Tooling — linting / evaluating an agent setup

> The category that answers "how do I know my workspace actually works". We have `verify-fast` for
> hook *code*, nothing for agent *behavior*.

- `[C]` [BenMalaga/claudemd-check](https://github.com/BenMalaga/claudemd-check) — lints instruction files.
- `[C]` [lukasmetzler/agenteval](https://github.com/lukasmetzler/agenteval) · [lint
  docs](https://github.com/lukasmetzler/agenteval/blob/main/docs/lint.md) — eval harness for agent
  configs.
- `[C]` [jed1978/instrlint](https://github.com/jed1978/instrlint) — instruction-file linter.
- `[C]` [How to Know Your Claude Code Setup Actually
  Works](https://ranjankumar.in/claude-code-testing-your-setup) — practitioner method for testing a
  setup beyond skill level.

## Comparable systems (structure to compare against, not to copy)

- `[C]`
  [jimy-r/agent-workspace-architecture](https://github.com/jimy-r/agent-workspace-architecture) —
  closest structural sibling found.
- `[C]` [kumakuma010/claude-second-brain](https://github.com/kumakuma010/claude-second-brain) ·
  [OoneBreath/claude-code-project-brain](https://github.com/OoneBreath/claude-code-project-brain) —
  `brain/` analogues.
- `[C]` [lifan-builds/context-harness](https://github.com/lifan-builds/context-harness) ·
  [amajorai/context.md](https://github.com/amajorai/context.md) — CONTEXT.md-style routing
  conventions in the wild.
- `[C]` [linuz90/claude-telegram-bot](https://github.com/linuz90/claude-telegram-bot) — already the
  `code/aiwbot` reference.
- `[C]` [JCode — Claude Code's harness rebuilt in Rust](https://www.instagram.com/reel/DbOOs0WpCXJ/)
  — [src: web:instagram.com] theopenstack claims one developer rewrote the *software layer between
  user and model* from scratch in Rust, yielding a lighter, faster assistant that runs several
  specialist agents on one project at once; the framing is that the harness, not the model, is what
  makes AI coding expensive. No repo linked (comment-gated), no numbers, no independent measurement
  — treat the cost claim as the interesting hypothesis, not a finding. Assessment task in
  `brain/goals/workspace-os.md` `[jcode-custo]`. Lucas: *"averiguar se realmente é bom... fiquei curioso pra entender se
  realmente é o harness que deixa tudo caro"*.

## Workspace visualization (diagrams generated from the tree)

> Evidence behind the workspace-visualization work in [/ROADMAP.md](../../ROADMAP.md). Captured 2026-08-18.

- `[A]` [Ghoniem, Fekete & Castagliola — readability of node-link vs matrix
  graphs](https://journals.sagepub.com/doi/10.1057/palgrave.ivs.9500092) (Information Visualization
  2005) — controlled experiment: **matrix representations beat node-link once a graph passes ~20
  vertices** on most tasks, losing only on path-following. The basis for drawing WOS's dense "what
  enforces what" relation as a grid, not a graph.
- `[A]` [Holten — Hierarchical Edge
  Bundles](https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Holten06.pdf) (IEEE TVCG 2006) —
  keeps a hierarchical layout while bundling cross-cutting edges so only real cross-tree
  dependencies stand out; invented for software adjacency data. The technique for "what reads what"
  over the CONTEXT.md tree without a hairball.
- `[A]` [Shneiderman — Visual Information-Seeking
  Mantra](https://infovis-wiki.net/wiki/Visual_Information-Seeking_Mantra) — overview first, zoom &
  filter, details on demand. A full-detail dump violates it whatever the technique; the reason the
  *is* and *becoming* pictures stay separate and start at overview.
- `[C]` [NN/g — Treemaps](https://www.nngroup.com/articles/treemaps/) · [AniMatrix — matrix-based
  software-evolution
  viz](https://www.researchgate.net/publication/265789153_AniMatrix_A_Matrix-Based_Visualization_of_Software_Evolution)
  — treemap for folder mass/activity (weak for depth); **matrix-over-time** (rows=component,
  cols=week) for the *becoming* picture, reusing the *is* picture's matrix grammar so one visual
  language serves both.
- `[C]` [Mermaid](https://mermaid.js.org/) ·
  [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) · [Sankey
  pitfalls](https://datasketch.blog/en/post/the-5-most-common-mistakes-in-designing-a-sankey-diagram-and-how-to-avoid-them/)
  — tooling verdict: **Mermaid (renders client-side in one self-contained HTML, zero compiled
  binary) + a hand-rolled `git log --numstat` parser** is the minimal provider-agnostic
  generate-from-tree pipeline; avoid Structurizr / D2 / Graphviz-as-binary / Gource (install + rot
  cost). Steal C4's context/container/component vocabulary without adopting the tool. Sankey caps at
  ~10–12 nodes/stage and is for flow-with-conservation, not dependency.

### The health shelf — is it well tied, what is loose, what is noise

> Added 2026-08-18. The five refs above answer *how do I draw what is there*, and every one of them
> is about an **inventory**. Lucas's actual question is a **health** question — *"is WOS well tied,
> does it have loose ends, too much noise, discardable things"* — and none of the inventory
> literature addresses it. That gap is why the first `ARCHITECTURE.html` rendered correctly and
> still did not earn its read.

- `[A]` [Wettel, Lanza & Robbes — Software Systems as Cities: A Controlled
  Experiment](https://si.usi.ch/assets/publications/conf/icse/icse2011/WettelLR11.pdf) (ICSE 2011) —
  41 subjects, four locations, three countries: an overview visualization beat a
  state-of-the-practice baseline (Eclipse + Excel) by **+24.26% correctness and −12.01% completion
  time**, both significant. Two findings matter more than the headline. **(1) The advantage
  concentrates on exactly our questions** — *spread* of a property across the system (+29–38%) and
  *impact* estimation (+40–50%) — because a list "without the context provided by an overview
  deceived some subjects into believing that the spread was dispersed." That is Lucas's "is it well
  tied" read, measured. **(2) The overview did not replace the table**: "CodeCity is faster at
  building an approximate overview, a spreadsheet is faster at finding precise answers in large data
  sets… could complement each other well." So the summary layer goes **above** the enforcement
  matrix rather than instead of it, and the standing proposal to cut the matrix is contradicted by
  evidence. **Reject the technique, keep the finding** — 3D and interactive breaks
  self-contained-no-script.
- `[A]` [Cleveland & McGill — Graphical Perception and Graphical Methods for Analyzing Scientific
  Data](https://notes.billmill.org/images/Cleveland%20and%20McGill%201985%20-%20Graphical%20Perception%20and%20Graphical%20Methods%20for%20Analyzing%20Scientific%20Data.pdf)
  (Science 1985) — the accuracy ranking of elementary perceptual tasks: position along a common
  scale beats length, which beats angle/area, which beats colour and density. The evidence behind
  the ROADMAP's own instruction to render strength **as magnitude rather than as marks to be
  counted** — the current page encodes enforcement as a glyph per cell, the least accurate channel
  available, which is why a densely gated region and a sparse one look alike.
- `[P]` [Baldwin, MacCormack & Rusnak — Hidden Structure: Using Network Methods to Map System
  Architecture](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2277795) (HBS working paper
  13-093) · [LaMantia, Cai, MacCormack & Rusnak — Evolution Analysis Using Design Structure
  Matrices](https://www.hbs.edu/ris/Publication%20Files/07-081.pdf) (HBS working paper 07-081) — the
  **design structure matrix** line of work: reachability over the dependency graph classifies every
  component by how much of the system it can see and how much can see it, turning "well tied" from
  taste into a computed property. The vocabulary transfers directly to WOS (routing edges and
  feature wiring *are* a dependency graph) but **the specific core/peripheral classification could
  not be read from source this session — both hosts refused the fetch**, so it is carried as a lead
  to verify before anything is built on it, not as a finding. Working papers, never peer reviewed:
  `[P]` and provisional by rule.
- `[C]` [Few — Common Pitfalls in Dashboard
  Design](https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf) · [Why Most
  Dashboards Fail](http://www.perceptualedge.com/articles/misc/WhyMostDashboardsFail.pdf) —
  practitioner, but the failure list is the one this page walked into: exceeding a single screen,
  showing detail where a summary was needed, and encoding by decoration rather than by magnitude.
  The single-screen constraint is the operational form of Lucas's *"impact and easiness"* bar.
- `[C]` [Tornhill — Code as a Crime
  Scene](https://www.adamtornhill.com/articles/crimescene/codeascrimescene.htm) · [CodeScene
  hotspots](https://codescene.ta.philips.com/docs/guides/technical/hotspots.html) — prioritising by
  **change frequency × size** rather than by size alone, so "noise" and "discardable" become ranked
  findings instead of a big rectangle. Needs git history, which is the *becoming* picture's data —
  **parked until the *is* picture reads well**, and recorded here so it is not re-derived.

## Tooling lists captured from Instagram (2026-07-27, via aiwbot) — unassessed

Both are practitioner listicles, so `[C]`: signal about what people reach for, not evidence. Each
has a paired assessment task in the owning goal's backlog — a ref that lands without one never gets read.

- `[C]` [Top 10 Open-Source Libraries to Fine-Tune LLMs
  Locally](https://www.analyticsvidhya.com/blog/2026/05/open-source-libraries-to-fine-tune-llm-locally/)
  — Unsloth, LLaMA-Factory, DeepSpeed, PEFT, Axolotl, TRL, torchtune, LitGPT, SWIFT, AutoTrain
  Advanced. Lucas: *"pode ser útil pensando no cenário de slms"* → bears on `code/dobra`'s SLM
  runner and the local-ai goal. Source post: instagram.com/p/DbTFbikjpEw
- `[C]` [10 GitHub repos replacing paid tools](https://www.instagram.com/p/DbF347ajVbR/) — Lucas:
  *"checar se algumas são melhores do que as que já temos no wos"*. **The ten names are in the
  carousel images, not the caption**, so extracting them needs the image path
  (`core/tools/video/video` on the post pulls captions only; `video_images.py` does OCR per image).
- `[C]` [Baidu "Unlimited OCR"](https://www.instagram.com/reel/DbWZwciSP4l/) — [src:
  web:instagram.com] claims a compact model that reads a 100-page PDF in one pass, preserving
  layout, tables and reading order, running locally under MIT. Lucas: *"checar se é útil pra gente"*
  → lands squarely on the open OCR dependency named in `brain/goals/ecovila.md` `[org-docs]`
  (image-only PDFs in `branches/ecovila/burocracia/` that `core/tools/paper/parse` returns empty
  for). Claim is a
  vendor/practitioner post, not a benchmark — verify on a real scanned PDF before touching the
  toolchain.
- `[C]` [Surfsense](https://www.instagram.com/reel/DbTp-OayCcU/) — [src: web:instagram.com]
  self-hostable research assistant in the NotebookLM/Perplexity mould, pitched as connecting your
  own sources. Overlaps what `core/tools` + the research flow already do, so the question is whether
  it beats the parts we own — no assessment task is tracked yet; pair one in the owning goal's
  backlog before acting on this.
- `[C]` [Claude Code animation/UI skill set](https://www.instagram.com/p/DbBJSzvnP3J/) · [same list,
  second post](https://www.instagram.com/p/Da5jnu9E_0n/) — [src: web:instagram.com] captured twice
  from different accounts (Matheus Castro, Rifqi Eka Hardianto), same six repos named only in the
  carousel images: `claude-code-skills`, `threejs-skills`, `gsap-skills`, `motion-design-skill`
  (Lottie), `design-dna` (extract a site's visual identity into tokens), `genjutsu` (UI system).
  Comment-gated — **no links published**, so any use starts with finding whether the repos exist.
  Folded into the "Survey outside skills" item in [core/ROADMAP.md](../ROADMAP.md).
- `[C]` [VoiceBox — voice cloning from 3s of audio](https://www.instagram.com/p/DbOtgWlmqOt/) —
  [src: web:instagram.com] vinisousabr claims an open-source, locally-run cloner covering 23
  languages at zero API cost, pitched against ElevenLabs, and doubling as voice-to-text against
  WhisperFlow. Comment-gated, no repo link, and the name collides with Meta's Voicebox — **identity
  unverified**. Ref-only: no Lucas note, no task. If it ever gets picked up, pt-BR support is the
  first thing to check, same as `KittenTTS`.
- `[C]` [Claude Code graph-native agent orchestration](https://www.instagram.com/p/DbVwFxaDYPw/) —
  [src: web:instagram.com] Vyzual AI: Claude Code shipped a graph-native way to orchestrate agents,
  and a separate viral post credits a Microsoft/Stanford/Anthropic "Graph Engineering" discovery —
  the post itself says only one of the two is real, so treat both as unverified. Lucas: *"acho que
  serve pra gente"* → bears directly on `code/flows` (graph workflow engine) and the craft flow;
  assessment task in `brain/goals/craft-flows.md` `[graph-native]`.

---
