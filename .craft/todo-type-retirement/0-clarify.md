# todo-type-retirement — clarify

## Carry
slug: todo-type-retirement | branch: feature/todo-type-retirement | root: /mnt/workspace
provider: anthropic | chain-deleg: none
tier-map: anthropic | verified-on: 2026-08-20
test-cmd: `make verify-fast` | e2e-cmd: `make entropy` (writes ISSUES.md — DO NOT RUN, concurrent session owns that file)
criticality: normal | verdict: standard
subtree: feature | supervision: io-signoff=no arch-review=none arch-review-supervised=no
criteria:
  C1 — every live line of `brain/TODO.md` has landed as a `[short-id] description` backlog item in a goal file (existing or new seed) or as an INBOX capture; nothing is lost, nothing is invented.
  C2 — `brain/TODO.md` no longer exists on disk (git rm).
  C3 — the TODO row is gone from `core/SCHEMA.md`'s type table and from `core/SCHEMA-placement.md`'s COLD row.
  C4 — the `TODO.md` row is gone from `brain/CONTEXT.md`'s routing table.
  C5 — `'life-todo'` is gone from `LEDGERS` in `core/hooks/entropy/dashboard/entropy-dashboard.py`, and `'TODO.md'` from `LEDGER_FILES` in `core/hooks/entropy/entropy_ledger.py` **only if that file is not owned by the concurrent session** (it is — see fence; raise it as a follow-up instead).
  C6 — the "four ledgers" phrasing in `ROADMAP-ledger.md` reads three.
  C7 — no tracked file still points a reader at `brain/TODO.md` as a live destination (`git grep 'TODO\.md'` returns only ROADMAP rows the orchestrator owns).
  C8 — `make verify-fast` is green.

## Clarify
intent: Retire `TODO.md` as a workspace `.md` type — fold its live content into the goals it serves, delete the file, and remove every declaration that would regenerate it.
motivation: Lucas reported twice, unprompted, that `TODO.md` is not being used — he writes tasks into `INBOX.md` instead. Ruled 2026-08-14 (ROADMAP-ledger.md the ledger-discipline front item 1). A type nobody writes to is mass, and mass in a re-read file is paid three times per session.
refs: ROADMAP-ledger.md § the ledger-discipline front item 1 · brain/SPECS.md § Backlog Ordering Policy · core/SCHEMA.md § type table · core/experiments/read-amplification.md
scope-files: brain/TODO.md (delete) · brain/goals/*.md (fold targets) · brain/INBOX.md (capture targets) · core/SCHEMA.md · core/SCHEMA-placement.md · brain/CONTEXT.md · ROADMAP-ledger.md (header phrasing only) · core/hooks/entropy/dashboard/entropy-dashboard.py (one dict entry) · core/skills/inbox.md + .claude/commands/inbox.md + .claude/commands/roundup.md (routing tables) · academy/refs/REFS.md · core/refs/REFS-*.md · branches/ecovila/*/CONTEXT.md · brain/goals/{ecovila,teaching-materials}.md (back-pointers) · .gitignore
expected-result: `brain/TODO.md` is gone; `git grep 'TODO\.md'` returns only historical ROADMAP/archive/memory prose; every task that was live is findable in a goal backlog or the INBOX; verify-fast green.
ambition: solid
criticality: normal tolerance: a mis-routed task is recoverable (it is one line in a goal file); a *lost* task is not — the fold must be lossless.
innovation: none — this is a migration, the judgment is per-line routing, not design.
verdict: standard
keep-trail: no

## Permission Panel (supervision profile)
io-signoff: no                # non-interactive session; defaults are permissive by spec
arch-review: none             # no architecture is being decided — a type is being deleted
arch-review-supervised: no

## Fences (orchestrator, non-negotiable — copy into every downstream spawn prompt)
A concurrent session owns and is actively editing:
  - `ISSUES.md`
  - every `ROADMAP-*.md` EXCEPT `ROADMAP-ledger.md`
  - `core/hooks/entropy/*.py` (the check modules, incl. `entropy_ledger.py`)
This chain may touch, in that directory, EXACTLY ONE THING: the `'life-todo'` entry of the
`LEDGERS` dict in `core/hooks/entropy/dashboard/entropy-dashboard.py`. Nothing else.
This chain does NOT delete the ROADMAP row (`ROADMAP.md` line 163, `ROADMAP-ledger.md` the ledger-discipline front
item 1) — the orchestrating session does. Report the outcome instead.
`ROADMAP-ledger.md` edits are limited to the "four ledgers" → "three" phrasing.
Do not run `make entropy` (it rewrites ISSUES.md).
Do not merge. Stage explicitly. Check the branch before committing.

## Loop 0 note — the interview did not happen, and could not
Loop 0 is specced as "the only interactive loop". This chain runs as a non-interactive subagent:
there is no user to interview. The clarify fields above are filled from Lucas's recorded ruling
(ROADMAP-ledger.md the ledger-discipline front item 1, 2026-08-14), which is more specific than an interview would
have produced — it already names both halves, their order, and the two honest outcomes for an
orphan task. The permissive panel defaults are used unchanged. Recorded as a flow finding, not a
flow violation.

executor: orchestrator model=anthropic/claude-opus-5 tier=max deleg=none
