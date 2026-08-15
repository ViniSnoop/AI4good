---
name: feedback_inbox_ref_task_pairing
description: "/inbox — an actionable ref must also spawn an assessment task, never land as ref-only"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e8a8e5e0-d9b6-41d4-bf96-4120838c2144
  modified: 2026-07-25T22:28:16.336Z
---

When `/inbox` routes a reference/link that carries actionable intent (Lucas's note says "investigar", "útil pro X", "pode servir pra Y", or the content plainly asks to evaluate/adopt), it must create BOTH a `refs/REFS.md` line AND a paired assessment task in the owning surface (project `ROADMAP.md ## Backlog`, or `brain/TODO.md` for cross-cutting). Pure archival refs with no intent stay ref-only.

**Why:** a link that only ever becomes a REFS.md line gets forgotten before its potential is ever assessed — the impact/improvement is never evaluated.

**How to apply:** ref line points to where the task lives; task points back to the ref. Phrase the task as the concrete next look ("assess whether X transfers to our pipeline"), not "read this". Policy is encoded in `core/skills/inbox.md` § "Policy — a ref is not the end of the line" (2026-07-25). Relates to [[project_core_schema]].
