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
| 3 | **Everything pushed, gitflow-shaped** — every `code/` repo on `main`/`feature/*`, zero unpushed, no repo without a remote | — | ✅ **MET 2026-08-14** — re-run, never trusted: one loop over `find . -name .git` asserting a remote and a legal branch per repo |
| 4 | **Clonable by a student** — fresh clone gets every capability; deps declared, no undocumented hand-installs | Front 10 | ✅ **MET 2026-08-16** — `SETUP.md` is an executed procedure, every dep declared in `core/tools/deps.txt`, both enforced by `verify-fast` |

Post-v1 validation is `[mvp-validate]`: use the system daily for 30 days, then assess whether it
reduced mental load. That is the real test and it can only run after v1.

## How to read this

Per-step `model` = the tier that is *enough* (a floor, not a ceiling).
🔴 needs Lucas · 🟡 pilot on one subtree first · 🟢 mechanical.

**Two open steps need Lucas's own judgment: 9.5, 15.1** — the single list, quoted here and
nowhere else. Everything else is agent work. Both are now *research-and-discussion* items rather
than questions with options attached, which is what he asked for on 2026-08-17 in both cases: a
capability nobody gave a fair trial, and a front too big to decide as a side question.
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

---

## Front 4 — workspace anti-entropy — **the keystone, v1 criterion 1**

> The real target: files grow, scatter, duplicate, and drift from naming/structure patterns.
> **Structure is a spec; drift is a test failure.** `code/` already has this (the `> spec:` gate);
> the agent library has [core/SCHEMA.md](core/SCHEMA.md). Nothing yet governs the shape of the
> workspace itself.

1. 🟡 **two projects declare `goal: none` while their goal file exists.** The project ⟺ goal link
   check blocks, and all 14 projects declare line 3 — but `gira` and `laplata` say `none` where
   `startapps-gira` / `startapps-laplata` sit on disk. So line 3 is *wrong*, not absent, which no
   check can catch: a content question, not a check failure.
   → **Lucas rules** whether those two projects really serve those goals; sonnet edits two lines.
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

6. 🟢 **sweep this repo's first-line-comment markers now that the gate is shut.** The hole is closed:
   `entropy_context.check_description` blocks at commit through the Tier 0 gate, ratcheted to what a
   commit adds, and asks the routing generator rather than a table of its own
   ([`core/hooks/SPECS.md`](core/hooks/SPECS.md) § First-line descriptions). What is left is the standing queue the ratchet deliberately does not
   charge anyone for. **Size it against [`entropy.md`](entropy.md), and re-run the generator before
   measuring** — every marker drained so far was a file the generator could already describe.
   **Scope here is this repo only**; the nested-repo majority is under § Blocked. → **model: sonnet**.

---

## Front 8 — The ledger discipline — **v1 criterion 2**

**Mass is the disease and only deletion cures it.** Collapsing four ledgers into one made this file
honest but not smaller — items went 158 → 123 while mass stayed flat, and Lucas reported feeling
lost twice more after it.

