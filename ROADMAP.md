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
| 4 | **Clonable by a student** — fresh clone gets every feature; deps declared, no undocumented hand-installs | Front 10 | ✅ **MET 2026-08-16** — `SETUP.md` is an executed procedure, every dep declared in `core/tools/deps.txt`, both enforced by `verify-fast` |

Post-v1 validation is `[mvp-validate]`: use the system daily for 30 days, then assess whether it
reduced mental load. That is the real test and it can only run after v1.

## How to read this

Per-step `tier` = the tier that is *enough* (a floor, not a ceiling). **Which concrete model
fills a tier is data and lives in [`core/flows/craft/routing.md`](core/flows/craft/routing.md),
never here** — a ledger that names a vendor's model goes stale the day that model does.
🔴 needs Lucas · 🟡 pilot on one subtree first · 🟢 mechanical.

**Twelve open steps need Lucas's own judgment: 4.11, 4.12, 4.13, 9.5, 10.6, 12.2, 15.1, 15.2, 15.3,
17.1, 18.1, 18.5** — the single list, quoted here and nowhere else. Everything else is agent work, and all nine are
*research-and-discussion* items rather than questions with options attached, which is what he has
asked for in every case.

**It went 5 → 9 → 12 on 2026-08-18, and the jump is the point rather than a backlog failure.** Lucas:
*"sometimes the WOS is growing with decisions I didn't recall making… I want to understand those
better and aid on the decision process."* Four items moved to 🔴 that morning because he asked to be
in them, not because they got harder. **18.1 had its opening sitting on 2026-08-18** — ruled a
standing front with three real halves — and is now the *deep* sitting it revealed, which may still
reshape what the other eight look like. It stays first and stays 🔴. **The two added that evening came out of the first
thing 18.3 built:** seeing `ARCHITECTURE.html` raised *which sectors get one* (18.5) and, with it,
whether `entropy.md` should scatter per repo the same way (4.13) — one artifact, two questions about
where an instrument belongs, both Lucas's to answer. **15.3 was routed out of the INBOX the same
evening**, on his ruling that confirmation bias in a plan is this front seen from the decision side.
Stating that number is part of the cure for feeling lost, so **keep it true** — it has been wrong
four times: once claiming one while five were live; once (2026-08-16) carrying four items marked 🔴
whose own `→ tier:` line said medium; once holding *two* lists of the same set, here and in
§ Sequencing, which named different threes and so were both wrong; and once (2026-08-17) still
saying *two* on the day Front 17 opened as the third — the count went stale the moment the front
that exists to catch stale self-description was added. **Derive it from the 🔴 marks.**
**This is the only list; § Sequencing points here rather than restating it.** Two lists of the same
set is the asymmetry, and the count is only ever its symptom, so the cure is one list rather than
two kept in sync. **🔴 means Lucas decides, not "this is hard"**; an item a high-tier agent can
rule on alone is 🟡. Re-derive the count from the marks before quoting it.

The whole Front 10 chain came off this list on 2026-08-16 — six 🔴 items closed in one sitting,
because they were one decision wearing six numbers and none of them could be taken alone. It is back
with one (10.6), and that is the shape to expect: draining a front to the bottom is what surfaces the
row whose blocker was never the work.

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
   → **tier: medium**.

---

## Front 4 — workspace anti-entropy — **the keystone, v1 criterion 1**

> The real target: files grow, scatter, duplicate, and drift from naming/structure patterns.
> **Structure is a spec; drift is a test failure.** `code/` already has this (the `> spec:` gate);
> the agent library has [core/SCHEMA.md](core/SCHEMA.md). Nothing yet governs the shape of the
> workspace itself.

1. 🟡 **entropy is reported "flat" every session and has roughly quadrupled in four days.** Lucas
   (INBOX 2026-08-17): *"sessions keep saying entropy is flat but on the last week it went from 270
   I think up to more than 400."* He is right and the real curve is steeper than his memory of it —
   re-derived from the file's own history, one command, which is the point:

   ```bash
   for c in $(git log --format=%h --since="12 days ago" -- entropy.md); do
     printf '%s  ' "$(git log -1 --format=%ad --date=short $c)"
     git show $c:entropy.md | grep -m1 -oE '[0-9]+ findings'
   done | sort -u
   ```

   `~94` (08-13) → `297` (08-14) → `402`…`435` (08-15) → `440` (08-17). **Every session compared
   itself only to the session before it, where the delta really is ±1, and wrote "flat" into the
   hand-off** — which the next session then inherited as fact. A true statement at one time scale,
   false at the one that matters, repeated because nothing re-checks the baseline. Front 17's shape
   with a number attached, and the cheapest possible fix: the dashboard should print a **trend
   against a dated baseline**, not a bare count, so "flat" becomes unwriteable when it is false.

   **Do not treat the 94 → 297 jump as rot until it is checked** — it lands on the day the scan
   went `nested=True` and new checks were added, so part of that step is almost certainly scope, not
   drift. Separating the two is the first task, and the answer decides whether this is a reporting
   bug or a real cleanup. → **tier: medium**.

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
   sit inside frozen `.loop/` run records.
   **Ruled 2026-08-17 (Lucas): rename everything, no exemption.** The case for exempting them was
   that a chain file records what was *run* that day, so rewriting it makes the record lie. Overruled
   — one token, one meaning, and a carve-out for run artifacts is a second rule to remember at every
   future rename. Git holds what the file said before.
   → **tier: medium**.
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
   **Scope here is this repo only**; the nested-repo majority is under § Blocked. → **tier: medium**.
7. 🟢 **the bash context gate reads paths out of a commit message body.** Lucas (INBOX 2026-08-17)
   and **reproduced twice in this session**: a heredoc `git commit -F -` whose *message* names
   `core/tools/web/fetch` is treated as a command touching that subtree, so the gate demands the
   CONTEXT.md before letting the commit through. The gate should read the command, not the text the
   command carries. `core/hooks/read/bash-context-gate.py`. → **tier: medium**.
