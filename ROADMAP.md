# Workspace-OS Roadmap — the v1 push

> **Single entrypoint for all workspace-os (wos) build work.** Goal file
> [brain/goals/workspace-os.md](brain/goals/workspace-os.md) holds *why*; this file holds *what*.
> [brain/TODO.md](brain/TODO.md) holds life tasks only; [core/ROADMAP.md](core/ROADMAP.md) holds
> agent-library internals only. An item lives in exactly one of the four — a copy is a bug.
> Evidence: [core/refs/REFS.md](core/refs/REFS.md) for external material,
> [core/experiments/](core/experiments/CONTEXT.md) for what we measured about ourselves — an
> intent item belongs here, a measurement over time belongs there, and neither restates the other.
>
> **Deletion policy: hard delete. Git is the history.** No strikethrough, no annotated corpses. A
> killed item gets one line under *Rejected* so it does not resurface looking new.
>
> **Completion is deletion, not `[x]`** (Lucas, 2026-07-30). Once a task's verification passes, cut
> the item out — do not tick it and leave it sitting there. A roadmap holds only what is still open,
> so its length is a real measure of remaining work. What was built is recorded by the code, its
> tests, and git. Keep a line only when the *next* session needs it to extend the work instead of
> recreating it, and write that line as present-tense state, never as a report of what was done.

## v1 definition of done

Four criteria. Nothing else gates v1.

| # | Criterion | Owner | State |
|---|-----------|-------|-------|
| 1 | **verify-fast green + Tier 0 live** — naming, placement, pointer integrity, size-as-signal deterministic; **this repo** clean, every nested repo on a shrinking baseline | Front 4 | checks live · **read [`entropy.md`](entropy.md) for the count, never a copy of it** |
| 2 | **One ledger, no duplicates** — this file is the sole wos ledger, verified by scan not eyeball | Front 8 | ✅ **MET 2026-07-30** — `test_no_item_lives_in_two_ledgers` |
| 3 | **Everything pushed, gitflow-shaped** — every `code/` repo on `main`/`feature/*`, zero unpushed, no repo without a remote | Front 11 | ✅ **MET 2026-08-14** — re-audited across every repo |
| 4 | **Clonable by a student** — fresh clone gets every capability; deps declared, no undocumented hand-installs | Front 10 | ✅ **MET 2026-08-16** — `SETUP.md` is an executed procedure, every dep declared in `core/tools/deps.txt`, both enforced by `verify-fast` |

Post-v1 validation is `[mvp-validate]`: use the system daily for 30 days, then assess whether it
reduced mental load. That is the real test and it can only run after v1.

## How to read this

Per-step `model` = the tier that is *enough* (a floor, not a ceiling).
🔴 needs Lucas · 🟡 pilot on one subtree first · 🟢 mechanical.

**Three open steps need Lucas's own judgment: 9.5, 11.3, 15.1** — the single list, quoted here and
nowhere else. Everything else is agent work.
Stating that number is part of the cure for feeling lost, so **keep it true** — it has been wrong
three times: once claiming one while five were live; once (2026-08-16) carrying four items marked 🔴
whose own `→ model:` line said sonnet; and once holding *two* lists of the same set, here and in
§ Sequencing, which named different threes and so were both wrong. **Derive it from the 🔴 marks.**
**This is the only list; § Sequencing points here rather than restating it.** Two lists of the same
set is the asymmetry, and the count is only ever its symptom, so the cure is one list rather than
two kept in sync. **🔴 means Lucas decides, not "this is hard"**; an item an opus-tier agent can
rule on alone is 🟡. Re-derive the count from the marks before quoting it.

The whole Front 10 chain came off this list on 2026-08-16 — six 🔴 items closed in one sitting,
because they were one decision wearing six numbers and none of them could be taken alone.

**Never cite an item number outside this file** — enforced on every commit by
`checks/citation-gate.py` ([`core/hooks/SPECS.md`](core/hooks/SPECS.md) § Git pre-commit). Completion
is deletion, so a cited number is a pointer to nothing the day the item lands; point at the section
that owns the rule instead.

Measurements never live here. The instrument is
[`core/tools/wos/session/context`](core/tools/wos/session/context); results live in
[`core/experiments/`](core/experiments/CONTEXT.md); drift counts live in [`entropy.md`](entropy.md).
Re-run them rather than quoting a number from this file.

**Load-bearing principle: automatic + zero-token beats agent-checked, and free checks are never
coupled to paid ones.** Deterministic scripts per-commit; human judgment on demand.

> **Evidence caveat, once for the whole doc.** Some steps lean on two strong but *unreviewed*
> preprints — progressive disclosure ([P] 2607.17598) and ACE ([P] 2510.04618). Provisional; never a
> hard gate.

---

## Front 3 — Memory and always-loaded context

0. 🟢 **measure `.claude/commands/`, then decide — the only unmeasured thing left at session start.**
   `mirror.sh` copies all 13 skills a *second* time as slash commands (52 KB on disk). That copy is
   folded into the system prompt, so it lands inside the **77% residual** that
   [`session/context`](core/tools/wos/session/context) cannot decompose — it is invisible to every
   number we have. It may be a real chunk of the residual or nothing at all, and the honest order is
   measure first: the cheapest probe is a session with the directory emptied, comparing turn-1
   context. **Do not cut it on suspicion** — that is the mistake the 1.6-3.5x inflation already
   taught. Record the result in [`core/experiments/context-window.md`](core/experiments/context-window.md).
   → **model: sonnet**.

