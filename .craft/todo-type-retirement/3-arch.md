# todo-type-retirement — architecture

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

## Amendment (orchestrator, tier=max) — Loops 3 and 3.5 are collapsed, not skipped

**Ruling.** This chain runs no architecture loop and no contract-layout loop. Both are recorded
here as executed-and-empty, with the reason, so the chain stays auditable.

**Why.** Loop 3 evaluates a *design*, and Loop 3.5 lays out *module/step I/O contracts before
code*. This chain deletes a document type. There is no module, no I/O boundary, no runtime call,
no data structure — the only executable artefact touched is one key of one Python dict, and the
plan already fixed its exact line. Every remaining decision in the task is a **routing judgment
about one line of Portuguese prose**, and Loop 1 made all 73 of them at high tier, individually,
in `1-plan.md` § Fold Map. A Loop 3 spawned on top of that has nothing to evaluate that Loop 1 did
not already decide; it would either restate the Fold Map or invent architecture for a document
move, and the second failure mode is the expensive one.

**Authority.** `craft.md` § Cost Gate — *"The flow must never cost more than the task"* — plus the
Loop 0 permission panel, which set `arch-review: none` (Loop 3.5's own recurrent concept-symmetry
review is therefore already off by the user-facing default). What Loop 3 normally *hands* Loop 4a
is a set of seams; the equivalent handoff here is the § Fold Map plus C1..C8, and 4a reads
`1-plan.md` directly.

**What this is NOT.** It is not the padaria shortcut. The bakery gate genuinely fails: ~25 files,
a data migration, and a delete that is not fully undone by reverting one hunk. The chain stays
`standard` and keeps Loops 4a, 4b, 5 and 6.

**FLOW FINDING (for the trial report).** The craft tree has exactly two speeds — `padaria`
(≤2 files, no migration) and the full contract-first `feature` subtree. A **content migration**
falls between them: it is far too large for the bakery gate and has nothing for an architecture or
contract loop to hold. `route.md`'s guardrail against adding subtrees casually is right, but the
gap is real, and it is a *very* common workspace task shape (retire a type, split a file over the
cap, fold one ledger into another). Today it costs an orchestrator amendment every time.
Cheapest honest fix: not a fifth subtree, but a documented **skip rule** in `craft-build.md` —
"Loops 3 and 3.5 are collapsed when the diff contains no executable artefact beyond configuration;
record the ruling in `3-arch.md`" — which turns an improvisation into flow.

## Handoff to Loop 4a
seams: none — no code boundary exists. Acceptance is file-state, and it is fully expressed by
C1..C8 in `1-plan.md`. Loop 4a writes an executable acceptance script, not unit tests: nothing
here is a unit, and a permanent test asserting `brain/TODO.md` is absent would be a test of a past
event, which the workspace deletes rather than keeps.

executor: orchestrator model=anthropic/claude-opus-5 tier=max deleg=none
