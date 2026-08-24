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

2. 🟡 **the count's biggest jump has never been separated into scope and rot.** The trend line now
   prints, so the count can no longer be called flat when it is not — but the reporting fix answered
   the smaller half. The count went ~95 (2026-08-13) to 297 (2026-08-14) in one day, and that day is
   also the day the scan went `nested=True` and new checks were added. **Part of that step is almost
   certainly scope, not drift, and nobody has checked which part.** Until someone does, the trend
   line's own baseline is a number of unknown meaning: it may be measuring a smaller tree rather than
   a cleaner one. Re-derive by running today's checks over that day's tree, or by re-running that
   day's check set over today's — either direction separates the two. The answer decides whether the
   remaining findings are a cleanup or a reporting artifact. → **tier: medium**.

   *Filed 2026-08-24 when the reporting half shipped. It was a sub-clause of the item that closed,
   and closing that item would have deleted this question with it — which is the failure the
   delete-on-completion policy is one edit away from causing every time an item holds two questions.*

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

---
## Rejected

- **Splitting `core/hooks/entropy/` four-and-four, shape against text** (2026-08-24). The seam was
  real — `corpus`/`naming`/`fanout`/`size` read the tree's shape, `context`/`ledger`/`stores`/`vendor`
  read its text — but costing it showed the hop removes less table than it adds, and the dashboard
  would import from two places to buy nothing. The directory holds over the fanout signal on purpose;
  the reason lives in its own `CONTEXT.md`.
- **Giving `core/` and `brain/` their own `ISSUES.md`** (2026-08-24). Both are parts of WOS, so the
  workspace repo's ledger covers them. The evidence that settled it: between them they hold 160
  findings and **not one hand-written bug** — 152 are size signals — so the two files would have held
  nothing but generated warnings. Fourteen ledgers, not sixteen.
