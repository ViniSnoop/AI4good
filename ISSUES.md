# Workspace issues
> What is currently untrue that we know about: hand-written issues first, every measured number
> inside its own generated block.

The scope is the **workspace itself** — the enforcement layer, the tools, the scaffold. A bug in a
project under `code/` belongs to that project's own `ISSUES.md`, and the entropy block below counts
every repo precisely so nothing goes dark while the ownership stays split.

Two rules, both from [`core/SCHEMA.md`](core/SCHEMA.md) § Boundaries where types nearly touch:
**never hand-edit inside a generated block**, and **never write a measured number outside one** — a
copied count is the drift these checks exist to catch. The FIXED gate governs the hand-written half
only, and it is satisfied the same way here as in every project: a bug flips to FIXED when a
matching regression spec exists and passes.

## B1 — `.opencode/wp-helpers.d.ts` is stale, and it switches the read gate off silently

**Symptom:** `tsc` fails on the stub with `Property 'stdin' does not exist on type '{}'`, so
`core/hooks/postedit/interfaces.sh` never regenerates it and the stub beside the source stays old.

**Why it is worse than a stale file:** `core/hooks/read/pre-read.sh` blocks a source read *only
while the stub beside it is current*. A stub that cannot be regenerated therefore does not merely
go out of date — it turns the interface-first discipline off for that file, and nothing says so.
That is the same failure shape the entropy dashboard's § Source files with no interface stub was
built to count, arriving through a different door.

**Repro:** run the stub generation over `.opencode/wp-helpers.js` and read the `tsc` output.

**Root cause:** unknown. The typed shape of the opencode plugin's helper argument is inferred as
`{}`, so every property access on it is an error; whether the fix is a JSDoc annotation on the
source or a `tsconfig` lib change is unestablished.

## B2 — a type that shards is allowlisted by enumeration, so its shards fall out of git

**Symptom:** found 2026-08-20, fixed in `.gitignore` the same day, and kept here because the
*mechanism* is still live. `.gitignore` allowlists `core/` file by file under a `core/*` deny. Every
shard of the law and of the conventions — the four `core/SCHEMA-*.md` and the four
`core/SPECS-*.md` — was therefore untracked, for as long as those types have been sharded. A fresh
clone got `SCHEMA.md` whose generated index points at four files that are not in the repo.

**Why nothing caught it:** the pointer-integrity check resolves links against the **working tree**,
where the files exist. `entropy_naming` sees a legal name in a legal place. The
`.gitignore` self-heal adds `!<domain>/<dir>/` for a **directory** that gains a `CONTEXT.md`, and a
shard is a file at a domain root, so it was outside every rule the workspace has. Three green
checks, one invisible hole.

**Still true after the fix:** the allowlist now names the shards by shape (`!core/SCHEMA-*.md`), but
that was a hand-edit, and the next type to shard at a domain root that is not `core/` will land in
the same hole. The durable fix is a Tier 0 check asserting that **every tracked type's siblings are
tracked too** — that a file passing `entropy_naming.TYPE_SLUG` is not ignored. It is not written.

## B3 — a mixed carousel is read as a video, so every slide after the first is never opened

**Symptom:** `core/tools/video/video` on an Instagram carousel whose **first slide is a video**
returns only that slide. Found 2026-08-20 draining the INBOX: `instagram.com/p/Db3di5dEpS4/` is an
eight-slide post, and the entry's whole point — MatrAIx / Persona 8B, on slide 3 — was invisible.
Lucas had to screenshot the slide by hand.

**Root cause, confirmed by reading it:** `video_core.assemble` reaches the image path only inside
`if not ok:` — the comment says *"an image post probes as a failure. Retry through gallery-dl before
giving up."* That holds for an all-image carousel, where yt-dlp returns nothing. A **mixed** carousel
succeeds under yt-dlp, so `ok` is true, `video_images.gather` never runs, and the frame sampler reads
the first slide's video alone.

**Repro:** run the URL above at `--level full`. The tell is five near-identical VLM captions of one
frame — the sampler re-describing slide 1 while seven slides sit unread.

**Why it is worse than a thin block:** `/inbox` states that an unextracted link is an unroutable
entry, so this silently converts *routable* entries into ones triaged on a caption alone. Nothing
reports a slide count, so the loss is invisible at the call site.