**And the cost of mass is now measured, not argued** (2026-08-17,
[`core/experiments/read-amplification.md`](core/experiments/read-amplification.md)): this file is the
single most re-read file in the workspace, **3.0 reads per session, 877k chars over 80 sessions** —
more than the whole `CONTEXT.md` chain costs per session, and the chain is what gets blamed. **A line
deleted here is not deleted once; it is deleted three times per session, forever.** That is the
answer to Lucas, INBOX 2026-08-17: *"I am not trusting Opus and WOS itself regarding the
size/entropy of the WOS, feeling maybe things are being scattered, entangled, an increasing
spaghetti. I wanted things to be very clear here. very concise, precise."* The instrument is
`core/tools/wos/session/reads`; re-run it rather than trusting this paragraph.

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
5. 🔴 **give flows and agents a deliberate trial, then judge them.** Lucas, same capture: *"um aluno
   comentou que existem formas diretas de o claudecode delegar pra subagentes… temos skills e isso
   me parece suficiente, mas talvez não seja."*

   The claim this item rested on — that nothing had ever been delegated — was an artifact of
   scanning the wrong directory. Corrected, with the hand-check, in
   [`core/experiments/delegation.md`](core/experiments/delegation.md): delegation happens, and **no
   workspace-authored agent has ever been spawned.**

   **Ruled 2026-08-17 (Lucas): do not delete on that.** *"low usage doesn't mean they don't have
   value… we did not work enough on these yet. IF we employ effort, do our best, and even then we do
   not use those, then it makes sense to delete."* Delete-weak-features assumes a fair trial and this
   layer never got one — reach was measured, worth was not. The work is **rounds of discussion and
   research**: what a flow is for, what an agent is for, whether a flow naming `agents:` in
   frontmatter is the right shape, and one deliberate run of each before anyone rules.
   → **model: opus**, with Lucas — several sittings, not one pass.
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
   **Studied 2026-08-17; the verdict is yours to take.** *Auto-close, not auto-continue* — and the
   study moved it further than expected: **every piece already exists and only the link is missing.**
   `session/context-meter.py` announces the crossings at zero token cost, and
   `core/tools/wos/roundup` is the close. What is unbuilt is `CTX_LOUD` **offering** the close.
   Two findings decide the shape:
   - **A quota limit ends the session; there is nothing to continue into.** Resuming means a *new*
     session, which is exactly roundup + fresh start. That is why *"triggers after a limit window
     renews"* already sits under § Rejected — the live case is covered.
   - **It must offer, never fire.** Closing a session mid-thought against the user's intent costs
     more than the expensive turns it saves, and the cost argument only holds at the top of the
     staircase. Re-run `session/usage` rather than trusting a number here.
   → **Lucas rules on offer-at-`CTX_LOUD`**; sonnet wires it.
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

---

## Front 10 — Portability & clonability — **v1 criterion 4**

> **Ruled 2026-08-16 (Lucas); every ruling is recorded where it is enforced, not here.** The harness
> is the installer and `SETUP.md` is the prose it executes — [`core/SCHEMA.md`](core/SCHEMA.md)
> § The `.md` type system. The registry's grouping, its columns, and the fact that `scope` **is** the
> general/Lucas-specific line (a column the sync reads, not a document) are declared in the header of
> [`core/features.txt`](core/features.txt) itself; the rule behind it is
> [`core/SPECS.md`](core/SPECS.md) § AD-14.

**Criterion 4 is met and the registry is live.** What remains is one mechanical backlog: a capability
whose `wired` column reads `-` cannot be switched off, so **the ablation cannot report on it**.
Wiring one is calling `feature_law.is_enabled()` where the rule is enforced and naming that file in
the column. Read the count from `core/tools/wos/features --findings`, never from here — and the
target is zero, because a row with no in-process switch now carries `n/a` and a reason rather than
sitting in the findings forever.

**The `skills` and `capabilities` groups are done, and doing them corrected the design**
([`core/SPECS.md`](core/SPECS.md) § AD-14). Skills share one wiring point in the mirror, because a
skill is markdown and the only real switch is the mirror declining to publish it. Capabilities were
filed alongside them and should not have been: a capability is a **CLI this workspace writes**, so it
has a moment of its own and guards at invocation, which buys a per-row behavioural answer instead of
one answer for the group. What is left is `hooks`, `context-tree` and `brain` — **one enforcement
file apiece, one call per row, mechanical**.

