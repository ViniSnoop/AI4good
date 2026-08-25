# Placement and routing
> Which directory a file belongs in, and how deep the routing may go.
> answers: where a file lives, how many hops to content, when a directory splits
> enforced-by: core/hooks/entropy/entropy_naming.py, core/hooks/entropy/entropy_fanout.py

### Placement: tier × read-frequency

§ Boundaries answers *which of two types*. This answers the prior question: **does this content earn
its place, and where does it belong?** Deleting is one of four outcomes, not the default one.

**Tier — ask what happens to an agent that never reads this.** Applied per *section*, never per file:

| Tier | Test | What it costs to carry |
|------|------|------------------------|
| **ESSENTIAL** | work comes out **wrong** — a rule broken, the wrong file edited, work lost | must be paid; put it where it is read without asking |
| **IMPORTANT** | work comes out **slower** — re-derived, re-asked, rediscovered | one hop away, never preloaded |
| **DESIRABLE** | **nothing changes** — rationale, provenance, the story of a change | git already holds it |

That question runs second. The first is **is it still true?** — checked against code, tests and
`git log`, not memory. An untrue ESSENTIAL is the most expensive object in the workspace.

**Read-frequency is a property of the enforcement layer, not a guess.**

| | Types | Why |
|---|---|---|
| **HOT** | `CONTEXT.md` | the only **enforced-read** type: `hooks/read/context-gate.py` demands the whole chain before any file access in a subtree |
| | `AGENTS.md`, `MEMORY.md` | folded into the system prompt every session |
| | `GOALS.md`, `ROADMAP.md` | induced-hot — the root `README.md` sends every reader to them first |
| **COLD** | `SPECS.md`, `REFS.md`, `ISSUES.md`, `SETUP.md`, `USER.md` | on demand only |
| **MACHINE-READ** | `SCHEMA.md` | cold to humans, parsed on every check — so its *tables* are load-bearing where its prose is not |

**Where the two axes meet:**

| | HOT | COLD |
|---|---|---|
| **ESSENTIAL** | **KEEP** | **PROMOTE** — it is arriving too late to prevent the error |
| **IMPORTANT** | **REDIRECT** down, leave one pointer line | **KEEP** |
| **DESIRABLE** | **CUT** | cut on sight; cheap either way |

**A provider's own directory is not a placement, it is an escape.** `AGENTS.md` § provider-agnostic
storage: state written to a harness's private path is outside the type system entirely — no type
owns it, no check reads it, and it does not survive a change of harness. Symlink the path the
harness insists on into the tree and the file becomes an ordinary instance again, checked like any
other. `brain/memory/` is the live case.

REDIRECT needs no new mechanism: `CONTEXT.md` (hot) already pairs with a sibling `SPECS.md` (cold),
which is the thin-front/leaf-detail split, and `ROADMAP.md` pairs with `ROADMAP-<slug>.md`. **A
constraint sitting in a `CONTEXT.md` head is the standard defect** — it is a SPECS answer trapped in
the one file the gate forces everyone to read. Measurement and its dashboard section:
[`ISSUES.md`](../ISSUES.md).

Compression is the **last** step and only on what survives, because it is measured to be nearly
worthless on this corpus — a pilot moved the worst offender 0.22% for a full model call. Placement
beats phrasing.

**The REDIRECT recipe, in order.** It survived contact with the whole `core/` corpus, and the order
is the part that pays:

1. **Delete what a hook already enforces.** A gate names its own fix when it fires, so restating it
   is pure cost. The exception is a number that changes how you write *before* the hook can speak —
   the 150/200 line caps stay.
2. **Move constraints to a sibling `SPECS.md`**, creating it if absent.
3. **Move data out** — alias lists, schemas, key tables.
4. **Delete stale claims.**
5. **Keep identity and navigation only.**

**Running step 1 first is what makes it cheap: six new `SPECS.md` instead of eleven.** Most of what
looked movable was already written better somewhere else — a path table duplicating the file's own
generated routing block, a layering table duplicating the child `CONTEXT.md`, a vocabulary section
restating this file verbatim. **Open the child `CONTEXT.md` and the file's own routing block before
relocating anything.**

**What replaces a moved section is one thin pointer line, never an instruction.** Write
`Gate behavior and the agent-shim contract: SPECS.md`; never "you must read SPECS.md". The check
fires on an over-size head *and* a modal, so the modal is the half that makes prose a trapped
constraint. A large head with no modals is identity and navigation, and is correct as it is — the
token warn is a signal, not a cap.

**A doc pass is a cheap fuzzer for the generators that read those docs.** Every pass over this
corpus has surfaced a generator bug rather than a prose problem, because relocating sections writes
file shapes nobody had written before — a `SPECS.md` inside `core/skills/` read as a skill and
failed the commit for every staged sibling; two extensions were scanned with no comment pattern and
so were reported as undescribed no matter how well they were commented. Expect one, and fix it at
the generator.

### No archive types

`ARCHIVE.md`, `HISTORY.md` and `.log/done.md` are **deleted, not renamed**. A file that is "never
auto-loaded, ask explicitly" is doing git's job. **Done work is deleted; git is the history.**

