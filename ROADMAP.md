# Workspace-OS Robustness Roadmap
> The v1-strong push: turn the workspace scaffold into something that survives weaker models, untrusted input, and its own drift. Goal: [workspace-os](brain/goals/workspace-os.md). Reference evidence: [core/refs/REFS.md](core/refs/REFS.md).

## How to read this

Each frente (front) below is a self-contained line of work with numbered steps. Every step
carries two tags:

- **model** — which tier is enough: `haiku` (mechanical), `sonnet` (normal engineering /
  writing), `opus` (design, security, cross-cutting judgment). This is the *floor* — a
  bigger model always works, it just costs more.
- **switch** — how to get that model onto that step (see the switching guide at the bottom).

**Impact flags** mark steps that change shared behavior and therefore **need discussion +
more evidence before shipping**, not just implementation:

- 🔴 **decide-first** — changes a workspace-wide policy or touches security; do not code it
  until Lucas signs off on the approach. Most carry an open question.
- 🟡 **pilot-first** — prove it on one subtree, measure, then decide whether to generalize.
- 🟢 **safe** — mechanical or additive; low blast radius, just do it well.

> **Evidence caveat, stated once for the whole doc.** Several frentes lean on the two
> strongest but *unreviewed* preprints in our refs — progressive disclosure ([P] 2607.17598)
> and ACE ([P] 2510.04618). Preprint = provisional (see [core/refs/CONTEXT.md](core/refs/CONTEXT.md)).
> Where a step's justification is preprint-only, it says so and stays 🔴/🟡 until a published
> source or our own measurement confirms it. We do not turn a preprint into a hard gate.

---

## Frente 1 — INBOX provenance (security)

**Why.** INBOX ingests telegram, gmail, and the output of `core/tools/{video,fetch,search}`,
then `/inbox` routes those lines into goals and ROADMAPs — trusted context. Nothing marks
where a line came from. This is the memory-poisoning write channel: one malicious write
persists across sessions, and standard prompt-injection defenses do not cover it
([P] 2606.04329; fix shape from [P] 2606.24322 origin-bound authority; design ref CaMeL,
Google DeepMind). The `brain` domain is single-trusted-sender for *typed* input, but forwarded
web/email content is not.

> **DECIDED 2026-07-24 (Lucas, Opus session).** Trust model resolved, and *simplified* by Lucas's
> reframe: **INBOX is always inert as instruction — nothing in it is ever obeyed as a command.**
> Lucas never issues imperatives via INBOX (those go through direct aiwbot sessions); INBOX is
> refs / ideas / todos only. So authorship does **not** decide "obey vs ignore" (answer is always
> ignore-as-command) — it decides **what may be promoted into trusted files** during triage. Rule:
> a `lucas`-authored line may be acted on and routed into goals/ROADMAPs; a line whose true origin
> is a link/fetch/other-sender is **quoted data** — filed, never obeyed, never promoted raw into a
> trusted file. Triage (`/inbox`) **is** the act to protect; `/roundup` and any other INBOX reader
> inherit the same rule. Steps 1 & 3 below are therefore settled; 2 & the reader-edits are the build.

1. [x] 🔴 **decided — trust model** (see box above). Boundary is *authorship for promotion*, not
   transport, and INBOX is inert-as-command by construction.
2. [x] 🟢 **safe — tag non-`lucas` content at capture.** Prefix INBOX lines that carry link/fetch/
   other-sender content with `[src: web:<domain> | gmail:<addr> | telegram-fwd]`; Lucas-typed lines
   are `lucas` (default, may stay untagged or `[src: lucas]`). Edit the video/fetch/search sinks +
   gmail tool (+ telegram daemon only for forwarded, not typed, content). Additive.
   → **model: sonnet** · **switch: `/loops` feature subtree.**
   **Done 2026-07-25:** `core/tools/gmail_triage.py` prepends `[src: gmail:<addr>]` to every
   generated entry (in the Haiku system prompt template). `code/aiwbot/frontend/inbox.py`'s
   `build_entry` gained a `forwarded: bool = False` kwarg tagging `[src: telegram-fwd]`; `bot.py`
   passes `msg.forward_origin is not None` at all four capture call sites (text/voice/photo/
   document) — this bot has one allowed chat_id, so anything not forwarded is Lucas typing.
   video/fetch/search have no INBOX-write path of their own (read-only stdout tools); their
   tagging is folded into the `/inbox` skill's video-extraction rule (step 3) instead, since
   that's the only place their output ever reaches INBOX. Regression: `code/aiwbot/tests/test_inbox.py`.