8. 🟡 **`core/SPECS.md` crossed the size signal and mixes seven concerns.** Lucas (INBOX
   2026-08-17), at 451 lines and 17 ADs; it is past 470 now. It holds tools, auth, flows, features,
   always-loaded prose, doubt and delegation. **Decide the split axis before cutting** — that is why
   it was not split mid-session, and the reason still stands: a split made in passing scatters
   instead of organising. → **tier: medium**, axis first.
9. 🟢 **the corpus is half Portuguese and the rule is English.** Lucas (INBOX 2026-08-17): *"somente
   o meu texto é em português, as conversas nas sessões, mas o resto, os docs, tudo em inglês
   inclusive pra economizar tokens."* `AD-15/16/17` were written in English; **`AD-01`–`AD-14` and
   the rest of the Portuguese corpus were not**, and AD-14 gained more Portuguese this session
   because matching a file's existing language beat mixing two inside one section. Convert whole
   files or whole ADs, never half of one. Quoted Lucas is his own words and **stays Portuguese**.
   → **tier: medium**.
10. 🟢 **one program should generate a stub, and two fragments should call it.**
    `generators/interfaces.sh` and `postedit/interfaces.sh` carry three near-identical
    `tsc --declaration --emitDeclarationOnly` invocations plus two copies of the stubgen call, which
    is why `interface-stubs` is the one feature needing two wired paths where `routing-tables` needs
    none — the latter's two moments already share `context_synchronizer.py`.

    **Both triggers are real and both stay.** Post-edit keeps the stub current *within* a session, and
    losing it does not merely delay a stub: `read/pre-read.sh` blocks a source read only while the
    stub beside it is current, so a stale stub makes the interface-first gate **silently stop
    enforcing**. Pre-commit stages the stub into the commit and sweeps stubless siblings, which is the
    only thing that ever catches a file entering outside Edit/Write. What is duplicated is the
    *invocation*, not the trigger: extract `core/hooks/stubgen/stub_one.sh <file>`, call it from both,
    and the feature collapses to a single wired path.

    **Not a rush job** (Lucas, 2026-08-18): *"my tendency is to refactor to one shared seam first but
    I do not want to do this in a rush and risk these features to be hindered."* The guard went in
    first precisely so the refactor is not carrying two jobs at once. → **tier: medium**.

11. 🔴 **the opencode shim was dead for weeks and no check could have noticed.** All eleven of its
    gate spawns pointed at `core/hooks/<script>` after those scripts moved into `read/`, `checks/`
    and `facade/` in the 2026-07-31 split. Repointed 2026-08-18, but the paths were only found by
    reading them: **nothing asserts that a shim's script paths resolve**, so the second harness's
    gate coverage is claimed rather than known. Lucas had the same item in the INBOX the same day
    (*"fully recover / adjust opencode wiring"*), which is the confirmation that repointing was not
    the whole ask.
    The decision is not how to write the check — it is whether opencode is still a runtime we
    support, because the answer sets how much this is worth. **Lucas asked (2026-08-18) to be walked
    through this rather than have it decided for him.** → **tier: medium** once decided.

12. 🔴 **a new top-level directory silently costs two commits.** `core/norms/` could not be staged
    until the pre-commit `.gitignore` self-heal added its allowlist line, and the heal runs *inside*
    the commit that needs it — so the commit that added the generated `AGENTS.md` shipped without the
    files it was generated from, and a clone at that commit regenerates an empty rule block. It
    self-corrected one commit later and nothing was lost, which is exactly why it will keep
    happening.
    Two ways out and they are not equivalent: heal *before* staging so one commit always suffices,
    or leave the behaviour and document it as the cost of a fail-closed allowlist. **Lucas asked
    (2026-08-18) to be walked through this rather than have it decided for him.**
    → **tier: medium** once decided.

13. 🔴 **Should entropy be scattered across the nested repos instead of pooled at the root?** Lucas,
    2026-08-18: *"entropy maybe should be scattered as well across each individual repo (maybe this
    is a task that deserves to be written somewhere, so we can DISCUSS this point in depth)."* Today
    one [`entropy.md`](entropy.md) at the workspace root counts this repo **and** all 25 nested ones,
    which is why a finding in `code/aiwbot` is read by a session working on the workspace and by
    nobody working on aiwbot. The pull the other way is real and is why this is a discussion rather
    than a task: the root file is a **ratchet**, and a number that must shrink only works while it is
    one number in one diff. Twenty-six ratchets is twenty-six baselines nobody watches. The same
    question is now open for the picture — `ARCHITECTURE.html` faces the identical split — so the two
    should be ruled together rather than drifting apart.
    → **tier: high**, with Lucas, its own sitting.

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
   → **tier: medium**. The fold needs a judgment call per line, so read them, do not batch.
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

   → **tier: medium**. The plan is the three findings above; it used to point at a file in
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
   larger win. → **tier: medium**.
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
   → **tier: high**, with Lucas — several sittings, not one pass.