**Lucas, 2026-08-20:** *"toda a triagem de INBOX deveria automaticamente decifrar imagens e vídeos,
incluindo OCR mas não somente isso, e sempre que possível usando zero-tokens."* The capability is
already there and already zero-token — tesseract plus a local VLM. It is the dispatch that is wrong,
not the extractors.

## B4 — a pre-edit block can exit non-zero with nothing on stderr

**Symptom:** an Edit to `code/isoroll-content/src/pipeline/kit_modules.py` was refused by
`core/hooks/checks/pre-edit.py` reporting **"No stderr output"** — no reason, no named fix. Found
during isoroll CP-3/CP-4.

**Why it matters:** running the same hook by hand with a payload that trips the size gate prints the
right message, so at least one rejection path returns non-zero silently. That breaks the contract in
[`core/hooks/SPECS.md`](core/hooks/SPECS.md) — a hook that blocks names the fix — and costs a round
of investigation per occurrence, which is the same silent-failure shape
[`core/SPECS.md`](core/SPECS.md) § Conventions exists to forbid.

**Root cause:** unknown. Which path exits quietly is unestablished; the size gate is not it.

## B5 — `core/tools/test/law/entropy/` says it mirrors the checks it tests, and it does not

**Symptom:** its `CONTEXT.md` described itself as mirroring `core/hooks/entropy/`, and the roadmap
row about that directory's fanout repeated the claim — *"it mirrors this directory one word apart"*.
One `ls` of each refutes both. Six names line up; two do not, in each direction:

- `entropy_corpus.py` and `entropy_size.py` have **no test file** in the mirror.
- `test_entropy_inventory.py` and `test_entropy_placeholders.py` test surfaces that live **inside
  other modules**, so their names answer to nothing next door.

**Why it matters more than a wrong description:** the fanout ruling for `core/hooks/entropy/` was
argued partly from symmetry — whatever is decided applies to the mirror "in the same commit, which
is the property mirroring buys." That property was assumed, not checked, so the argument rested on
something untrue. It also means `size_signals` and the corpus selector — the check that decides
*which files every other check may look at* — are covered only incidentally.

**Root cause of the gap:** unestablished, and it is a real decision rather than an oversight to
correct in passing. Either those two modules deserve their own test files, or their coverage
genuinely belongs where it already sits and the *name* is what should change. Nothing asserts either
way today, which is why the claim could drift unnoticed for as long as both directories existed.

**Repro:** `ls core/hooks/entropy/ core/tools/test/law/entropy/` and compare the stems.

## B8 — the `!code/<repo>/CONTEXT.md` allowlist block is dead config

**Symptom:** `.gitignore` lines ~48–56 carefully re-allow the `CONTEXT.md` of four nested repos
(`gira`, `laplata`, `cria`, and `freeai` when it was added) with the `!code/<repo>/` +
`code/<repo>/*` + `!code/<repo>/CONTEXT.md` triple. **None of them is tracked.** The wholesale
`code/<repo>` entries in the nested-repo list further down the file (~line 182 onward) come later
and win, so every line in that block is inert.

**Repro:** `git ls-files code/gira/CONTEXT.md code/laplata/CONTEXT.md code/cria/CONTEXT.md
code/freeai/CONTEXT.md` → returns nothing. Verified 2026-08-24.

**Why it matters:** it is config that reads as if it works. Someone adding the fifth repo will copy
a pattern that has never once had an effect, and the `code/` routing table's claim to describe
nested repos rests on files git cannot see.

**Root cause is known; the fix is a decision, not a patch.** Either the block is dead and should be
deleted outright, or the two blocks are in the wrong order and the nested-repo list should come
*before* the allowlist. Which one depends on whether a nested repo's `CONTEXT.md` is meant to be
visible to the workspace repo at all — and that question is `ROADMAP-portability.md`'s (it is the
same boundary the `code/aiwbot` absorb ruling just moved). Do not reorder blindly: making four
`CONTEXT.md` files suddenly tracked changes what the Tier 0 corpus contains.

Found by a parallel `zcode` session, 2026-08-21; confirmed by hand 2026-08-24.

<!-- entropy:start -->
## Entropy

> Generated by `core/hooks/entropy/dashboard/entropy-dashboard.py`, which scans the whole tree. Never edit inside this block, and never copy a count out of it — a copied number is the drift these checks exist to catch.