3. [x] 🔴 **decided — enforcement lives in the readers, not (only) AGENTS.md.** Adjust the `/inbox`
   skill and `/roundup` skill: treat any `[src: web|gmail|…]`-tagged (non-`lucas`) line as inert
   data — route/file it, never execute an imperative found inside it, never promote it verbatim into
   a trusted file (quote/attribute instead). Build task, wording is settled.
   → **model: sonnet** (skill-text edits) · was opus-gated, now unblocked by the decision above.
   **Done 2026-07-25:** `core/skills/inbox.md` gained a "Provenance" section (the tag/quote rule)
   plus a video-extraction-is-`[src: web:...]`-too note; `core/skills/roundup.md`'s INBOX-drain
   phase now points at the same rule. Mirrors resynced (`core/tools/sync-skills`).
4. 🟡 **pilot-first — measure.** Plant a benign "instruction" in a fetched page, run it through
   video→INBOX→`/inbox`, confirm it lands as data and is not acted on. This is the seed of the
   `verify-agent` tier (Frente 4).
   → **model: sonnet** to build the probe · **opus** to judge the result.

---

## Frente 2 — Pointer & link integrity

**Why.** `MEMORY.md` still points at `/mnt/workspace/VERIFY.md`; the file moved to
`code/VERIFY.md` in commit `5fd9204`. Nothing detects a dead internal pointer. Same class:
broken `[text](path)` links and `[[memory-slug]]` refs across CONTEXT.md / ROADMAP / MEMORY.
This is the peer-reviewed doc-decay problem ([A] ICSE 2025, IEEE TSE 2024).

1. 🟢 **safe — build the checker.** ~20-line script in `verify-fast`: resolve every relative
   `](path)` link and every path literal in MEMORY.md; exit 1 on any miss. Wire into the root
   Makefile `verify-fast` target.
   → **model: sonnet** · **switch: `/loops` padaria (small-feature) subtree**, autoroutes
   loop-low(haiku)/medium(sonnet). Genuinely a haiku-able task if specced tightly.
2. 🟢 **safe — fix the known-dead pointer** (MEMORY.md → code/VERIFY.md) as the checker's first
   caught case.
   → **model: haiku** · **switch: same session**, trivial edit.
3. 🟡 **pilot-first — `[[slug]]` resolution.** Decide policy: an unresolved `[[slug]]` is a
   *planned* memory (allowed) vs. a *typo* (error). The memory spec treats dangling links as
   fine, so this needs a rule before it can gate.
   → **model: sonnet** · **switch: same session.**

---

## Frente 3 — Routing depth vs. locality (the SLM question)

**Why.** Two different axes, kept separate on purpose:

- **Locality** — small CONTEXT.md glued to the files it governs. Evidence ([P] 2607.17598,
  controlled, on haiku-4.5 + qwen3.6-27b): *"the weaker the agent's native navigation, the
  earlier the skill pack earns its keep"*; the flat pack hits ~2× accuracy at ½ the tokens vs.
  raw at corpus scale, and the always-loaded index is the most cache-friendly input. **For a
  workspace that must run on Sonnet and SLMs, scattered local CONTEXT.md is not overhead — it
  is what makes weak models work, and it is cheaper.** → keep it.
- **Depth** — how many hops to content. Same paper: a second routing level is *not* uniformly
  free; it hurt some tasks, helped open-QA. Cost is task- and scale-specific.

**Net:** the rodada-1 "flatten everything" was wrong for locality, right only for depth — and
even depth is now "measure per task", not "decree".

1. [x] 🔴 **DECIDED + WRITTEN 2026-07-24, INDUCED 2026-07-25.** Policy recorded in
   [SCHEMA.md](core/SCHEMA.md) § *Routing depth and locality*: keep CONTEXT.md local and granular
   (locality is what makes weak models work + is the most cache-friendly input — [P] 2607.17598);
   cap **chain depth**, not file count; measure before adding a routing level. **Induction fix
   (2026-07-25):** the full policy sat only in `core/SCHEMA.md` — a cold, core-scoped doc that a
   cross-subtree agent never loads, so it was written but not *induced where needed*. Promoted the
   rule to [AGENTS.md](AGENTS.md) (the always-read root), which folds F5's size-as-signal into the
   same bullet; SCHEMA.md keeps the evidence + preprint caveat. Still **not enforced** (no depth
   check) — enforcement is Frente 4 Tier 0.