7. 🟡 **show context growth continuously, not just at two thresholds.** Lucas, same capture:
   *"gostaria de ver o crescimento da janela de contexto em tempo real, o claude code no vs code
   não mostra. tem alguma forma barata de me mostrar isso?"*
   [`core/hooks/session/context-meter.py`](core/hooks/session/context-meter.py) already reads the
   size the API reports and speaks at `CTX_WARN` / `CTX_LOUD` — the ask is the *trend* between
   them, and the cheapest honest answer is probably a statusline rather than more hook output,
   since the hook's whole design point is costing zero tokens until crossed. **Do not make it
   chatty every turn**; that trades the thing being measured for the measurement.
   → **tier: medium**.
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
   **Ruled 2026-08-17 (Lucas), and the ruling reshaped the item.** The framing above was wrong on a
   fact: the offer is *already there*, as prose aimed at the agent —
   `message()` in `session/context-meter.py` ends with *"Run /roundup to close this session once the
   current thread is done."* What is missing is not the offer, it is **who sees it and when**. It is
   a `UserPromptSubmit` hook, so it lands in the agent's context at the *start* of a turn, and Lucas
   never sees it at all.
   His call: **show both crossings, to both of us, at the END of a response** — not at prompt
   submit. *"it wouldn't interrupt your flow"*, and he stops missing it.
   **The same gap, reported independently** (Lucas, INBOX 2026-08-17): *"algumas vezes o agente pede
   para eu autenticar no gmail ou gdrive mas é no meio de uma conversa longa e eu não vi a
   solicitação."* Confirmed live this session — a consent request sat unclicked through four
   exchanges. So this is not only the meter: **anything the agent needs Lucas to physically do is
   currently said in the middle of agent-facing prose and missed.** One mechanism serves both, which
   is why they are one row.
   **The open question is mechanical and must be checked, not assumed**: which hook fires at end of
   response in each harness, and whether its output can reach the user's terminal without also being
   billed into the agent's context. **Measure the cost before wiring** — the current message is one
   short line, at most once per threshold per session, but "probably free" is exactly the claim this
   workspace keeps getting wrong. → **tier: medium**, after that check.
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
   the number exists. → **tier: high**, with Lucas on whether to act on it.

---

## Front 10 — Portability & clonability — **v1 criterion 4**

> **Ruled 2026-08-16 (Lucas); every ruling is recorded where it is enforced, not here.** The harness
> is the installer and `SETUP.md` is the prose it executes — [`core/SCHEMA.md`](core/SCHEMA.md)
> § The `.md` type system. The registry's grouping, its columns, and the fact that `scope` **is** the
> general/Lucas-specific line (a column the sync reads, not a document) are declared in the header of
> [`core/features.txt`](core/features.txt) itself; the rule behind it is
> [`core/SPECS.md`](core/SPECS.md) § AD-14.

**Criterion 4 is met and the registry is live.** A feature whose `wired` column reads `-` cannot be
switched off, so **the ablation cannot report on it**. Wiring one is calling
`feature_law.is_enabled()` where the rule is enforced and naming that file in the column. Read the
count from `core/tools/wos/features --findings`, never from here — and the target is zero with **no
exceptions left**: the `n/a` column is empty, because the rows that carried it were category errors
rather than hard cases (`core/SPECS.md` § AD-14).

**The backlog is down to `telegram-capture`, and it is not mechanical** — it is item 6 below. Every
other row's guard was verified by running the feature both ways, never by grepping for the slug.

`skills` share one wiring point in the mirror, because a skill is markdown and the only real switch
is the mirror declining to publish it; a **tool** is a CLI this workspace writes, so it has a moment
of its own and guards at invocation, which buys a per-row behavioural answer instead of one answer
for the group.

**A feature that fires at two moments takes two paths, and the exception proves the rule.** Where the
two moments already share a program the guard goes in the program and one path is honest —
`routing-tables` is `context_synchronizer.py`, reached from both pre-commit and post-edit. Where they
do not, both fragments are named: `interface-stubs` and `lint-typescript` each keep a commit-time
half that stages or blocks and an edit-time half that keeps the artifact current, and guarding one
leaves the other writing. **`gates/project-contract.sh` hosts three features in one file**, so the
slug-names-the-file rule cannot apply there; that is a finding, not a rename to force.

**`norms` is live** — `core/norms/<slug>.md`, published into `AGENTS.md`'s generated rule block by
`core/hooks/routing/norms.py`, which is also the group's one switch. Rule order comes from the
registry, so moving a rule up the prompt means moving its row. Contract:
[`core/SCHEMA.md`](core/SCHEMA.md) § Layer: norm.

**`agents` and `flows` still have no rows**, and the seam is a *rendering* mirror rather than the
symlink one skills use. Ruled 2026-08-18 (Lucas): extend the mirror, not the read gate. Grounding
found the layer carries a **double asymmetry** the extension has to resolve first:

- `core/agents/` holds five research agents (`lead`, `researcher`, `writer`, `verifier`, `reviewer`)
  mirrored **nowhere** — they are file contents pasted as a system prompt, not spawnable agent types.
- `.claude/agents/craft-{high,medium,low}.md` and `.opencode/agents/craft-*.md` are hand-written
  **twice with no source in `core/`**, while [`core/SCHEMA.md`](core/SCHEMA.md) § Layer: agent calls
  them mirrors and states *"There is no generator, so keep each mirror's `model:` in sync with its
  source `tier:` by hand."*

**The two mirrors diverge on purpose**, which is why a symlink cannot serve: Claude Code's carries
`model: opus`, opencode's carries **no** `model:` line (stripped per the agnostic principle) plus
`mode: subagent`. So the work is one source per agent carrying `tier:`, and a generator resolving
`tier` → per-runtime frontmatter from [`core/flows/craft/routing.md`](core/flows/craft/routing.md) —
which deletes a documented hand-sync hazard as a side effect, and makes the five research agents
spawnable for the first time.

**Flows have no mirror location at all**, and that is the open question, not an oversight: a skill
names `core/flows/craft/*.md` by literal path, so publishing flows means moving where every skill
points. Decide that before building, because the pointer rewrite is the whole cost.

**Not built at the tail of the drain session it was scoped in** — it sits on `/craft`'s live spawn
path, and a frontmatter mistake breaks spawning until something catches it. → **tier: medium**,
agents first, flows after the pointer question is answered.

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

   **It has real users now, and they change the shape** (Lucas, INBOX 2026-08-17): *"tive algumas
   reuniões com alunos hoje, quero que todos eles usem algum setup com HARNESS + uma versão desse
   workspace que contemple pelo menos o ramo da pesquisa e produção de artigos."* So the public repo
   stops being only the ablation's precondition and becomes a deliverable with a deadline shaped by
   his teaching. It also names the **minimum useful subset**: the research and paper-writing branch,
   not the whole scaffold. Second, separable deliverable: a **prompt in Portuguese** for students to
   paste into whichever harness they use, letting them and the harness decide what to adopt — his
   words, so it stays Portuguese, and it is the one artifact here that is not English by rule.

   The features file (step 4) ships as scaffold — it is the thing that makes a subset installable — with
   the profile replaced by a placeholder on the way out. **The sync's allowlist is the deliverable**,
   not the copy: a path that is not on it does not travel, so adding a new top-level directory fails
   closed.
   → **tier: medium**.

