# experiments — Specs
> The format every file in this directory follows, and the discipline that keeps a stored number trustworthy.

## The one rule that makes a stored number safe

[`session/CONTEXT.md`](../tools/wos/session/CONTEXT.md) says these reports are re-run, never
quoted from memory — a ledger of stored numbers is in direct tension with that unless every row
carries the command that produced it. That is why `Method` is a runnable line and not prose. A row
whose command no longer runs is a dead row: delete it, do not annotate it.

## The format

| Section | Holds |
|---|---|
| `> question` | line 2, the one question this experiment answers |
| `## Method` | the runnable command, plus what counts as the measurement |
| `## Results` | a dated table, append-only — one row per run |
| `## What changed` | what we did because of it, or `nothing yet` |
| `## Limitations` | what this cannot tell you. Never omit it |

The append-only table is the deliberate exception to *done work is deleted*: everywhere else a
finished row is cut; here the trend is the artifact, and the cost work already proved what a single
current-state number does — it steered the ledger for weeks while being wrong in every claim.

## Honest reporting rules

Inherited verbatim from the ablation-bench pilot, which earned them:

- Never infer a metric from absence. If the instrument did not report it, the cell is `—` and the
  reason goes in `## Limitations`.
- Freeze definitions before the run. A metric redefined mid-run measures nothing.
- A negative result is a result. The pilot's hypothesis was not supported and that row stays.
- Record what the arm actually was, not what it was meant to be.

## Writing a new one

Name it for the question, lowercase, no date in the filename — the dates live in the table. Add
the row to an existing file rather than creating a second file on the same question; a fork is how
a ledger stops being comparable over time.
