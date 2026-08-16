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
deve ser feito com excelência. Não vamos ser ingênuos."* What follows records where the second round
**corrected** the first, twice. Those corrections are the reason to trust the rest.

## What was measured

All 21,672 main-chain turns in `~/.claude/projects/-mnt-workspace/*.jsonl`, replayed through
[`session_cost.py`](core/tools/wos/session/session_cost.py)'s rates — the `usage` fields the API itself
reported, not estimates.

**Output is 14.9% of spend at sticker price** ($548 of $3,672), which reads minor and is the trap.
Cache read is 51.0%, cache write (1h) 32.6%. **An output token is not paid once** — it lands in the
thread and every later turn re-reads it:

- mean share of a turn's context that is **self-authored: 75.7%**
- spend attributable to our own output: **86.9%**
- effective multiplier on one output token: **~5.8x sticker**
- the eight priciest sessions ($115–$184) run **88–98% self-authored**

Entries 3 and 6 are therefore **one mechanism**: long sessions cost more because the assistant fills them
with its own writing, then pays to re-read it every turn.

**The popular fix targets the wrong slice.** Output is **86.1% tool_use arguments** (Bash 26.6%,
Write 25.4%, Edit 23.8%) against **13.9% prose to the user**. "SHUT UP AND WORK" attacks that 13.9%
— ~12% of spend amplified. That also **bounds the open question in
[`core/experiments/caveman-cost.md`](core/experiments/caveman-cost.md)**: caveman compresses prose, so
its ceiling is ~12%, computable now without the Frente 10.4 toggle registry.

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
| **Re-emitting a file already in context** — `Write` over an open path (879,502 chars = 34% of Write output) + shell heredoc writes (354,100) | **≈13% of all output**, ~11% of spend amplified | yes — one gate, two paths | take it |
| Length of files we author | Write total 2.59M = 25% of output | prompt only | take it |
| Prose to the user | 1.54M = 13.9% | caveman already on | bound it, don't re-litigate |
| Subagent delegation | 1.2% of output, but each worker is a whole session (turn-1 ≈17.7k tok) | policy + cap | note only |
| Session length | multiplier is linear in turns remaining | `context-meter` live | already built |

Deliberately **not** proposed: a global terseness rule (ACL 2025: wrong budgets degrade work), and
lowering `effort` to shorten output (Anthropic: it does not reliably move visible length).

## Instruments before prose — the reorder Lucas asked for

*"É difícil perceber que estamos avançando... a ausência de benchmark, medições e testes visíveis me
faz duvidar se nossas edições estão boas ou confundindo as coisas."* (2026-08-15)

That is a gap in the workspace, not a mood. This repo has an instrument for **tidiness**
([`entropy.md`](entropy.md)) and one for **correctness** (`verify-fast`, 293 tests). It has **none for
value**. Nothing on disk answers *are sessions getting cheaper* or *is the agent getting better*, so
every session's worth is argued in prose — and prose is exactly what cannot be audited. The RTK bug is
the proof: it was invisible for weeks precisely because no standing number tracked it, and when a
number finally moved it was still misread.

**So steps 2 and 3 run before step 1.** The plan built the writeup first and the instruments last;
that ordering is what produced a session whose output Lucas cannot check. Inverted, every `/roundup`
from the next one onward prints its own cost, and the writeup gets numbers that regenerate.

Two additions the reorder needs:

- **A compaction-adoption number** in the same block: share of Bash calls the shim actually rewrote.
  This exact bug would have shown as a flat zero on day one. A lever with no standing metric is a
  lever nobody can tell is broken.
- **The benchmark already has a home.** `brain/INBOX.md` carries *"o WOS pode virar um artigo. o estudo
  de ablação, se bem feito, me parece bem publicável."* The ablation study and the benchmark Lucas is
  asking for are the same artifact — a before/after over a fixed task set, with the gates and skills
  switched off one at a time. Route that entry to a paper house and it stops being two wishes.

**Until one of these lands, prefer changes whose effect is visible in a number**, and say plainly in
the hand-off which number moved. A session that cannot name one is a session Lucas has to take on faith.

## Steps

0. 🔴 **RTK is wired twice, and precedence between them is undefined.**
   `~/.claude/settings.json` registers `PreToolUse: Bash → rtk hook claude` globally, and
   `/mnt/workspace/.claude/settings.json` registers the shim. Both fire on every Bash call here. Where
   only the shim answers the shim wins (verified), but for a payload both rewrite — `git status` ⏎
   `ls -la` — two competing `updatedInput` values are returned and the harness documents no rule for
   picking one. Observed behaviour today is the shim, which is the correct outcome by luck rather than
   by contract. Decide one: drop the Bash matcher from the global file (compaction outside this
   workspace then needs `rtk init -g --hook-only` re-run against the shim), or point the global entry
   at the shim by absolute path and accept the workspace-path dependency. **Verify by the delta method,
   with a payload both hooks would rewrite** — that is the only shape that discriminates.
   → **model: opus**, because the wrong choice degrades every repo on the machine.

