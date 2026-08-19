# Model tier and cost
> Small models, routing and cascades, and what the output side actually costs.
> answers: which tier suffices, where the spend is, the interface an agent acts through

## Model tier — small models, routing, cascades

> Live constraint: the workspace must work on Sonnet-tier and on SLMs via `/craft` + `code/dobra`,
> not only on frontier models.

- `[P]` [Is Progressive Disclosure All You Need…](https://arxiv.org/abs/2607.17598) — *see above.*
  The harness-dependence result is the empirical basis for keeping instructions local and scattered
  when the driving model is weak.
- `[A]` [STaD: Scaffolded Task Design for Identifying Compositional Skill Gaps in
  LLMs](https://aclanthology.org/2026.findings-acl.1977.pdf) (ACL Findings 2026) — scaffolding
  reveals and compensates capability gaps.
- `[P]` [Small Language Models Fine-tuned to Coordinate Larger Language
  Models](https://arxiv.org/abs/2310.18338) — SLM-as-orchestrator pattern; relevant to dobra's
  inversion.
- `[P]` [A Unified Approach to Routing and Cascading for LLMs](https://arxiv.org/abs/2410.10347) —
  theory for the tier map `/craft` uses.
- `[P]` [UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade
  Routing](https://arxiv.org/abs/2605.18796) (2026) — escalate on calibrated uncertainty, not on
  task label.
- `[C]` [three-lane model routing](https://www.instagram.com/reel/DbHHdF4gLWS/) — cheap model
  compresses all input, expensive model reads only the briefing. Also in `core/WATCHLIST.md`.

## Output cost & the interface an agent acts through

> The evidence behind [/ROADMAP-cost.md](../../ROADMAP-cost.md); the measurement it may
> not contradict is [`core/experiments/output-cost.md`](../experiments/output-cost.md).

- `[A]` [SWE-agent: Agent-Computer Interfaces Enable Automated Software
  Engineering](https://arxiv.org/abs/2405.15793) (NeurIPS 2024) — LM agents are a new class of end
  user; the interface they act through measurably changes behavior and performance. **The strongest
  published backing for this workspace's own bet: a gate beats a paragraph.**
- `[A]` [Token-Budget-Aware LLM Reasoning](https://arxiv.org/abs/2412.18547) (ACL Findings 2025) —
  reasoning output is *"unnecessarily lengthy"* and compresses under a prompted budget, **but a
  wrong budget degrades the answer**; dynamic per-task budgets beat one fixed number. The direct
  argument against a blanket terseness rule, and it applies with more force to `effort`, where the
  budget buys correctness rather than brevity.
- `[A]` [Harness Engineering for Agentic AI Coding Tools](https://arxiv.org/abs/2602.14690) (AIware
  2026) — 2,853 repos, eight configuration mechanisms: context files dominate and are often the
  *only* mechanism, `AGENTS.md` is becoming the cross-tool standard, few repos adopt Skills or
  Subagents. **Our bet on executable enforcement is the rare one, not the crowded one** — and ours
  is small by this baseline, with unusually much already moved out of it into hooks.
- `[A]` [LLMLingua](https://aclanthology.org/2023.emnlp-main.825/) (EMNLP 2023) ·
  [LLMLingua-2](https://aclanthology.org/2024.findings-acl.57/) (ACL Findings 2024) — input-prompt
  compression ~20x. **Captured to rule it out**: it compresses a request before sending, and the
  harness owns our request.
- `[P]` [Decoding the Configuration of AI Coding Agents](https://arxiv.org/abs/2511.09268) · `[P]`
  [Chain of Draft](https://arxiv.org/abs/2502.18600) — provisional, unread past the abstract.
- `[V]` First-party Opus 5 guidance, served by the `claude-api` skill — four points that each killed
  or shaped an item here: **`effort` is not a length lever** (it moves thinking volume, not reliably
  visible output); **files written to disk run long**, so deliverable length is calibrated
  explicitly or not at all; **Opus 5 over-delegates to subagents**, the reverse of 4.8; and **delete
  verification instructions**, because Opus 5 verifies unprompted and asking again causes
  over-verification — a delete, not a rewrite, inverting the usual self-check advice.