6. 🔴 **`code/aiwbot` lives in its own repo and that is why one feature cannot be switched off.**
   `telegram-capture` is the last row reading `-`, and every wiring available today is wrong rather
   than merely awkward: a `code/aiwbot/...` path in the column makes this repo's Tier 0 test assert
   on a nested repo's content, which Front 4 forbids for a reason this repo cannot fix; reopening
   `n/a` contradicts the ruling that the column is empty. So the row is blocked on a question about
   where the code lives, not on wiring effort. **`core/features.txt` now says exactly that in its
   own header** — it claimed the opposite for a day, and the page reading `1 of 69` beside a header
   claiming no exceptions left is what caught it.

   Lucas, 2026-08-18: *"aiwbot is part of WOS, it is deeply entangled, it is not meant for general
   purpose bots… maybe we could version it inside the WOS repo and delete the aiwbot repo."*

   **For absorbing it:** the seam becomes an ordinary in-process guard; the gates already fire there
   through the global `core.hooksPath`, so nothing is lost; one less repo to keep on a legal branch
   and pushed; and the registry reaches zero without an exception.
   **Against:** the public scaffold sync would have to exclude it by allowlist rather than by it
   living elsewhere, which moves a boundary that currently cannot be got wrong; a bot token and a
   systemd unit are machine state, and `SETUP.md` already carries them; and aiwbot has its own verify
   suite, its own history and its own `AgentBackend` seam, which is exactly the shape `code/*` is for.

   **The tie-breaker to settle first is the public repo**, not the wiring: if the scaffold ships the
   research and paper-writing subset, whether a Telegram bridge is inside the workspace or beside it
   is answered by what a student clones. Decide that, and this row decides itself.
   → **tier: high**, one sitting.

---

## Front 12 — The `.md` type system (decided 2026-07-30)

> **The law is [`core/SCHEMA.md`](core/SCHEMA.md)** — § The `.md` type system holds the allowlist and
> the one question each type answers, § Boundaries where types nearly touch holds the three conflicts
> and their resolving rules, § Retired tokens holds what each rename retired. This front holds only
> the migrations that have not landed.

2. 🔴 **`entropy.md` is a lowercase `.md` at the workspace root, and the type system says that is an
   instance.** Lucas (INBOX 2026-08-17): *"it is a bit strange to have a lowercase.md file on the
   root... I want to discuss it with opus a bit."* The rule he is reacting to is real and this file
   is the exception to it: `UPPERCASE.md` is a **type**, `lowercase.md` is an **instance**, and the
   root holds types only — `AGENTS.md`, `README.md`, `ROADMAP.md`, `SETUP.md`, `CLAUDE.md`. So
   `entropy.md` is either mis-typed or it is a genuine fourth kind — a **generated report**, which
   no current type covers and which `entropy.md` is the only instance of. That is the question, and
   it is his because the answer either renames a file every session writes or adds a type to the
   allowlist. Pairs with Front 4's trend item: if the report starts carrying a dated baseline, what
   it *is* changes too. → **tier: medium**, with Lucas.

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
   → **tier: medium**.

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
   → **tier: high** for the design, medium to run it.

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
   → **tier: high**, with Lucas, in a session about this and nothing else.

2. 🔴 **a check that greps for a name is not evidence, and one of ours proved it by passing wrongly.**
   `test_features_wiring.py` asked whether a row claiming a switch really had one by checking that
   the feature's slug appeared somewhere in the named file. On 2026-08-18 the `symmetry` norm
   **passed that check by accident** — on the word *asymmetry*, in an unrelated comment, in a file
   that never mentioned the norm at all. The registry would have reported the rule as switchable
   while nothing switched it: the exact silent pass this front exists for, inside the test written
   to prevent it.

   Fixed where it was found — that file's grep is now scoped and the real work is done by
   behavioural checks that run the feature both ways. What is **not** done is the sweep: **how many
   other checks in this repo prove a name is present rather than that a behaviour happened**, which
   is [`core/SPECS.md`](core/SPECS.md) § Conventions applied to our own suite for the first time.
   **Lucas asked (2026-08-18) to be walked through this rather than have it decided for him.**
   → **tier: medium**, and it is the cheapest item in this front by a wide margin.

3. 🔴 **The agent agrees with the frame it was handed, and nothing catches that either.** Lucas
   (INBOX 2026-08-18, routed here 2026-08-18 by his ruling — it is this front seen from the decision
   side rather than the assertion side): *"resolver de forma definitiva o viés de confirmação dos
   modelos (e dos harness). pelo menos no PLAN mode. ou em todos os casos de tomada de decisão."*

   His own three-part shape, and the third part is the constraint: **first** a mechanism to notice
   that a decision is being taken at all; **second** *"não quero transformar os agentes em críticos
   ferrenhos e cegos"* — the cure must not be a contrarian reflex, which is the same failure with
   the sign flipped; **third** a method — detect the decision, grade its criticality, research it,
   investigate impacts, then ground the pros and cons (adversarial shapes, flows, SDD are candidates
   he named and explicitly did **not** pick). His words on scope: *"não quero também definir COMO
   resolver esse problema agora… esse é um problema grande que deve ser resolvido com pesquisa."*

   **Why it sits here rather than opening a front:** this front already says the agent emits
   confident claims nothing checks. A plan the agent produced by agreeing with the premise it was
   handed is one of those claims, and PLAN mode is where it is most expensive — the whole session
   downstream is built on it. **Do not open this with a prompt rule** either, for the reason stated
   directly above.
   → **tier: high**, with Lucas, research first and its own sitting.

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
   → **tier: medium**.
