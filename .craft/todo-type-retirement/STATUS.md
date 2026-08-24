# todo-type-retirement — chain status
provider: anthropic | tier-map: anthropic | chain-deleg: none
status: active | commit: 8117c02 | last-loop: 4a | last-updated: 2026-08-24
subtree: feature | verdict: standard

Waits on: Loop 4b (code until green) — apply `1-plan.md` § Fold Map, then T5–T9.

Done so far: Loops 0–4a. T1 (the `google-migration` goal seed + `branches/google-migration/`
cockpit) and T4 (the 31-row drive queue, moved verbatim) both landed and are committed in
`8117c02`. Acceptance is at **C4b and C8 green, C1/C2/C3/C4/C5/C6/C7 red** — run
`.craft/todo-type-retirement/acceptance.sh` for the live count. C1 has 30 of 33 short-ids still
missing, so the FOLD is the bulk of what is left, not just the delete.

Fences LIFTED 2026-08-24: the concurrent session that owned `ISSUES.md`, the `ROADMAP-*.md` set
and `core/hooks/entropy/*.py` has ended. Loop 4b may now also close the two follow-ups
`1-plan.md` § Follow-ups recorded as out-of-chain:
  1. drop `'TODO.md'` from `LEDGER_FILES` in `core/hooks/entropy/entropy_ledger.py`.
  3. rewrite `brain/memory/feedback_inbox_ref_task_pairing.md` — it is LIVE POLICY, folded into
     every session's system prompt, and it currently tells `/inbox` to write tasks into the file
     this chain deletes. Highest-consequence item in the chain.
Follow-up 2 (the `ROADMAP.md` / `ROADMAP-ledger.md` row) stays the orchestrating session's.

Branch: `feature/todo-type-retirement`, cut from the current HEAD and already checked out.
`feature/roundup-md-cap` — what the Carry lines used to name — has been merged into develop and is
behind it; resuming there would have reverted work. Do NOT create or switch branches.