2. 🟡 **pilot-first — measure our own depth.** Instrument what actually loads at session start
   (AGENTS.md chain + every CONTEXT.md on a typical path + memory) and the real hop count to a
   leaf. This is the existing `core/ROADMAP.md` "Audit context building" item — merge, don't
   duplicate. Decide per-path if any level is dead weight.
   → **model: sonnet** to instrument + tabulate · **opus** to read the tradeoff.
3. 🟡 **pilot-first — SLM confirmation run.** Before trusting the preprint on *our* content,
   run one real task on a small model (via `code/dobra` / opencode) against the flat vs. nested
   layout, our files, and compare. Ties into loop-engineering `[A2] opencode-reliability`.
   → **model: sonnet** to design + judge · execution is *by* the SLM under test.

---

## Frente 4 — workspace anti-entropy (reframed 2026-07-24)

> **Reframed by Lucas, 2026-07-24.** The original frente was "verify-agent: 5 behavioral gold
> tasks". Lucas widened it to the real target: the recurring decay he has flagged repeatedly —
> **files grow, scatter, duplicate, and drift from naming/structure patterns.** verify-agent is now
> *one detector inside* a three-tier strategy, not the whole frente.

**The frame (the load-bearing idea): structure is a spec; drift is a test failure.** `code/` already
has this (the `> spec:` gate); the agent library has it ([SCHEMA.md](core/SCHEMA.md), frontmatter).
Nothing governs the **shape of the workspace itself** — naming, placement, size, pointers,
redundancy. Promote structural soundness to a first-class enforced spec, checked like code. This
**subsumes** Frente 2 (pointer integrity), Frente 5 (size reframe), and three `brain/TODO.md` items
(200-LOC-.md, filename enforcement, "standardization as a recurring need → skill"). One concept.

**Why.** The self-improvement survey ([P] 2607.13104) names evaluation as *the* open problem for
scaffolds; practitioner tools (claudemd-check, agenteval, instrlint) only lint text. Anti-entropy is
broader than eval — it is detection + consolidation across the whole tree.

**Cost-ordered by Lucas's rule "automatic + zero-token beats agent-checked":**

1. 🟢 **Tier 0 — per-commit, zero-token, deterministic.** No LLM. Scripts in the pre-commit/verify
   path: **naming** (kebab-case, full words not truncations — the `architect`>`arch` rule made
   machine-checkable); **placement** (a file's location matches its declared type — extend
   `sync-skills`); **pointer integrity** (= Frente 2, every `](path)`/`[[slug]]` resolves); **size as
   a *signal not a cap*** — warn-for-delta-review when a *curated* doc crosses a threshold, **never
   force-summarize** (ACE brevity-bias trap, [P] 2510.04618 — this is Frente 5 made concrete); the
   **Frente-6 self-healing allowlist**. Emits into the dashboard (below).
   → **model: sonnet** · **switch: `/loops`.**
2. 🟡 **Tier 1 — periodic, cheap-agent, `/compass`-cadence.** The token-costing checks, **separated
   from Tier 0** (Lucas: free checks must not be coupled to paid ones) and run weekly / opt-in / on
   the `/loop` scheduler — *not* every commit, nothing here is critical-often. On sonnet/haiku,
   **through the aiwbot backend so it is harness-portable** (opencode/kimicode — Lucas's requirement;
   the Agent-tool runner would Claude-Code-lock it). Detectors: **behavioral gold tasks** (routing
   correctness — cold subagent, **substring-assert** grading per Lucas, start with **3** tasks not 5,
   seed = the Frente-1 provenance probe); **semantic scatter/redundancy** (schedule the existing
   `/dedup`, don't run per-commit); **misplacement audit** (does each doc still match its folder's
   `CONTEXT.md` charter?).
   → **model: sonnet** runner + judge · graded subagents run at the tier under test.
3. 🟡 **Tier 2 — on-demand, human-triggered: a `/tidy` skill (Opus judgment).** Reads the cached
   Tier-0/1 findings and does the *consolidation* — merge / move / rename / delete — as **curated
   delta, not monolithic rewrite** (ACE context-collapse). This is the "standardization skill" TODO
   given a precise job. Only runs when Lucas chooses.
   → **model: opus** · **switch: same session or `/loops` high tier.**
4. 🟢 **The unifying artifact — an entropy dashboard.** One generated report written by the automatic
   Tier-0/1 checks: naming violations, oversized curated docs, dead pointers, dup candidates,
   misplaced files. Agents and Lucas read the **dashboard** (pre-computed, cheap), never re-scan the
   tree. Detection is automatic and cached; only the Tier-2 *decision* costs tokens — the
   "automatic + zero-token" principle applied to entropy itself.
   → **model: sonnet** · **switch: `/loops`.**

