# [ health | mental | year ] workspace OS

A centralized personal operating system: all thoughts, projects, demands, full-life organization in one place. Automated setup that eases how life gets managed, reduces mental pressure, and enables goals and dreams to move from idea to action. Reliable, productive, and genuinely used — not just designed. Currently in MVP prototyping phase. First validated version expected in ~6 months.

>**signals**  
transformative · essential · thrilled

>**owns**  
`core` · `ROADMAP.md` · `SETUP.md` · `AGENTS.md` · `Makefile` · `entropy.md`

>**dynamics**  
immersed mode · advancing motion · intrinsic source  
2026-07-22 compass: highest wind + in-flow this session — mvp-gaps localized then closed, gitflow enforced, gitlinks killed, `/compass` shipped. Lucas ordered it #1: make v1 strong (gaps 1&2 cleanup) + finish aiwbot.  
2026-07-29: the work is no longer *discovering* what to fix — it is draining a known list. Ledgers collapsed to one entrypoint, v1 given an explicit 4-criterion gate. Momentum now depends on the gate staying honest, not on new insight.  
2026-08-13 compass: **confirmed #1 for a second cycle, and the numbers back it — 29 of 29 workspace commits in 14 days landed here.** Hooks became a root of law plus families, 37 tools became eight, the verify suite split by what it asserts, the session got a size meter, the INBOX drained to zero. The gate held honest under all of it: criterion 3 went *backwards* on purpose when a re-audit across 25 repos found three remotes missing, rather than staying a green tick that was false. What is left is not build — it is **one decision and one mechanical frente**. This is a finish.

## selected next achievement
    [v1] pass the four-criterion v1 gate — Tier 0 anti-entropy live · one ledger, no duplicates · everything pushed and gitflow-shaped · clonable by a student

**All build work lives in [/ROADMAP.md](../../ROADMAP.md)** — the single wos ledger (12 frentes + two
ready-to-execute batches, each step tagged with model tier and impact flag). This file holds only why,
signals, dynamics, and timing. Plans do not live in goal files (AGENTS.md).

**ease-start**  
The gate is two rows from done and **one of them is a decision, not work — yours, and nobody else can
make it.** Open [/ROADMAP.md](../../ROADMAP.md) § Frente 11 and read the one paragraph about
`branches/casinhas`: `modelo/sketchup-referencia/volume-lucas-v04.skp` is **199 MB**, over GitHub's
hard 100 MB limit, so the push is rejected outright. Three ways out, and you only have to point at one:

1. **Git LFS** for `*.skp` — keeps the file in the repo, needs `git lfs migrate import`, rewrites history.
2. **Drop the binary from history**, keep it local via `.gitignore` — also rewrites history.
3. **Leave the repo local** and carve criterion 3 to exclude it deliberately — no rewrite, and the
   criterion stays honest because the exclusion is written down rather than assumed.

Read the paragraph, say a number. **5 minutes, zero typing.** Criterion 3 goes green mechanically
after that, and criterion 4 (Frente 10 — SETUP split + declared deps) is sonnet-tier from there.

**findings — the 3 original gaps, all localized (2026-07-21 sweep), all resolved or absorbed:**
1. **overengineering → the `core/hooks/` layer.** ~40 files, 3068 LOC, apparent near-duplicate families.
   Investigation reversed most of the diagnosis: `copilot-*` is LIVE (wired to the craft flow) and the
   `.pyi` mirrors are LIVE (the interface-first read-gate requires them) — not dead weight. Genuine
   cruft was one FUSE orphan. `brain_stats.py` 393 LOC was split into three files under 200, which also
   surfaced a **real bug**: the attention dashboard was measuring noise, because the hook force-`git
   add`ed all 54 goal files every commit. `telegram_daemon.py` (814 LOC) is gone entirely, replaced by
   `code/aiwbot`. **Closed 2026-07-25.**
