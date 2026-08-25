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

3. 🟢 **drain the entropy dashboard.** `make entropy` → [`ISSUES.md`](ISSUES.md) § Entropy, the whole
   workspace and its nested repos in seconds. Read the report; never re-scan the tree. **Never copy
   its counts into this file** — a copied number is the drift these checks exist to catch, and the
   summary table at the top of the report is the interface. Criterion 1 wants it reading clean.

   The dashboard scans nested repos, the **tests do not** — an assertion in this repo about
   another repo's content fails for reasons this repo cannot fix, and each nested repo runs its
   own verify. Where a check is green workspace-wide it is asserted at zero in `verify-fast`
   (retired tokens, duplicate slugs); where it is not, `test_entropy_naming.py` holds a named
   **baseline** so a new violation fails the build and a fixed one must leave the list.

8. 🟡 **the 200-line cap gate waits on five `.md` files, and every one is in a nested repo.**
   Three are `code/spacemantics`' — `dsl/SPEC.md`, `dsl/EXAMPLES.md`,
   `dsl/LEXICON.md` — and renaming them is that repo's design question, filed in its own roadmap.
   Two are `code/isoroll-content/ROADMAP.md` and `code/isoroll-module/ROADMAP.md`, whose mass is
   undeleted finished work: **cut under *completion is deletion* first, split only what is still
   over** (Lucas's ruling). Since the scatter generalised, each repo's own `ISSUES.md` carries its
   numbers. Nothing here moves until they do, so the gate flip is the last step and this row is a
   watch rather than work. → **tier: medium**.

11. 🟡 **Two rules that never met the corpus they govern.** Filed 2026-08-24, one item because they
    share that cause.
    - **The two caps pull against each other.** Wrapping
      `academy/administration/coordenacao-lc/novo-ppc-bcc/ROADMAP-ementas.md` took it from 195 to
      270 lines, past the hard 200. Reverted: it trades one finding for another and blocks the
      commit. Nothing says which cap wins when a file sits near the other.
    - **`AGENTS.md` cannot satisfy the cap** while `test_norms` reads the published block line by
      line — see § Rejected. Either that test rejoins continuations, or the most-read file in the
      workspace keeps three findings forever. → **tier: medium**.

12. 🟢 **a type that shards has no check that its siblings are tracked.** Live mechanism, found
    2026-08-20: `.gitignore` allowlists `core/` file by file under a `core/*` deny, so all eight
    `core/SCHEMA-*.md` and `core/SPECS-*.md` shards were untracked and a fresh clone got an index
    pointing at files not in the repo. Three checks were green through it — pointer integrity
    resolves against the **working tree**, `entropy_naming` sees a legal name in a legal place, and
    the `.gitignore` self-heal only re-allows a *directory* that gains a `CONTEXT.md`. The allowlist
    now names the shards by shape (`!core/SCHEMA-*.md`), but that was a hand-edit and the next type
    to shard at a domain root that is not `core/` lands in the same hole. The durable fix is a Tier 0
    check asserting that a file passing `entropy_naming.TYPE_SLUG` is not ignored. → **tier: medium**.

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

- **Shortening the frontmatter descriptions instead of exempting them** (2026-08-24). The
  alternative to the ruling that granted `over_column_cap` its third exemption: keep the cap
  absolute and rewrite all 38 over-long `description:` lines to fit. Refused because it degrades
  the field to satisfy a display rule — for the 15 `core/skills/` and `core/flows/` files the
  description **is** the model's invocation trigger, and median 156 → 120 characters is a quarter
  of the dispatch text gone; for the 23 `brain/memory/` files it is the line recall is chosen on.
  The ruling and its reasoning are `core/hooks/limits.env` § BLOCK_COLS. What the implementation
  then found is the part worth keeping: `core/tools/wos/wrap` had **already** been skipping
  frontmatter from a private list of its own, so the exemption existed and only the law was
  silent — granting it moved a rule into the law rather than adding one, and deleted the copy.

- **Cutting `entropy_fields.py` and `shard_table.py` under the 150-line warn** (2026-08-25). Both
  came down — 166→150 and 175→169 — by deleting narrative the law already carried. What is left in
  each is rationale that exists nowhere else, so reaching the number meant summarizing a rule to hit
  it. The signal asked for a review; the review is this line. Do not re-cut them.
- **Wrapping `core/norms/*.md` to the column cap** (2026-08-24). A norm is one line by contract:
  `norms.py` publishes each rule as a `- ` line into `AGENTS.md` and `test_norms` reads the block
  back the same way, so a wrapped rule loses its continuation and vanishes from the published set.
  Tried, reverted, suite green again. The three findings `AGENTS.md` carries are the price, and the
  item above holds the two ways out.
- **Splitting `core/hooks/entropy/` four-and-four, shape against text** (2026-08-24). The seam was
  real — `corpus`/`naming`/`fanout`/`size` read the tree's shape, `context`/`ledger`/`stores`/`vendor`
  read its text — but costing it showed the hop removes less table than it adds, and the dashboard
  would import from two places to buy nothing. The directory holds over the fanout signal on purpose;
  the reason lives in its own `CONTEXT.md`.
- **Giving `core/` and `brain/` their own `ISSUES.md`** (2026-08-24). Both are parts of WOS, so the
  workspace repo's ledger covers them. The evidence that settled it: between them they hold 160
  findings and **not one hand-written bug** — 152 are size signals — so the two files would have held
  nothing but generated warnings. Fourteen ledgers, not sixteen.
