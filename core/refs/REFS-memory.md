# Agent memory
> How an agent remembers, and what untrusted text does to that store.
> answers: memory architecture, injection into a trusted store

## Agent memory — architecture

- `[A]` [How Memory Management Impacts LLM Agents: An Empirical Study of
  Experience-Following](https://arxiv.org/abs/2505.16067) (ACL 2025, 65 cites) — **peer-reviewed**
  evidence that memory *management policy* (what gets added/removed) dominates outcomes; error
  propagation and misalignment accumulate. Closest published anchor to what `/inbox` + goals do.
- `[P]` [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) (arXiv, ~970
  cites) — virtual-memory paging metaphor; heavily cited, still a preprint.
- `[P]` [MemOS: An Operating System for Memory-Augmented
  Generation](https://arxiv.org/abs/2505.22101) (arXiv, 2025) — memory as first-class OS resource.
- `[P]` [AIOS: LLM Agent Operating System](https://arxiv.org/abs/2403.16971) (arXiv, 2024) —
  kernel/scheduler framing for agent systems.
- `[P]` [Are We Ready For An Agent-Native Memory System?](https://arxiv.org/abs/2606.24775) (arXiv,
  2026-06) — memory as a data-management system with lifecycle governance; criticises that
  evaluation is only end-to-end black box.

## Agent memory — security (untrusted input → trusted memory)

- `[P]` [From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning in LLM
  Agents](https://arxiv.org/abs/2606.04329) (arXiv, 2026-06) — 4 write channels
  (explicit-instruction, system-prompt-driven, **compaction-driven**, experience-to-procedure), 9
  structural vulnerabilities, 6 attack classes, MPBench. **One successful write persists across
  sessions**; existing prompt-injection defenses do not cover it. Our INBOX ingest path exactly.
- `[P]` [Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound
  Authority](https://arxiv.org/abs/2606.24322) (arXiv, 2026-06) — content-based and lineage-based
  trust are both malleable; proposes origin-bound authority. Shape of the fix for INBOX provenance
  tagging.
- `[P]` [Defeating Prompt Injections by Design (CaMeL)](https://arxiv.org/abs/2503.18813) (Google
  DeepMind, 2025) · [code](https://github.com/google-research/camel-prompt-injection) —
  capability/dataflow separation between planner and untrusted data. Reference design for "fetched
  content is data, never instruction".
- `[P]` [Securing AI Agents with Information-Flow Control](https://arxiv.org/abs/2505.23643) (arXiv,
  93 cites) — IFC applied to agent pipelines.
- `[P]` [System-Level Defense against Indirect Prompt Injection: An Information-Flow
  Perspective](https://arxiv.org/abs/2409.19091) (arXiv, 88 cites).
- `[A]` [Red-Teaming LLM Multi-Agent Systems via Communication
  Attacks](https://arxiv.org/abs/2502.14847) (ACL 2025, 112 cites) — peer-reviewed anchor for
  multi-agent trust boundaries.
- `[A]` [SecAlign: Defending Against Prompt Injection with Preference
  Optimization](https://arxiv.org/abs/2410.05451) — model-level defense; complementary to
  system-level.
- `[P]` [Memory Poisoning Attack and Defense on Memory Based
  LLM-Agents](https://arxiv.org/abs/2601.05504) (arXiv, 2026-01).