2. **messy → uncollected garbage, not doc sprawl.** The "mess" was `.Trash-1000` (6.6 GB) and root
   `.venv` (7.6 GB) inflating every find/grep — real curated docs number **736** (measured 2026-07-29;
   earlier counts of 617 and 2266 were both wrong, one under-scoped and one counting `.venv`). 6.6 GB
   reclaimed 2026-07-22; `.venv` is live and stays. **A landmine surfaced during the purge:**
   5.8 GB of that trash was `datasets/relativistic_raytracer` — the **sole surviving copy**, since
   Zenodo record 20240662 is deleted (HTTP 410, "personal-data", 2026-05-24). Convention gap it exposed:
   `datasets/*/CONTEXT.md` promises "re-download from the Zenodo link", but a link can 410, and a
   dataset with no live copy plus a dead link is unrecoverable. **Closed 2026-07-22**; the remaining
   floor-sweeping is Frente 6.1.
3. **the gentle-resurfacing rhythm was missing.** Strong at *capture* (inbox/gmail/telegram/goals),
   but nothing gently resurfaced the *inspiring work waiting*. Explicitly **not** an accountability
   gap — that anxious tone is the opposite of this workspace's purpose ([SPECS.md](../SPECS.md) § Rationale).
   Fixed by folding motivation-ordering, timing negotiation, and guilt-free ditching into `/compass`,
   plus a soft nudge. **Closed 2026-07-22** — first dogfood of the new skill.

**Root read**: gaps 1&2 were "too much" (machinery, cruft); gap 3 was "too little", and the answer was
never to *chase* — it was to let the gentle partner resurface good wind on a soft rhythm. Ordering by
motivation wins over deadline pressure.

>**timing**  
*target · first validated version in ~6 months (around November 2026)  
anchor · none external  
closure · using the system daily without friction, all domains covered, trust established  
tolerance · timeline is aspirational — what matters is direction, not date  
fallback · iterate — MVP can always be extended*

## backlog

> [ ] [v1] the four-criterion gate — see [/ROADMAP.md](../../ROADMAP.md) § v1 definition of done  
> [ ] [mvp-validate] use the system daily for 30 days, then assess: does it reduce mental load? By definition post-v1 — this is the achievement v1 exists to make measurable  
> [ ] [daily-use] the practical layer actually gets used — TODO redesign, dashboard freshness, mobile capture (ROADMAP Frente 8 + 12.5)  
> [ ] [domain-coverage] `branches/` covers all active life domains and every `GOALS.md` stub has a real goal file (ROADMAP Frente 12.6)  
> [ ] [content-in] course materials and Google Drive brought in under a decided strategy (ROADMAP Frente 12.1, parked until v1)  
> [ ] [offline-resilient] survives a world without internet — Reticulum for network, Kiwix for corpus (parked, ROADMAP § Parked)  

## done

<!-- done:start -->

> [x] [mvp-gaps] DONE 2026-07-22 — all 3 gaps localized with hard numbers (see findings above): (1) `core/hooks` overengineering (~40 files / 3068 LOC), (2) 14 GB workspace-root cruft (`.Trash-1000` + root `.venv`), (3) reframed to the missing gentle-resurfacing rhythm → shipped as the `/compass` fold. Closed via `/compass`, first dogfood of the new skill.
> [x] [v1-strong] DONE 2026-07-29 — superseded by the explicit [v1] gate. Its three parts each landed or moved: cruft reclaimed (6.6 GB, gap 2), hooks de-overengineered (gap 1, and the diagnosis partly reversed — most "duplicate families" were live), telegram_daemon retired into `code/aiwbot`. What remained became ROADMAP Frentes 6 and 12.8.
> [x] [roadmap-entrypoint] DONE 2026-07-29 — wos work collapsed from four overlapping ledgers (~94 items, 789 lines, four of them already false) into one: `/ROADMAP.md`. Goal file = why, `brain/TODO.md` = life, `core/ROADMAP.md` = library. Deletion policy set: hard delete, git is the history. Discipline now tracked as ROADMAP Frente 8.<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-08-14  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |     116 |
| trimester   |     165 |
| semester    |     175 |
| year        |     175 |
| 2-year      |     175 |
| 4-year      |     175 |
<!-- stats:end -->