**One open finding, deliberately not cleaned up:** `codeburn` is an externally installed npm binary
with no wrapper of ours to guard. It is **not** quietly marked `n/a` — AD-14 closes that set at five,
and admitting a sixth is Lucas's ruling.

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

   **It runs OUTSIDE this workspace, and that is a correction, not a detail** (Lucas, 2026-08-17:
   *"the ablation test WILL NOT be done INSIDE the WOS. we can't do that. this will be an
   experiment!"*). A system cannot run the experiment on itself. The harness builds **variants** of
   a checkout — one feature off in each — and runs one task suite against all of them. The variants
   come from the **public repo** (his call), which has two consequences taken deliberately: the
   public scaffold is a **hard precondition** of this item, and the task suite must be **synthetic**,
   since that scaffold ships `brain/` as empty structure by design. Designing the suite is study
   work and belongs to the paper twin.

   **The other precondition is the reason the last attempt produced nothing.**
   [`core/ROADMAP.md`](core/ROADMAP.md) § ablation-bench ran once and yielded no signal for exactly
   one reason: there was no clean way to turn a single feature off. The toggle registry is not a
   sibling of this item, it is its instrument — *"it also would ease ablation tests so we can indeed
   see the impacts of each option"* (Lucas, 2026-08-14). Building the bench before the switch
   repeats the failure. Two ways a feature goes off, and the registry only knows the first:
   an in-process switch, or a variant built without it — [`core/SPECS.md`](core/SPECS.md) § AD-14.

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

1. 🔴 **What is the store, and what earns a row? — POSTPONED 2026-08-17, and the postponement is the
   ruling.** Asked to pick between a new structure and a query layer over what exists, Lucas declined
   the frame: *"are we talking about the knowledge graph? this is an entirely new front in my view…
   there are some conceptual collisions, redundancies and ambiguities we must solve. also, building
   it is not simple… we have to be extra careful on this design."* It opens with research and a
   design sitting of its own, or it does not open.

   Inherited, so the next session starts warm: the two live stores are
   [`brain/memory/`](brain/memory/CONTEXT.md) (26 files, wikilinked, in every system prompt) and
   `core/refs/REFS.md` (209 lines, tier-marked, and absent from the most-re-read list — nobody reads
   it). A third store is the failure named EDIT > CREATE, so resolving the collisions is the first
   work item, not a caveat.
   → **model: opus**, with Lucas, in a session about this and nothing else.
**Do not open this with a prompt rule.** That is the cheapest-looking move and the one the evidence
above already rejects.

## Silent failure is the failure mode this workspace actually has

The rule this cost six bugs to learn is [`core/SPECS.md`](core/SPECS.md) § Conventions: **a check
that proves something *happened* beats one that proves it did not error.**

## Front 16 — post-v1, and the ledger is open again on purpose

**Ruled 2026-08-16 (Lucas), after all four v1 criteria went green.** The governing constraint
(*"quero zerar o roadmap do WOS o quanto antes"*) was a filter for reaching v1, not a permanent ban:
asked where three real ideas should land, he chose to **reopen this ledger** rather than push them
into `core/ROADMAP.md` or leave them in the INBOX. So v1 is a milestone, not a stopping point —
**but the filter that got us here still applies to what enters**: an item another repo owns is
refiled there, and a finding worth keeping goes into the `SPECS.md` section that owns the rule.

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

## Declared but unbuilt — a rule with a `SPECS.md` section and no implementation

Five checks were relocated out of this ledger on 2026-08-17, into the `SPECS.md` sections that
declare them. **The relocation was right and the accounting was not.** A rule belongs beside the
thing it governs, so the sections stay — but a `SPECS.md` states what must be true and cannot say
whether anything enforces it yet, so the *build* was left with no home and the item count flattered
the work state. **The declaring section is the spec; the row here is the work.** Each row is deleted
the day its check runs; this section is deleted when the last one does.

1. 🟢 **the finished-work prose gate.** `entropy/entropy_ledger.py` already carries the detector and
   the dashboard counts it, but `checks/type-gate.py` imports only `goal_vocabulary` and
   `wiki_link_hits`, so the finished-work half **reports and never blocks**. One import plus one
   call, **ratcheted to what a commit adds** like every other Tier 0 check — the standing queue is
   non-trivial and a gate that fails on the day it lands trains people to ignore it.
   Declared: [`core/hooks/SPECS.md`](core/hooks/SPECS.md) § The next gate. → **model: sonnet**.
2. 🟢 **the `core/experiments/` and `REFS.md` discipline checks.** The two rules this workspace cites
   as proof it knows how to doubt — a runnable `## Method`, dated `Results`, `Limitations` never
   omitted; and `REFS.md`'s `[A]`/`[B]`/`[P]`/`[V]`/`[C]` tier markers — and **neither is verified by
   anything.** Both stores are small and closed, which is what makes them the obvious next Tier 0.
   Declared: [`core/SPECS.md`](core/SPECS.md) § AD-16 band 1. → **model: sonnet**.
3. 🟢 **the loop-cap check: a step that declares a loop must declare its cap.** Greppable,
   deterministic, zero-token, and true of every flow rather than of one technique. It is the inverse
   of the shape under § Rejected — requiring the adversarial step creates the death loop, requiring
   the bound is what makes requiring the step safe.
   Declared: [`core/flows/craft/SPECS.md`](core/flows/craft/SPECS.md). → **model: sonnet**.
4. 🟢 **roundup compares the declared model split against the actual one.** `core/tools/wos/roundup`
   already prints the per-session split at every close; what is missing is the plan **declaring its
   expected split** and roundup comparing. It forces nobody to delegate — it makes deviation visible
   and dated instead of invisible, and needs no new instrument.
   Declared: [`core/SPECS.md`](core/SPECS.md) § AD-17. → **model: sonnet**.
5. 🟢 **import the auto-trigger.** `/craft` must be typed, which is the missing half of AD-17: the
   assignment is carried at plan time and no executor reads it outside the flow. The mechanism
   imports without the methodology — the rest of that repo stays under § Rejected.
   Declared: [`core/flows/craft/SPECS.md`](core/flows/craft/SPECS.md) § Judged against Superpowers.
   → **model: sonnet**.

**The generalising fix, flagged and deliberately not taken:** a Tier 0 check asserting that every
check named in a `SPECS.md` § has an implementing file. It would enforce exactly the drift that
produced this section — and it costs one more row, so it is Lucas's call rather than a decision made
in passing while cleaning up.

## Blocked — waiting on a trigger

Open work this repo cannot advance today, either because another checkout owns the commit or because
the thing that would justify it has not happened. **Each line names the event that reopens it**, so
nothing here is measured against progress and § Open stays a true count of what is drainable now.
A row moves back up the moment its trigger fires. A row whose trigger never fires is a candidate for
§ Rejected, not a permanent resident — this section is not a second parking lot.

- **Flip fanout to a hard block** (Lucas 2026-07-31: hard block, no grandfathering). Coherent only at
  zero: the pre-commit hook is global (`core.hooksPath`), so switching it on while a nested repo is
  over the cap fails every commit in that repo, **including the commits that would fix it**. This
  repo, `code/aiwbot` and `code/flows` are drained; `apptime` and `spacemantics` carry their own
  items on `feature/workspace-drift-refile`. What the draining taught is
  [`code/SPECS.md`](code/SPECS.md) § Splitting an over-full directory — five rules, each of which
  cost a session to find.
  → **trigger: the parallel isoroll session refiles its own drift.** `isoroll-content/src/pipeline`
  and `isoroll-module/src/render` and their siblings, plus the one file over `BLOCK_LINES`; writing
  into those checkouts from here is the mid-flight collision the git-integrity criterion exists to
  prevent. Then: add fanout to `core/hooks/checks/` beside the type gate and delete `BASELINE` from
  `test_entropy_fanout.py` in the same commit. → **model: sonnet**, one repo at a time.

- **The nested-repo majority of the first-line-comment queue.** Sized against
  [`entropy.md`](entropy.md), after re-running the generator — every marker drained so far was a file
  the generator could already describe.
  → **trigger: a session in each nested repo.** This repo's half stays in Front 4.

- **A second compaction shim, for copilot.** `core/hooks/compact/bash-compact-rewrite.py` hardcodes
  `rtk hook claude` in two places, so only one vendor gets multi-line splitting;
  `.github/hooks/rtk-rewrite.json` runs `rtk hook copilot` raw and keeps the first-line-only behavior
  the shim exists to fix. An instruction does not substitute: copilot carries one (*"Always prefix
  shell commands with `rtk`"*), but an instruction is INDUCED and cannot split a multi-line command,
  which is the exact behavior the shim exists to fix.
  → **trigger: a copilot session actually runs in this workspace.** Measured 2026-08-17 — every
  tracked Bash call to date is Claude and no copilot session has ever run here, so a second shim
  today is built for zero users. Re-run the counter, never quote it.
  Two things this does not gate: the rewrite rate is **unexplained** (whether the unrewritten half is
  commands not worth rewriting or a silent gap is not measured), and the upstream report to
  `rtk-ai/rtk` is outward-facing and **stays Lucas's to send**, never sent unilaterally.

- **The last two `ROADMAP-<slug>` renames.** `code/isoroll-module/REFACTOR.md` →
  `ROADMAP-refactor.md`, and `code/dobra/DECISIONS.md`, which is not a roadmap at all — decisions are
  *what must be true and why*, so it folds into that project's `SPECS.md`. **Sweep the file's own
  content, not just the references to it**: a gitignored file has been exempt from every check the
  workspace runs, so renaming one is a first import, not a move, and it arrives carrying tokens the
  corpus retired months ago.
  → **trigger: a session in `isoroll-module` / `dobra`.** Both are commits this repo cannot make.
  → **model: sonnet**, one file per commit.

- **The `.d.ts` half of the stub gap** — 203 files, all in nested repos, counted in
  [`entropy.md`](entropy.md) under the criterion-1 baseline rule.
  → **trigger: a session in each nested repo.**

- **What makes a stored fact go stale.** A hash-addressed store is only as good as its refresh rule;
  a confidently-served 2026-07 fact is the same failure with extra steps. Every fact needs a
  measured-on date and a claim about how fast its subject moves — harness behaviour ages in weeks, a
  published result in years.
  → **trigger: the knowledge-store sitting in Front 15 opening.** A refresh rule needs a store to
  refresh. → **model: sonnet**, then.

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

- **Adopting `obra/Superpowers` in place of our craft flow** — same arc, but its uniform subagent dispatch has no per-task tier/effort routing and no file-relayed Carry, the two mechanisms built for quota rather than developer time. Its *trigger* is imported instead (`core/flows/craft/SPECS.md`).
- **Gating on the presence of an adversarial step** — the originally proposed shape; an adversary always finds something, so the gate is a loop with no exit. What is gated is the **bound** (exit condition + numeric cap), which is what makes requiring the step safe.
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

**The plan is four tracks, named rather than numbered.** An item number is a moving target under a
delete-on-completion policy, and this section is where the two-lists asymmetry has bitten twice — so
it points at work by name and at people by mark, never by number.

**Track A — wire the registry to zero.** One feature per commit: call `feature_law.is_enabled()`
where the rule is enforced, then name that file in the `wired` column. **`hooks`, `context-tree` and
`brain` are one call site apiece**, mechanical. **`capabilities` needs a group seam first** — the
shape to copy is `core/tools/wos/skills/mirror.sh`, which is what lets the whole skills group share
one wiring point instead of paying a call site per row.
Read the count from `core/tools/wos/features --findings`, never from here; its target is zero, and
`n/a` rows are excluded because a switch cannot exist for them, never because wiring one is work.
Per [`core/SPECS.md`](core/SPECS.md) § AD-14: honesty is a **behavioural probe**, not a grep — and a
capability living in several files stores them all and names the primary, or the ablation measures
something nobody removed whole.
**Cheapest-first is safe now, and was not before.** Ordering by files-touched used to bury the rows
the study names; all four gates Lucas named for measurement, plus `rtk-compaction`, are already
wired, so nothing high-signal is left for that ordering to hide. → **model: sonnet**.

**Track B — the one hard chain, because each step is the next one's precondition.**
1. The **public scaffold repo** at `code/wos/` and its one-way sync. It stopped being a neighbour of
   the ablation on 2026-08-17 and became its **hard precondition**: the experiment runs on variants
   built from the public repo, so no public repo means no arms to compare. Students needing a
   research-branch workspace makes it demand as well as precondition.
2. The **ablation**, against whatever is switchable by then. Design is opus and belongs to the paper
   twin; the run is sonnet.

**Track C — unordered and mechanical, all sonnet.** Everything under § Declared but unbuilt, plus the
open rows in Fronts 3, 4, 8, 9 and 16 and the declaration-table rename to `.tsv`
([`core/SCHEMA.md`](core/SCHEMA.md) § The `.md` type system). Two of these are waiting on one word
from Lucas rather than on work: whether `CTX_LOUD` should **offer** the session close, and whether
frozen run records are exempt from the state-dir rename.

**Track D — the sittings.** The 🔴 rows, plus the thinking-effort measurement, which additionally
needs Track A finished because it runs on the registry.

**Needing Lucas: the list is in § How to read this and only there.** It used to be restated here and
the two copies named different threes, each missing a different item, both claiming three. **Two
lists of the same set is the asymmetry; the count is only its symptom.**

## Model-switching guide

The canonical guide lives in the flow that produced this plan:
**[`core/flows/research/scout.md`](core/flows/research/scout.md) → "Canonical model-switching guide"**
(same-session `/model` · `/craft` autorouting · Agent-tool `model:` override · `/handoff`).
Mapping: 🔴 → **Opus, same session**; 🟢/🟡 → **Sonnet via `/craft`** (mechanical parts drop to haiku).
