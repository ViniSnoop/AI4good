# Output cost
> Output tokens are more expensive than input — by how much, and where are ours?

Opened by two captures on 2026-08-15: *"de forma geral output tokens são bem mais caros que input
tokens. estudar formas de reduzirmos"* and the Claude Code usage report. Lucas set the method:
research, brainstorm, then repeat refining — *"isso é crítico e deve ser feito com excelência. Não
vamos ser ingênuos."* The plan built on it is [`ROADMAP-output-cost.md`](../../ROADMAP-output-cost.md);
this file is the measurement it must not contradict.

**It took three passes and each one cut the previous headline.** That is the finding, as much as any
number below.

## Method

Two commands. The first is the authority for every row in the first table:

```bash
core/tools/wos/session/usage                       # spend split, self-authored share, multiplier
```

Composition of logged output, which `usage` does not print:

```bash
cd ~/.claude/projects/-mnt-workspace && python3 - <<'EOF'
import json, glob, collections
tool = collections.Counter(); prose = 0
for f in glob.glob('*.jsonl'):
    for ln in open(f, errors='replace').read().splitlines():
        try: d = json.loads(ln)
        except: continue
        if d.get('type') != 'assistant' or d.get('isSidechain'): continue
        for b in ((d.get('message') or {}).get('content') or []):
            if not isinstance(b, dict): continue
            if b.get('type') == 'text': prose += len(b.get('text') or '')
            elif b.get('type') == 'tool_use':
                tool[b.get('name', '?')] += len(json.dumps(b.get('input') or {}))
total = prose + sum(tool.values())
print(f'prose {prose/total:.1%}'); [print(f'{k} {v/total:.1%}') for k, v in tool.most_common(5)]
EOF
```

Composition is counted in characters, not tokens, and per content block — so it is unaffected by
the record-duplication bug below, which is a `usage` fault only.

## Results

| Date | turns | spend | output at sticker | self-authored share | bill traceable to it | multiplier | Verdict |
|---|---|---|---|---|---|---|---|
| 2026-08-15 | 21,672 | $3,672 | 14.9% | 75.7% | 86.9% | 5.8x | **Withdrawn.** Every column inflated — see correction 3. |
| 2026-08-16 | 11,381 | $1,765 | 12.9% | 11.5% | 24.8% | **1.9x** | Output is real and secondary. Cache read is 59.1% of the bill. |

Where the billed output token goes (2026-08-16): **35.0% logged** — text and tool-call arguments,
which land in the thread and are re-read every turn — and **65.0% unlogged**, which is thinking plus
anything else the transcript drops, and is paid exactly once.

Composition of the logged 35% (2026-08-16, 11.59M chars):

| Slice | Share of logged output |
|---|---|
| `Bash` arguments | 26.2% |
| `Write` arguments | 25.3% |
| `Edit` arguments | 23.9% |
| prose to the user | 13.7% |
| everything else (`ExitPlanMode`, `AskUserQuestion`, `TodoWrite`, `Read`, `Agent`) | 10.9% |

**"SHUT UP AND WORK" attacks the 13.7%.** Against billed output that is 13.7% × 35% ≈ **4.8%**, and
against the whole bill under 1%. That also bounds [`caveman-cost.md`](caveman-cost.md): caveman
compresses prose, so that is its ceiling.

## Three corrections, in the order they were forced

**1. Bash heredocs: 55% → 3.7%** (2026-08-15). First pass: 55% of Bash output is heredoc payload,
with `core/tools/telegram_daemon.py` written whole eight times. Second pass split them by what they
*do*: writes a file (`cat >`/`tee >`) 128 calls / 354,100 chars / 26% of heredoc volume; stdin to an
interpreter (analysis, writes nothing) 430 calls / 599,203 / 44%. Shell-written files are 3.7% of
logged output, not ~15%. What survived is **governance, not cost**: those 128 writes met no gate at
all — `pre-edit.py` and `bugs-gate.py` are `PreToolUse: Edit|Write`, and the only Bash gate was a
*read* gate.

**2. RTK: four wrong stories before the test that held** (2026-08-15). Retracted in order: *"we
deleted RTK.md and lost the instruction"*; *"the hook only tracks"*; *"the hook does not rewrite at
all"* — measured as `rtk gain` delta 0; and *"PreToolUse cannot mutate tool input"*, the hypothesis
that delta implied. What is true: `PreToolUse` **does** apply `updatedInput` without requiring
`permissionDecision: "allow"`, and **rtk parses the first line of a payload and nothing else**. The
delta-0 test was submitted as one multi-line Bash call, so its probe commands sat on lines 2 and 3
and never reached rtk. **A negative result is a claim about the probe before it is a claim about the
system** — vary the probe's shape before believing it. Details:
[`core/hooks/compact/SPECS.md`](../hooks/compact/SPECS.md).

**3. The instrument built to end the guessing was itself wrong** (2026-08-16), in two independent
ways that pushed the same direction:

- **A transcript record is not a turn.** Claude Code writes one record per content block and repeats
  the whole `usage` object on each — 22,354 records against 11,370 responses, **1.97x**, with
  `output_tokens` identical across every record of an id. `session_log.walk()` deduped on `requestId`
  from the start and had a test for it; `usage` ran its own loop and did not.
- **Thinking was counted as thread content.** It is billed inside `output_tokens`, but its text is
  never persisted (`{'type': 'thinking', 'thinking': '', 'signature': …}`) and it never re-enters a
  later turn's context. `self_authored()` added raw `output_tokens` to the cumulative thread, which
  drove the ratio to its 1.0 cap within a few turns and reported 75.7%.

The lesson is correction 2's, one turn further out and more uncomfortable: **the probe we built to
replace a bad probe was never itself probed.** The instrument printed a startling number, the number
was quoted into a roadmap, a hand-off and a limits file, and nothing checked it against a second
method. Correction 1 came from re-reading raw data; correction 2 from varying a probe; correction 3
only from re-deriving the tool's own output by hand. Do that once before quoting a new instrument.

## What changed

- `usage` merges records by `requestId` and accumulates only *logged* output into the thread;
  "what counts as one API response" moved to `session_turns.py` with eight tests
  ([`core/tools/test/wos/test_usage.py`](../tools/test/wos/test_usage.py)).
- The output line now prints its logged/unlogged split, so the half that is paid once is visible.
- `ROADMAP.md` Frente 9, `ROADMAP-output-cost.md` and `core/hooks/limits.env` had the withdrawn
  numbers deleted, not softened.
- The re-emit gate was **demoted from a cost item to a governance item**: at 1.9x it is worth ~1% of
  spend, and the ungated-write hole is the whole of its remaining case.

## Limitations

- **The unlogged 65% is a residual, not a measurement.** Thinking text is never in the transcript,
  so it is inferred by subtraction and carries every other unlogged thing with it. Never report it
  as "thinking" alone.
- **Logged tokens are estimated from characters** at a declared 3.6 chars/token
  (`session_turns.CHARS_PER_TOKEN`). It is declared rather than derived because the obvious
  calibration — responses with no thinking block — measures 1.6 chars/token and so is not clean
  either. Tool-call JSON is denser than 3.6, which makes the logged share a **floor**.
- **The self-authored share caps at 1.0 per turn and ignores compaction**, so it remains an upper
  estimate even after the fix.
- **Absolute spend is list price**, and does not reflect a subscription. Ratios are the trustworthy
  part; the ROADMAP § Frente 9 caveat about the absolute total still stands.
- **Subagent turns are excluded** — they are billed in their own transcripts under
  `<session>/subagents/`, which this measurement does not open.
