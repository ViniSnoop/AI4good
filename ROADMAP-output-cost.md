# Roadmap — what our own output costs

> Plan for INBOX entries 2, 3 and 6 (2026-08-15), referenced from [`ROADMAP.md`](ROADMAP.md) § Frente 9.
> Written by the planning session; the build is the next session's work.
> **Deletion policy is this repo's: completion is deletion.** Cut an item when its verification passes.

## Why

Three captures were one question:

- *"o AGENTS.md voltou a parecer meio grande… avaliar ele com bastante carinho"*
- *"output tokens são bem mais caros que input. estudar formas de reduzir"*
- the Claude Code usage report — 73% of spend above 150k context, 44% subagent-heavy, `/roundup` 14%

Lucas set the method: **research (papers + web), brainstorm, then repeat refining** — *"isso é crítico e
deve ser feito com excelência. Não vamos ser ingênuos."* Three rounds have now corrected this file,
the third one hardest: the instrument it was rewritten around was itself wrong by 2x. The corrections
are recorded in [`core/experiments/output-cost.md`](core/experiments/output-cost.md) and are the
reason to trust what survives.

## What was measured

**The measurement lives in [`core/experiments/output-cost.md`](core/experiments/output-cost.md)** —
its Method is runnable, its Results are dated, and it is the authority. What follows is only what
this plan needs to rank its own items.

**Output is 12.9% of spend at sticker price**, and **24.8% once every later turn's re-read is
counted** — a multiplier of **1.9x**, not the 5.8x this file carried until 2026-08-16. Cache read is
**59.1%** and owns the bill. Only **35% of billed output tokens are logged** — text and tool-call
arguments, the part that lands in the thread; the other 65% is thinking, which is paid once.

Entries 3 and 6 are still **one mechanism** — long sessions cost more because every turn re-reads the
whole thread — but the thread is filled far less by our own writing than this file claimed: a mean
turn is **11.5%** self-authored, not 75.7%.

**The popular fix targets the wrong slice.** Logged output is **86.3% tool_use arguments** (Bash
26.2%, Write 25.3%, Edit 23.9%) against **13.7% prose to the user**. "SHUT UP AND WORK" attacks that
13.7%, which is 4.8% of billed output and **under 1% of the bill**. That is also the ceiling on
[`core/experiments/caveman-cost.md`](core/experiments/caveman-cost.md), now recorded there.

## Evidence from outside

Peer-reviewed, and what each transfers:

- **SWE-agent — Agent-Computer Interfaces Enable Automated Software Engineering** (NeurIPS 2024,
  arXiv 2405.15793). LM agents are a new class of end user; the interface they act through measurably
  changes behavior and performance. The strongest published backing for this workspace's own bet —
  **a gate beats a paragraph** — and why item 4 is a hook, not a rule in `AGENTS.md`.
- **Token-Budget-Aware LLM Reasoning** (ACL 2025 Findings, arXiv 2412.18547). Reasoning output is
  *"unnecessarily lengthy"* and compresses under a prompted budget — **but a wrong budget degrades the
  answer**, and dynamic per-task budgets beat one fixed number. Direct argument against a blanket
  terseness rule.
- **Harness Engineering for Agentic AI Coding Tools** (AIware 2026, ACM/IEEE; arXiv 2602.14690).
  2,853 repos, eight configuration mechanisms: context files dominate and are often the *only*
  mechanism, `AGENTS.md` is becoming the cross-tool standard, and few repos adopt Skills or Subagents.
  The baseline entry 2 should be judged against — it says our bet on executable enforcement is the rare
  one, not the crowded one.
- **LLMLingua** (EMNLP 2023) / **LLMLingua-2** (ACL 2024 Findings). Input-prompt compression ~20x.
  Named to rule it out: it compresses a request before sending, and Claude Code owns our request.

Preprints, flagged: *Decoding the Configuration of AI Coding Agents* (arXiv 2511.09268);
*Chain of Draft* (arXiv 2502.18600).

First-party (Anthropic Opus 5 guidance, via the `claude-api` skill):

- **`effort` is not a length lever** — it moves thinking volume, not reliably visible output. A short
  conciseness instruction cut user-facing length ~20%. Kills the cheapest-sounding idea.
- **Files written to disk run long on Opus 5**; calibrate deliverable length explicitly.
- **Opus 5 over-delegates to subagents** (the reverse of 4.8); cap it explicitly.
- **Delete verification instructions** — Opus 5 verifies unprompted, so they cause over-verification.
  A delete, not a rewrite; it inverts the usual self-check advice.

## Two corrections the second round forced