**Research lead (offered, not yet run — budget).** Two on-point links already in `brain/INBOX.md`
(`awesome-harness-engineering`, `best-of-Agent-Harnesses`) + the core/ROADMAP "survey outside skills"
item. Mine them for prior-art anti-entropy tooling on a **Sonnet** subagent (spare Opus credits)
before building Tier 0.

---

## Frente 5 — Anti-collapse: size policy reframe

**Why.** TODO.md backlog carries "consider a 200-LOC limit for `.md` files too". ACE
([P] 2510.04618) measures the opposite failure: **brevity bias** (a summary drops the domain
heuristic that mattered) and **context collapse** (monolithic rewrite erodes a doc until
performance falls off a cliff). The fix is *incremental delta*, not a size cap that forces
summarizing.

1. [x] 🔴 **DECIDED 2026-07-24.** Reframe applied: split-by-navigation (many small linked files) =
   yes; hard line-cap that forces a curated ROADMAP/CONTEXT to be summarized = no (ACE brevity-bias +
   context-collapse, [P] 2510.04618). `brain/TODO.md` line 120 rewritten to say this. The enforcement
   home is **Frente 4 Tier 0** — size becomes a *delta-review signal*, never a cap. This step is now
   a pointer into that frente, not standalone work.
2. 🟡 **pilot-first — anti-collapse gate (optional).** A hook that flags an edit shrinking a
   curated `.md` above X% without an explicit `consolidate:` intent, forcing append-delta as
   the default. Needs the Frente-3 audit first to know which files are "curated". Impact:
   touches the edit path.
   → **model: sonnet** to build · **opus** to set the threshold + exemptions.

---

## Frente 6 — Hygiene (fast, low-risk)

1. 🟢 **safe — clean the goal file.** `brain/goals/workspace-os.md` is 23.6 KB and embeds a
   superseded 12-step Telegram-bot plan (lines 58-75), which the aiwbot rebuild replaced. Move
   the live remnant to `code/aiwbot/ROADMAP.md` or delete it with a one-line rejection note
   (per [[feedback_delete_weak_features]]). AGENTS.md says plans live in roadmaps, not goal
   files.
   → **model: sonnet** · **switch: same session.**
2. [x] 🔴 **DECIDED 2026-07-24 — self-healing allowlist, not a warn-gate.** `.gitignore` uses a
   `core/*` denylist with an explicit allowlist, so **any new `core/` subdir is silently untracked**
   → invisible on the second machine (already bit `core/refs/`). Lucas rejected a warn-gate — warnings
   nag forever, force agents to open `.gitignore`, and breed fatigue. **Chosen design (automatic,
   zero-token, zero-warning):** a pre-commit hook detects any new domain subdir that **contains a
   `CONTEXT.md`** (the existing "this is structural" signal) but lacks its `!core/<dir>/` allow line,
   then **adds the line itself and stages it** — self-heal, no human/agent action. A subdir with no
   `CONTEXT.md` stays ignored (correctly project-internal/scratch). The rare "structural but
   deliberately ignored" case warns **once** and is recorded in a resolved-list so it never re-fires.
   *Note: the WATCHLIST-ignored TODO this referenced is already fixed — `!core/WATCHLIST.md` is on
   `.gitignore:107`; clear brain/TODO.md line 128.*
   → **model: sonnet** — ~15-line hook addition; the rule (CONTEXT.md ⟺ tracked) is settled.
   **Done 2026-07-25:** `.hooks/gitignore-self-heal.sh`, wired into `.hooks/pre-commit` (§0b,
   guarded to the workspace repo only — this hook file is global via `core.hooksPath`). Generalized
   beyond `core/*` to every domain using the same denylist pattern (`code/`, `academy/`, `branches/`,
   `brain/`, `models/`, `datasets/`) — same bug, same fix, no reason to special-case core. Exceptions
   list at `.hooks/gitignore-exceptions.txt`. Regression: `core/tools/test/test_gitignore_self_heal.py`.
   **First run on the real repo found the bug live, at scale — 20 subdirs across `code/`, `academy/`,
   `branches/`, `core/` were silently untracked** (`code/aiwbot`, `dobra`, `spacemantics`, `apptime`,
   `corpora`, `flows`, `futebots`, `isometric-perspective`, `isoroll-content`, `isoroll-module`, `ppc`,
   `prog1`, `programacao1`, `shortvid`, `voti`; `academy/administration`, `refs`, `talks`, `teaching`;
   `branches/ecovila`; `core/prompts`) — invisible on the second machine this whole time. Of those,
   15 `code/` entries are own-repo projects (AGENTS.md) and get the narrow triplet (`!dir/` +
   `dir/*` + `!dir/CONTEXT.md`, matching the existing laplata/gira/cria shape — the script checks
   for a nested `.git` and branches on it); the other 5 (`academy/{administration,refs,talks,
   teaching}`, `branches/ecovila`, `core/prompts`, `code/{prog1,programacao1}`) are plain content
   dirs and get the bare unignore, full content trackable. `.gitignore` now allowlists all of them
   (staged); their contents still show `??` (untracked) — **not staged or committed**, that's a
   separate, much bigger call Lucas should make deliberately, not something to fold into this fix
   silently.
