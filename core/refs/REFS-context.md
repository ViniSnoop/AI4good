# Context engineering
> Filling a context window well, and scaffolds that rewrite their own rules.
> answers: progressive disclosure, skill packs, self-improving contexts

## Context engineering & progressive disclosure

- `[V]` [Effective context engineering for AI
  agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  (Anthropic, 2025-09) — attention as finite budget, context rot, just-in-time retrieval via file
  paths, compaction / note-taking / sub-agents. **The design our `CONTEXT.md` + context-gate already
  implements** — but see Gloaguen below: a vendor is authoritative about its product, not
  independent evidence that the pattern works.
- `[V]` [Equipping agents for the real world with Agent
  Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
  (Anthropic) — SKILL.md spec, always-loaded description + on-demand body. Matches `core/skills/`.
- `[V]` [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
  (Anthropic) — tool definitions as code cut token overhead vs. loading every tool schema. Supports
  our bash-CLI tools over MCP wiring.
- `[P]` [Is Progressive Disclosure All You Need for Long-Context
  Agents?](https://arxiv.org/abs/2607.17598) (arXiv 2607.17598, 2026-07) — **first controlled
  study.** 3 harnesses × 3 models (gpt-5.4-mini, qwen3.6-27b, claude-haiku-4.5) on ∞Bench. Results:
  one disclosure level ≥ two; *"the weaker the agent's native navigation, the earlier the skill pack
  earns its keep"*; at corpus scale flat pack ≈ 2× accuracy at ½ the tokens vs raw; depth cost is
  task- and scale-specific, not uniform; the always-loaded index is the most cache-friendly input.
  **Governs our CONTEXT.md depth-vs-scatter policy.**
- `[P]` [Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding
  Agents?](https://arxiv.org/abs/2602.11988) (Gloaguen et al., ETH Zurich SRI, arXiv 2602.11988,
  2026-02, rev. 2026-06) — **the strongest evidence against us.** Across LLMs, agents, and both
  generated and developer-committed files: context files do *not* generally raise task success, and
  cost **>20% more inference**. Verdict on the exact thing we generate: *"repository overviews,
  although popular and recommended by model providers, are not helpful"*, and directory listings did
  not speed navigation. What survived: *"instructions in the context files are well followed"* —
  they earn their place for **non-standard practices**, not for inventory.
- `[C]` [When AGENTS.md Backfires](https://notchrisgroves.com/when-agents-md-backfires/) ·
  [MarkTechPost
  summary](https://www.marktechpost.com/2026/02/25/new-eth-zurich-study-proves-your-ai-coding-agents-are-failing-because-your-agents-md-files-are-too-detailed/)
  — practitioner reading of the above. Notes the countervailing result (Lulla et al.): **curated**
  context files cut runtime 28.6% and output tokens 16.6% on focused PRs, while Gloaguen's harm
  result is concentrated in **LLM-generated** files. Treat "curated vs generated" as the axis, not
  "context files: yes/no".
- `[P]` [CodeCompass: Navigating the Navigation Paradox in Agentic Code
  Intelligence](https://arxiv.org/abs/2602.20048) (arXiv 2602.20048, 2026-02) — bigger context does
  not fix navigation; the failure mode moves from retrieval capacity to **navigational salience**.
  Graph-structured dependency navigation 99.4% vs 76.2% vanilla and 78.2% BM25 on hidden-dependency
  tasks. **The standing critique of our `API` column**: a flat symbol list is the weak form of what
  a dependency graph does properly.
- `[P]` [Probe-and-Refine Tuning of Repository Guidance for Coding
  Agents](https://arxiv.org/pdf/2606.20512) · `[P]` [Agent READMEs: An Empirical Study of Context
  Files for Agentic Coding](https://arxiv.org/pdf/2511.12884) — method and field survey; each
  guidance component should be kept only if measured to help. Not yet read past the abstract.
- `[A]` [Lost in the Middle: How Language Models Use Long
  Contexts](https://aclanthology.org/2024.tacl-1.9/) (TACL 2024) — canonical positional-degradation
  result underlying "context rot".
- `[A]` [Where to Show Demos in Your Prompt: A Positional Bias of In-Context
  Learning](https://aclanthology.org/2025.emnlp-main.1503.pdf) (EMNLP 2025) — placement inside the
  prompt changes accuracy; matters when instructions split across files.
- `[A]` [Do Prompt Positions Really Matter?](https://aclanthology.org/2024.findings-naacl.258.pdf)
  (NAACL Findings 2024) — same axis, earlier evidence.
- `[A]` [Mind the instructions: consistency and interactions in prompt-based
  learning](https://aclanthology.org/2023.conll-1.20.pdf) (CoNLL 2023) — instruction-wording
  sensitivity; weaker model, larger variance.
- `[A]` [When Punctuation Matters: Prompt Robustness Methods for
  LLMs](https://aclanthology.org/2025.findings-emnlp.1109.pdf) (EMNLP Findings 2025) — formatting
  brittleness, large-scale comparison.
- `[C]` [Anthropic cut >80% of Claude Code's system
  prompt](https://www.instagram.com/p/DbQNApxEnCh/) — [src: web:instagram.com] Vyzual AI reports six
  "inverted practices" replacing hardcoded rules: judgement over rules, interfaces over examples,
  disclosure over dumping; `TodoWrite` said to go from ~9.1k chars of worked examples to an
  enum-typed interface (pending/in_progress/completed), verification and code review moved out to
  on-demand skills, tool definitions deferred behind `ToolSearch`. **The post itself flags that the
  80%/no-loss claim is self-reported with no published benchmark — not independently verifiable,
  never cite the number.** The framework is testable on our own docs, which is the part worth
  having; assessment task in [/ROADMAP.md](../../ROADMAP.md) § Memory and always-loaded
  context. Lucas: *"ver se é verdade e se for estudar como aproveitar no wos"*.

### What this evidence actually settles for us (2026-07-30)

Two `[V]` vendor posts and one `[P]` preprint told us to build `CONTEXT.md`; a second `[P]` preprint
now says the inventory half of it does not pay. Both are unreviewed, so neither decides alone — what
decides is that we measured our own tree. The verdict, kept here so the next session inherits it
instead of re-litigating:

| Claim | Holds for us? | Why |
|---|---|---|
| Routing/navigation is the right job for `CONTEXT.md` | **yes** | our Subdirectory table is 5% of the corpus; nothing in the evidence argues against cheap navigation, and 2607.17598 calls the always-loaded index the most cache-friendly input |
| "Repository overviews are not helpful" (Gloaguen) | **partly** | it convicts *generated* overview prose. Our `Description` is each file's own first-line comment — curated at source, 6% placeholder noise — which lands on Lulla's helpful side |
| Per-file symbol dumps earn their place | **no** | the `API` column is the flat form CodeCompass beats with a dependency graph. Trimmed to non-`test_*` symbols; a real graph is the open question |
| "Context files cost >20% inference" | **not at our scale** | measured: 457 tok median per chain, cached, ~one `AGENTS.md`. The 55k corpus figure is a sum nobody pays |
| Instructions/non-standard practices are what pays | **yes, strongly** | the one thing both studies agree on. It is the `CONTEXT.md` *head*, not the tables |

**Open, and honest about it:** nobody has A/B'd our own tables on our own tasks. Probe-and-refine
(above) is the method for that if the question ever becomes load-bearing. Until then the tables stay
because they are cheap per chain, not because the evidence endorses them.

## Self-improving scaffolds & evolving contexts

- `[P]` [Agentic Context Engineering (ACE): Evolving Contexts for Self-Improving
  LMs](https://arxiv.org/abs/2510.04618) (arXiv 2510.04618v3, Stanford + SambaNova, rev. 2026-03) —
  names **brevity bias** and **context collapse**; contexts as growing playbooks updated by
  *incremental delta*, never monolithic rewrite; +10.6% agents, +8.6% finance; adapts from execution
  feedback, no labels. **Argues against a hard size cap that would force summarizing our
  ROADMAP/CONTEXT files.**
- `[P]` [Self-Improvements in Modern Agentic Systems: A Survey](https://arxiv.org/abs/2607.13104)
  (arXiv 2607.13104, KAUST/Schmidhuber, 2026-07) — agent = foundation model + **scaffold** (prompts,
  memory, tools, control logic); self-improvement = update operator on the scaffold; flags
  **evaluation** as the open problem. Gives workspace-os its vocabulary: Lucas is the update
  operator.
- `[A]` [Voyager: An Open-Ended Embodied Agent with LLMs](https://arxiv.org/abs/2305.16291) (TMLR
  2023, ~2000 cites) — lifelong skill library persisted outside the model. Already cited by
  `code/dobra`.
- `[A]` [Generative Agents: Interactive Simulacra of Human
  Behavior](https://dl.acm.org/doi/10.1145/3586183.3606763) (UIST 2023) — memory stream + reflection
  + retrieval; canonical file-backed agent-memory architecture.
- `[P]` [Transferable Self-Evolving Playbooks for Agentic Security
  Auditing](https://arxiv.org/abs/2606.16420) (arXiv, 2026-06) — playbook-as-artifact pattern in a
  second domain.
