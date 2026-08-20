# Workspace anti-entropy
> Does the tree still have the shape we said it has, and does anything check? Holds the Tier 0
> checks, the ratchet that makes their count shrink, and rules declared in a `SPECS.md` with no
> implementation. Open it for a check, a drifted name or an unenforced limit — never for what the
> drift *means*, which is legibility's.
> priority: essential

## Front 4 — workspace anti-entropy — **the keystone, v1 criterion 1**

> The real target: files grow, scatter, duplicate, and drift from naming/structure patterns.
> **Structure is a spec; drift is a test failure.** `code/` already has this (the `> spec:` gate);
> the agent library has [core/SCHEMA.md](core/SCHEMA.md). Nothing yet governs the shape of the
> workspace itself.

1. 🟡 **entropy is reported "flat" every session and has roughly quadrupled in four days.** Lucas
   (INBOX 2026-08-17): *"sessions keep saying entropy is flat but on the last week it went from 270
   I think up to more than 400."* He is right and the real curve is steeper than his memory of it —
   re-derived from the count's own history, one command, which is the point. It spans the two files
   the count has lived in — `entropy.md` until 2026-08-19, the entropy block of `ISSUES.md` after —
   because a trend that stops at a rename is the same blindness in a new place:

   ```bash
   for c in $(git log --format=%h --since="12 days ago" -- entropy.md ISSUES.md); do
     printf '%s  ' "$(git log -1 --format=%ad --date=short $c)"
     { git show "$c:ISSUES.md" 2>/dev/null || git show "$c:entropy.md" 2>/dev/null; } \
       | grep -m1 -oE '[0-9]+ findings'
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

3. 🟢 **drain the entropy dashboard.** `make entropy` → [`ISSUES.md`](ISSUES.md) § Entropy, the whole
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
   charge anyone for. **Size it against [`ISSUES.md`](ISSUES.md) § Entropy, and re-run the generator before
   measuring** — every marker drained so far was a file the generator could already describe.
   **Scope here is this repo only**; the nested-repo majority is under § Blocked. → **tier: medium**.
8. 🟡 **Five `.md` files are still over the 200-line cap, and the gate cannot go live until none are.**
   Ten on 2026-08-19 morning; Lucas's rulings that afternoon closed five of them and **none of the
   five left is workspace work**:
   - **Three belong to `code/spacemantics`** — `dsl/SPEC.md`, `dsl/EXAMPLES.md`, `dsl/LEXICON.md`.
     Renaming them is that repo's design question and is already filed in its own roadmap. Nothing
     here moves until it rules.
   - **Two were filed as blocked on a live session** holding staged changes to
     `code/isoroll-content/ROADMAP.md` and `code/isoroll-module/ROADMAP.md`. **That diagnosis is
     wrong.** Both worktrees are clean of those files and both files are still over the cap — the
     staging was never what held them there. Read the current numbers from
     [`ISSUES.md`](ISSUES.md) § Entropy, which also shows *why*: both carry ticked items and one
     carries strikethrough, so the mass is undeleted finished work.

     **Cut, then split only what is still over** (Lucas's ruling, item 13): apply *completion is
     deletion* to both files first and re-measure. A roadmap that long under a delete-on-completion
     policy is mostly finished work, and sharding it would preserve the mass across more files —
     the superficial fix rather than the root-cause one.

   `s3_batch.sh` at 209 is code, not `.md`, and predates the rule. The `outputs/*.md` files the raw
   line count surfaces are **not** violations — `core/hooks/generated.txt` excludes them, which is
   worth knowing before someone re-derives the list by hand and reports nine.

   **What the closing session learned, and the next one should expect.** The two names that looked
   like they needed an allowlist entry needed neither: `UI_SPEC.md` needed the `SPECS.md` name its own
   repo already used nine times, and `REFACTOR.md` was **done work** whose branch no longer existed.
   Reach for *is this still true* before *what type is this*. Two traps fired on the way: a deleted
   file's row in `core/SCHEMA.md`'s transient-exemption table keeps its exemption alive, because every
   backticked name there is parsed as one; and a document being deleted can be the sole record of
   something live — `REFACTOR.md` held the only copy of bug B29, which `ISSUES.md` was supposed to have.
   → **tier: medium**, and the gate flip is the last step, not the first.
9. 🟢 **the corpus is half Portuguese and the rule is English.** Lucas (INBOX 2026-08-17): *"somente
   o meu texto é em português, as conversas nas sessões, mas o resto, os docs, tudo em inglês
   inclusive pra economizar tokens."* `AD-15/16/17` were written in English; **`AD-01`–`AD-14` and
   the rest of the Portuguese corpus were not**, and AD-14 gained more Portuguese this session
   because matching a file's existing language beat mixing two inside one section. Convert whole
   files or whole ADs, never half of one. Quoted Lucas is his own words and **stays Portuguese**.
   → **tier: medium**.
11. 🟡 **`core/hooks/entropy/` holds eight one-question checks and crossed the fanout signal.**
    Joined the baseline 2026-08-20, when the size and vendor checks landed. **The name has not
    drifted** — every module there really does answer one question about the corpus, which is what
    that directory is for, so this is the cost of the design working rather than the responsibility
    problem the signal usually means. That is exactly why it needs a decision instead of a rising
    threshold. The seam, if it is worth paying one hop for: split on what each check **reads** — the
    tree's *shape* (`corpus`, `naming`, `fanout`, `size`) against its *text* (`context`, `ledger`,
    `stores`, `vendor`). Four and four, and the dashboard imports from two places instead of one.
    **Splitting costs one hop; pay it only when it removes more table than it adds**, so the honest
    answer may be to leave it and let the baseline hold. Whatever is decided applies to
    `core/tools/test/law/entropy/` in the same commit: it mirrors this directory one word apart and
    crossed the signal for the same reason, which is the property mirroring buys.
    → **tier: medium**.

13. 🟡 **scatter entropy into every code repo, and collect one number at the root.** RULED
    2026-08-20 (Lucas) — the discussion is closed and what remains is work.

    **The ruling, in three parts.** *(a)* **Every CODE repo gets a local `ISSUES.md`**: the workspace
    repo and everything under `code/`. Papers and `branches/` stay pooled — they are not code and
    their findings are few. `core/` and `brain/` are **undecided and must be evaluated**, since both
    live inside the workspace repo and may already be covered by its own ledger. *(b)* **The root
    sums.** One collected number, not a table of cells each with its own baseline: *"sum it up, I am
    aware of the tradeoff, that said, optimizing/solving the sum solves it all."* The sum keeps the
    ratchet a single number in a single diff, which is the property that made it work. *(c)* The
    picture rides along — see [`ROADMAP-legibility.md`](ROADMAP-legibility.md).

    **What the evidence says the work is, and it is smaller than the item feared.** The scope is
    **16 ledgers, not 26**, and they cover **91%** of findings; the 9% in papers and `branches/` stay
    at the root. The other number that decides the shape: the root `ISSUES.md` is **91% generated
    block** — the hand-written half holding the real bugs is buried under it. So the root stops
    dumping findings and becomes an index of counts plus its own local findings, which is the routing
    pattern every other type here already uses. Re-read both numbers from
    [`ISSUES.md`](ISSUES.md) § Entropy rather than trusting these.

    **The one thing to get right:** the sum must be recomputed from the local ledgers, never
    hand-carried. A collected number that any repo can write into is the copied-count drift these
    checks exist to catch.
    → **tier: medium**.

---
## Declared but unbuilt — a rule with a `SPECS.md` section and no implementation

A rule belongs beside the thing it governs, so each of these is declared in a `SPECS.md` § — but a
`SPECS.md` states what must be true and cannot say whether anything enforces it yet, which left the
*build* with no home and made the item count flatter than the work state. **The declaring section is
the spec; the row here is the work.** Each row is deleted the day its check runs; this section is
deleted when the last one does. The rows below are the count; the ones that landed were the ones
with nothing to decide, so what is left each needs one judgment first, named in its row.

4. 🟢 **roundup compares the declared model split against the actual one.** `core/tools/wos/roundup`
   already prints the per-session split at every close; what is missing is the plan **declaring its
   expected split** and roundup comparing. It forces nobody to delegate — it makes deviation visible
   and dated instead of invisible, and needs no new instrument.
   Declared: [`core/SPECS-discipline.md`](core/SPECS-discipline.md) § AD-17. → **tier: medium**.
5. 🟢 **import the auto-trigger.** `/craft` must be typed, which is the missing half of AD-17: the
   assignment is carried at plan time and no executor reads it outside the flow. The mechanism
   imports without the methodology — the rest of that repo stays under § Rejected.
   Declared: [`core/flows/craft/SPECS.md`](core/flows/craft/SPECS.md) § Judged against Superpowers.
   → **tier: medium**.

**The generalising fix, flagged and deliberately not taken:** a Tier 0 check asserting that every
check named in a `SPECS.md` § has an implementing file. It would enforce exactly the drift that
produced this section — and it costs one more row, so it is Lucas's call rather than a decision made
in passing while cleaning up.