3. 🟢 **safe — re-measure the doc count.** Goal file claims "617 curated `.md`"; a sweep today
   (excluding `.venv`/`.git`/`node_modules`) counts 2266. Either the old number was wrong or it
   tripled; gap-2 was closed on that number. Re-measure and correct the goal file before
   declaring v1.
   → **model: haiku** · **switch: same session** (one `find | wc` + an edit).

---

## Frente 7 — Scaffold update log (optional; paper thread)

**Why.** The survey ([P] 2607.13104) frames the workspace as a *scaffold* and Lucas as the
*update operator*. Git records *what* changed, not *what signal motivated it* or *whether it
worked*. A `core/SCAFFOLD-LOG.md` (one line per scaffold change: trigger → change → outcome)
closes that. Bonus: no published longitudinal study of one real user evolving an agent scaffold
exists — this is paper-shaped, and Lucas runs a Hybrid Intelligence lab. Ties to
[[project_dobra]] and the `spec-driven-development` goal.

1. 🟡 **pilot-first — decide if it earns its keep.** A log only helps if it is actually
   written. Trial: append one line per scaffold change for two weeks, see if it gets used.
   → **model: sonnet** · **switch: same session.** Defer until Frentes 1-6 settle.

---

## Sequencing (recommended)

> Updated 2026-07-24: all six 🔴 decide-first steps are now **settled** (Frentes 1, 3, 5, 6 fully;
> Frente 4 reframed to *workspace anti-entropy*, which **subsumes Frente 2 and Frente 5**). What
> remains is build work, all Sonnet/Haiku tier — no Opus judgment left gated. Order by
> (impact × cheapness) ÷ risk:

1. **Frente 1** (provenance) — only real security gap, and cheap. Build: tag non-`lucas` at capture
   + adjust `/inbox` + `/roundup` readers.
2. **Frente 6** (hygiene) — self-healing allowlist hook + doc-count re-measure; clears the deck.
3. **Frente 4 Tier 0** (anti-entropy, deterministic) — the zero-token per-commit checks; folds in
   **Frente 2** (pointer integrity) and **Frente 5** (size-as-signal). Highest structural payoff.
4. **Frente 4 Tier 1** (periodic cheap-agent) — gold tasks + `/dedup` + misplacement, `/compass`-paced.
5. **Frente 4 Tier 2** (`/tidy`) + **entropy dashboard** — consolidation on demand.
6. **Frente 3.2** (depth audit) — the one remaining measurement step; policy already written.
7. **Frente 7** (scaffold log) — optional, the paper thread.

Frentes 1, 3, 4, 5 each open with a 🔴 **decide-first** step. Those are the discussions to have
before any code — that is the point of marking them.

---

## Model-switching guide

The per-step `model` + `switch` tags above use the workspace's canonical model-switching guide,
which lives in the reusable flow that produced this plan:
**[`core/flows/research/scout.md`](core/flows/research/scout.md) → "Canonical model-switching guide"** (same-session
`/model` · `/loops` autorouting · Agent-tool `model:` override · `/handoff`). It is methodology,
not specific to this plan, so it is not re-tabulated here.

**Mapping for this roadmap:** 🔴 decide-first steps → **Opus, same session** (judgment about
shared behavior). 🟢/🟡 build steps → **Sonnet via `/loops`** (mechanical parts drop to haiku
automatically; e.g. Frentes 1.2, 2.1, 4.3). Run **haiku deliberately** only inside the
`verify-agent` gold tasks (Frente 4.2), where the weak model is the subject under test, spawned
via the Agent-tool override.
