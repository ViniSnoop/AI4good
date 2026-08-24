# todo-type-retirement — code until green

## Carry
slug: todo-type-retirement | branch: feature/todo-type-retirement | root: /mnt/workspace
provider: anthropic | chain-deleg: none
tier-map: anthropic | verified-on: 2026-08-20
test-cmd: `make verify-fast` | e2e-cmd: none (`make entropy` writes the fenced ISSUES.md — DO NOT RUN)
criticality: normal | verdict: standard
subtree: feature | supervision: io-signoff=no arch-review=none arch-review-supervised=no
criteria: C1..C8 — see `1-plan.md`
tasks: T1..T9 — see `1-plan.md` § Plan; per-line routing in § Fold Map
context: /mnt/workspace/AGENTS.md · /mnt/workspace/brain/CONTEXT.md · /mnt/workspace/brain/SPECS.md
         · /mnt/workspace/brain/goals/CONTEXT.md · /mnt/workspace/core/CONTEXT.md

## Note — mid-4b recovery
Prior executor died on a weekly limit after landing T1+T4 (`8117c02`), never reaching this file.
Re-verified ground truth via `acceptance.sh` first: C4b+C8 green, 7 red, C1 30/36 missing — matched
`STATUS.md`. This session covers T2, T3, T5, T6, T7, T8, T9.

## Code
attempt 1: T2+T3 — re-read `brain/TODO.md` in full (plan's Fold Map abbreviates lines) and applied
every remaining row verbatim: 8 short-ids + 2 absorptions already landed by prior sessions verified,
not redone; appended 26 short-id items across 10 goal files, one absorb-in-place
(`[research-tools]`), 4 INBOX captures (newest-first). Redid `finance-terreno` properly — its grep
passed by coincidence (old pointer text itself contained "jatobá") but the dangling pointer still
needed deleting per the Fold Map. C1 coverage script → 0 missing.
T5: `git rm brain/TODO.md`; dropped `.gitignore` line `!brain/TODO.md`.
T6: dropped the `TODO.md` row/mentions from `core/SCHEMA.md`, `core/SCHEMA-placement.md`,
`entropy-dashboard.py` + `test_entropy_ledger.py` `LEDGERS` (+ "four"→"three" wos-ledger wording),
`ROADMAP-ledger.md` line 10. Fence lifted, closed: dropped `TODO.md` from `LEDGER_FILES` in
`entropy_ledger.py` (Follow-up 1).
T7: fixed the named lines in `core/skills/{inbox,roundup}.md` (source), ran `sync-skills` to
regenerate the `.claude/commands/` mirrors (never hand-edited them); fixed all cited lines in
`academy/refs/REFS.md`, `core/refs/REFS-tooling.md`, `core/refs/REFS-unjudged.md`,
`branches/ecovila/{,burocracia/}CONTEXT.md`, `brain/goals/ecovila.md`. Small additions beyond the
plan's exact line list, same defect class in the same paragraphs: roundup.md's adjacent "TODO vs
ROADMAP" footnote (direct explanation of the row I'd just changed) and ecovila.md's ease-start "ver
TODO" phrase. Fence lifted, closed: rewrote `brain/memory/feedback_inbox_ref_task_pairing.md` to
name the goal backlog / INBOX fallback instead of `brain/TODO.md` (Follow-up 3, flagged
highest-consequence by the orchestrator).
T8: regenerated `brain/CONTEXT.md` (dropped the stale TODO.md row), `brain/goals/CONTEXT.md`
(no-op, already current), `branches/CONTEXT.md` (added the `google-migration/` row).
2 reds found and fixed mid-loop, both from `make verify-fast`/entropy checks rather than the
red/green TDD loop 4a set up (this task has no code seam, per `3-arch.md`'s Amendment): (1)
`test_pointer_integrity` on a dead `[brain/TODO.md](brain/TODO.md)` link in `ROADMAP.md`'s own
header prose (line 10 — not the front-item row the orchestrator reserved, which never held a
markdown link) — reworded, "one of the four"→"three". (2) my own new `brain/INBOX.md` provenance
tag tripped the dated-completion-report entropy check (banned verb "retired" near a date) — a real
corpse by the project's own rule; reworded to drop the banned verb.
green: yes run: `508 passed in 35.60s` (matches Carry baseline; `acceptance.sh` C8 also PASS)
touched: `brain/TODO.md` (deleted), `.gitignore`, `core/SCHEMA.md`, `core/SCHEMA-placement.md`,
`core/hooks/entropy/{dashboard/entropy-dashboard.py,entropy_ledger.py}`,
`core/tools/test/law/entropy/test_entropy_ledger.py`, `ROADMAP-ledger.md`, `ROADMAP.md`,
`core/skills/{inbox,roundup}.md`, `.claude/commands/{inbox,roundup}.md`, `academy/refs/REFS.md`,
`core/refs/{REFS-tooling,REFS-unjudged}.md`, `branches/ecovila/{,burocracia/}CONTEXT.md`,
`brain/goals/ecovila.md`, `brain/memory/feedback_inbox_ref_task_pairing.md`, `brain/CONTEXT.md`,
`branches/CONTEXT.md`, `brain/INBOX.md`, and 10 other `brain/goals/*.md` files (teaching-materials,
workspace-os, career-ufrpe, burocracia-academica, cria, craft-flows, local-ai, rpg-isoroll,
paper-megatruth, finances, home-casinhas).

## Acceptance script — final run
PASS C1 · C2 · C3 · C4 · C4b · C5 · C7 · C8 — FAIL C6: still present (1 failed)

C6 is red for a reason outside this chain: the surviving "four ledgers" hit (line 36) sits inside
the ledger-discipline **front-item row itself**, self-quoting its own future edit — exactly the row
`1-plan.md` § Follow-ups item 2 and the orchestrator's spawn prompt both mark **not mine** ("the
orchestrating session deletes those"). Line 10, the actual C6 target, reads "three" since attempt 1.
Same non-chase protocol the orchestrator set for the ISSUES.md/C7 case in `4a-tests.md`.

## Observation for the orchestrator (not a flag — reporting, not blocking)
Some hook fired mid-loop and rewrote `ISSUES.md`'s generated blocks (767→769 findings) — not invoked
via `make entropy` or the dashboard script by this executor. Net effect was positive (the stale
`brain/TODO.md` finding it carried is gone, which is why C7 went fully green with no WARN needed),
but `ISSUES.md` is FENCED and now shows in the diff regardless. Not reverted — reverting a fenced
file isn't this executor's call either, and the content is more accurate than before. Flagging so
Loop 6 knows the diff exists and where it came from.

executor: craft-medium model=anthropic/claude-sonnet-5 tier=medium deleg=none