The same rule applies *inside* a file, not only to whole files (Lucas, 2026-07-30): **a completed
`ROADMAP.md` item is cut, not ticked.** `[x]` is an annotated corpse with a checkbox — it keeps
paying rent in every read of the file, and it makes the roadmap's length measure history instead of
remaining work. Trim on verified completion. Keep a line only when the next session needs it to
*extend* the work rather than recreate it, and write that line as present-tense state ("extend
`core/hooks/checks/type-gate.py`"), never as a report ("✅ built the type gate").

One thing git cannot hold: an approach we *tried and rejected* was never committed. That content has
exactly one home — a one-line entry under `## Rejected` in the relevant `ROADMAP.md` (for a ditched
goal, under `## Ditched` in `brain/GOALS.md`). One line, with the reason, so a dead idea does not
resurface looking new.

## Routing depth and locality (structural policy)

> Decided 2026-07-24 on two axes, since grown to four. Governs how every subtree is structured, not
> just the library. They stay **deliberately separate** — conflating them produced the wrong
> "flatten everything" call in an earlier round, and that is the reason the count keeps rising
> rather than the axes merging.

**Locality — keep it.** Small `CONTEXT.md` glued to the files it governs is **not** overhead. On a
workspace that must also run on Sonnet and small local models, scattered local `CONTEXT.md` is what
*makes weak models navigate*, and the always-loaded index is the most cache-friendly input there is.
Do **not** consolidate local CONTEXT.md to "reduce clutter" — granularity is the feature.

**Depth — cap it.** What costs is *hops to content*: a second routing level is not uniformly free —
it helps some tasks, hurts others. So cap **chain depth**, not **file count**. When in doubt about
adding a routing level, **measure** (a real task on the tier you care about), do not decree.

**Fanout — signal it.** "File count is not the metric" governs **CONTEXT.md granularity** and nothing
else. Source files in one directory are a different axis: `workspace_scanner.SPLIT_THRESHOLD` reads
`WARN_FILES` from [`limits.env`](hooks/limits.env) — never its own copy of the number — and
`entropy_fanout.py` reports it to the dashboard rather than to a stdout nobody reads, which is what
let the tail grow unopposed before.

**Document size — cap it, and make the root route.** One authored `.md` is capped at `BLOCK_LINES`,
the same number code is held to, because the trade is the same shape: a shard adds a hop, so it pays
only when it sheds more than the routing row it costs. What makes prose different from a directory
is that the shard's readers are *sessions deciding whether to read it*, so shedding content is only
half the move — the index has to carry enough to make that decision without opening anything. The
shape of the split is § A type that outgrows the cap is cut; the fields a shard publishes so the
index can route to it are § Layer: shard.

The evidence this axis was added on (2026-08-18, `core/tools/wos/session/reads` over 89 transcripts):
`ROADMAP.md` at 1222 lines was the most re-read file in the workspace, 130 reads for 983k chars, and
**ten whole-file reads carried 56% of those chars** while the median read was 2.2k. Mass is not paid
evenly — it is paid by the reads that give up on navigating and take the whole thing.

The four axes, kept separate on purpose:

| Axis | Rule | Enforced by |
|---|---|---|
| **locality** | many small local `CONTEXT.md` = good, never consolidate | judgement |
| **depth** | cap hops to content; measure before adding a routing level | judgement |
| **fanout** | `WARN_FILES=7` asks for a look, `BLOCK_FILES=10` is the cap | `entropy_fanout.py`, dashboard |
| **document size** | `BLOCK_LINES=200` caps one authored `.md`; a root that sheds shards routes to them | `pre-edit.py`, dashboard |

**Where they meet:** splitting an over-full directory *adds a hop*, so fanout and depth trade against
each other directly. Pay the hop only when the split removes more table than it adds. A directory in
the dozens pays — the routing table it sheds dwarfs the one hop it costs. A directory at 8-9 files
does not: the hop costs more than the two rows it saves, which is why `WARN_FILES` asks for a look
instead of blocking. Current offenders are listed in [`ISSUES.md`](../ISSUES.md) § Directories
holding too many files; read that rather than a worked example, which goes stale the moment the
split lands.

**Net rule:** many small local CONTEXT.md files = good; deep CONTEXT.md → CONTEXT.md → CONTEXT.md
chains = the thing to bound. For *routing levels*, hop count is the metric, not file count. For
*source files in one directory*, fanout is the signal — **two** numbers, symmetric with the file
pair, both in [`core/hooks/limits.env`](hooks/limits.env): warn at 7, block at 10. The gap between
them is deliberate and is where "a split that saves two rows does not pay for its hop" lives.

### What the routing table may spend tokens on

**No session reads the corpus; it reads a chain.** A corpus-wide sum is therefore the wrong number to
optimise, and the cost that is real is row *count* per chain — i.e. the fanout signal above, not the
table's existence. So the table stays; two rules trim what it says. Re-run
[`core/tools/wos/session/context`](tools/wos/session/CONTEXT.md) for the live figures rather than
quoting any printed here.

1. **A generated column empty on every row is not emitted.** 773 of 1242 rows carried an em-dash
   `Interface`, paying width to say "nothing here". `File` and `Description` always survive.
2. **`test_*` symbols are not API** — the runner collects them, no module imports one. Keyed on the
   **symbol, never the path**: a `tests/`-directory exemption would be a door to walk production code
   through, dodging the facade and interface-stub gates. Guarded by
   `test_a_production_symbol_in_a_test_directory_still_appears`.

The `Description` column is **not** on the table for trimming: it is each file's own first-line
comment, written by hand at the source and only *surfaced* here. Measured noise is 6%. That is
curated content, which is the side of the evidence split that helps — see [refs/REFS.md](refs/REFS.md)
§ Context engineering.

**Evidence + caveat.** Controlled study on haiku-4.5 + qwen3.6-27b ([P] 2607.17598): the flat skill
pack reaches ~2× accuracy at ½ the tokens vs. raw at corpus scale, and *"the weaker the agent's
native navigation, the earlier the skill pack earns its keep."* **Preprint = provisional** (see
[refs/CONTEXT.md](refs/CONTEXT.md)); this policy is a default, not a hard gate. Nothing here has been
measured on our own corpus — [ROADMAP.md](../ROADMAP.md) is where that would happen.
