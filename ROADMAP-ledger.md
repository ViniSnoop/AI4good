# Ledger discipline
> One ledger with no duplicates, and what each `.md` type is allowed to be.
> priority: essential

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
