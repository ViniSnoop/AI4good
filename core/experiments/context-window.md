# Context window composition
> What fills a session's context window, split by source, and how much of it the workspace controls.

Asked because a session cannot see its own window, so every claim about what fills it was an
estimate — including the ones steering always-loaded context. The suspicion under
it was specific: that the auto-memory store duplicates what `USER.md`, `goals/` and the CONTEXT chain
already carry, and is therefore worth folding.

## Method

```bash
core/tools/wos/session/context                   # this project
core/tools/wos/session/context --project <slug>  # any other
```

Reads `~/.claude/projects/<slug>/*.jsonl` and `<slug>/<session>/subagents/*.jsonl`. Turn-1 context is
exact (the `usage` fields). Per-source attribution is by character count, converted at a ratio
measured **per turn** rather than an assumed constant. Sources the transcript does not label
(`CLAUDE.md`, `AGENTS.md`, `MEMORY.md`) are measured on disk; what remains after both is the
**residual** — harness system prompt plus tool schemas — reported as its own line.

## Results

| Date | turn-1 | residual | skills | memory | CLAUDE | agents | SessionStart | chars/tok | Note |
|---|---|---|---|---|---|---|---|---|---|
| 2026-08-15 | 27,585 | 15,388 (56%) | 4,454 | 1,874 | 1,337 | 1,314 | 2,261 | 2.43 | **Wrong — see below.** First release. |
| 2026-08-15 | 27,585 | 21,162 (77%) | 2,530 | 1,198 | 855 | 754 | 654 | 2.23 | Corrected: sizes the text, not the JSON envelope. |
| 2026-08-15 | 27,585 | 21,419 (78%) | 2,530 | 1,196 | **599** | 754 | 654 | 2.23 | After the cuts. See the two caveats below. |

**Row 1 was inflated 1.6–3.5x, and it is kept because deleting it would hide the failure mode.**
`session_log.py` sized each injected block with `len(json.dumps(att))` — counting JSON escaping — and
`hook_success` blocks store their payload **twice**, in `content` and in `stdout`. The `SessionStart`
hook was worst hit at 3.5x. Guarded now by `test_a_hook_payload_stored_twice_is_counted_once`.

**Growth after turn 1** (corrected run): assistant output 38%, user prompts 12%, `Read` 8.6%,
`Bash` 7.6%, **CONTEXT.md reads 4.6%**. The chain is 851 reads over 98 sessions, 6 median.

**Subagents, measured for the first time**: 47 workers, 1,457 turns, turn-1 **17,738 tok** median
(p25 10,856 · p75 24,133), peak 71,326 median / 315,142 worst, $79 total. They live in
`<session>/subagents/*.jsonl` and were invisible to every earlier report.

**Two caveats on row 3, and the second is a property of the instrument itself.** The `CLAUDE.md`
chain fell 855 → 599 tok because `~/.claude/RTK.md` moved into `SETUP.md`; that source is measured on
disk, so it moves immediately. **The skill listing still reads 2,530 even though six descriptions
were shortened by 525 chars the same day** — everything the transcript labels is a *median over 98
past sessions*, so a change made today only appears as future sessions accumulate. Read the labelled
rows as "what sessions have been paying", never as "what the next session will pay". The residual
rising to 21,419 is the same artefact, not a regression: it is the arithmetic remainder.

## What changed

- **The memory-store question is answered: do not fold it.** At ~1,198 tok it is not where the cost
  is. The always-loaded-context item is updated.
- **The cuts were made and are worth ~394 tok** (~256 from `RTK.md` leaving the always-loaded chain,
  ~138 from six skill descriptions), against a scoped ceiling of ~1,600. The rest of the ceiling is
  caveman, which Lucas kept — see [`caveman-cost.md`](caveman-cost.md).
- **The cascade fear is retired.** The CONTEXT.md chain is 4.6% of growth.
- **Cuts were scoped and found small.** Ceiling ~1,600 tok (5.8%). A session in an empty directory
  with no workspace skills still costs 32k, so the workspace adds 4–9k. Only 36% of the skill listing
  is workspace-owned — three harness plugins outweigh every workspace skill combined.
- **`UserPromptSubmit = 16% of growth` was withdrawn as an artifact**, not acted on.

## Limitations

- **Shares are of *logged* material.** At 2.23 chars/token against a prose rate of 3.8, ~41% of
  growth is material the transcript never records. It is spread across the reported rows in
  proportion, so any single row is an upper bound.
- **A source riding along with that unlogged material claims tokens it never brought.** The
  `UserPromptSubmit` hook read 10.8% of all growth while being **121 characters**. Such rows are
  flagged `†`; a flagged row is never a finding.
- **The residual is opaque.** 77% of turn 1 is harness system prompt and tool schemas and nothing
  here can decompose it. `.claude/commands/` duplicates all 13 skills a second time (52 KB) and lands
  *inside* that residual — unmeasured, and the first thing to look at if it ever matters.
- **Observational only.** No arm, no control; nothing here shows a change *caused* anything. See
  [`subagent-context-chain.md`](subagent-context-chain.md) for the one real ablation.
- **One project slug per run.** The tool prints what it skipped.