2026-08-25 · 2369 tracked files scanned · **605 findings** (2026-08-13: 95 · +510 over 12 days), 109 of them here

| Check | Findings |
|-------|----------|
| Off-allowlist `.md` types | 8 |
| CONTEXT.md hand-written inventories | 4 |
| Naming and placement | 1 |
| Projects not declaring their goal | 0 |
| Wiki-links naming nothing | 0 |
| Retired tokens still alive | 2 |
| Roadmap item numbers cited outside a roadmap | 0 |
| Items claimed by two ledgers | 0 |
| Size signals | 58 |
| Source files with no interface stub | 2 |
| Directories holding too many files | 10 |
| Prose describing finished work | 4 |
| Unanswered scaffold placeholders | 11 |
| Doubt stores missing their own discipline | 0 |
| Ledgers naming a model where they mean a tier | 0 |
| Header fields naming code that is not there | 0 |
| Truncated routing descriptions | 1 |
| Constraints trapped in a CONTEXT.md head | 5 |
| Repos on an unmerged feature branch | 1 |
| Remote branches already merged into their base | 2 |

### Findings per code repo

*Each repo keeps its own `ISSUES.md`; this table is the index and the sum. Open the repo to see what its findings are.*

| Repo | Findings |
|------|----------|
| [`code/aiwbot`](code/aiwbot/ISSUES.md) | 127 |
| [`code/apptime`](code/apptime/ISSUES.md) | 21 |
| [`code/corpora`](code/corpora/ISSUES.md) | 12 |
| [`code/cria`](code/cria/ISSUES.md) | 6 |
| [`code/dobra`](code/dobra/ISSUES.md) | 16 |
| [`code/flows`](code/flows/ISSUES.md) | 90 |
| [`code/freeai`](code/freeai/ISSUES.md) | 8 |
| [`code/gira`](code/gira/ISSUES.md) | 5 |
| [`code/isoroll-content`](code/isoroll-content/ISSUES.md) | 45 |
| [`code/isoroll-module`](code/isoroll-module/ISSUES.md) | 97 |
| [`code/laplata`](code/laplata/ISSUES.md) | 4 |
| [`code/ppc`](code/ppc/ISSUES.md) | 6 |
| [`code/spacemantics`](code/spacemantics/ISSUES.md) | 57 |
| [`code/voti`](code/voti/ISSUES.md) | 2 |
| **collected** | **605** |

### Off-allowlist `.md` types

*route via core/SCHEMA.md § four disposal routes*

- academy/papers/2027-CHI-cria/outputs/CRISES.md: 'CRISES.md' is not a known .md type.
- academy/papers/2027-ICLR-dobra/PLAN.md: 'PLAN.md' is not a known .md type.
- branches/casinhas/PROJETO.md: 'PROJETO.md' is not a known .md type.
- branches/casinhas/burocracia/BUROCRACIA.md: 'BUROCRACIA.md' is not a known .md type.
- branches/casinhas/burocracia/docs/INDICE.md: 'INDICE.md' is not a known .md type.
- branches/instituto/FUNDING.md: 'FUNDING.md' is not a known .md type.
- branches/instituto/MOTOR.md: 'MOTOR.md' is not a known .md type.
- branches/instituto/RALOS.md: 'RALOS.md' is not a known .md type.

### CONTEXT.md hand-written inventories

*the routing block owns inventory*

- academy/papers/2026-JBCS-relativistic_raytracer/lib/CONTEXT.md: hand-written file inventory (9 bullets/table rows listing real files).
- academy/papers/2026-JBCS-relativistic_raytracer/sections/CONTEXT.md: hand-written file inventory (6 bullets/table rows listing real files).
- academy/papers/2026-SIBGRAPI-relativistic_raytracer/lib/CONTEXT.md: hand-written file inventory (3 bullets/table rows listing real files).
- academy/papers/2026-SIBGRAPI-relativistic_raytracer/tables/CONTEXT.md: hand-written file inventory (3 bullets/table rows listing real files).

### Naming and placement

*kebab-case ASCII, types where their scope allows*

- code/_templates/module.SPEC.md: 'module.SPEC.md' is neither a lowercase instance nor a known type.

### Projects not declaring their goal

*line 3 of a code/ CONTEXT.md*

Clean.

