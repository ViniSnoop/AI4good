# Vocabulary
> One word per idea, one idea per word, and every token a rename retired.
> answers: which spelling is canonical, what a term means, what may no longer be written
> enforced-by: core/hooks/entropy/entropy_ledger.py, core/hooks/entropy/entropy_vendor.py,
> core/hooks/checks/citation-gate.py

## Vocabulary

Aliases that mean exactly one thing, so a reader never has to guess whether two spellings are two
concepts. This is **data, not a rule** — which is why it lives here and not in the always-loaded
`AGENTS.md` (moved 2026-07-30).

| Canonical | Also written |
|-----------|--------------|
| **workspace-os** | `wos` · `WOS` · `w-os` · `W-OS` |
| **craft flow** | the `/craft` skill, `core/flows/craft/` (retired spellings: § Retired tokens) |
| **Front** | a top-level workstream in `ROADMAP.md` (retired spelling: `Frente`) |

### Terms with one meaning

The table above resolves two spellings to one concept. These resolve one word to one **definition**,
and they were added (2026-08-17) because their absence produced category errors that survived weeks:
the registry filed a TeX toolchain and a `.venv` as features, and no word existed for a rule that is
written down and obeyed but never enforced.

| Term | Definition |
|------|------------|
| **feature** | Something **this workspace authors** that can be switched off in-process, declared in [`features.txt`](features.txt). One layer or a combination of them — a hook, a tool, a skill, an agent, a flow, a norm, or several at once. Third-party machine state is not a feature — it is a `SETUP.md` step plus a `core/tools/deps.txt` line. The test: if switching it off leaves nothing running to observe the difference, it is substrate, not a feature |
| **layer** | One of `hooks · tools · skills · agents · flows · norms` — each names a directory under `core/`, except `norms`. A feature is one layer or a combination of them |
| **norm** | A rule that exists only as written words and is obeyed rather than enforced — the INDUCED half of the line whose ENFORCED half is `file_law.py` / `schema_law.py` / `feature_law.py`. A norm that acquires a checker stops being a norm and becomes a hook |

**Why `Front` and not `Workstream`** — ruled 2026-08-16 (Lucas). *"progress on several fronts"* is
ordinary English for parallel areas of effort, which is exactly what these are, so the word carries
the meaning without the military or meteorological reading a bare *front* invites. It also keeps the
initial, so every existing habit of reference survives the rename. A roadmap heading is a
**contract**, and this workspace writes contracts in English even where its rationale is Portuguese.

**A Front number is not a citable identifier.** Closed items are deleted, so `Front 4.1` becomes a
dead pointer the day the work lands — cite the `SPECS.md` or `SCHEMA.md` section that owns the rule
instead. Numbering is legal only inside `ROADMAP.md` / `ROADMAP-<slug>.md`, and in commit messages,
which git keeps.

### Retired tokens

**A rename is finished when its old token appears nowhere.** Until then the leaves drift back and the
drift is indistinguishable from entropy — the lesson of the `loops`→`flows` rename, which kept
resurfacing because nothing asserted its completion.

This table *is* the assertion. `core/hooks/entropy/entropy_ledger.py` fails if any token below survives in a
tracked file, this file excepted — the law has to be able to name what it retires. Add a row the
moment a rename lands, and delete the prose that would otherwise explain it: git holds the history,
this table holds the guard.

| Retired token | Replacement | Retired |
|---------------|-------------|---------|
| `loop-engineering` | `craft` | 2026-07-23 |
| `loop-router` | `route` | 2026-07-23 |
| `loop-architecture` | `architect` | 2026-07-23 |
| `LOOP-TREE` | `tree.md` | 2026-07-23 |
| `KNOWN-BUGS` | `ISSUES.md` | 2026-07-30 |
| `/loops` | `/craft` | 2026-08-17 |
| `BUGS.md` | `ISSUES.md` | 2026-08-19 |


**The skill rename is a shape, not a word, for the same reason `Frente` is.** `loops` is ordinary
English — the corpus holds a thousand honest uses, from "file-relayed loops" to "execution loops"
to "Loop 0..6" as step names — so a bare `loops` row would fail on correct prose the day it was
written. What is retired is the **command**, so the row is the invocation shape `/loops`. The
per-run state dir `.loop/<slug>/` is a *different* token on the same rename and is deliberately
absent: it is still live in fourteen directories across three repos, and a row that fails today
teaches people to ignore the check. It joins this table when that sweep lands.

**`Frente`→`Front` (2026-08-16) is deliberately *not* a row here, and the reason is a limit of
this table.** Every token above is a coined string that can only mean the thing it names, so a
bare-word match is safe. `frente` is an ordinary Portuguese noun — `branches/casinhas/CONTEXT.md`
uses it in a table header to mean a work front on a building site — and a row would have failed
on honest prose the day it was written, which is precisely what the paragraph above says trains
people to ignore a check. `core/hooks/checks/citation-gate.py` owns that rename instead, by
matching the **citation shape** `Frente <n>` rather than the word. The word stays legal; the
pointer does not. **A rename whose old spelling is also a real word needs a shape, not a token.**

Not yet listed because the rename has not landed: `SPEC.md`→`SPECS.md` (load-bearing in five
enforcement points; see [ROADMAP.md](../ROADMAP.md)). A token joins this table only when
the sweep is complete — a row that fails on the day it is written trains people to ignore the check.

### A vendor's model name is data, never a directive

**Ruled 2026-08-17 (Lucas), reading a step assignment: *"nothing in WOS should be tied to a specific
vendor/company/model."*** A ledger assigns a **tier** — `low` · `medium` · `high` — and which model
fills a tier is data, in [`core/flows/craft/routing.md`](flows/craft/routing.md) and nowhere else. A
ledger that names a model goes stale the day that model does, and ties the workspace to one vendor
in the one place a reader looks for what to do next.

**This is a shape, not a token**, for the same reason `Frente` is: the same word is honest in one
position and wrong in another. `**model: opus**` is a directive and is forbidden; `` `model: opus` ``
in prose reporting a measurement, quoting a stale id, or describing what a provider's frontmatter
resolves to is data and is fine. `core/hooks/entropy/entropy_vendor.py` matches the bolded
assignment and nothing else — a flat token ban would fire on every honest use and be switched off
inside a week.