1. 🟢 **Record the measurement — `core/experiments/output-cost.md`.** One file per question, per
   [`core/experiments/SPECS.md`](core/experiments/SPECS.md): *"output tokens are more expensive than
   input — by how much, and where are ours?"* Carry the tables, the method, the citations, **and both
   corrections above** — a 55% headline that became 3.7% is exactly what that directory exists to stop.
   Limitations to state: composition shares are of *logged* output only (thinking is billed inside
   `output_tokens` but never stored in transcripts); the self-authored share caps `cum_output/context`
   at 1.0 and ignores compaction, so 75.7% is an upper estimate.
   Then update [`core/experiments/caveman-cost.md`](core/experiments/caveman-cost.md): its Results row
   and first Limitation both say the benefit side needs the toggle registry. The *ceiling* no longer does.
   → **model: sonnet**.

2. 🟢 **`usage` grows a component split.** In [`core/tools/wos/session/usage`](core/tools/wos/session/usage),
   reusing `session_cost.py`'s `RATES` and the existing `turns()` loop — no second walker. Add the
   component table (fresh / cache-write 1h / 5m / cache-read / output), per-model output share, the
   self-authored share and the multiplier. ~35 lines. Frente 9's law: anything step 1 states must be
   re-runnable in one command. → **model: sonnet**.

3. 🟢 **Per-session cost in the roundup — closes Frente 9.4.** That frente says outright it *"is a wiring
   job, not a new instrument."* Wire it into [`core/tools/wos/roundup`](core/tools/wos/roundup), printed
   with the state facts in Phase 4 — not the skill, because it has one right answer. The script has no
   session id: resolve the current transcript as the newest-mtime `*.jsonl` under
   `~/.claude/projects/-mnt-workspace/`. Respect Frente 9.2 — shares, $/turn, output share; **no absolute
   total** while the ~8% gap is open. A few lines only: `/roundup` is itself 14% of usage.
   → **model: sonnet**.

4. 🟡 **One gate for re-emitting a file already in context.** Two paths, one rule — a gate covering only
   `Write` moves the behavior to `cat >`, which is where 128 ungated writes already went.
   - **`Write`** — extend [`core/hooks/checks/pre-edit.py`](core/hooks/checks/pre-edit.py). It hooks
     `PreToolUse: Write` but only inside `if not os.path.exists(file_path)`, so it covers creation and
     nothing else. Add the `else` branch: file exists **and** payload over threshold → warn that an
     `Edit` costs ~3x less (Edit averages 1,194 chars against Write's 3,596) and does not re-inject the
     file into context.
   - **`Bash`** — a new `PreToolUse: Bash` check matching `cat|tee > <path> <<`. Same message. This half
     closes the enforcement hole, not just the cost one.
   - **Warn, never block.** A legitimate full rewrite is common; the honest failure mode of this whole
     plan is a gate that makes real work harder. Zero-token until it fires.
   - Threshold is a number → [`core/hooks/limits.env`](core/hooks/limits.env), read through
     `file_law.py`, never inlined in a checker. Message names **one action**.
   → **model: opus** for the gate, sonnet for tests.

5. 🟢 **Two prompt changes, and only two.** Both target measured mass; neither is a global terseness rule.
   **Deliverable length** (the 25% of output that is `Write`): *"Match the length of written deliverables
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

1. `verify-fast` green (283 passing today; steps 2 and 4 must not drop one).
2. **Step 2 checks step 1**: run `core/tools/wos/session/usage` and confirm every component share matches
   the table in `output-cost.md`. On disagreement the file is wrong — the tool is the authority.
3. **Step 3**: run `core/tools/wos/roundup`; the cost block prints, names a model split, prints no
   absolute dollar total.
4. **Step 4**, four cases, all asserted beside the existing `pre-edit` coverage — the current bug is
   precisely a branch never exercised: `Write` to an existing file over threshold → warns, write still
   succeeds · `Write` to a new path → silent · `Bash` with `cat > existing << 'EOF'` → warns, still runs ·
   `Bash` with `python3 - <<'EOF'` (analysis, no redirect) → **silent**, or the gate fires on every
   measurement script behind this plan.
5. **Step 6** stops at the verdict table and waits for Lucas.
