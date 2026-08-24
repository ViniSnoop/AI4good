# todo-type-retirement — ground

## Carry
slug: todo-type-retirement | branch: feature/roundup-md-cap | root: /mnt/workspace
provider: anthropic | chain-deleg: none
tier-map: anthropic | verified-on: 2026-08-20
test-cmd: `make verify-fast` | e2e-cmd: none (`make entropy` writes the fenced ISSUES.md — DO NOT RUN)
criticality: normal | verdict: standard
subtree: feature | supervision: io-signoff=no arch-review=none arch-review-supervised=no
criteria:
  C1 — every live line of `brain/TODO.md` landed per § Fold Map; nothing lost, nothing invented.
  C2 — `brain/TODO.md` no longer exists on disk (`git rm`).
  C3 — TODO row gone from `core/SCHEMA.md` type table and from `core/SCHEMA-placement.md` COLD row.
  C4 — `TODO.md` row gone from `brain/CONTEXT.md` routing table (by regeneration, not hand-edit).
  C5 — `'life-todo'` gone from `LEDGERS` in `core/hooks/entropy/dashboard/entropy-dashboard.py`
       and from the mirror `LEDGERS` in `core/tools/test/law/entropy/test_entropy_ledger.py`.
       `entropy_ledger.py` `LEDGER_FILES` is FENCED → reported follow-up, not an edit.
  C6 — "four ledgers" phrasing in `ROADMAP-ledger.md` line 10 reads three.
  C7 — no tracked file points a reader at `brain/TODO.md` as a live destination.
  C8 — `make verify-fast` is green.
tasks:
  T1 — new goal seed `google-migration` + `branches/google-migration/` cockpit — brain/goals/, branches/ — high
  T2 — fold `today` + `week` + `month` rows into their destinations — brain/goals/*.md, brain/INBOX.md — medium
  T3 — fold `backlog` rows into their destinations — brain/goals/*.md, brain/INBOX.md — medium
  T4 — move the 31-row drive queue verbatim into the cockpit ROADMAP — branches/google-migration/ROADMAP.md — medium
  T5 — delete the file and its .gitignore allowlist line — brain/TODO.md, .gitignore — low
  T6 — kill the type at every declaration site — core/SCHEMA.md, core/SCHEMA-placement.md, 2 py files, ROADMAP-ledger.md — medium
  T7 — fix live back-pointers at the SOURCE, then regenerate the mirrors — core/skills/*.md, refs, branches, goals — medium
  T8 — regenerate the generated routing blocks — brain/CONTEXT.md, brain/goals/CONTEXT.md, branches/CONTEXT.md — low
  T9 — run `make verify-fast`, green — — low
context: /mnt/workspace/AGENTS.md · /mnt/workspace/brain/CONTEXT.md · /mnt/workspace/brain/SPECS.md
         · /mnt/workspace/brain/goals/CONTEXT.md · /mnt/workspace/core/CONTEXT.md

## Ground
branch-created: feature/roundup-md-cap base: 5cbb7b14174946e5229acea5edb3b1248a143bd1 (merge-base with develop; branch pinned by orchestrator, verify-only, no checkout)
paths: 60/60 ok | missing: none
  ✓ All 60 existing files across T1–T9 verified present.
  ✓ Parent directories for new files exist: brain/goals/, branches/.
  ✓ New files: brain/goals/google-migration.md, branches/google-migration/CONTEXT.md, branches/google-migration/ROADMAP.md (directories will be created by T1; parent dirs exist).
test-cmd-runs: yes (exit 0)
  `make verify-fast` ran successfully: 500 passed in 17.75s.

## Verification of Orchestrator Addenda
(a) `core/tools/wos/sync-skills` exists and is executable: ✓ /mnt/workspace/core/tools/wos/sync-skills
(b) `core/hooks/routing/context_synchronizer.py` exists: ✓ (5.6K, executable mode 777)
(c) `git grep -c 'TODO\.md'` baseline: 48 total hit lines across 25 files; recorded for post-migration verification.

executor: craft-low model=anthropic/claude-haiku-4.5 tier=low deleg=none
