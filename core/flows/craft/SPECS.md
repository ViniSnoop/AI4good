# Craft Flows — Specs
> Why `craft.md` stays one file instead of splitting further.

`craft.md` was one ~52 KB file mixing the always-loaded protocol with tables and history each loop
paid for eight times. The 2026-07-23 split follows what is actually read when: always-needed stays
in one file; per-chain and never-needed content became the subfiles beside it (`routing.md`,
`runtimes.md`, `prior-art.md`, the trunk `route.md`, the map `tree.md`). This is deliberately not
blind fragmentation — the whole spine (Core Principle, Carry, Autorouting, Return Flags, Loops
0–6.5, Cost Gate, Field Practice) stays one file, because a loop executor needs all of it in a
single read.

## Adversarial review: require the bound, not the step (ruled 2026-08-17)

The ask was *"have adversarials as our standards, maybe enforced — e.g. a plan that doesn't have any
adversarial steps is rejected"*. Two findings move it, and the second inverts what gets built.

**The standard already exists here.** Loop 1 is an adversarial plan review with FATALs and tier
escalation, and Loop 3 runs a second adversarial pass at architecture. What the ask describes is the
flow's default, not a gap — for work that goes through `/craft`.

**The gate to build is the bound, not the adversarial step.** The source that proposed the technique
also names its failure — it *"can be a death loop"* — and a gate that demands an adversarial step, on
a plan whose adversary always finds something, is a loop with no exit. The termination rule was never
actually open: [`core/flows/CONTEXT.md`](../CONTEXT.md) § Rules that hold for every flow already
requires every loop to declare an exit condition **and** a numeric cap, and to deliver the best
artifact so far when the cap is hit. `research/sota.md` declares its cap; **Loop 1 did not** — it
said *"until the review passes"*, so the workspace's own adversarial review was the unbounded case
the practitioner warns about. Fixed here: exit at zero unresolved FATALs, cap 3 passes, surviving
FATALs carried as `verdict: FAIL`.

So the checkable shape is the inverse of the one proposed: **a step that declares a loop must declare
its cap** — greppable, deterministic, zero-token, and true of every flow rather than of one technique.
Requiring the adversarial step is what creates the death loop; requiring the bound is what makes
requiring the step safe. `validate_flow_loops` in
[`core/tools/wos/skills/validate.sh`](../../tools/wos/skills/validate.sh) enforces it over every
file under `core/flows`, and rejects the commit through `sync-skills --check`. Whole-file rather
than per-step: one cap governs the flow, and finding where a step ends in prose would be a guess.

**Evidence limit, stated rather than papered over:** both practitioner method docs behind this are
**unread** — `WebFetch` refuses claude.ai artifacts and `core/tools/web/fetch` gets only the
disclaimer ([`core/refs/REFS.md`](../../refs/REFS.md)). The ruling rests on the captions plus our own
flow. Lucas pasting those docs is the only path that adds evidence.

## Judged against `obra/Superpowers`: keep the flow, import the trigger (ruled 2026-08-17)

*"Será que eu deveria usar o superpowers?"* — read from the repository, not the capture. Its arc is
ours: brainstorm a spec → isolated branch → plan in bite-sized tasks written for *"an enthusiastic
junior engineer with poor taste, no judgement, no project context"* → subagent-per-task with
two-stage review → red/green TDD → code review → finish the branch. Loops 0–6 answer the same
questions in the same order, so **"is it good" is not the question and the arc is not the answer.**

**What it does that we do not, and only one item is load-bearing.** Its skills **trigger
automatically** — a session-start hook plus descriptions written to fire, so the methodology is
*"mandatory workflows, not suggestions"*, while `/craft` must be typed. It also uses a git worktree
per feature rather than a branch, splits into ~15 independently-triggering skills instead of one
spine, ships named `systematic-debugging` / `verification-before-completion` workflows we lack, and
packages itself for 14 harnesses.

**What we have that it does not, and why that decides it.** Per-task **tier and effort with
escalation rules** — cost-aware model routing, absent from its uniform subagent-per-task dispatch —
and the **file-relayed Carry**, where a fresh session reads exactly one file. Both exist because this
workspace's binding constraint is quota, not developer time. Adopting Superpowers wholesale would
trade the two mechanisms built for our actual constraint to gain an arc we already have. **So the
flow is not deleted, and that outcome was genuinely on the table.**

**The importable part is the trigger, and it is the missing half of
[`core/SPECS-discipline.md`](../../SPECS-discipline.md) § AD-17.** That AD found the assignment already carried at plan
time with no executor reading it outside `/craft`, and
[`core/experiments/delegation.md`](../../experiments/delegation.md) prices it: 9 of 37 spawns are the
`craft-*` mirrors, the only structural ones. Superpowers' answer to exactly that gap is to make
invocation automatic rather than typed. Importing the mechanism does not require importing the
methodology.