**1. Bash heredocs: 55% → 3.7%.** Bash was the largest unexamined slice. First pass: 55% of Bash output
is heredoc payloads, with `core/tools/telegram_daemon.py` written whole **eight times** (3× `Write` at
28,697 chars, 5× `cat > … << 'DAEMON'`) — ~200k chars for one file. Second pass split them by what they
do: **writes a file** (`cat >`/`tee >`) 128 calls / 354,100 chars / 26%; **stdin to an interpreter**
(analysis, writes nothing) 430 calls / 599,203 / 44%; other 31%. So shell-written files are **3.7% of
all output**, not the ~15% the raw figure implied — most heredoc volume is legitimate throwaway analysis.

What survives is **governance, not cost**: those 128 writes met **no gate at all**. `pre-edit.py` and
`bugs-gate.py` are `PreToolUse: Edit|Write`; the only Bash hook is `bash-context-gate.py`, a *read* gate.
`brain/INBOX.md`, `HISTORY.md` and `core/tools/test/law/test_entropy_ledger.py` were all written past the
200-line size gate, the first-line-comment check and the CONTEXT.md description requirement. **Frente 4.6
predicted this** (*"files written by a generator, by a shell heredoc, by `git checkout`"*); this is the
first time it is measured.

**2. RTK: four wrong stories before the test that held.** Lucas asked whether RTK still runs on Bash and
said it deserved a test. Every explanation written before running one was wrong, including the last two,
which were written *by* a test.

