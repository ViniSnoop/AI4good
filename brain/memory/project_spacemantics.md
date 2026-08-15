---
name: project_spacemantics
description: spacemantics project — verifiable spatial DSL giving LLMs spatial capability; 4 houses (goal+code+paper+skills); read code+paper CONTEXT before any session
metadata: 
  node_type: memory
  type: project
  originSessionId: d6c727ba-f4c1-477b-8912-8097021ad9a7
  modified: 2026-07-19T18:06:26.323Z
---

**spacemantics** = give LLM agents spatial/visual capability (2D/2.5D/3D/4D-time) via a verifiable
spatial DSL + deterministic checker (semantics↔geometry; "model eyes never assert geometry, code owns
truth"). Prepose analogy generalized to agent spatial cognition. First deliverable = benchmark+method
paper proving cross-dimensional, cross-model lift (Haiku/Sonnet/Opus/Fable + GLM/DeepSeek).

Promoted 2026-07-12 from the `[visual-semantics]` seed in [[project_isoroll_scene]]'s sibling goal
craft.md. Follows the [[project_hybrid_ideation]] (cria) precedent: one brain goal
spanning a code capability + paper twin.

**Four houses** (read the CONTEXT of the target house before a session):
- `brain/goals/spacemantics.md` — coordinating hub (backlog M0-M3).
- `code/spacemantics/` — engine: `dsl/ checker/ perception/ tasks/ bench/`. ROADMAP M1 = 2.5D vertical
  slice first (most reuse from isoroll). Own git repo (git-init'd, no commit yet).
- `academy/papers/spacemantics/` — benchmark+method paper (pre-venue). Experiment design + literature
  in `outputs/research-brief.md`, plan in ROADMAP.md.
- `core/skills/spacemantics/` (planned M1) — geom-text/iso-text/spatial-3d-text/motion-text, grow from
  existing `core/skills/iso-visual.md`.

Heavy internal reuse: iso-visual.md (hard rule + 6 failure modes), isoroll DSL-V2-MEMO / sheet_qc /
src/assemble / painter's-algorithm; `code/corpora/` for the CV perception thread; casinhas
ifcopenshell render-for-truth for 3D. CV thread is prune-later (go/no-go per primitive). DSL named
**texpace**; surface = closed controlled-English v2 (verbs=sugar; articles=identity type system).

**Remotes (2026-07-17 — these caused a mixup, pin them):**
- code: **public GitHub** `github.com/lsfcin/spacemantics` (branch `main`, MIT). M1 W3 checker DONE:
  `checker/` scores TOP·DIR·DIST·faces·quant·HOLD·Allen on definite scenes O(n²), 39 tests green, CLI
  `python -m checker examples/office.json`. Filter run → `dsl/CHECKABILITY.md`, 4 core concepts demoted.
- paper Overleaf = `git.overleaf.com/6a5430c59a5fe10adf1fc68b` (texpace, ICLR 2026 template, branch
  `main`). **Was created by Overleaf-duplicating Dobra**, so it carried Dobra content until swapped
  2026-07-17. Dobra's OWN Overleaf is a DIFFERENT url `6a48660e2fa100e8e2c6bc04` — do not confuse.
  Local `academy/papers/spacemantics/` now tracks the texpace Overleaf as origin/main.

**M1 W2b + W3 DONE (2026-07-17):** surface v2 fully regenerated — TYPES/EXAMPLES/GRAMMAR-PROSE/
GRAMMAR-JSON/SPEC + paper `sections/04_method.tex` (dual surface + ablation, paper recompiles 10pp).
GRAMMAR-PROSE article rule is syntactic (`move a ball` = grammar error); GRAMMAR-JSON grounds on the
REAL checker AST. Note: weekly limit is per SUBAGENT TIER (Sonnet), not the main Opus thread — main
thread can just do the work directly. Only W3b (prose→AST parser impl) left, deferred to M1 tail
(grammar written+traced; it's an M2 ablation axis, not a checker dependency).

**Visual pilot + M2 blocker (2026-07-19):** built `bench/` (WITH/WITHOUT harness — 3 arms: WITHOUT
one-shot · blind k-retries control · WITH k-retries w/ checker verdicts; checker scores all) and
`adapters/` (`texpace→SVG`, checker verdicts drawn on the picture; `python -m adapters scene.json`).
Published visual demo artifact. **Fixed a real checker bug**: 2D profile was unimplemented — `above` was
+Z (gravity) not +Y, and thin 2D boxes read as EC under tolerance; now honors C1 (above=+Y, Z flattened),
43 tests green. **KEY DECISION for the experiment** (Lucas's framing): WITH×WITHOUT = same model, two
conditions — WITHOUT emits raw target format (SVG) directly; WITH emits texpace → checker verifies+loops →
render. Both rendered, eyeballed. **BLOCKER:** no on-slate model here (no Anthropic/opencode key); Gemini
is off-slate + free-tier quota dies mid-loop. M2 unblock = wire Anthropic+opencode branches into
`bench/model_client.py` (provider is data) + build SVG→scene parser (to score the WITHOUT raw-SVG arm).
Completed work archived to `code/spacemantics/HISTORY.md`; ROADMAP pending-only.