4. 🟢 **a `forms` tool family, provider leaf `gforms`.** Lucas, INBOX 2026-08-18: *"adicionar o
   gforms ao WOS."* The shape is already dictated by
   [`core/tools/SPECS.md`](core/tools/SPECS.md) — a family directory is the feature and the tool
   inside it is the provider, so this is `core/tools/forms/gforms` beside `calendar/gcalendar` and
   `files/gdrive`, reusing [`core/tools/auth/gauth.py`](core/tools/auth/gauth.py) rather than
   minting a second Google credential path. It lands as a row in `core/features.txt` (group
   `tools`, `runs: on-demand`), a `deps.txt` line and a `SETUP.md` step, which is the whole join.
   **What is not decided is what it reads** — a form's responses are the useful half and the
   question is whether that is a new capability or a `files/` download in disguise.
   → **tier: low**.
3. 🟡 **then reinforce the goal↔roadmap link, possibly enforced.** Same capture, and deliberately
   second: *"depois gostaria de reforçar a conexão entre os goals e os roadmaps, não sei se tem
   como, talvez até algo ENFORCED"*. Every goal file already carries an `>**owns**` block and every
   plan is supposed to live in a `ROADMAP.md`; what is missing is anything asserting the two agree.
   **Do not design this before item 2 reports** — if goal files turn out to be read rarely, the fix
   is not a stronger link to them.
   → **tier: medium**.

## Front 17 — the workspace describes itself wrongly, and the description is what we build on

Lucas, 2026-08-17, after the fourth correction in one session: *"I am quite tired of phrases like
'the roadmap item was factually wrong'… all we do here are Opus sessions, we have verifications and
other guards, and yet these appear more often than not. I am WARNING us that this is shady and WE
MUST find a way to avoid this… it is taking away all my confidence that we are actually making
progress."* His diagnosis, which is the sharper half: *"you, the model, infer and decide tons of
directions from just a wind of thought, making it a hard truth."*

**Four specimens from that one session, and they share a shape.** The handoff asserted a group seam
was needed where none was; AD-14 asserted tools had nowhere to put a call, reasoning from
skills and generalising; the context-meter item asserted an offer was unbuilt while it sat in the
message string; `core/features.txt`'s header asserted its groups match the tree. Every one is a
**claim about our own codebase, written into a durable file, with no probe attached** — and each was
then inherited by a later session as settled fact. A fifth, mine, in the same hour: four consecutive
reports that a token had not been written, made by checking a directory the tool does not write to,
while the tool printed its real path on its own last line.

**Three more specimens, 2026-08-17, and all three died to a probe that cost one command.** The
registry called `latex` third-party machine state we do not author — one `grep` finds
`hooks/stubgen/tex-*` and `core/tools/paper/`, ours. `heredoc-gate`'s row claimed `blocks`; running
it both ways shows it prints a warning and returns 0, so it **warns**. And § How to read this said
*two* items need Lucas while three were marked 🔴 — the count went stale the day this front opened
as the third. **The pattern is now dated and repeatable: every false claim this session was about
our own tree, was written into a durable file, and was refuted by one `grep`, one `ls`, or one run.**
None needed judgment; they needed anyone to check. That is the evidence this front asked for.

**The asymmetry that makes this tractable.** This workspace already has the discipline — for
*numbers*. *"Re-run it, never quote it"* is everywhere and it works; `entropy.md`, `session/usage`
and `--findings` are all quoted-from-nowhere by rule. There is **no equivalent for structural
claims**: *"nothing calls X"*, *"there is nowhere to put Y"*, *"Z is unbuilt"*, *"these groups match
the tree"*. Those are strictly **cheaper** to verify than any number — one `grep`, one `ls`, one run
— and nothing asks anyone to. Guarded the expensive claims, left the cheap ones open.

**This is not Front 15 and the difference is load-bearing.** That front is about technical opinions
on the *outside world*, where the fix is search and a knowledge store. This is **self-description**,
where the answer is already on disk and simply was not read.

