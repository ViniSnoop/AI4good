# Agent discipline
> What an always-loaded rule must prove, when doubt costs, when to delegate.
> governs: AGENTS.md, core/norms/, core/agents/, core/flows/craft/

### AD-15 — What an always-loaded rule must prove to keep its place (2026-08-17)

Applies to text loaded in **every session**: `AGENTS.md`, `CONTEXT.md` heads, always-listed skills.
The question is **not length**. It is: *could this be a tool parameter, an enum, or a hook's error
message instead of prose?* What survives that question is prose that pays for itself. Three columns
per rule:

| column | when | what happens |
|---|---|---|
| **delete** | a **blocking, ratcheted** gate already applies it | leaves the prose; the hook is the rule |
| **move** | a check *could* apply it, but none does today | **stays in the prose** until a gate blocks |
| **keep** | judgment no check can hold | stays, and its reason stays with it |

**The discriminator between `delete` and `move` is blocking, not the existence of a detector** — it
is what separated two neighbouring `AGENTS.md` lines in this pass. `UPPERCASE.md = a type` left
because `checks/type-gate.py` stops the commit. `DONE WORK IS DELETED` stayed:
`entropy/entropy_ledger.py` owns the finished-work detector, but `type-gate.py` imports only its
wiki-link half, so the rule is **reported and never blocked** — deleting prose on the strength of a
report trades enforcement for nothing. An existing, unwired detector is the `move` column.

**Counterweights, because indiscriminate pruning is the one way this audit makes things worse** (the
`prompt-audit` keep-list): context is never cruft; cruft ≠ length; **no deletion is justified by
character count alone**. An audit that finds nothing changes nothing.

**Scope note:** this governs **always-loaded** text. Prose in a `SPECS.md`, read on demand, does not
pay that toll and is not under this rule.

**And this is not a cost item.** `AGENTS.md` is a single-digit fraction of turn 1
([`core/experiments/context-window.md`](experiments/context-window.md) — re-run it, never quote from
here): halving it saves nothing measurable, and selling that as savings repeats the error the cost
front spent three weeks undoing. The gain is enforcement, not tokens.

The frame came from a practitioner post (`[C]`, `core/refs/REFS.md`) claiming a **>80%** cut to
Claude Code's system prompt. **That number is self-reported with no published benchmark — not
citable.** What is testable, and is the whole value, is the frame: our own hooks already prove its
mechanical half — a hook's error message is a zero-token instruction arriving exactly when it applies.

### AD-16 — Doubt is not charged when asserting; it is charged when storing (2026-08-17)

The ask was a way to stop the agent being confidently wrong. **Asking for doubt in prose is the cheap
half and has already been tried**: this workspace is thick with *re-run it, never quote it*, and that
prevented neither the wrong number that steered a front for three weeks nor four asserted-then-
retracted explanations of the rtk hook. So the question is not how to request caution, it is **where
caution becomes a gate**. Three bands, and the first contradicts the premise this item was filed
under:

**1. Rule written, nothing checking — the cheap win, and it included our own.** The
`core/experiments/` discipline (runnable `Method`, dated `Results`, `Limitations` never omitted) and
`core/refs/REFS.md`'s tier markers (`[A]`/`[B]`/`[P]`/`[V]`/`[C]`) are the two rules this workspace
cites as proof it knows how to doubt, and for months nothing verified either: they held because a few
careful sessions followed them, not because anything charged for them — INDUCED wearing ENFORCED's
costume. `core/hooks/entropy/entropy_stores.py` charges for them now, in the commit gate and on the
dashboard. Both stores are small, closed and clean, so the check went in **total rather than
ratcheted**: the ratchet exists for an inherited backlog, and there was none to inherit.

**2. Enforced by construction — the mechanism that already works, never named as one.** Write the
claim **where a parser already reads**, and it is audited on every commit for free. That is what
law-in-data does (`core/SCHEMA.md` is parsed, never restated in a checker), which makes *"a checker
that restates the law is the drift checkers exist to catch"* a doubt rule at heart. Proved in the act
of writing AD-15: one sentence of mine in § The one exception added two false types to the allowlist,
and `test_law_comes_from_schema` failed the commit — the test weighed no confidence, it read the
artifact.

**3. Not chargeable — stop trying.** The truth of a fresh technical claim, spoken in a turn. No gate
holds that. What the workspace does instead is **make the error cheap and its discovery fast**, which
is what the tests did above.

**Corollary this session paid for, sibling to *build the instrument, then check the instrument*: a
claim about our own enforcement layer is checked at the call site, never at the module.**
`entropy_ledger.py` owns the finished-work detector, but `type-gate.py` imports only `wiki_link_hits`
— anyone stopping at *"the module has the check"* would have deleted an `AGENTS.md` rule that nothing
in practice enforces. Owning a detector and charging for it are separate facts.

### AD-17 — Delegation is already mandatory where an executor reads the assignment; elsewhere it is advice (2026-08-17)

The ask: *"gostaria que ele delegasse mais ao sonnet pra economizar… seria ótimo se tivesse uma forma
mais garantida"*, with the **plan** as the proposed trigger — the moment work is cut into tasks is
the cheap point to decide who executes each one.

**That trigger is already built, in two places.** The Loop 1 plan table in
`core/flows/craft/craft.md` carries `tier` and `effort` columns **per task row**, and the same loop's
adversarial review charges that each row be executable by its assigned tier. `ROADMAP.md` carries a
`model` line per item. Making *the plan carry the assignment* is not what is missing.

**What is missing is an executor that reads it.** Inside `/craft` there is one: `runtimes.md` spawns
per tier, and the measurement shows the effect — of 37 spawns in
[`experiments/delegation.md`](experiments/delegation.md), **9 are the `craft-*` mirrors**, the only
structural ones; the rest are ad-hoc builtins. Outside `/craft` nothing reads the tag, so it is
advice — the same defect class as the first-line comment, where the rule existed and the number grew
anyway. **Hence the reading of the opus-heavy split: it measures how much work bypasses the flow that
routes**, not per-task indiscipline. The lever is routing more work through `/craft`, not building a
second router beside it.

**Delegating ≠ parallelising, and conflating them is what makes the proposal feel risky.** Offered a
shape with parallel workers, Lucas chose **no parallelism** (2026-08-17) — and refusing concurrent
workers in one checkout is not refusing a cheaper model per task. The common case, and the one that
moves the split, is **sequential** delegation.

**The chargeable half, and it is cheap:** `core/tools/wos/roundup` already prints the per-session
split at every close. Have the plan **declare its expected split** and roundup compare declared
against actual. It forces nobody to delegate; it makes deviation **visible and dated** instead of
invisible — which is what turned the other fronts. That is band 1 → 2 of AD-16, and the feedback loop
needs no new instrument.