### Wiki-links naming nothing

*a [[slug]] is a goal file or an item in one*

Clean.

### Retired tokens still alive

*a rename is unfinished until these are zero*

- branches/casinhas/ROADMAP-orcamento.md: retired token 'KNOWN-BUGS' survives (line 42).
- branches/instituto/MOTOR.md: retired token 'loop-engineering' survives (line 30).

### Roadmap item numbers cited outside a roadmap

*a closed item is deleted — cite the SPECS.md/SCHEMA.md section that owns the rule*

Clean.

### Items claimed by two ledgers

*v1 criterion 2 — an item lives in one place*

Clean.

### Size signals

*a signal for review, never a cap — do not summarize to fit*

- .craft/commands-mirror-cost/0-clarify.md — 2 line(s) over the 120-column cap (first at line 9)
- AGENTS.md — 3 line(s) over the 120-column cap (first at line 6)
- academy/administration/coordenacao-lc/novo-ppc-bcc/ROADMAP-ementas.md — 48 line(s) over the 120-column cap (first at line 3)
- academy/papers/2026-JBCS-relativistic_raytracer/CONTEXT.md — 2 line(s) over the 120-column cap (first at line 4)
- academy/papers/2026-JBCS-relativistic_raytracer/refs/CONTEXT.md — 1 line(s) over the 120-column cap (first at line 50)
- academy/papers/2026-SIBGRAPI-relativistic_raytracer/CONTEXT.md — 1 line(s) over the 120-column cap (first at line 4)
- academy/papers/2027-CHI-cria/CONTEXT.md — 2 line(s) over the 120-column cap (first at line 4)
- academy/papers/2027-CHI-cria/ROADMAP.md — 6 line(s) over the 120-column cap (first at line 3)
- academy/papers/2027-CHI-cria/refs/CONTEXT.md — 1 line(s) over the 120-column cap (first at line 35)
- academy/papers/2027-CHI-cria/refs/REFS.md — 24 line(s) over the 120-column cap (first at line 8)
- academy/papers/2027-ICLR-dobra/PLAN.md — 1 line(s) over the 120-column cap (first at line 2)
- academy/papers/2027-ICLR-dobra/refs/CONTEXT.md — 1 line(s) over the 120-column cap (first at line 34)
- academy/papers/ai4good/CONTEXT.md — 3 line(s) over the 120-column cap (first at line 2)
- academy/papers/ai4good/ROADMAP.md — 4 line(s) over the 120-column cap (first at line 2)
- academy/papers/ai4good/refs/CONTEXT.md — 1 line(s) over the 120-column cap (first at line 2)
- academy/papers/ai4good/refs/REFS.md — 1 line(s) over the 120-column cap (first at line 2)
- academy/papers/mechanism-search/CONTEXT.md — 2 line(s) over the 120-column cap (first at line 2)
- academy/papers/mechanism-search/draft.md — 5 line(s) over the 120-column cap (first at line 2)
- academy/papers/mutual-credit-ai/CONTEXT.md — 1 line(s) over the 120-column cap (first at line 2)
- academy/papers/mutual-credit-ai/draft.md — 4 line(s) over the 120-column cap (first at line 6)
- academy/papers/pls-pix/CONTEXT.md — 1 line(s) over the 120-column cap (first at line 2)
- academy/papers/pls-pix/draft.md — 5 line(s) over the 120-column cap (first at line 2)
- academy/papers/spacemantics/refs/CONTEXT.md — 1 line(s) over the 120-column cap (first at line 43)
- academy/papers/wos-ablation/CONTEXT.md — 1 line(s) over the 120-column cap (first at line 2)
- academy/papers/wos-ablation/refs/CONTEXT.md — 1 line(s) over the 120-column cap (first at line 2)
- academy/papers/wos-ablation/refs/REFS.md — 1 line(s) over the 120-column cap (first at line 2)
- academy/refs/REFS.md — 1 line(s) over the 120-column cap (first at line 117)
- brain/INBOX.md — 1 line(s) over the 120-column cap (first at line 42)
- brain/attachments/instituto-estrategias.md — 4 line(s) over the 120-column cap (first at line 21)
- brain/goals/craft-flows.md — 3 line(s) over the 120-column cap (first at line 121)
- brain/goals/cria.md — 1 line(s) over the 120-column cap (first at line 65)
- brain/goals/home-casinhas.md — 3 line(s) over the 120-column cap (first at line 53)
- brain/goals/spacemantics.md — 2 line(s) over the 120-column cap (first at line 57)
- brain/goals/spec-driven-development.md — 1 line(s) over the 120-column cap (first at line 46)
- brain/goals/workspace-os.md — 3 line(s) over the 120-column cap (first at line 118)
- branches/casinhas/CONTEXT.md — 10 line(s) over the 120-column cap (first at line 2)
- branches/casinhas/PROJETO.md — 7 line(s) over the 120-column cap (first at line 6)
- branches/casinhas/burocracia/BUROCRACIA.md — 12 line(s) over the 120-column cap (first at line 2)
- branches/casinhas/burocracia/CONTEXT.md — 1 line(s) over the 120-column cap (first at line 2)
- branches/casinhas/burocracia/docs/INDICE.md — 1 line(s) over the 120-column cap (first at line 36)
- branches/casinhas/refs/REFS.md — 3 line(s) over the 120-column cap (first at line 4)
- branches/instituto/CONTEXT.md — 6 line(s) over the 120-column cap (first at line 2)
- branches/instituto/FUNDING.md — 3 line(s) over the 120-column cap (first at line 2)
- branches/instituto/MOTOR.md — 11 line(s) over the 120-column cap (first at line 2)
- branches/instituto/RALOS.md — 5 line(s) over the 120-column cap (first at line 2)
- branches/instituto/ROADMAP.md — 5 line(s) over the 120-column cap (first at line 14)
- branches/instituto/nucleo-arede.md — 10 line(s) over the 120-column cap (first at line 2)
- branches/instituto/nucleo-circuito.md — 15 line(s) over the 120-column cap (first at line 2)
- branches/instituto/nucleo-civica.md — 14 line(s) over the 120-column cap (first at line 2)
- branches/instituto/nucleo-laplata.md — 12 line(s) over the 120-column cap (first at line 2)
- branches/instituto/nucleo-virada.md — 16 line(s) over the 120-column cap (first at line 2)
- core/norms/CONTEXT.md — 1 line(s) over the 120-column cap (first at line 5)
- core/norms/one-action.md — 1 line(s) over the 120-column cap (first at line 6)
- core/norms/split.md — 1 line(s) over the 120-column cap (first at line 6)
- core/norms/storage.md — 1 line(s) over the 120-column cap (first at line 6)
- core/refs/REFS-context.md — 1 line(s) over the 120-column cap (first at line 36)
- core/refs/REFS-legibility.md — 1 line(s) over the 120-column cap (first at line 23)
- core/refs/REFS-tooling.md — 2 line(s) over the 120-column cap (first at line 67)

