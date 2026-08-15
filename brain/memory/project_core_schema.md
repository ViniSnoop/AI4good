---
name: project-core-schema
description: "core/ agent-library soundness work — enforced frontmatter contract, tier unification, deferred sweep"
metadata: 
  node_type: memory
  type: project
  originSessionId: b984cbbb-d1a1-4ff4-a01a-76dd62abd2f0
  modified: 2026-07-18T17:35:19.876Z
---

Making the `core/` agent library structurally sound = SPEC-v0 pilot of [[spec-driven-development]] (the `core/` side; a parallel track does the `code/` module-spec side).

**Canonical docs (read before continuing):** `core/SCHEMA.md` (the enforced per-layer frontmatter contract + flow-type/discipline matrix; `deepresearch` is the oracle) and `core/ROADMAP.md` (status + the deferred sweep).

**Shipped 2026-07-18** (commit `refactor(core): enforce per-layer frontmatter contract`): SCHEMA.md, flows/+agents/ templates, tier unified (`thinking:`/`model:`→`tier:` on core/agents), reviewer/lead/MIGRATION-STATUS bugs fixed, `compare` flow normalized, `sync-skills` validates frontmatter + prunes orphan mirrors (wired into pre-commit §10a).

**Deferred sweep (in ROADMAP):** 2b loop-agent `tier:` source + `tier-map.json` + generator for `.claude/agents/loop-*` (kills last `model: haiku` in source) — but loop-* files are often contended by a parallel session, see [[feedback-parallel-sessions]]; the flow sweep (disciplines on the other flows); mechanism-search normalize; flow/agent field validation.
