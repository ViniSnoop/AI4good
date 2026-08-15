# experiments
> What we measured about this workspace, when, and what changed because of it. One file per question.

**Why this exists.** *"No feature in this workspace has ever been measured"*
([/ROADMAP.md](../../ROADMAP.md) Frente 10.4). Every instrument we own —
[`session/context`](../tools/wos/session/context), [`session/usage`](../tools/wos/session/usage),
[`entropy.md`](../../entropy.md) — prints the present and forgets. Git holds the past but does not
make it *readable*, so nobody can answer "did that change help?" without archaeology. This directory
is the readable half.

**How it differs from `core/SCAFFOLD-LOG.md`**, which [/ROADMAP.md](../../ROADMAP.md) § Rejected
killed as *"git plus this file already carry trigger→change"* — and it must differ, or it is a
resurrection. That log narrated **changes**. This records **measurements over time**, each with the
command that reproduces it. A narrated change is redundant with git; a time series is not.

## The one rule that makes a stored number safe

[`session/CONTEXT.md`](../tools/wos/session/CONTEXT.md) says these reports are **re-run, never
quoted from memory** — and a ledger of stored numbers is in direct tension with that unless every
row carries **the command that produced it**. That is why `Method` is a runnable line and not prose.
A row whose command no longer runs is a dead row: delete it, do not annotate it.

## The format

| Section | Holds |
|---|---|
| `> question` | line 2, the one question this experiment answers |
| `## Method` | the **runnable command**, plus what counts as the measurement |
| `## Results` | a dated table, **append-only** — one row per run |
| `## What changed` | what we did because of it, or `nothing yet` |
| `## Limitations` | what this cannot tell you. Never omit it. |

**The append-only table is the deliberate exception to *done work is deleted*.** Everywhere else a
finished row is cut; here the **trend is the artifact**, and Frente 9 already proved what a single
current-state number does — it steered the ledger for weeks while being wrong in every claim.

## Honest reporting rules

Inherited verbatim from the ablation-bench pilot, which earned them:

- **Never infer a metric from absence.** If the instrument did not report it, the cell is `—` and
  the reason goes in `## Limitations`.
- **Freeze definitions before the run.** A metric redefined mid-run measures nothing.
- **A negative result is a result.** The pilot's hypothesis was not supported and that row stays.
- **Record what the arm actually was**, not what it was meant to be.

## Writing a new one

Name it for the question, lowercase, no date in the filename — the dates live in the table. Add the
row to an existing file rather than creating a second file on the same question; a fork is how a
ledger stops being comparable over time.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`caveman-cost.md`](caveman-cost.md) | Caveman activation cost |
| [`context-window.md`](context-window.md) | Context window composition |
| [`subagent-context-chain.md`](subagent-context-chain.md) | The CONTEXT.md chain and who pays for it |
<!-- routing:end -->