Retracted in order: *"we deleted RTK.md and lost the instruction"* (commit `804ab0a` moved
provider-neutral prose into `SETUP.md`, correct by this repo's first rule); *"the hook only tracks"*;
**"the hook does not rewrite at all"** — measured as `rtk gain` delta = 0 over `git status` and
`ls -la core`; and **"Claude Code's `PreToolUse` cannot mutate tool input"**, the hypothesis that delta
implied. The last two are the interesting ones, because the delta was real and the reading of it was not.

**What is actually true** (Claude Code 2.1.218, each verified by experiment):

- `PreToolUse` **does** apply `hookSpecificOutput.updatedInput`, and **without** requiring
  `permissionDecision: "allow"` — checked with two probe hooks differing in exactly that field.
  Both rewrote. Upstream reports the opposite (`claude-agent-sdk-python#381`, open; `claude-code#15897`,
  closed then observed fixed in 2.1.168), so this is version-dependent and undocumented either way.
- **rtk parses the first line of a payload and nothing else.** `git status` rewrites; `cd x; git status`
  on one line rewrites both; `cd x` ⏎ `git status` rewrites **nothing at all** — a non-rewritable first
  line makes rtk decline the whole call.
- The delta-0 test therefore measured its own payload shape. It was submitted as one multi-line Bash
  call, so `git status` and `ls -la core` sat on lines 2 and 3 and never reached rtk.
- `rtk discover`'s *0.5% adoption* is partly an artifact: transcripts record the command the **model
  sent**, and a working hook rewrites after that. It cannot see its own successes.

**The mass, re-measured** over 5,628 Bash calls: **23.4% open with `cd`** — rtk's one shot spent on a
`cd`, everything after it dropped — and **1,249 rewritable commands are stranded on lines 2+**, 783 of
them `git`. So entry 6's lever survives the correction; only its cause changed, from *dead wiring* to
*a parser that stops at line 1 meeting an agent that writes multi-line shell*.

**The reusable lesson, also corrected.** The first draft said: a capability can be documented as
automatic while doing nothing for weeks, and only a counter says otherwise. Half right. The counter
*did* say otherwise — and was still misread, because the test payload was written in the same
multi-line style that was the bug. **A negative result is a claim about the probe before it is a claim
about the system.** Vary the probe's shape before believing what it reports.

## Levers, ranked

| Lever | Measured mass | Enforceable? | Verdict |
|---|---|---|---|
| **The unlogged 65% of output** — thinking, billed and invisible | **~8% of the whole bill**, the largest single output slice | `effort` / model routing | **measure first** — see § The lever nobody has looked at |
| Session length | every turn re-reads the thread; 4.2x from the cheapest context band to the dearest | `context-meter` live | already built, and still the biggest |
| Re-emitting a file already in context — `Write` over an open path + shell heredoc writes | ≈13% of *logged* output → **~1% of spend** | yes — one gate | **governance only**, step 4 |
| Length of files we author | `Write` 25.3% of logged output | prompt only | take it, cheaply |
| Prose to the user | 13.7% of logged output → **<1% of spend** | caveman already on | bounded; do not re-litigate |
| Subagent delegation | 1.2% of logged output, but each worker is a whole session (turn-1 ≈17.7k tok) | policy + cap | note only |

Deliberately **not** proposed: a global terseness rule (ACL 2025: wrong budgets degrade work).

**The ranking inverted on 2026-08-16** and it is worth saying why plainly. Every row here was sized
against *logged* output, which turned out to be a third of what is billed, and against a 5.8x re-read
multiplier that turned out to be 1.9x. The two levers this plan was built to justify — the re-emit
gate and prose compression — are together worth ~2% of spend. The one it explicitly rejected is the
largest.

## The lever nobody has looked at

**Thinking is 65% of billed output tokens and no instrument in this workspace can see it.** Its text
is never written to the transcript, so every composition number ever quoted here — including all of
the ones above — describes the other 35%.

This reopens what the first round closed. Anthropic's guidance is that **`effort` is not a length
lever**: it moves thinking volume, not reliably visible output. That was read as *effort is not a
cost lever* and the idea was dropped. But thinking volume **is** billed, at output rates, and is the
biggest slice of it. The guidance and the rejection do not actually agree.

What is **not** claimed: that lowering effort is free. Thinking is where the reasoning happens, and
the same ACL 2025 result that bars a global terseness rule — a wrong budget degrades the answer —
applies here with more force, because this budget buys correctness rather than brevity.

So: **measure before touching it.** The arm is the same shape as caveman's — the same task at two
effort levels, comparing billed output per turn *and* whether the work came out right — and it needs
the feature-toggle registry (Frente 10.4) to switch cleanly. No behavior change until then.
→ **model: opus**, with Lucas in the loop.

## Instruments before prose

*"É difícil perceber que estamos avançando... a ausência de benchmark, medições e testes visíveis me
faz duvidar se nossas edições estão boas ou confundindo as coisas."* (2026-08-15)

That was a gap in the workspace, not a mood. This repo had an instrument for **tidiness**
([`entropy.md`](entropy.md)) and one for **correctness** (`verify-fast`) and **none for value**, so
every session's worth was argued in prose — which is exactly what cannot be audited. The RTK bug is
the proof: invisible for weeks because no standing number tracked it, and when a number finally moved
it was still misread.

**Two instruments now exist**, both re-runnable in one command:

- `core/tools/wos/session/usage` prints the **billed-component split**, the logged/unlogged split of
  output, the self-authored share and the multiplier. **The tool is the authority; a row here it
  cannot reproduce should be deleted.**
- `core/tools/wos/roundup` prints, per session, `$/turn` + model split + output share + **compaction
  adoption**: the share of Bash calls the shim actually rewrote. This exact bug would have shown as a
  flat zero on day one. A lever with no standing metric is a lever nobody can tell is broken.

**And an instrument is not evidence until something checks it.** `usage` agreed with the one-off
script this file was originally written from, which read as confirmation and was not: both summed
transcript *records* rather than API responses, so they agreed while being 1.97x wrong together, and
the agreement is what stopped anyone looking further. Three weeks later the numbers were re-derived
by hand and every headline moved. **Two implementations of the same misunderstanding are one
measurement** — a new instrument owes one hand-check against raw data before anything is quoted from
it. Recorded as correction 3 in
[`core/experiments/output-cost.md`](core/experiments/output-cost.md).

**The benchmark still has no home.** `brain/INBOX.md` carries *"o WOS pode virar um artigo. o estudo
de ablação, se bem feito, me parece bem publicável."* The ablation study and the benchmark Lucas asked
for are the same artifact — a before/after over a fixed task set, with the gates and skills switched
off one at a time. Routing that entry to a paper house is still open, and is the remaining half of
this section.

**Prefer changes whose effect is visible in a number**, and say plainly in the hand-off which number
moved. A session that cannot name one is a session Lucas has to take on faith.

## Known asymmetry — compaction is Claude-only

`core/hooks/compact/bash-compact-rewrite.py` hardcodes `rtk hook claude` in two places, so **only
Claude Code gets multi-line splitting**; every other vendor still gets rtk's line-1-only behavior.
`core/hooks/copilot/` exists precisely to translate other vendors onto the canonical gates, and this
directory has no equivalent. Concretely: `.github/hooks/rtk-rewrite.json` runs `rtk hook copilot`
raw, carrying the same first-line-only bug the shim exists to fix.

**Measure before building.** Decide whether that directory grows a copilot shim — its output shape
differs — or whether copilot's "always prefix with `rtk`" instruction already covers it. The
adoption counter is the instrument that can answer it, and it is now the cheap way to find out.

One task still open upstream: rtk itself declines the whole call when line 1 is not rewritable, and
nobody outside this workspace has the shim. Worth reporting to `rtk-ai/rtk` with the four-shape
table from [`core/hooks/compact/SPECS.md`](core/hooks/compact/SPECS.md).

## Steps


4. 🟡 **Close the ungated-write hole — governance, not cost.** A new `PreToolUse: Bash` check matching
   `cat|tee > <path> <<`. **128 shell heredoc writes met no gate at all**: `pre-edit.py` and
   `bugs-gate.py` are `PreToolUse: Edit|Write`, and the only Bash hooks are a read gate and the rtk
   shim, so `brain/INBOX.md`, `HISTORY.md` and `test_entropy_ledger.py` were all written past the
   200-line size gate, the first-line-comment check and the CONTEXT.md description requirement.
   Frente 4.6 predicted exactly this.
   - It must **not** fire on `python3 - <<'EOF'` — stdin to an interpreter writes nothing and is 44%
     of heredoc volume, including every measurement script behind this plan.
   - **Warn, never block**, and say why in `core/hooks/SPECS.md`: a `PreToolUse` hook fires *after*
     the model has emitted the payload, so the tokens are already spent and blocking only makes the
     turn re-emit. The gate teaches turn N+1; it cannot recover turn N.
   - Message names **one action**: use `Write`, so the file gates apply. Any threshold goes in
     [`core/hooks/limits.env`](core/hooks/limits.env) through `file_law.py`, never inlined.
   - The `Write`-over-an-open-path half of this item is **dropped**. Its case was cost, and the cost
     was ~1% of spend, not the 11% this file claimed.
   → **model: opus** for the gate, sonnet for tests.

5. 🟢 **Two prompt changes, and only two.** Both target measured mass; neither is a global terseness rule.
   **Deliverable length** (25.3% of logged output is `Write`): *"Match the length of written deliverables
   to what the task needs; do not pad with filler sections, redundant summaries, or boilerplate."*
   **Delete verification scaffolding** — audit `core/skills/` and `AGENTS.md` for *"double-check"* /
   *"verify before"* phrasing and cut it. → **model: sonnet**.

6. 🔴 **The `AGENTS.md` pass — advances Frente 3.1, and is not a cost item.** Say so plainly: `AGENTS.md`
   is **754 tokens, 2.7% of turn 1** ([`core/experiments/context-window.md`](core/experiments/context-window.md)).
   Halving it saves nothing measurable; selling it as savings repeats the error Frente 9 spent weeks on.
   Run it as a real audit with the `claude-api` skill's `shared/prompt-audit.md` method and — more
   importantly — **its keep-list**: *context is never cruft; cruft ≠ length; never justify a deletion by
   character count alone.* Deliver a three-column verdict per rule: **delete** (a hook already enforces
   it), **move** (a hook could), **keep** (judgment no check can hold). Two findings already in hand:
   - `UPPERCASE.md = a type, lowercase.md = an instance` is enforced by `type-gate.py` and
     `schema_law.py` off `core/SCHEMA.md` — prose restating a live check is the drift checks exist to catch.
   - **`PLANS LIVE IN ROADMAPS` is contradicted live**: the planning session was required by the harness
     to write its plan to `~/.claude/plans/`. Either the rule gains an exception for harness-imposed
     paths, or the plan is copied into the target ROADMAP at exit — this file is that copy. Lucas's call.

   One line of context for the verdict: AIware 2026 finds context files dominate across 2,853 repos and
   `AGENTS.md` is becoming the standard. Ours is small by that baseline; what is unusual is how much has
   already moved out of it into hooks. **Propose, do not swing** — he asked for *bastante carinho*.
   → **model: opus**, with Lucas in the loop.

7. 🟢 **Route the three entries out of `brain/INBOX.md`.** Entry 2 → Frente 3.1 + step 6's verdict table;
   entry 3 → the new experiment file; entry 6 → Frente 9 evidence, its three claims superseded by the
   numbers above. Delete all three; leave 1, 4, 5. → **model: haiku**.

## Verification

1. `verify-fast` green (305 passing today; step 4 must not drop one).
2. **The tool checks the experiment file**: run `core/tools/wos/session/usage` and confirm every share
   matches [`core/experiments/output-cost.md`](core/experiments/output-cost.md). On disagreement the
   file is wrong — the tool is the authority.
3. **Step 4**, four cases, asserted beside the existing gate coverage in
   `core/tools/test/workspace/gates/`: `cat > existing << 'EOF'` → warns, still runs ·
   `tee > path <<` → warns · `python3 - <<'EOF'` (analysis, no redirect) → **silent**, or the gate
   fires on every measurement script behind this plan · a plain command → silent.
4. **Step 6** stops at the verdict table and waits for Lucas.