1. 🟡 **test the six "inverted practices" against our own instructions.** Claim, from a practitioner post
   (`[C]`, ref in [core/refs/REFS.md](core/refs/REFS.md), captured INBOX 2026-07-31, Lucas: *"ver se é
   verdade e se for estudar como aproveitar no wos"*): Anthropic cut **>80%** of Claude Code's system
   prompt for its newest models and replaced hardcoded rules with judgement over rules, interfaces over
   examples, disclosure over dumping — `TodoWrite` reportedly going from ~9.1k chars of worked examples to
   an enum-typed interface, verification and code review moving out of the prompt into on-demand skills,
   and tool definitions deferred behind `ToolSearch` until needed.
   **The 80% number is self-reported with no published benchmark and is not independently verifiable — do
   not cite it.** The *framework* is testable here, which is the whole value: our own hooks already prove
   the mechanism half of it (a hook's error message is a zero-token instruction that arrives exactly when
   it applies), and the MOVE OUT bucket in 3.2 is the same move by another name.
   Concrete probe, cheapest first: take the two or three most rule-shaped surfaces we own — `AGENTS.md`,
   the fattest `CONTEXT.md` heads, and the skills flagged in `core/ROADMAP.md` — and ask per rule whether
   it could be a **tool parameter, an enum, or a hook message** instead of prose. Whatever survives that
   question is prose that earns its place. Feeds directly into 3.2's MOVE OUT and the skills audit.
   → **model: opus** for the judgement pass, sonnet for the rewrites.
2. 🟡 **the `AGENTS.md` pass — and say plainly that it is not a cost item.** Lucas asked for it as
   one (*"o AGENTS.md voltou a parecer meio grande… avaliar ele com bastante carinho"*), but it is
   **754 tokens, 2.7% of turn 1** ([`core/experiments/context-window.md`](core/experiments/context-window.md)):
   halving it saves nothing measurable, and selling it as savings repeats the error Front 9 spent
   three weeks inside. Run it as a real audit with the `claude-api` skill's `shared/prompt-audit.md`
   method and, more importantly, **its keep-list** — *context is never cruft; cruft ≠ length; never
   justify a deletion by character count alone*. Deliver a three-column verdict per rule: **delete**
   (a hook already enforces it), **move** (a hook could), **keep** (judgment no check can hold).

   Two findings already in hand. `UPPERCASE.md = a type, lowercase.md = an instance` is enforced by
   `type-gate.py` and `schema_law.py` off `core/SCHEMA.md` — prose restating a live check is the
   drift the checks exist to catch. And **`PLANS LIVE IN ROADMAPS` is contradicted live**: the
   harness requires a planning session to write its plan to `~/.claude/plans/`, a path no clone of
   this workspace would ever get. Either the rule gains an exception for harness-imposed paths or
   the plan is copied into the target ROADMAP at exit — **that half is Lucas's call**; the rest is
   agent work. Ours is small against the AIware 2026 baseline (`core/refs/REFS.md` § Output cost),
   and what is unusual is how much has already moved out of it into hooks. **Propose, do not swing.**
   → **model: opus**.

---

## Front 4 — workspace anti-entropy — **the keystone, v1 criterion 1**

> The real target: files grow, scatter, duplicate, and drift from naming/structure patterns.
> **Structure is a spec; drift is a test failure.** `code/` already has this (the `> spec:` gate);
> the agent library has [core/SCHEMA.md](core/SCHEMA.md). Nothing yet governs the shape of the
> workspace itself.

1. 🟢 **Tier 0 — per-commit, zero-token, deterministic.** Live: `core/hooks/checks/type-gate.py` (ratchet, only
   what a commit *adds*) + `schema_law.py` · `entropy_naming.py` · `entropy_ledger.py`, asserted by
   35 tests in `verify-fast`. Every rule is **parsed from `core/SCHEMA.md`**, never restated in a
   checker. Covered: type allowlist, hand-inventory, filename shape, directory case, type placement,
   retired tokens, duplicate slugs, size-as-signal.
   The **project ⟺ goal link** check went straight to blocking, no warn phase: the backfill turned
   out to be already done, all 14 projects declaring line 3. Six declare `goal: none` — and two of
   those, `gira` and `laplata`, **have** goal files (`startapps-gira`, `startapps-laplata`). A
   content question for Lucas, not a check failure.
   **Wiki-link resolution — decided 2026-07-30 (Lucas), and shipped.** A double-bracketed slug may
   name a goal file *or* a bracketed item inside one: both are real pointers
   (`spec-driven-development` is the file, `prompt-dsl` is an item in `craft-flows.md`) and both
   resolve by scan. Vocabulary is 333 names. One dead link found and fixed — `dobra` is a project,
   not a goal; its goal is `local-ai`. That closes pointer integrity, and Tier 0 with it.

   Conventions the checks had to be taught, each because it is a law that outranks ours: snake_case
   Python modules and `__init__`, PascalCase/camelCase in JS/TS, uppercase venue acronyms in
   `academy/papers/<year>-<VENUE>-<slug>`, `_`-prefixed scaffolding, and **received documents keep
   their names** — the 91 tracked paths with spaces and accents are all `.docx`/`.pdf` from the PPC
   process, where the filename *is* the provenance. Decided the same way: `core/tools/*` CLI
   entrypoints stay extensionless, which is the convention for anything meant to be run by name.
   → **model: sonnet** · **switch: `/craft`.**
2. 🟢 **finish the retired-word rename at the per-run state dir.** APPROVED 2026-07-29 (Lucas: *"we
   renamed loops to be flows but apparently this keeps coming back"*). It keeps coming back because
   it **was never a drift problem** — the rename stopped at the flow pool (`core/flows/`, flow
   renamed `craft`) while the generators still emit the retired word *legitimately*, so no naming
   check could ever flag it. The skill half is closed — the command is `/craft`, the file is
   `core/skills/craft.md`, and `core/SCHEMA.md` § Retired tokens guards the invocation shape.

   What is left is the state dir, and it is the larger half: `.loop/<slug>/` is hardcoded in
   `craft.md`, `architect.md`, `runtimes.md` and `routing.md`, with 14 live dirs across `aiwbot`,
   `isoroll-content` and `isoroll-module`; the cross-run pattern library is
   `core/flows/.loop-skills/`. Scope: `.loop/` → `.craft/`, `.loop-skills/` → `.craft-skills/`, and
   the live dirs migrate with it. Add that token to § Retired tokens the day it lands — **not
   before**, because a row that fails on the day it is written trains people to ignore the check.
   **Keep "Loop 0..6" as step names** — an iterative step really is a loop; that word is correct
   English, not the retired label.
   **Verify with `make entropy`, not `git grep`** ([`core/SPECS.md`](core/SPECS.md) § Conventions —
   it is how this rename was declared done twice). Four survivors surfaced that way, and two of them
   sit inside frozen `.loop/` run records: a chain file records what was *run* that day, so rewriting
   it makes the record lie. **Decide whether run artifacts are exempt before touching them.**
   → **model: sonnet**.
3. 🟢 **drain the entropy dashboard.** `make entropy` → [`entropy.md`](entropy.md), the whole
   workspace and its nested repos in seconds. Read the report; never re-scan the tree. **Never copy
   its counts into this file** — a copied number is the drift these checks exist to catch, and the
   summary table at the top of the report is the interface. Criterion 1 wants it reading clean.

   The dashboard scans nested repos, the **tests do not** — an assertion in this repo about
   another repo's content fails for reasons this repo cannot fix, and each nested repo runs its
   own verify. Where a check is green workspace-wide it is asserted at zero in `verify-fast`
   (retired tokens, duplicate slugs); where it is not, `test_entropy_naming.py` holds a named
   **baseline** so a new violation fails the build and a fixed one must leave the list.

5. 🟡 **drain to zero, then flip fanout to a hard block** (Lucas 2026-07-31: hard block, no
   grandfathering). The flip is coherent only at zero — the pre-commit hook is global
   (`core.hooksPath`), so switching it on while nested repos are over the cap fails every commit in
   those repos, including the commits that would fix it. Live lists in [`entropy.md`](entropy.md);
   when they read Clean, add fanout to `core/hooks/checks/` beside the type gate and delete
   `BASELINE` from `test_entropy_fanout.py` in the same commit.

   **This repo, `code/aiwbot` and `code/flows` are drained.** What the draining taught is written
   into [`code/SPECS.md`](code/SPECS.md) § Splitting an over-full directory — five rules, each of
   which cost a session to find, and that is where a future repo will look for them rather than in
   a ledger item that closes.

   **Everything remaining lives in nested repos and is refiled there (2026-08-16)**, because a
   workspace commit cannot touch those files and a pointer to another ROADMAP is a duplicate by
   definition. `apptime` and `spacemantics` carry their own items now, on
   `feature/workspace-drift-refile`. The isoroll pair — `isoroll-content/src/pipeline` and its
   siblings, `isoroll-module/src/render` and its siblings, plus the one file over `BLOCK_LINES` —
   were **not** refiled: both checkouts are held by the parallel isoroll session and writing into
   them from here is the mid-flight collision Front 11 exists to prevent. **That session refiles
   them**, and until it does, this repo cannot flip the gate.
   → **model: sonnet**, one repo at a time.

6. 🟢 **sweep the first-line-comment markers now that the gate is shut.** The hole is closed:
   `entropy_context.check_description` blocks at commit through the Tier 0 gate, ratcheted to what a
   commit adds, and asks the routing generator rather than a table of its own
   ([`core/hooks/SPECS.md`](core/hooks/SPECS.md) § First-line descriptions). What is left is the standing queue the ratchet deliberately does not
   charge anyone for. **Size it against [`entropy.md`](entropy.md), and re-run the generator before
   measuring** — every marker drained so far was a file the generator could already describe.
   Most of the queue is nested-repo work, so it is one repo at a time. → **model: sonnet**.

---

## Front 8 — The ledger discipline — **v1 criterion 2**

Collapsed 2026-07-29 (four ledgers → one) and cut 2026-07-30 (52 open steps → 17). The collapse made
the ledger honest but not smaller — items went 158 → 123 while mass stayed flat, and Lucas reported
feeling lost twice. **Mass is the disease and only deletion cures it.**

1. 🟢 **`TODO.md` dies as a type — fold its content into goals, then delete the file.** Ruled
   2026-08-14. Lucas reported twice, unprompted, *"sinto que o TODO.md simplesmente não tá sendo
   usado"*, and the evidence was always that he writes tasks into the INBOX instead. He chose
   **both** the delete and the fold, and they are not alternatives — they are the two halves of one
   move, in order:

   1. **Fold** — every live line in `brain/TODO.md` becomes a backlog item in the goal it actually
      serves (`[short-id] description`, per [brain/SPECS.md](brain/SPECS.md) § Backlog Ordering).
      A task with no goal is the interesting case and there are only two honest outcomes: it belongs
      to a goal that does not exist yet (write the seed — a goal file's minimum is two lines), or it
      is capture, not commitment, and belongs in the INBOX.
   2. **Delete** — remove the file, then the type: the row in `core/SCHEMA.md`'s type table, the
      mention in [brain/CONTEXT.md](brain/CONTEXT.md), and the "four ledgers" phrasing in this
      file's own header, which becomes three. Deleting the file while leaving the type declared
      would regenerate it — that is the lesson job A of Front 12.1 already paid for.

   **Why this beats redesigning it.** The redesign question was *"what would make it get checked
   daily"*, and the honest answer is nothing: `/compass` is already the review ritual and it reads
   goals, so a second surface competes with a ritual that works. Capture goes to INBOX, commitment
   goes to a goal backlog — no third place, no boundary to police. This is the *delete weak features*
   rule applied to our own scaffold instead of to code.
   → **model: sonnet**. The fold needs a judgment call per line, so read them, do not batch.
3. 🟡 **the attention dashboard measures the wrong thing** (Lucas, INBOX 2026-08-13). It counts
   edits to the goal's **own `.md` file**, not work **on** the goal — so the 2026-08-13 compass
   rendered `workspace-os ░░░░░░░░░░ 1 touch` in the same fortnight that **29 of 29** workspace
   commits were wos (hooks, tools, verify, session, entropy). Any goal whose work lands in `code/`
   or `core/` reads as dead, and the compass's Pareto has to be hand-corrected every cycle — the
   exact manual correction the workspace exists to kill. Each goal declares the paths it **owns**
   in a `>**owns**` block, and the counter counts commits touching those paths.

   **Scoped 2026-08-13, and the scoping moved it off `brain_dashboard.py` alone — three findings
   the one-line framing above missed:**
   - **The work is in other repos.** `code/*`, `academy/papers/*` and `branches/*` are gitignored
     by the workspace repo and are **24 independent git repos**, so `git log -- code/spacemantics`
     from root returns nothing, forever. Ownership buys nothing without resolving each path to its
     governing repo (walk up to nearest `.git`) and running git *there*. This is the load-bearing
     half of the fix.
   - **The instrument measures its own observer.** `/compass` writes back to every goal file it
     reviews; next cycle those goals read as active *because they were reviewed*. Drop commits whose
     changed paths lie **entirely** within `brain/goals/*.md` + `brain/GOALS.md` — a rule that reads
     what changed, not how it was described, so commit style cannot game it.
   - **Area bars must union, not sum.** `area_touches[area] += c` double-counts the moment one
     commit advances two goals (workspace-os owns `core/`, craft-flows owns `core/flows/craft/`).
     Count distinct `(repo, sha)` pairs. Overlap *between goals* stays intentional — that commit
     really did advance both.

   Measured set is `declared owns ∪ {the goal file}`, so a goal with no block behaves exactly as
   today: **life goals (dance, sleep, yoga) have no repo and their file genuinely is the artifact.**
   An empty `>**owns**` is not a gap to fill. Harvest one `git log --name-only` per *declared repo*
   (~12), not one per goal (~52 subprocesses today). New module
   `core/hooks/brain/brain_attention.py` owns the counting —
   [`brain_dashboard.py`](core/hooks/brain/brain_dashboard.py) is at **194 lines against
   `BLOCK_LINES=200`** and must shrink by handing counting away, not grow.

   **Committed 2026-08-14 as work in progress, and the shrink did not happen.** The session doing
   this was halted mid-flight; its tree was coherent (module imports, `brain_stats.py` consumes it,
   dashboard runs, `verify-fast` green) so it was committed rather than lost. But
   `brain_dashboard.py` went **194 → 196** and `brain_stats.py` is at **177**: counting moved out
   and something else moved in. Both are warns now, four and twenty-three lines from a hard block
   respectively — so the next session on this front starts by paying that down, before adding
   anything.
   **The parser is fixed and tested (`test_brain_attention.py`), so start from a quiet baseline.**
   It used to read the goal's body as repo paths and print nine warnings per commit. Worth
   remembering while doing the counting work: nothing was ever *miscounted* by it, which is why it
   survived — the output was wrong in a way that changed no number.

   → **model: sonnet**. The plan is the three findings above; it used to point at a file in
   `~/.claude/plans/`, which `AGENTS.md` forbids — a plan lives in the ROADMAP of the thing it
   changes, not in harness-owned state no clone of this workspace would ever get.

---

## Front 9 — Cost & model routing

> **Every number this front used to carry now lives in
> [`core/experiments/output-cost.md`](core/experiments/output-cost.md)** — the composition of output,
> the $/turn staircase by context band, and the three claims the audit retired. Re-run it, never
> quote it: [`core/tools/wos/session/usage`](core/tools/wos/session/usage). What the front holds is
> what is still *intended*.
>
> The two findings that decide the items below: **context size is the driver, not output volume**
> (4.2x from the cheapest band to the dearest, 88% of spend above 100k), and **65% of billed output
> is unlogged thinking** — invisible to every instrument here, and the largest single slice. The
> discipline that cost the most to learn is now
> [`core/experiments/SPECS.md`](core/experiments/SPECS.md) § build the instrument, then check it.
>
> Both halves of the session transition are already live: `context-meter.py` announces the crossings
> at zero token cost, `core/tools/wos/roundup` closes the session, and the split is
> [`core/SPECS.md`](core/SPECS.md) § AD-09.

1. 🟢 **safe — cheaper models where the work is mechanical.** Measured split (2026-08-16):
   opus-5 56.5%, opus-4.8 27.5%, fable 8.3%, sonnet 7.7%, haiku ~0%. Worth doing, but note the
   ceiling — routing cannot beat a 4x context multiplier, and the transition above already took the
   larger win. → **model: sonnet**.
3. 🟡 **make delegation happen, instead of hoping for it.** Lucas, INBOX 2026-08-15: *"só tenho
   confiado no opus. mas gostaria que ele delegasse mais ao sonnet pra economizar quando fosse
   pertinente. não sei como fazer isso, seria ótimo se tivesse uma forma mais garantida de fazer
   isso acontecer."* Item 1 says routing is *worth doing* and measures the split at opus 84% /
   sonnet 7.7%; this item is why that split has not moved. **A per-item `→ model:` line in this
   file is advice an agent may skip, and mostly does** — same class of defect as Front 4.6's
   first-line comment, where a rule existed and the number still grew.

   His proposed trigger is the concrete part: *"talvez se toda vez que o modo plan fosse utilizado
   ou toda vez que o prompt pedisse para montar um plano para cada tarefa do plano o modelo
   definisse qual modelo/agente deveria executar aquela tarefa… seria bom ter a delegação como
   parte de uma política natural mas o plano poderia ser um gatilho mais evidente."* Planning is
   already the moment the work is cut into tasks, so it is the one point where per-task routing is
   free to decide and cheap to record. Make the plan *carry* the assignment rather than leaving it
   to recall at execution time.

   **Its feedback loop is already wired**: [`core/tools/wos/roundup`](core/tools/wos/roundup) prints
   the per-session model split at every close, so whether this item moves the opus/sonnet ratio is
   readable without new instrumentation. A delegation policy nobody measures per session would be
   unenforced advice one more time.
   **Partly demonstrated 2026-08-16**: this session's own plan carried a `model:` per task, which is
   the mechanism in its cheapest form — the plan *is* the assignment record. What is unbuilt is
   anything that makes it non-optional.
   → **model: opus** for the mechanism, sonnet to wire it.
5. 🔴 **discuss — should this workspace have agents, or are skills enough?** Lucas, same capture,
   and flagged by him as a discussion rather than a task: *"um aluno comentou que existem formas
   diretas de o claudecode delegar pra subagentes, ele falou acho que com @. é fato que não temos
   agentes no workspace, me pergunto se deveríamos. temos skills e isso me parece suficiente, mas
   talvez não seja. esse é um ponto que merece discussão ao meu ver."*

   Two facts to put on the table before opinions. `core/agents/` **does** exist — lead, researcher,
   writer, verifier, reviewer, ported from Feynman — so the claim "não temos agentes" is about them
   being unused, not absent; find out which is true before designing anything. And the measured
   fact from this front: *zero* sidechain messages across 328 transcripts, which is why the
   "59% from subagent-heavy sessions" claim was retired. **Nothing has ever been delegated here**,
   so this is a question about a capability with no usage data at all, not a tuning question.
   Same treatment as Front 10.1: bring options and trade-offs, decide with Lucas, do not arrive
   with one answer.
   → **model: opus**, with Lucas in the loop — not a solo pass.
7. 🟡 **show context growth continuously, not just at two thresholds.** Lucas, same capture:
   *"gostaria de ver o crescimento da janela de contexto em tempo real, o claude code no vs code
   não mostra. tem alguma forma barata de me mostrar isso?"*
   [`core/hooks/session/context-meter.py`](core/hooks/session/context-meter.py) already reads the
   size the API reports and speaks at `CTX_WARN` / `CTX_LOUD` — the ask is the *trend* between
   them, and the cheapest honest answer is probably a statusline rather than more hook output,
   since the hook's whole design point is costing zero tokens until crossed. **Do not make it
   chatty every turn**; that trades the thing being measured for the measurement.
   → **model: sonnet**.
8. 🟡 **auto-continue when the session limit is hit.** Lucas, INBOX 2026-08-16: *"estudar uma forma
   de ativar um 'auto-continue' do claude code quando o limite das sessões é atingido."* Filed here
   rather than in `code/aiwbot` because the thing that must survive the interruption is this
   workspace's session ritual, not a bot's transport.
   **Study before building** — the honest first question is what the harness actually does at the
   limit and what state survives it, and the second is whether resuming is even right: a session
   that hit the limit is a session at maximum context, where `/roundup` plus a fresh start is
   cheaper per turn than continuing (the staircase is in the experiment file). The likely answer is
   *auto-close, not auto-continue*. → **model: sonnet** to study, Lucas to rule.
9. 🟡 **the lever nobody has looked at: thinking is 65% of billed output and no instrument here can
   see it.** Its text is never written to the transcript, so every composition number we have
   describes the other 35%. This reopens what was closed once: Anthropic's guidance is that `effort`
   is not a *length* lever — it moves thinking volume, not reliably visible output — which was read
   as *not a cost lever* and dropped. But thinking volume **is** billed at output rates, and is the
   biggest slice of it. The guidance and the rejection never actually agreed.

   **Not claimed: that lowering effort is free.** Thinking is where the reasoning happens, and ACL
   Findings 2025 (a wrong budget degrades the answer, `core/refs/REFS.md` § Output cost) bites harder
   here than anywhere, because this budget buys correctness rather than brevity. So **measure before
   touching it**: same arm shape as `caveman-cost.md` — one task at two effort levels, comparing
   billed output per turn *and* whether the work came out right. It needs a clean switch, so it runs
   on the feature registry, and it is the same instrument Front 14 needs. No behavior change until
   the number exists. → **model: opus**, with Lucas on whether to act on it.
10. 🟡 **compaction is Claude-only, and that is a provider-agnosticism hole.**
   `core/hooks/compact/bash-compact-rewrite.py` hardcodes `rtk hook claude` in two places, so only
   one vendor gets multi-line splitting; `.github/hooks/rtk-rewrite.json` runs `rtk hook copilot`
   raw and carries the first-line-only behavior the shim exists to fix. `core/hooks/copilot/` exists
   precisely to translate other vendors onto the canonical gates and has no equivalent here.
   **Measure before building**: `roundup` already prints compaction adoption, so it can answer
   whether copilot's "always prefix with `rtk`" instruction already covers this before a second shim
   is written. One outward-facing follow-on, Lucas's call: report the line-1-only decline upstream to
   `rtk-ai/rtk` with the four-shape table in
   [`core/hooks/compact/SPECS.md`](core/hooks/compact/SPECS.md). → **model: sonnet**.

---

## Front 10 — Portability & clonability — **v1 criterion 4**

> **Ruled 2026-08-16 (Lucas); every ruling is recorded where it is enforced, not here.** The harness
> is the installer and `SETUP.md` is the prose it executes — [`core/SCHEMA.md`](core/SCHEMA.md)
> § The `.md` type system. The registry's grouping, its columns, and the fact that `scope` **is** the
> general/Lucas-specific line (a column the sync reads, not a document) are declared in the header of
> [`core/features.txt`](core/features.txt) itself; the rule behind it is
> [`core/SPECS.md`](core/SPECS.md) § AD-14.

**Criterion 4 is met and the registry is live.** What remains is one mechanical backlog: a capability
whose `wired` column reads `-` cannot be switched off, so **Front 14 cannot report on it**. Wiring one
is calling `feature_law.is_enabled()` where the rule is enforced and naming that file in the column.
Read the count from `core/tools/wos/features --findings`, never from here. The open design question
— whether the honesty test stays a literal grep, which forces one call site per row — is
[`core/SPECS.md`](core/SPECS.md) § AD-14, last paragraphs.

5. 🟡 **the public scaffold repo and its one-way sync.** A **separate public repository**, not a
   branch — personal history never leaves this repo, where a branch would carry every commit that
   ever touched `brain/`. That is what makes the general/Lucas-specific line checkable on every run
   instead of documented.

   **Ruled 2026-08-16 (Lucas), both open questions closed:**
   - **`brain/` crosses as empty structure** — `CONTEXT.md`, an empty `INBOX.md` and `GOALS.md`, one
     example goal file. No real goals, no `USER.md`, no attachments. The brain system is half the
     value of WOS; shipping `core/` alone hands someone an enforcement layer with nothing to enforce
     on. An example rich enough to look like real personal data is the thing to avoid.
   - **Sync is one-way, contributions land as INBOX entries.** The script pushes private → public
     and nothing auto-flows back. A useful PR is read and re-implemented here by hand, captured
     through `brain/INBOX.md` like every other input. The private repo stays the single source of
     truth, and contribution stays honest rather than blocked.
   - **The public checkout lives at `code/wos/`**, as a nested repo like every other project. Lucas:
     *"maybe a good idea is for us to have it here as a code repo under `code/wos/` so it is easy to
     monitor it. this workspace repo is private, mine and only I use it amongst my machines (two
     laptops), and the public is for my students and anyone else."* Still its own repository with its
     own history — that is what keeps personal commits from crossing — this only fixes where the
     working copy sits. It pays twice: the sync becomes an ordinary write into a tree that can be
     `git diff`ed **before** anything is pushed, so **the allowlist is reviewable as a diff rather
     than trusted as a script**; and the public repo inherits the gates, since `core/hooks` is wired
     globally and fires in every nested repo. Mechanically free — `code/wos` joins the `code/*`
     ignore list like `aiwbot` and `apptime`, so no gitlink forms.

   The registry (step 4) ships as scaffold — it is the thing that makes a subset installable — with
   the profile replaced by a placeholder on the way out. **The sync's allowlist is the deliverable**,
   not the copy: a path that is not on it does not travel, so adding a new top-level directory fails
   closed.
   → **model: sonnet**.

---

## Front 11 — Git & sync integrity — **v1 criterion 3 — ✅ MET 2026-08-14**

**The criterion holds, and it is re-run rather than trusted** — one loop over `find . -name .git`
asserting a remote and a legal branch per repo. The rule that came out of closing it is
[`core/SPECS.md`](core/SPECS.md) § Conventions, first bullet: a finding older than a week is a
hypothesis.

3. 🔴 **is spec-driven development resumed, rescoped, or killed?** Lucas, 2026-08-15: *"sobre SDD
   (SPEC DRIVEN DEVELOPMENT), sinto que começamos isso mas esquecemos completamente."* The ledger
   is [`code/ROADMAP-spec-drive.md`](code/ROADMAP-spec-drive.md) and it is **readable now** — it was
   gitignored by the `code/*` rule, so every edit stayed on one machine, which is a sufficient
   explanation for the forgetting on its own.

   **The decision cannot be deferred cheaply, because the gates are live either way.** `pre-commit`
   §1d and `read/spec-read-gate.py` fire on every session regardless of whether anyone is still
   rolling this out, which makes an *abandoned* rollout more expensive than a dead one. Read the
   file's own Open items with fresh eyes and rule.

   **What tracking it immediately revealed, and it is the argument for the whole `.gitignore`
   allowlist discipline:** the moment the file entered the corpus it failed `verify-fast` on three
   retired tokens from the July `loops`→`flows` rename. Every other file was swept then. This one
   could not be seen, so for a month it kept pointing readers at a flow file that had been renamed,
   **An untracked file does not merely lack backup — it opts out of every
   check the workspace has**, and goes on giving instructions while it rots.

   **Read [`github/spec-kit`](https://github.com/github/spec-kit) before ruling** (ref in
   [`core/refs/REFS.md`](core/refs/REFS.md); Lucas, INBOX 2026-08-16: *"vale a pena pesquisar bem
   pra não pegar a primeira opção sem pensar"*). It is input to the decision, not a replacement for
   it — ours is already wired into five enforcement points, so the honest question is what spec-kit
   does that those do not, and whether adopting it would mean deleting our gates or feeding them.
   → **model: opus**, with Lucas.

---

## Front 12 — The `.md` type system (decided 2026-07-30)

> **The law is [`core/SCHEMA.md`](core/SCHEMA.md)** — § The `.md` type system holds the allowlist and
> the one question each type answers, § Boundaries where types nearly touch holds the three conflicts
> and their resolving rules, § Retired tokens holds what each rename retired. This front holds only
> the migrations that have not landed.

1. 🟢 **the `SPEC.md` → `SPECS.md` migration — the one part of retyping that is still wos work.**
   `core/hooks/checks/type-gate.py` stops *new* off-allowlist names; the existing ones are
   enumerated live in [`entropy.md`](entropy.md) — read the report, never re-scan.

   **Three `SPEC.md` instances**: `spacemantics`, `aiwbot`, and `code/_templates/module.SPEC.md`.
   The template is the generator, so it moves first or the name grows straight back. This is
   **one reviewed change, never piecemeal**, because the singular spelling is load-bearing in five
   enforcement points — `core/hooks/pre-commit` §1d, `read/spec-read-gate.py`,
   `read/context-tracker.py`, `core/tools/wos/spec-scan`, `core/tools/wos/spec-contract-check` —
   and in the `> spec:` convention every `code/` CONTEXT.md declares. Only when it lands does
   `SPEC.md` earn its row in `core/SCHEMA.md` § Retired tokens; a row written before the sweep
   completes fails on day one and trains people to ignore the check.

   **The rest is refiled (2026-08-16).** spacemantics' eleven spec-shaped names are that repo's
   design question and now live in its ROADMAP; the twenty-name long tail across nine repos is
   each repo's own, as are the completed-milestone corpses still sitting in `flows` and `aiwbot`.
   [`entropy.md`](entropy.md) keeps counting all of it, so nothing goes dark.

   **The lesson that generalises, from draining the six `HISTORY.md`: delete the generator before
   the artefact, or the name grows back.** Four ROADMAP headers were *instructing every future
   session* to write one. And rejected-approach content is the single thing git cannot hold — save
   it to `ROADMAP.md § Rejected` before the file goes.
   → **model: sonnet**.
2. 🟡 **does `entropy.md` sit in the right place, and should its name be uppercase?** Lucas, INBOX
   2026-08-15. It is the one always-present report at the workspace root that is not on the type
   allowlist, so the question is real rather than cosmetic. The evidence points at *lowercase, stays
   put*: § The four disposal routes sends a **generated** file to a lowercase instance name (the
   `LABELS` → `labels.md` precedent), and this file is written by
   `core/hooks/entropy/entropy-dashboard.py` and committed by `core/tools/wos/roundup`, never
   authored. What is genuinely open is whether the root is its place — every other generated
   artifact lives beside its generator or under `outputs/`, and `outputs/` is untracked while this
   one must be tracked to serve as the criterion-1 ratchet. Decide once and write the answer into
   `core/SCHEMA.md` so it stops looking like an oversight.
   → **model: opus** — one ruling, then at most a `git mv`.
3. 🟢 **the transient initiative doc is `ROADMAP-<slug>.md` — ruled 2026-08-14, three renames left.**
   The "fourth type" turned out not to be a type. Lucas's ruling was to unify by semantic symmetry
   with zero conceptual intersection, and *"make sure as well that we do not create a new .md file
   for each specific minor thing"* — and once asked that way the answer falls out of the type table:
   a rollout is *intent, plan, and what we rejected*, scoped to one initiative, which is the ROADMAP
   question exactly. It never needed a name, it needed a **scope suffix**, and `AGENTS.md` already
   sanctions `ROADMAP-<slug>.md`. **Five differently-named files were the symptom of a missing
   suffix, not of a missing type.** The law is rewritten in
   [`core/SCHEMA.md`](core/SCHEMA.md) § *The one exception*, membership is closed at four, and
   `test_type_gate.py` now asserts the exempt set by equality so a fifth name cannot appear quietly.

   **Done:** the skill-suite migration report under `core/` is deleted — it opened with *"What was
   done (2026-07-05)"*, an annotated corpse of a finished migration. Lucas called it *"very shady…
   do we really need that one?"* and he was right. Its one durable paragraph (the convention for
   skill `refs/` folders, plus the suite-folder rule) moved to `core/SCHEMA.md` § Layer: skill.

   **Left, and both are nested-repo commits this repo cannot make:**
   `code/isoroll-module/REFACTOR.md` → `ROADMAP-refactor.md`, and `code/dobra/DECISIONS.md`, which
   is not a roadmap at all — decisions are *what must be true and why*, so it folds into that
   project's `SPECS.md`.

   **Sweep the file's own content, not just the references to it.** A file that was gitignored has
   been exempt from every check the workspace runs, so a rename of one is a first import, not a
   move — expect it to arrive carrying tokens the rest of the corpus retired months ago.
   → **model: sonnet**, one file per commit.

---

## Front 14 — ablation: nothing in this workspace has ever been measured

> **The paper twin is [`academy/papers/wos-ablation/`](academy/papers/wos-ablation/CONTEXT.md)**
> (2026-08-16). Lucas: *"o WOS pode virar um artigo. o estudo de ablação, se bem feito, me parece
> bem publicável."* The ablation and the paper are one artifact, so the experimental design lives
> there and this front holds only the build work it depends on.

1. 🟡 **build the instrument, then run the ablation.** Lucas, INBOX 2026-08-15: *"um engenheiro
   líder da Anthropic sugeriu de tempos em tempos a gente 'deletar' o CLAUDE.md e ver como modelos
   top (como o Opus) performam, dizendo que poderíamos nos surpreender. ou seja, diminuir a carga de
   instruções. esta recomendação é bem forte pro nosso caso. tudo que o WOS faz (ou pelo menos boa
   parte) é contornar ingenuidades do modelo. realmente precisamos fazer um benchmark com estudos de
   ablação em breve."*

   **The premise is falsifiable and nobody has tried to falsify it.** This workspace exists to
   compensate for model failures; a stronger model may not need the compensation, and every rule
   that outlives its failure is pure cost. The claim cuts at the whole scaffold, not just the docs.

   **Precondition, and it is the reason the last attempt produced nothing.**
   [`core/ROADMAP.md`](core/ROADMAP.md) § ablation-bench ran once and yielded no signal for exactly
   one reason: there was no clean way to turn a single feature off. So the toggle registry in
   Front 10.4 is not a sibling of this item, it is its instrument — *"it also would ease ablation
   tests so we can indeed see the impacts of each option"* (Lucas, 2026-08-14). Building the bench
   before the switch repeats the failure.

   **Named for measurement by Lucas (INBOX 2026-08-16), and the list is the scope:** *"incluir na
   nossa medição do estudo de ablação as funcionalidades da fachada, das interfaces, do limite de
   LOC, limite de arquivos, enfim, fazer o planejamento desse estudo com bastante calma."* Facade
   discipline, interface-first reads, the 150/200-line cap and the 7/10-file fanout cap — the four
   restraint gates nobody has ever measured, each of which shapes how every file in this workspace
   is written. *"com bastante calma"* is a constraint on the study, not a mood: these are the
   workspace's most load-bearing rules, so a weak design produces a number that gets quoted forever.

   Scope is the whole enforcement layer, not the `.md` corpus: hooks, skills, tools, `AGENTS.md`
   itself. The corpus drain is downstream — its verdicts are judgement calls today precisely because this
   instrument does not exist, and it says so rather than implying they are measured.
   → **model: opus** for the design, sonnet to run it.

---

## Front 15 — the agent is confidently wrong, and nothing catches it

Lucas, INBOX 2026-08-16: *"vi um comentário sobre o OPUS ter MUITA SEGURANÇA sobre pontos que na
verdade ele estava errado… eu gostaria que todas as opiniões técnicas da IA fossem tomadas com base
em pesquisas."* His two proposals: a **knowledge base** — a curated store, cheap to look up, refreshed
when a stored fact is old enough to have moved — and an **instruction**: *"YOU DON'T KNOW THINGS,
don't feel too certain, search before giving precise technical opinions."*

**This workspace has the case study, and it is not hypothetical.** Front 9 was steered for three
weeks by a confident, re-runnable, wrong number. The instrument agreed with the script it replaced,
which read as confirmation and was not, because both shared one misunderstanding. Before that, four
consecutive explanations of the rtk hook were asserted and retracted. In neither case was the agent
short of information; it was short of the habit of checking.

**What that case study says about the two proposals, and it cuts against the easy one.** The
instruction is the cheap half and is the half already tried: the workspace is thick with
*re-run it, never quote it* prose, and it did not prevent either failure. Prose asking for doubt is
INDUCED, and this repo's whole bet is that INDUCED loses to ENFORCED. So the front's real question
is **what a confidence check looks like as a gate**, not as a paragraph.

Three sub-questions, in the order they can be answered:

1. 🔴 **What is the store, and what earns a row?** The wikilinked memory store
   ([`brain/memory/`](brain/memory/CONTEXT.md)) and `core/refs/REFS.md` already exist and already
   hold curated facts — a third store is the failure
   this workspace names EDIT > CREATE. Establish first whether the graph Lucas wants is a **new
   structure** or a **query layer and a freshness field** over what is there. → **model: opus**,
   with Lucas.
2. 🟡 **What makes a stored fact go stale?** A hash-addressed store is only as good as its refresh
   rule; a confidently-served 2026-07 fact is the same failure with extra steps. Every fact needs a
   measured-on date and a claim about how fast its subject moves — harness behaviour ages in weeks,
   a published result in years. → **model: sonnet**.
3. 🟡 **Where can doubt be enforced rather than requested?** The one mechanism proven here is the
   experiments ledger: a number is not quotable until it has a runnable Method
   ([`core/experiments/SPECS.md`](core/experiments/SPECS.md)), and its new corollary — *a new
   instrument owes one hand-check against raw data before anything is quoted from it*. Extending
   that discipline beyond numbers to technical claims is the concrete, non-prose version of what
   Lucas asked for. → **model: opus**.

**Do not open this with a prompt rule.** That is the cheapest-looking move and the one the evidence
above already rejects.

## Silent failure is the failure mode this workspace actually has

The rule this cost six bugs to learn is [`core/SPECS.md`](core/SPECS.md) § Conventions: **a check
that proves something *happened* beats one that proves it did not error.**

Open, and per-repo drain work rather than a wos item: the `.d.ts` half of the stub gap — 203
files, all in nested repos, now counted in [`entropy.md`](entropy.md) under the criterion-1
baseline rule.

## Front 16 — post-v1, and the ledger is open again on purpose

**Ruled 2026-08-16 (Lucas), after all four v1 criteria went green.** The governing constraint
(*"quero zerar o roadmap do WOS o quanto antes"*) was a filter for reaching v1, not a permanent ban:
asked where three real ideas should land, he chose to **reopen this ledger** rather than push them
into `core/ROADMAP.md` or leave them in the INBOX. So v1 is a milestone, not a stopping point —
**but the filter that got us here still applies to what enters**: an item another repo owns is
refiled there, and a finding worth keeping goes into the `SPECS.md` section that owns the rule.

1. 🟡 **adversarial review as a standard, possibly enforced.** Lucas, INBOX 2026-08-16: *"have
   adversarials as our standards, maybe enforced… e.g., a plan that doesn't have any adversarial
   steps is rejected"*. The natural home is the craft flow's plan step
   ([`core/flows/craft/`](core/flows/craft/CONTEXT.md)), which already has a plan-review stage — so
   the question is whether that stage becomes a *requirement with a shape a check can see*, the way
   the citation gate matches `Frente <n>` rather than a word.

   **Design against the failure the source itself names**: the practitioner who proposed this says
   the technique *"can be a death loop"*. A gate that demands an adversarial step, on a plan whose
   adversary always finds something, is a loop with no exit. Whatever ships needs a termination
   rule before it needs a check. Refs and the two unread method docs: `core/refs/REFS.md`
   § Adversarial review as a standard.
   → **model: opus** for the shape, sonnet to wire it.
2. 🟡 **measure which `UPPERCASE.md` files are actually read, and what they cost.** Lucas, INBOX
   2026-08-16: *"sinto que arquivos de objetivos (goals) são pouco usados. roadmaps são muito
   usados. gostaria de primeiro ter esse monitoramento de forma automática (zero-token) de quais
   arquivos UPPERCASE.md são lidos e com que frequência (e se possível o custo em tokens de leitura
   deles). tudo isso monitorado no tempo."*

   **Ordering is explicit and it is the whole point: measure first, then act.** He suspects goal
   files are dead weight; this measures it instead of assuming it. The instrument is close to
   existing — [`core/tools/wos/session/context`](core/tools/wos/session/context) already attributes
   context growth per file from the transcripts, so this is mostly a longitudinal store plus a
   per-type rollup, not a new measurement. Results belong in
   [`core/experiments/`](core/experiments/CONTEXT.md), never in this file.
   → **model: sonnet**.
3. 🟡 **then reinforce the goal↔roadmap link, possibly enforced.** Same capture, and deliberately
   second: *"depois gostaria de reforçar a conexão entre os goals e os roadmaps, não sei se tem
   como, talvez até algo ENFORCED"*. Every goal file already carries an `>**owns**` block and every
   plan is supposed to live in a `ROADMAP.md`; what is missing is anything asserting the two agree.
   **Do not design this before item 2 reports** — if goal files turn out to be read rarely, the fix
   is not a stronger link to them.
   → **model: sonnet**.
4. 🟡 **evaluate `obra/Superpowers` against our own craft flow.** Lucas, INBOX 2026-08-16: *"será
   que eu deveria usar o superpowers?"* It is the same shape as `/craft` — spec from an interview,
   plan written for a junior engineer, subagent-driven TDD — and it installs across 14 harnesses,
   so it is provider-agnostic the way we are. **The question is not whether it is good, it is
   whether it is better than the flow we already run**, and the answer has to name what it does
   that `core/flows/craft/` does not. A real outcome here is deleting our own flow.
   → **model: opus** — this is a judgement about our own work.
## Parked — explicitly out of v1

- **`[gdrive-integration]` / `[courses-import]`** — content migration, large. Per-folder work lives in
  `brain/TODO.md`.
- **`[offline-resilience]`** — the gaps are (a) network: [Reticulum](https://github.com/markqvist/Reticulum),
  E2E without infrastructure, and (b) an offline corpus: **Kiwix** (all of Wikipedia offline — almost
  certainly the "NOMAD project" Lucas half-remembered). Refs in `core/refs/REFS.md`.
- **Serious OCR** — real need (image-only PDFs in `branches/ecovila/burocracia/` where
  `core/tools/paper/parse` returns empty; test Baidu "Unlimited OCR" first), but it belongs where the PDFs
  are, not in the wos ledger.

## Rejected — killed 2026-07-30, one line each

Kept only so a dead idea does not resurface looking new. Accepted price: some will resurface in
months anyway. Cheaper than a list nobody reads.

- **INBOX provenance probe** — Front 1 shipped; the probe measures a threat model already ruled inert.
- **SLM confirmation run** — depends on `dobra` maturity that does not exist; the preprint stays provisional, which is fine.
- **Tier 1 periodic cheap-agent detectors** (gold tasks, scheduled `/dedup`, misplacement audit) — paid detection of what Tier 0 catches free.
- **Tier 2 `/tidy` skill** — a new skill to do what a human can do directly from the dashboard; scatter.
- **High-coupling / import-graph detection** — no evidence coupling is hurting anything.
- **Anti-entropy prior-art research lead** — a reading list, not work.
- **Anti-collapse edit gate** — self-declared optional, touches the edit path, guards a failure never observed here.
- **`/inbox` offers `/compass` on a trigger** — speculative UX on the one path whose whole virtue is being cheap.
- **`>routing` tier·effort metadata on goal files** — metadata for a router that reads fine without it.
- **Model-routing strategy doc** — the routing that pays is already in the per-step model tags and `/prepare`.
- **Benchmark craft flow vs SOTA repos** — expensive comparison against repos with different cost priorities.
- **Triggers after a limit window renews** — infrastructure to wake a dead session; `ScheduleWakeup` covers the live case.
- **`[task-metric]` closed-vs-created instrument** — measuring the ledger is more ledger; the honest signal is Lucas saying he feels lost, and he does say it.
- **Retroactive ref→task pairing** — the policy holds going forward; old unpaired refs can rot.
- **Scaffold update log** (`core/SCAFFOLD-LOG.md`) — the paper thread; git plus this file already carry trigger→change. Revisit only if a paper is actually written.
- **Downloads unification across devices** — cross-device config, life logistics, not scaffold.
- **Dated `GOALS.md` attention re-check** — a calendar reminder for 2026-08-06, not a ledger row. Verified *not* a live bug; the 14-day window washes the old history out on its own.
- **opencode + copilot parity** — aiwbot's own premise; lives in `code/aiwbot/ROADMAP.md`.
- **Nested-repo git graph in VSCode** — IDE trivia.
- **Google Slides API + slide templates** — content tooling.
- **Mobile INBOX Android app** — aiwbot is already the away-from-PC front door.
- **`brain` coverage sweep** (`[brain-full-files]`, `[branches-coverage]`) — content completeness, not scaffold.
- **English-learning mode** — was disabled once already; weak signal.
- **aiwbot as away-from-PC front door** — a pointer to another ROADMAP is a duplicate by definition.
- **Extract the "10 GitHub repos that replace paid tools" list** — a listicle.
- **Evaluate Surfsense** — our `core/tools/web/{search,fetch}` + `core/tools/paper/{papers,parse}` + research flow already cover it.
- **Research-flow hallucination audit** — real but unforced; no observed fabrication.
- **`pre-edit.py` vs `check-line-counts.sh` scope disagreement** — policy nit, no live symptom.
- **`core/tools/paper/papers --ss` live smoke** — it will smoke itself on the next real use.
- **Commit the `.claude/commands/{drive,calendar}.md` symlinks** — done inline rather than tracked.
- **`/caveman compress` on workspace docs** — piloted on the worst offender: 8571 → 8552 chars, **0.22%**, for one full quota call. The docs have no lexical fat, so placement beats phrasing and compression stays the last step on an already-reduced surface (core/SCHEMA.md § Placement).
- **A media-host allowlist for INBOX link extraction** — deciding which links the video tool runs from a list of known hosts (instagram/youtube/tiktok/…) is faster, and the list rots into exactly the silent skip the batch fix exists to kill. Every link is attempted; one with no media falls back to `core/tools/web/fetch`.
- **A `Write`-over-an-open-path gate** — its case was cost, and the cost is ~1% of spend once the re-read multiplier was corrected from 5.8x to 1.9x. The heredoc half shipped, on the governance grounds it never lost.
- **Lowering `effort` to shorten output** — rejected as a *length* lever (it does not reliably move visible output) and that still holds. It is **not** rejected as a cost lever; that is Front 9.9.
- **A global terseness rule** — a wrong token budget degrades the answer (ACL Findings 2025).
- **LLMLingua-style prompt compression** — it compresses a request before sending, and the harness owns our request.
- **A "match deliverable length to the task" rule in `AGENTS.md`** — `Write` arguments are 25.3% of *logged* output, which is 35% of billed output, which is 12.9% of spend: **~1% of the bill**, bought with one more always-loaded paragraph asking for restraint. INDUCED loses to ENFORCED, and this front already paid to learn it.
- **The "delete verification scaffolding" prompt sweep** — audited 2026-08-17 and the corpus is already clean: every `verify`/`confirm` in `AGENTS.md`, `core/skills/` and `core/agents/` names a specific probe (`install.md`'s Verify step, `lead.md`'s file-exists check), not the generic self-checking Opus 5 over-runs on.
- **The ~8% unexplained spend gap between `usage` and the one-off script** — the premise is void. Both summed transcript records instead of API responses, so they agreed on shares while being 1.97x wrong together, and the agreement is what stopped anyone looking. Absolute spend is list price and has never been checked against a bill; that is the only caveat left.

## Sequencing

**All four v1 criteria are met.** Everything left is past v1, so the governing constraint in
[`brain/goals/workspace-os.md`](brain/goals/workspace-os.md) applies at full force: an item that does
not earn its keep is a candidate for *Rejected*, not the backlog.

The one ordered chain, because each step is the next one's precondition:

1. **wire the registry's findings** — one feature per commit, `feature_law.is_enabled()` where the
   rule is enforced, then name that file in the `wired` column. The count lives in
   `core/tools/wos/features --findings`, never here.
   **Cheapest-first is the right order only among features the ablation does not name**: ordering by
   files-touched maximises rows closed per hour and leaves the study with nothing to measure.
   `rtk-compaction` is the row that ordering would bury, and `core/tools/deps.txt` already prices its
   absence at 60-90% of a session.
2. **10.5** — the public scaffold repo at `code/wos/` and its one-way sync.
3. **14.1** — the ablation, against whatever is switchable by then.

Everything else is unordered and mechanical: **4.2**, **4.6**, **8.3**, **12.1**.

**Needing Lucas: the list is in § How to read this and only there.** It used to be restated here and
the two copies named different threes, each missing a different item, both claiming three. **Two
lists of the same set is the asymmetry; the count is only its symptom.**

## Model-switching guide

The canonical guide lives in the flow that produced this plan:
**[`core/flows/research/scout.md`](core/flows/research/scout.md) → "Canonical model-switching guide"**
(same-session `/model` · `/craft` autorouting · Agent-tool `model:` override · `/handoff`).
Mapping: 🔴 → **Opus, same session**; 🟢/🟡 → **Sonnet via `/craft`** (mechanical parts drop to haiku).
