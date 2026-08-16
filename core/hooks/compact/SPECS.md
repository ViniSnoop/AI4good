# compact — Specs
> What the rtk shim may rewrite, what it must leave alone, and the two harness facts it rests on.

Companion to [`CONTEXT.md`](CONTEXT.md), which says what this directory is and routes into it.

## Why a shim sits in front of `rtk hook claude`

rtk parses the **first line** of a Bash payload and nothing else, and when that line is not
rewritable it declines the whole call. Measured over 5,628 Bash calls in this workspace's
transcripts (2026-08-15):

| Shape | Before the shim |
|---|---|
| `git status` | rewritten |
| `cd x; git status` (one line) | both rewritten |
| `cd x` ⏎ `git status` | **nothing** rewritten |
| `git status` ⏎ `ls -la` | line 1 only |

**23.4% of calls open with `cd`**, spending rtk's single shot on it, and **1,249 rewritable commands
sit on lines 2+** — 783 of them `git`. Single-line `;` and `&&` chains were never affected.

## The safety contract

**The shim must never reshape shell it cannot read.** It splits a payload only when every line
stands alone as a simple command; a heredoc, a block keyword, a line continuation or an odd quote
count sends the untouched payload to `rtk hook claude` and passes its verdict through unchanged.

**The bail is always the safe direction.** Failing to compact costs tokens; corrupting a command
costs correctness. The live example the tests hold: a commit message quoted across two lines, whose
second line begins with a word that is also a command name — split naively, prose becomes an
executable. Risk cases in `core/tools/test/workspace/gates/test_bash_compact_rewrite.py` deliberately
outnumber success cases.

**A missing binary must fail open.** Compaction is an optimisation, so no rtk means the command runs
exactly as written, never blocked and never altered.

## Two undocumented harness facts this rests on

Both verified by experiment on Claude Code 2.1.218, neither stated in the hooks documentation:

1. `PreToolUse` **does** apply `hookSpecificOutput.updatedInput`.
2. It does so **without** requiring `permissionDecision: "allow"` — checked with two probe hooks
   differing in exactly that field; both rewrote. This matters beyond convenience: setting `allow`
   to buy a rewrite would auto-approve every command the shim touches, so not needing it keeps
   compaction out of the permission system entirely.

Upstream reports the opposite of both at various versions (`claude-agent-sdk-python#381`, open;
`claude-code#15897`, closed then observed fixed in 2.1.168), so this is version-dependent.
**Re-test after a harness upgrade, and never by re-reading configuration** — run a command through a
live session and watch `rtk gain`'s counter move. The configuration looked correct for weeks while
every multi-line call went uncompacted, and the delta test that first caught it was itself misread,
because the test payload was written in the same multi-line style that was the bug.
