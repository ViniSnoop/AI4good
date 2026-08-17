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
requiring the step safe. That check is unbuilt, and it is band 1 of
[`core/SPECS.md`](../../SPECS.md) § AD-16: a rule written with nothing verifying it.

**Evidence limit, stated rather than papered over:** both practitioner method docs behind this are
**unread** — `WebFetch` refuses claude.ai artifacts and `core/tools/web/fetch` gets only the
disclaimer ([`core/refs/REFS.md`](../../refs/REFS.md)). The ruling rests on the captions plus our own
flow. Lucas pasting those docs is the only path that adds evidence.
