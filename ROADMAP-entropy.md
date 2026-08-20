# Workspace anti-entropy
> Tier 0 checks, the shrinking-baseline ratchet, and rules declared but unbuilt.
> priority: essential

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
   ([`core/hooks/SPECS.md`](core/hooks/SPECS-generators.md) § First-line descriptions). What is left is the
   standing queue the ratchet deliberately does not
   charge anyone for. **Size it against [`entropy.md`](entropy.md), and re-run the generator before
   measuring** — every marker drained so far was a file the generator could already describe.
   **Scope here is this repo only**; the nested-repo majority is under § Blocked. → **tier: medium**.
7. 🟢 **the bash context gate reads paths out of a commit message body.** Lucas (INBOX 2026-08-17)
   and **reproduced twice in this session**: a heredoc `git commit -F -` whose *message* names
   `core/tools/web/fetch` is treated as a command touching that subtree, so the gate demands the
   CONTEXT.md before letting the commit through. The gate should read the command, not the text the
   command carries. `core/hooks/read/bash-context-gate.py`. → **tier: medium**.
8. 🟡 **Five `.md` files are still over the 200-line cap, and the gate cannot go live until none are.**
   Ten on 2026-08-19 morning; Lucas's rulings that afternoon closed five of them and **none of the
   five left is workspace work**:
   - **Three belong to `code/spacemantics`** — `dsl/SPEC.md`, `dsl/EXAMPLES.md`, `dsl/LEXICON.md`.
     Renaming them is that repo's design question and is already filed in its own roadmap. Nothing
     here moves until it rules.
   - **Two are blocked on a live session** holding staged changes to `code/isoroll-content/ROADMAP.md`
     and `code/isoroll-module/ROADMAP.md`. Check `git status` in both before touching either; the
     work that unblocks them is somebody else's commit, not ours.

   `s3_batch.sh` at 209 is code, not `.md`, and predates the rule. The `outputs/*.md` files the raw
   line count surfaces are **not** violations — `core/hooks/generated.txt` excludes them, which is
   worth knowing before someone re-derives the list by hand and reports nine.

   **What the closing session learned, and the next one should expect.** The two names that looked
   like they needed an allowlist entry needed neither: `UI_SPEC.md` needed the `SPECS.md` name its own
   repo already used nine times, and `REFACTOR.md` was **done work** whose branch no longer existed.
   Reach for *is this still true* before *what type is this*. Two traps fired on the way: a deleted
   file's row in `core/SCHEMA.md`'s transient-exemption table keeps its exemption alive, because every
   backticked name there is parsed as one; and a document being deleted can be the sole record of
   something live — `REFACTOR.md` held the only copy of bug B29, which `BUGS.md` was supposed to have.
   → **tier: medium**, and the gate flip is the last step, not the first.
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
## Declared but unbuilt — a rule with a `SPECS.md` section and no implementation

A rule belongs beside the thing it governs, so each of these is declared in a `SPECS.md` § — but a
`SPECS.md` states what must be true and cannot say whether anything enforces it yet, which left the
*build* with no home and made the item count flatter than the work state. **The declaring section is
the spec; the row here is the work.** Each row is deleted the day its check runs; this section is
deleted when the last one does. **Three left of six**, and the three that landed were the ones with
nothing to decide — what is left each needs one judgment first, named in its row.

4. 🟢 **roundup compares the declared model split against the actual one.** `core/tools/wos/roundup`
   already prints the per-session split at every close; what is missing is the plan **declaring its
   expected split** and roundup comparing. It forces nobody to delegate — it makes deviation visible
   and dated instead of invisible, and needs no new instrument.
   Declared: [`core/SPECS-discipline.md`](core/SPECS-discipline.md) § AD-17. → **tier: medium**.
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
