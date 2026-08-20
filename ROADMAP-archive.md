# Archive
> What is NOT being worked on, and what would change that? Three kinds: blocked on a named
> trigger, parked as out of scope, killed outright — each keeping its reason so a dead idea cannot
> return looking new. Read it before proposing something that sounds obvious; nothing here counts
> toward the drain, so Open reads empty.

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
  [`code/SPECS-style.md`](code/SPECS-style.md) § Splitting an over-full directory — five rules, each of which
  cost a session to find.
  → **trigger: the parallel isoroll session refiles its own drift.** `isoroll-content/src/pipeline`
  and `isoroll-module/src/render` and their siblings, plus the one file over `BLOCK_LINES`; writing
  into those checkouts from here is the mid-flight collision the git-integrity criterion exists to
  prevent. Then: add fanout to `core/hooks/checks/` beside the type gate and delete `BASELINE` from
  `test_entropy_fanout.py` in the same commit. → **tier: medium**, one repo at a time.

- **The nested-repo majority of the first-line-comment queue.** Sized against
  [`ISSUES.md`](ISSUES.md), after re-running the generator — every marker drained so far was a file
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
  [`ISSUES.md`](ISSUES.md) under the criterion-1 baseline rule.
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

- **Adopting `obra/Superpowers` in place of our craft flow** — same arc, but its uniform subagent
  dispatch has no per-task tier/effort routing and no file-relayed Carry, the two mechanisms built
  for quota rather than developer time. Its *trigger* is imported instead
  (`core/flows/craft/SPECS.md`).
- **Gating on the presence of an adversarial step** — the originally proposed shape; an adversary
  always finds something, so the gate is a loop with no exit. What is gated is the **bound** (exit
  condition + numeric cap), which is what makes requiring the step safe.
- **INBOX provenance probe** — Front 1 shipped; the probe measures a threat model already ruled inert.
- **SLM confirmation run** — depends on `dobra` maturity that does not exist; the preprint stays
  provisional, which is fine.
- **Tier 1 periodic cheap-agent detectors** (gold tasks, scheduled `/dedup`, misplacement audit) —
  paid detection of what Tier 0 catches free.
- **Tier 2 `/tidy` skill** — a new skill to do what a human can do directly from the dashboard; scatter.
- **High-coupling / import-graph detection** — no evidence coupling is hurting anything.
- **Anti-entropy prior-art research lead** — a reading list, not work.
- **Anti-collapse edit gate** — self-declared optional, touches the edit path, guards a failure never observed here.
- **`/inbox` offers `/compass` on a trigger** — speculative UX on the one path whose whole virtue is being cheap.
- **`>routing` tier·effort metadata on goal files** — metadata for a router that reads fine without it.
- **Model-routing strategy doc** — the routing that pays is already in the per-step model tags and `/prepare`.
- **Benchmark craft flow vs SOTA repos** — expensive comparison against repos with different cost priorities.
- **Triggers after a limit window renews** — infrastructure to wake a dead session; `ScheduleWakeup`
  covers the live case.
- **`[task-metric]` closed-vs-created instrument** — measuring the ledger is more ledger; the honest
  signal is Lucas saying he feels lost, and he does say it.
- **Retroactive ref→task pairing** — the policy holds going forward; old unpaired refs can rot.
- **Scaffold update log** (`core/SCAFFOLD-LOG.md`) — the paper thread; git plus this file already
  carry trigger→change. Revisit only if a paper is actually written.
- **Shipping `codeburn` as a workspace feature** — an external npm binary we do not author, wired
  into no gate, run by hand. Ruled 2026-08-17: the registry names what this workspace can switch off
  in order to measure it, and there is no rule of ours to disable. Deleted from `SETUP.md`,
  `core/features.txt` and `core/profile.txt` together, which keeps the step ⟺ feature join intact.
  Install it as a personal tool if you want it.
- **Downloads unification across devices** — cross-device config, life logistics, not scaffold.
- **Dated `GOALS.md` attention re-check** — a calendar reminder for 2026-08-06, not a ledger row.
  Verified *not* a live bug; the 14-day window washes the old history out on its own.
- **opencode + copilot parity** — aiwbot's own premise; lives in `code/aiwbot/ROADMAP.md`.
- **Nested-repo git graph in VSCode** — IDE trivia.
- **Google Slides API + slide templates** — content tooling.
- **Mobile INBOX Android app** — aiwbot is already the away-from-PC front door.
- **`brain` coverage sweep** (`[brain-full-files]`, `[branches-coverage]`) — content completeness, not scaffold.
- **English-learning mode** — was disabled once already; weak signal.
- **aiwbot as away-from-PC front door** — a pointer to another ROADMAP is a duplicate by definition.
- **Extract the "10 GitHub repos that replace paid tools" list** — a listicle.
- **Evaluate Surfsense** — our `core/tools/web/{search,fetch}` + `core/tools/paper/{papers,parse}` +
  research flow already cover it.
- **Research-flow hallucination audit** — real but unforced; no observed fabrication.
- **`pre-edit.py` vs `check-line-counts.sh` scope disagreement** — policy nit, no live symptom.
- **`core/tools/paper/papers --ss` live smoke** — it will smoke itself on the next real use.
- **Commit the `.claude/commands/{drive,calendar}.md` symlinks** — done inline rather than tracked.
- **`/caveman compress` on workspace docs** — piloted on the worst offender: 8571 → 8552 chars,
  **0.22%**, for one full quota call. The docs have no lexical fat, so placement beats phrasing and
  compression stays the last step on an already-reduced surface (core/SCHEMA-placement.md § Placement).
- **A media-host allowlist for INBOX link extraction** — deciding which links the video tool runs
  from a list of known hosts (instagram/youtube/tiktok/…) is faster, and the list rots into exactly
  the silent skip the batch fix exists to kill. Every link is attempted; one with no media falls
  back to `core/tools/web/fetch`.
- **A `Write`-over-an-open-path gate** — its case was cost, and the cost is ~1% of spend once the
  re-read multiplier was corrected from 5.8x to 1.9x. The heredoc half shipped, on the governance
  grounds it never lost.
- **Lowering `effort` to shorten output** — rejected as a *length* lever (it does not reliably move
  visible output) and that still holds. It is **not** rejected as a cost lever; that is Front 9.9.
- **A global terseness rule** — a wrong token budget degrades the answer (ACL Findings 2025).
- **LLMLingua-style prompt compression** — it compresses a request before sending, and the harness owns our request.
- **A "match deliverable length to the task" rule in `AGENTS.md`** — `Write` arguments are 25.3% of
  *logged* output, which is 35% of billed output, which is 12.9% of spend: **~1% of the bill**,
  bought with one more always-loaded paragraph asking for restraint. INDUCED loses to ENFORCED, and
  this front already paid to learn it.
- **The "delete verification scaffolding" prompt sweep** — audited 2026-08-17 and the corpus is
  already clean: every `verify`/`confirm` in `AGENTS.md`, `core/skills/` and `core/agents/` names a
  specific probe (`install.md`'s Verify step, `lead.md`'s file-exists check), not the generic
  self-checking Opus 5 over-runs on.
- **The ~8% unexplained spend gap between `usage` and the one-off script** — the premise is void.
  Both summed transcript records instead of API responses, so they agreed on shares while being
  1.97x wrong together, and the agreement is what stopped anyone looking. Absolute spend is list
  price and has never been checked against a bill; that is the only caveat left.