### Source files with no interface stub

*the read gate only fires when a stub exists — a missing one turns it off silently*

- code/eslint.shared.js — no .d.ts
- core/tools/test/workspace/harness/test_hook_environment.py — no .pyi

### Directories holding too many files

*splitting costs one hop — pay it only when it removes more table than it adds*

- academy/administration/coordenacao-lc/novo-ppc-bcc/ementas — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- academy/papers/2026-JBCS-relativistic_raytracer/sections — 8 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- academy/papers/2026-JBCS-relativistic_raytracer/sections/06_results — 8 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/hooks/entropy — 9 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/hooks/routing — 8 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/skills/caveman/hooks — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/skills/caveman/scripts — 10 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/tools/test/law/entropy — 12 code files in one directory, over the BLOCK_FILES cap; split by responsibility if the split removes more table than the hop adds
- core/tools/test/workspace/gates — 8 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds
- core/tools/wos — 8 code files in one directory, over the WARN_FILES signal; split by responsibility if the split removes more table than the hop adds

### Prose describing finished work

*git is the history — cut it, or rewrite it as present-tense state*

- academy/papers/2026-JBCS-relativistic_raytracer/outputs/submission-checklist.md:58: a dated completion report — prose describing finished work.
- academy/papers/2027-CHI-cria/ROADMAP.md:11: a ticked item — prose describing finished work.
- academy/papers/2027-ICLR-dobra/ROADMAP.md:23: a ticked item — prose describing finished work.
- branches/casinhas/ROADMAP.md:6: a ticked item — prose describing finished work.

### Unanswered scaffold placeholders

