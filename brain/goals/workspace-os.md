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
make it.** Open [/ROADMAP.md](../../ROADMAP.md) § Git & sync integrity and read the one paragraph about
`branches/casinhas`: `modelo/sketchup-referencia/volume-lucas-v04.skp` is **199 MB**, over GitHub's
hard 100 MB limit, so the push is rejected outright. Three ways out, and you only have to point at one:

1. **Git LFS** for `*.skp` — keeps the file in the repo, needs `git lfs migrate import`, rewrites history.
2. **Drop the binary from history**, keep it local via `.gitignore` — also rewrites history.
3. **Leave the repo local** and carve criterion 3 to exclude it deliberately — no rewrite, and the
   criterion stays honest because the exclusion is written down rather than assumed.

Read the paragraph, say a number. **5 minutes, zero typing.** Criterion 3 goes green mechanically
after that, and criterion 4 (clonability — SETUP split + declared deps) is sonnet-tier from there.

**Known risk — dataset with no live backup:** `datasets/relativistic_raytracer` (5.8 GB) is the sole
surviving copy of its data — Zenodo record 20240662 returns HTTP 410 ("personal-data"), gone since
2026-05-24. The `datasets/*/CONTEXT.md` convention of "re-download from the Zenodo link" breaks
whenever the link goes dead with no live copy behind it.

**Root read**: ordering by motivation wins over deadline pressure — the gentle-resurfacing rhythm
that capture alone couldn't provide now lives in `/compass`.

>**timing**  
*target · first validated version in ~6 months (around November 2026)  
anchor · none external  
closure · using the system daily without friction, all domains covered, trust established  
tolerance · timeline is aspirational — what matters is direction, not date  
fallback · iterate — MVP can always be extended*

## backlog

> [ ] [v1] the four-criterion gate — see [/ROADMAP.md](../../ROADMAP.md) § v1 definition of done  
> [ ] [mvp-validate] use the system daily for 30 days, then assess: does it reduce mental load? By definition post-v1 — this is the achievement v1 exists to make measurable  
> [ ] [daily-use] the practical layer actually gets used — TODO redesign, dashboard freshness, mobile capture (ROADMAP § The ledger discipline)  
> [ ] [domain-coverage] `branches/` covers all active life domains and every `GOALS.md` stub has a real goal file (ROADMAP § the .md type system)  
> [ ] [content-in] course materials and Google Drive brought in under a decided strategy (ROADMAP § Parked, until v1)  
> [ ] [offline-resilient] survives a world without internet — Reticulum for network, Kiwix for corpus (parked, ROADMAP § Parked)  

## done

<!-- done:start -->

> [x] [mvp-gaps] DONE 2026-07-22 — all 3 gaps localized with hard numbers (see findings above): (1) `core/hooks` overengineering (~40 files / 3068 LOC), (2) 14 GB workspace-root cruft (`.Trash-1000` + root `.venv`), (3) reframed to the missing gentle-resurfacing rhythm → shipped as the `/compass` fold. Closed via `/compass`, first dogfood of the new skill.
> [x] [v1-strong] DONE 2026-07-29 — superseded by the explicit [v1] gate. Its three parts each landed or moved: cruft reclaimed (6.6 GB, gap 2), hooks de-overengineered (gap 1, and the diagnosis partly reversed — most "duplicate families" were live), telegram_daemon retired into `code/aiwbot`. What remained became ROADMAP Frentes 6 and 12.8.
> [x] [roadmap-entrypoint] DONE 2026-07-29 — wos work collapsed from four overlapping ledgers (~94 items, 789 lines, four of them already false) into one: `/ROADMAP.md`. Goal file = why, `brain/TODO.md` = life, `core/ROADMAP.md` = library. Deletion policy set: hard delete, git is the history. Discipline now tracked as ROADMAP § The ledger discipline.<!-- done:end -->

## stats
<!-- stats:start -->
last-touch: 2026-08-16  ·  trend: advancing

| period      | touches |
|-------------|----------|
| month       |     193 |
| trimester   |     237 |
| semester    |     252 |
| year        |     252 |
| 2-year      |     252 |
| 4-year      |     252 |
<!-- stats:end -->