1. 🔴 **Open with a research and design sitting, and build nothing before it.** Ruled 2026-08-17: it
   gets its own front and its own session. Candidate mechanisms, none chosen — picking one from a
   wind of thought would be the same failure the front exists to name: a structural claim must carry
   the command that falsifies it; handoffs may not restate a claim without its probe (the handoff is
   the *amplifier* — it is how the seam claim reached today's session pre-loaded as fact); an
   adversarial step in the flows; a defined vocabulary, since several of these were category errors
   a glossary prevents at source (`core/SCHEMA.md` § Vocabulary defines three terms).
   **Bring evidence, not intuition**: the specimens above are dated and re-checkable, and the first
   work is deciding what a *provable* claim about our own code looks like.
   → **tier: high**, with Lucas, in a session about this and nothing else.

## Front 18 — Lucas can no longer read his own workspace, and that is the root cause

Lucas, 2026-08-18, closing the session that drained the feature registry: *"sometimes the WOS is
growing with decisions I didn't recall making… some words that are hard for me to instantly
understand are ledger, seam, probe… I feel sometimes things are growing and I am losing the
understanding of what is happening in WOS. this whole renaming / wiring of features, hooks, tools,
etc, was due to that in my opinion."*

**That last clause is the finding.** The feature registry, the group rename, the `capability` sweep —
weeks of work — were all downstream attempts to fix a legibility problem nobody had named. Treating
them as separate cleanups is why each one only helped for a while. His two rules, in his words:

1. **Language is the thing.** *"this whole WOS is meant for LLMs, language IS the thing"* — so a
   word chosen badly is not a documentation defect, it is a defect in the system itself. Semantic
   symmetry is part of it: one idea, one word, everywhere.
2. **Simpler, better organised, more often than not.** *"our language choices can be simpler… this
   would help me and you (harness+model)."* Both readers, not just the human.

This front never closes. It is the standing check that the workspace stays understandable to the
person who owns it, and the place to route the next *"when was that decided?"*

1. 🔴 **The deep sitting: research and brainstorm what this front actually is, then build.**
   The opening question — *"is it a front at all"* — was answered in the 2026-08-18 sitting. **Ruled
   (Lucas): it IS a front, standing; and all three halves below (18.2/18.3/18.4) are real work, none
   killed.** What is NOT settled is the front's shape — Lucas: *"this deserves discussion, research
   and brainstorming, I don't think we will handle all we need in this small assessment."* So the
   halves may split, merge or gain a fourth, and their ordering is open. This row does not close when
   the halves are listed; it closes when the front has had the research sitting it asks for.

   **Opening material, carried as a hypothesis to test — not a fact** (this is the Front 17
   discipline applied to itself): *Fronts 15, 17 and 18 may be three faces of one root — the
   workspace emits durable text its readers cannot trust or parse.* 17 = the agent writes false
   structural claims about our own code; 15 = false confident claims about the outside world; 18 =
   words and quiet decisions Lucas cannot read. Lucas's own line is the evidence for it — the
   feature-registry and rename churn was *"downstream of a legibility problem nobody had named."*
   **Falsification path:** if the three halves land and 15's and 17's symptoms do not ease, the
   framing was wrong and these stay three separate fronts. Bring evidence to the sitting, not the
   framing pre-accepted. **First evidence in, and it cuts for the root:** legibility is a *measurable*
   property, not taste — generated context bloat lowers agent task success and raises cost, and
   instruction accretion degrades adherence to the earliest, highest-consequence rules (ETH Zurich
   2026 and the AGENTS.md-bloat literature, [`core/refs/REFS.md`](core/refs/REFS.md) § Legibility
   prior art). The corollary is sharp: the fix is subtraction, so solving *"I cannot read my
   workspace"* by adding explanation makes it worse for both readers.

   **The 2026-08-18 sitting ran the diagram half:** 18.3's shape is ruled below, 18.2's criterion is
   refined, and 18.4 is reshaped by the decision-record finding. What the front still owes its own
   session: the **jargon audit** (18.2's internal replacement work) and the **one-root test** above —
   both deferred here deliberately, neither cheap enough to fold into a mixed session.
   → **tier: high**, with Lucas, its own session about this and nothing else.

2. 🟡 **Replace the words that need a glossary to be read.** A definition is a patch; the fix is the
   plain word. Named by Lucas: **ledger**, **seam**, **probe**. Found beside them in one pass over
   our own prose: **ratchet**, **corpus**, **substrate**, **fanout**, **hop**, **shim**, **spine**,
   **surface**, **law**, **drift**, **honesty test**, **boy-scout**. Some earn their keep and some
   are showing off, and telling those apart is the work — *gate* is worth its definition, *seam*
   almost certainly is not (it means "the place the switch goes").

   Two products, in order: a **plain-word replacement** per term that survives the cut, applied
   across the corpus the way `capability` → `feature` was; and the survivors defined in **one place**
   — [`core/SCHEMA.md`](core/SCHEMA.md) § Vocabulary already holds three definitions and is the home,
   so nothing new gets built for this. **Criterion ruled 2026-08-18 (Lucas): the best, most precise
   word wins, and simpler breaks the tie** — he will learn a new word if it is genuinely the best one,
   and drop a word that is only showing off. Mature terminology practice says the same (precision over
   economy, clarity a hard constraint — [`core/refs/REFS.md`](core/refs/REFS.md) § Legibility prior
   art), so the rule is confirmed, not invented.

   **First case run, and it changed what the audit is looking for.** Lucas, 2026-08-18, on the
   registry's `enforcement: none`: *"what is none… that it does nothing? is none the best word?"*
   The word was fine; it was carrying **two facts** — "fires by itself and applies no pressure" and
   "you call it" — and that ambiguity had already made a session report the workspace's capability
   layer as its largest block of dead weight. The fix was a second column (`runs: automatic |
   on-demand`), not a better word. **So the audit's first question is whether a confusing term is
   underspecified rather than badly named**; a rename would have buried the defect under a nicer
   label. Rejected on the way: `serves` as a replacement value, and `passive`/`active` as the new
   column's values — `active` collides with "switched on", which this registry declares everywhere.

   **A word list beats asking a model, and Lucas proved it while naming the diagram tool** — he
   went to a thesaurus, came back with *architect / blueprint / diagram / scheme*, and picked one.
   So the audit gets an instrument: a small `core/tools/web/thesaurus` over an open synonym API
   (Datamuse needs no key), zero tokens per lookup against a model asked to free-associate. It
   offers candidates; the criterion above still decides. → **tier: low** to build, before the audit
   runs, not blocking it. → **tier: medium** for the audit itself, after the sitting.

3. 🟡 **Keep trying shapes for the *is* picture until Lucas can read it, then cut.** The page opens
   on a heat grid split by what starts a feature, with five findings under it, above the detail
   tabs. **What is open is not "build a summary" but "which drawings earn their place"**, and Lucas
   sets the pace: *"we are still at the level of trying different visualizations to cut it later,
   so no rush in discarding anything yet."*

   **The question was restated and it is not the one this row used to hold.** Lucas: *"1) in a
   glance see if WOS is well tied, if it has loose ends, if it has too much noise, discardable
   things, see the value in a glance, 2) spot the GAPS, what is missing."* That is a **health**
   read, not the inventory read the first version answered — an inventory says what is there,
   health says what is loose, what is dead weight, what is absent. All three original drawings are
   inventories, which is the deeper reason none of them landed.

   **Both queued shapes are drawn, so the cut is now the whole of this row.** They answer Lucas's
   standing want — *"I am missing seeing some trees, graphs… sequences of thing1 → thing2 → thing3…
   how things are connected or not"* — and both sit above the tab strip. Where a graph pays is
   settled by evidence rather than taste: Ghoniem says matrices beat node-link past ~20 nodes
   ([`core/refs/REFS.md`](core/refs/REFS.md) § Workspace visualization), which is why the 107-node
   routing tree reads as wallpaper and a six-node fan-in does not.

   - **the lifecycle sequence — KEPT (Lucas, 2026-08-18).** One band per session moment, the
     on-demand features detached beside the chain. It passed the health read at a glance, so it
     stays and every shape beside it is judged against it.
   - **the wiring fan-in — drawn in THREE shapes, and two of them die at Lucas's next look.**
     `views/diagram_fanin.py` holds a converging node-link plus a bars renderer called at both
     grains, because he asked to compare rendered output rather than a mockup. 69 features resolve
     to 47 wiring points and two carry 24 of them. `views/CONTEXT.md` carries the cut condition so
     the rack cannot outlive the decision. → **tier: low**, one look and two deletions.

   Every finding on the page carries a target read off a declaration, and the one nobody has
   decided — *are declared layers holding no feature a defect?* — prints `undecided` so it cannot
   pass for a met one. Pinned by `test_diagram_health.py`. → **tier: medium** for the row.

   **The picture's boundary — DEFERRED by Lucas, 2026-08-18**, after the worry was measured:
   *"to respect the context tree I think we may leave as it is now… let's not overcomplicate this
   for now, we have bigger priorities."* What settles it is that **WOS versions nothing at all
   inside a nested repo** — `git ls-files academy/papers/2027-ICLR-dobra` returns zero files, and
   the same holds for `code/dobra` and `branches/casinhas`. Each paper and project owns every one
   of its own files in its own repository. What reaches the picture is the paper's **name**, from
   the routing table in `academy/papers/CONTEXT.md`, so the leak is one row of a parent's index
   rather than versioned content. The candidate rule if it is ever taken up: a directory whose
   children are instances rather than structure stops at its own name — and the declared signal
   for "instance" already exists, since every one of them is its own git repo.

   **One ruling still Lucas's**, raised by an outside critique of the page: `core/features.txt`
   opens by saying **no feature in this workspace has ever been measured**, and the diagram of the
   workspace's self-knowledge never says so. That is the ablation front's subject and belongs to it
   rather than here, so what is open is only whether the page should carry the sentence at all.

   **The cut list is collected and deliberately unspent**, per the pacing above: the treemap
   answers neither question, the routing spine is 107 nodes to say two numbers, and the tab
   mechanism hides two thirds of the page from the diff and the printed artifact. **Do not act on
   it** until the new shapes have been seen — and one candidate is already dead on evidence, see
   the row below.

4. 🟡 **The other two pictures — *becoming* and *goal*.** *Becoming* is generated from git history;
   *goal* is authored intent, the only one of the three not tree-derived, since the future is not on
   disk. **Both wait on the row above** — a second and third picture that cannot be read at a glance
   multiplies the problem rather than the value. Goal is the one that pays: **goal − is = the roadmap made visible**, what is left to build seen rather
   than listed. The data for *becoming* is proven and waiting — per-nested-repo `git log` via
   `nested_repos()` + [`core/hooks/git/branch_debt.py`](core/hooks/git/branch_debt.py).

   **The standing rules the built half already keeps, and the next two inherit:** generated from the
   tree and never drawn by hand; zero-token and deterministic (no timestamp, no sha, so `--check`
   means something); one self-contained HTML file committed in-tree; every edge either renders
   declared data or is labelled *inferred*; total and fail-loud, printing `parsed N of M` and naming
   what it could not read.

   **A summary does not replace the detail, and that is now measured rather than assumed.** In a
   41-subject controlled experiment across three countries, an overview beat a state-of-the-practice
   table by +24% correctness and −12% time, concentrated on exactly the *spread* and *impact*
   questions Lucas is asking — **but the table stayed faster for precise lookups and the authors
   conclude the two complement each other** (Wettel, Lanza & Robbes, ICSE 2011,
   [`core/refs/REFS.md`](core/refs/REFS.md) § The health shelf). So the summary goes *above* the
   enforcement matrix, and the standing proposal to cut that matrix is dead on evidence.

   **Nothing on the page is inferred**, so the next two pictures inherit a page with no
   apologies on it: [`core/hooks/trigger/`](core/hooks/trigger/CONTEXT.md) reads the firing moment
   out of the registrations, and what it cannot place is counted as a gap. **The transferable
   finding is that a registry asked to be authored turned out to be derivable** — the same shape as
   the `runs` column the session before, and the rule the next picture should carry into git
   history too: look for the declaration before writing a new one.
   → **tier: medium** for *becoming*; *goal* needs Lucas's intent before it can be drawn.

5. 🔴 **Which sectors deserve an `ARCHITECTURE.html`, and what does each one need that the
   workspace document does not?** Lucas, 2026-08-18, on seeing the first one: *"I envision an
   ARCHITECTURE.html file for each code project… maybe an ARCHITECTURE.html file even for papers, we
   have to think this through, which sectors of the WOS deserve one and which are the
   particularities."* The renderers are already reusable and `core/hooks/generated.txt` already
   globs `*/ARCHITECTURE.html`, so the build is not the hard part — **the question is what each
   sector's picture is *of*.** A code project has properties the workspace does not: call structure,
   sequence over time, module dependency. A paper has others again. Answering that per sector is the
   work; generating one document per repo before answering it would produce twenty-five drawings
   nobody reads. → **tier: high**, with Lucas, before any second document is generated.

6. 🟡 **A session must not decide things quietly, and the record of *why* must survive.** The
   complaint under all of the above is *"decisions I didn't recall making."* Two shapes, the second
   reshaped by the research (seed, not yet ruled — [`core/refs/REFS.md`](core/refs/REFS.md)
   § Legibility prior art): the hand-off names **what this session decided without asking**, separate
   from what it did (a decision that cannot be stated in one line was too big to take alone, so the
   section is a filter as well as a record); and, for decisions with lasting blast radius, a **minimal
   decision record** — Context / Decision / Consequences, one file each, superseded rather than
   rewritten. That record logs the rejected option space git commit messages lose, so it captures
   *why*, not work-product, and does **not** contradict "done work is deleted, git is the history" —
   the § Rejected list here is already a partial version of it. Shape belongs in
   [`core/SPECS.md`](core/SPECS.md) § AD-09; [`core/skills/handoff.md`](core/skills/handoff.md)
   carries the hand-off half. → **tier: medium**.

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
   Declared: [`core/hooks/SPECS.md`](core/hooks/SPECS.md) § The next gate. → **tier: medium**.
2. 🟢 **the `core/experiments/` and `REFS.md` discipline checks.** The two rules this workspace cites
   as proof it knows how to doubt — a runnable `## Method`, dated `Results`, `Limitations` never
   omitted; and `REFS.md`'s `[A]`/`[B]`/`[P]`/`[V]`/`[C]` tier markers — and **neither is verified by
   anything.** Both stores are small and closed, which is what makes them the obvious next Tier 0.
   Declared: [`core/SPECS.md`](core/SPECS.md) § AD-16 band 1. → **tier: medium**.
3. 🟢 **the loop-cap check: a step that declares a loop must declare its cap.** Greppable,
   deterministic, zero-token, and true of every flow rather than of one technique. It is the inverse
   of the shape under § Rejected — requiring the adversarial step creates the death loop, requiring
   the bound is what makes requiring the step safe.
   Declared: [`core/flows/craft/SPECS.md`](core/flows/craft/SPECS.md). → **tier: medium**.
4. 🟢 **roundup compares the declared model split against the actual one.** `core/tools/wos/roundup`
   already prints the per-session split at every close; what is missing is the plan **declaring its
   expected split** and roundup comparing. It forces nobody to delegate — it makes deviation visible
   and dated instead of invisible, and needs no new instrument.
   Declared: [`core/SPECS.md`](core/SPECS.md) § AD-17. → **tier: medium**.
0. 🟢 **the ledgers name vendor models where they should name tiers.** Lucas, 2026-08-17, reading a
   step assignment: *"nothing in WOS should be tied to a specific vendor/company/model."* He was
   right and it was wider than the one line he saw — 26 routing directives across both ledgers said
   `model: sonnet` / `model: opus` where the workspace already has the abstraction: `/craft` routes
   by **tier**, and [`core/flows/craft/routing.md`](core/flows/craft/routing.md) is the one file
   holding which concrete model fills a tier per provider.
   **The sweep is done; what is unbuilt is the guard.** Nothing stops the next session writing a
   model name back in, which is the shape § Retired tokens exists for — except that a bare vendor
   name is legitimate as *data* (a measured split, a quoted stale model id in a bug report) and
   illegitimate as a *directive*, so a flat token ban would fire on the honest uses. The check has to
   read position, not presence. Pairs with the `core/tier-map.json` extraction in
   [`core/ROADMAP.md`](core/ROADMAP.md), which removes the last such name from source.
   → **tier: medium**.
5. 🟢 **import the auto-trigger.** `/craft` must be typed, which is the missing half of AD-17: the
   assignment is carried at plan time and no executor reads it outside the flow. The mechanism
   imports without the methodology — the rest of that repo stays under § Rejected.
   Declared: [`core/flows/craft/SPECS.md`](core/flows/craft/SPECS.md) § Judged against Superpowers.
   → **tier: medium**.

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
  `test_entropy_fanout.py` in the same commit. → **tier: medium**, one repo at a time.

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
  → **tier: medium**, one file per commit.

- **The `.d.ts` half of the stub gap** — 203 files, all in nested repos, counted in
  [`entropy.md`](entropy.md) under the criterion-1 baseline rule.
  → **trigger: a session in each nested repo.**

- **`gira` and `laplata` declare `goal: none` while their goal files exist.** The project ⟺ goal
  link check blocks and all 14 projects declare line 3, but these two say `none` where
  `startapps-gira` / `startapps-laplata` sit on disk — line 3 is *wrong*, not absent, which is
  precisely what no check can catch. **Ruled 2026-08-17 (Lucas): yes, those projects serve those
  goals — point line 3 at them.** So the judgement is spent and only the commit is left; the
  attention counter starts seeing work on both goals instead of reading them as dead.
  → **trigger: a session in `code/gira` / `code/laplata`.** One line each, in their own repos.

- **What makes a stored fact go stale.** A hash-addressed store is only as good as its refresh rule;
  a confidently-served 2026-07 fact is the same failure with extra steps. Every fact needs a
  measured-on date and a claim about how fast its subject moves — harness behaviour ages in weeks, a
  published result in years.
  → **trigger: the knowledge-store sitting in Front 15 opening.** A refresh rule needs a store to
  refresh. → **tier: medium**, then.

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
- **Shipping `codeburn` as a workspace feature** — an external npm binary we do not author, wired into no gate, run by hand. Ruled 2026-08-17: the registry names what this workspace can switch off in order to measure it, and there is no rule of ours to disable. Deleted from `SETUP.md`, `core/features.txt` and `core/profile.txt` together, which keeps the step ⟺ feature join intact. Install it as a personal tool if you want it.
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

**Track A — wire the registry to zero.** Drained 2026-08-18 down to one row, whose blocker is a
decision rather than work; what is left of the track is Front 10 and needs no separate plan. The
three layers with no rows at all — `agents`, `flows`, `norms` — are named there too.

**Track B — the one hard chain, because each step is the next one's precondition.**
1. The **public scaffold repo** at `code/wos/` and its one-way sync. It stopped being a neighbour of
   the ablation on 2026-08-17 and became its **hard precondition**: the experiment runs on variants
   built from the public repo, so no public repo means no arms to compare. Students needing a
   research-branch workspace makes it demand as well as precondition.
2. The **ablation**, against whatever is switchable by then. Design is high tier and belongs to the
   paper twin; the run is medium.

**Track C — unordered and mechanical, all medium tier.** Everything under § Declared but unbuilt, plus the
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
Mapping: 🔴 → **high tier, same session**; 🟢/🟡 → **medium via `/craft`** (mechanical parts drop to
low). Which model fills each tier is data in that file, never in this one.
