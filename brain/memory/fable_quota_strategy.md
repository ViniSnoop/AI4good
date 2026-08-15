---
name: fable-quota-strategy
description: "How Lucas spends remaining Fable 5 quota (won't renew) — Fable decides, Opus writes, Sonnet executes; multiview session DONE 2026-07-07"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7be7df5c-291b-4611-a357-7fc5ceabe31c
---

As of 2026-07-06 Lucas is in the FINAL window of Fable 5 access, little quota left (74% weekly used on 2026-07-07), won't renew.

**Why:** Fable's edge is dense reasoning/architecture, not execution loops; workspace hooks add big fixed context cost per session, so long agentic Fable sessions waste quota.

**How to apply:** Doctrine: **Fable decides, Opus writes, Sonnet executes.** The craft flow (`core/flows/craft/craft.md` + `/loops` + craft-low/medium/high agents) is the routing backbone — after the window closes, route all planning through `/loops` autorouting on Opus/Sonnet. If a Fable session drifts into grunt work, hand off to a cheaper model.

Status of prepared Fable prompts in `core/prompts/`:
- `fable-multiview.md` — **CONSUMED 2026-07-07**, prompt file DELETED 2026-07-08. Session delivered F1 procedural + multiview spine in `code/isoroll-content` (branch `feature/f1-procedural-spine`, now merged to `develop` with postproc-tests + env-utility-repair; canonical plan `ROADMAP-content-gen.md`).
- `fable-instituto.md` — **FIRING 2026-07-08** (final Fable window); deliverable `brain/attachments/instituto-estrategias.md`. Delete the prompt file once delivered.

Naming rule from that session: provider-agnostic file names ([[feedback-provider-agnostic-naming]]). Related: [[project-casinhas]].
