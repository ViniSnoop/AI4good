# todo-type-retirement — tests first

## Carry
slug: todo-type-retirement | branch: feature/roundup-md-cap | root: /mnt/workspace
provider: anthropic | chain-deleg: none
tier-map: anthropic | verified-on: 2026-08-20
test-cmd: `make verify-fast` | e2e-cmd: none (`make entropy` writes the fenced ISSUES.md — DO NOT RUN)
criticality: normal | verdict: standard
subtree: feature | supervision: io-signoff=no arch-review=none arch-review-supervised=no
criteria: C1..C8 — see `1-plan.md`
tasks: T1..T9 — see `1-plan.md` § Plan; per-line routing in § Fold Map
context: /mnt/workspace/AGENTS.md · /mnt/workspace/brain/CONTEXT.md · /mnt/workspace/brain/SPECS.md
         · /mnt/workspace/brain/goals/CONTEXT.md · /mnt/workspace/core/CONTEXT.md

## Note on Loops 3 / 3.5
Per `3-arch.md` § Amendment (orchestrator, tier=max): both loops ran collapsed-and-empty — no
module, no I/O boundary, no runtime call exists in this task, only a document migration. Handoff
to this loop is `1-plan.md` § Fold Map + C1..C8 directly; there are no seams to test at, only
file-state to assert.

## Tests
Not unit tests: nothing in this task is a unit, and a permanent test asserting `brain/TODO.md` is
absent would assert a past event — the workspace deletes done work rather than keeping corpse
tests. Loop 4a instead writes one throwaway acceptance script, `acceptance.sh`, that dies with
`.craft/`. It is not added to `core/tools/test/`.

| check file | covers | asserts |
|-----------|--------|---------|
| `acceptance.sh` C1 | criterion C1 (Fold Map landed) | every non-DELETE row's short-id (33), the 3 absorb clauses, and the 4 INBOX phrases are greppable in their named destination file — pairs hardcoded from reading `1-plan.md` § Fold Map, not parsed at runtime |
| `acceptance.sh` C2 | criterion C2 (TODO.md deleted) | `brain/TODO.md` absent from disk AND untracked by git |
| `acceptance.sh` C3 | criterion C3 (type declaration killed) | no `TODO.md` in `core/SCHEMA.md` or `core/SCHEMA-placement.md` |
| `acceptance.sh` C4 | criterion C4 (routing table regenerated) | no `TODO.md` row in `brain/CONTEXT.md` |
| `acceptance.sh` C4b | new cockpit exists and is real | `brain/goals/google-migration.md`, `branches/google-migration/{CONTEXT,ROADMAP}.md` exist and are non-empty; ROADMAP.md has exactly 31 `^- \[ \]` rows |
| `acceptance.sh` C5 | criterion C5 (ledger entry killed) | no `life-todo` in `entropy-dashboard.py` or `test_entropy_ledger.py` |
| `acceptance.sh` C6 | criterion C6 (ledger count text) | no "four ledgers" in `ROADMAP-ledger.md` |
| `acceptance.sh` C7 | criterion C7 (pointer integrity) | `git grep -l 'TODO\.md'` returns only the orchestrator's named allowlist; WARN (non-failing) for the 2 fenced-this-session files on that list |
| `acceptance.sh` C8 | criterion C8 (green build) | `make verify-fast` exits 0 |

red-run: 7 failed as expected (C1, C2, C3, C4, C4b, C5, C6, C7) | wrong-failures: none — C8
(`make verify-fast`) passes in the current unmigrated tree, which is correct: verify-fast checks
the *current* repo state, and nothing has broken it yet. C8 turning red is not expected until
Loop 4b starts moving files; it will be re-run for real at the end of 4b.

## Observation for the orchestrator (not a flag — reporting, not blocking)
`acceptance.sh` C7 currently fails partly because `ISSUES.md:269` names `brain/TODO.md` in a
generated entropy finding (line-length cap). `ISSUES.md` is FENCED (do not edit) and is not on the
orchestrator's C7 allowlist. That line is a `make entropy` artifact; this chain is forbidden from
running `make entropy`, so nothing in Loops 4a/4b can make C7 fully green from inside this chain —
it depends on a later, out-of-chain entropy regeneration (once `brain/TODO.md` is gone, the finding
naturally stops appearing). Flagging for awareness only; the script is written exactly to the
orchestrator's spec and the allowlist is verbatim as given.

## Acceptance script run (current state — expected RED)
Command: `/mnt/workspace/.craft/todo-type-retirement/acceptance.sh`

```
FAIL C1: 39 missing — 'excalidraw-aula02' not in brain/goals/teaching-materials.md (+38 more)
FAIL C2: still on disk; still tracked
FAIL C3: in core/SCHEMA.md; in core/SCHEMA-placement.md
FAIL C4: row still present
FAIL C4b: brain/goals/google-migration.md missing/empty; branches/google-migration/CONTEXT.md missing/empty; branches/google-migration/ROADMAP.md missing/empty
FAIL C5: in entropy-dashboard.py; in test_entropy_ledger.py
FAIL C6: still present
WARN C7: brain/memory/feedback_inbox_ref_task_pairing.md is fenced this session — follow-up still open
WARN C7: core/hooks/entropy/entropy_ledger.py is fenced this session — follow-up still open
FAIL C7: outside allowlist: .claude/commands/inbox.md .claude/commands/roundup.md .gitignore ISSUES.md academy/refs/REFS.md brain/CONTEXT.md brain/goals/ecovila.md brain/goals/teaching-materials.md branches/ecovila/CONTEXT.md branches/ecovila/burocracia/CONTEXT.md core/SCHEMA-placement.md core/SCHEMA.md core/hooks/entropy/dashboard/entropy-dashboard.py core/refs/REFS-tooling.md core/refs/REFS-unjudged.md core/skills/inbox.md core/skills/roundup.md core/tools/test/law/entropy/test_entropy_ledger.py
PASS C8
---
8 check(s) FAILED
```

Exit code: 1. Confirmed RED — nothing has been migrated yet, as expected before Loop 4b runs.

executor: craft-medium model=anthropic/claude-sonnet-5 tier=medium deleg=none