*a generator asked a question — answer it at the source, never by cutting the marker*

- academy/administration/CONTEXT.md:13: 1 unanswered placeholder(s).
- academy/administration/coordenacao-lc/novo-ppc-bcc/CONTEXT.md:2: 2 unanswered placeholder(s).
- academy/papers/2026-JBCS-relativistic_raytracer/outputs/CONTEXT.md:10: 2 unanswered placeholder(s).
- academy/papers/2026-JBCS-relativistic_raytracer/refs/CONTEXT.md:69: 3 unanswered placeholder(s).
- academy/papers/2026-SIBGRAPI-relativistic_raytracer/refs/CONTEXT.md:29: 10 unanswered placeholder(s).
- academy/papers/2027-CHI-cria/refs/CONTEXT.md:30: 1 unanswered placeholder(s).
- academy/papers/2027-ICLR-dobra/CONTEXT.md:42: 1 unanswered placeholder(s).
- academy/papers/2027-ICLR-dobra/refs/CONTEXT.md:29: 1 unanswered placeholder(s).
- academy/papers/ai4good/CONTEXT.md:26: 1 unanswered placeholder(s).
- academy/papers/spacemantics/CONTEXT.md:36: 1 unanswered placeholder(s).
- academy/papers/spacemantics/refs/CONTEXT.md:30: 1 unanswered placeholder(s).

### Doubt stores missing their own discipline

*an experiment states its Method, Results, What changed and Limitations; a judged reference carries a source tier*

Clean.

### Ledgers naming a model where they mean a tier

*which model fills a tier is data — core/flows/craft/routing.md*

Clean.

### Header fields naming code that is not there

*a field naming our own tree is a claim, and it is checked before a later session inherits it as fact — core/SCHEMA-outgrowing.md § the field table*

Clean.

### Truncated routing descriptions

*the source wrote past the bound — shorten it there, never edit the table*

- branches/casinhas/CONTEXT.md: 2 truncated description(s) — burocracia/, ROADMAP.md.

### Constraints trapped in a CONTEXT.md head

*the only enforced-read type — move the contract to a sibling SPECS.md*

- academy/papers/2026-JBCS-relativistic_raytracer/CONTEXT.md: head is 437 tok carrying 1 constraint(s).
- academy/papers/2026-JBCS-relativistic_raytracer/refs/CONTEXT.md: head is 645 tok carrying 3 constraint(s).
- academy/papers/2027-CHI-cria/refs/CONTEXT.md: head is 438 tok carrying 2 constraint(s).
- academy/papers/2027-ICLR-dobra/refs/CONTEXT.md: head is 412 tok carrying 2 constraint(s).
- academy/papers/spacemantics/refs/CONTEXT.md: head is 547 tok carrying 2 constraint(s).

### Repos on an unmerged feature branch

*promote when the work is green, or say which reason applies — /roundup Phase 5*

- . — feature/self-description-grounding is 4 ahead of main

### Remote branches already merged into their base

*safe to delete, and outward-facing — `git -C <repo> push origin --delete <branch>`, Lucas*

- . — 29 merged into main: git -C . push origin --delete feature/brain-attention feature/craft-flows feature/drive-core-write feature/entropy-column-drain feature/feature-registry feature/flows-pool-reorg feature/front18-diagram-ruling feature/gforms feature/hooks-deoverengineer feature/inbox-link-batch feature/inbox-triage-2026-07-26 feature/md-cap-and-shards feature/roadmap-drain feature/roundup-2026-07-23 feature/roundup-2026-07-28 feature/roundup-2026-07-29 feature/roundup-craft-flows feature/roundup-inbox-drain feature/roundup-md-cap feature/sync-goal-todo-docs feature/sync-strategy feature/todo-type-retirement feature/workspace-robustness-plan feature/wos-decisions-sprint feature/wos-install feature/wos-ledger-truthup feature/wos-push-sweep feature/wos-typeset feature/zcode-shim
- branches/casinhas — 1 merged into main: git -C branches/casinhas push origin --delete feature/routing-row-rebase

<!-- entropy:end -->

<!-- verify:start -->
## Verification

> Generated by `core/tools/wos/roundup` at session close. The suite is the authority; this is its last result, never a claim that it is still true.

2026-08-24 · `make verify-full` · **green (542 passed)**
<!-- verify:end -->
