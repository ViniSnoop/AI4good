# When a document outgrows its type
> Where an unclassified name goes, and how a type that passed the cap splits.
> answers: what to do with an off-allowlist name, how a type shards, what an index keeps
> enforced-by: core/hooks/checks/type-gate.py, core/hooks/checks/pre-edit.py,
> core/hooks/entropy/entropy_fields.py

### The four disposal routes

An off-allowlist `UPPERCASE.md` is not automatically wrong — it is *unclassified*. **Ask *is this
still true* before *what type is this***: a name that looks like it needs an allowlist entry is often
done work, or a type its own repo already spells right. Route what survives (decided 2026-07-30):

| Route | When |
|-------|------|
| lowercase instance | **generated** by a tool |
| lowercase instance | hand-authored **content** |
| → `SPECS.md` | hand-authored **constraint** |
| new type | answers a question **no type answers** — `SETUP.md` is the only one that ever qualified |

**A generated measurement that is also a ratchet is tracked, at the root** (ruled 2026-08-17,
resited 2026-08-19). **The question a generated measurement answers decides where it goes**, and the
entropy report therefore takes no route at all: "what is currently untrue that we know about" already
has a type, so it is a *block* inside the root [`ISSUES.md`](../ISSUES.md) — written by
[`core/hooks/entropy/dashboard/entropy-dashboard.py`](hooks/entropy/dashboard/entropy-dashboard.py)
beside a verify block written by [`core/tools/wos/roundup`](tools/wos/roundup). A drift finding, a red
suite and a hand-written bug are three answers to one question, kept apart by markers rather than by
filenames. It sits at the root rather than beside its generator because `outputs/` is gitignored and
**a ratchet that is not tracked cannot ratchet** — being diffable commit over commit is what makes
"the count must shrink" a check rather than a feeling — and because a file that measures the whole
workspace does not live inside one of the things it measures, the same rule that puts
`core/SCHEMA.md` at `core/` root rather than in `core/hooks/`.

**The host is half authored, and that is the one cost this shape carries.** `ISSUES.md` is named in
[`core/hooks/generated.txt`](hooks/generated.txt), which waives the line cap for the whole file
rather than for its blocks, so the hand-written issues above them lose the size signal too. The
alternative — a per-block cap — would be a second numeric law answering the question `BLOCK_LINES`
already answers. If the hand-written half outgrows a screen it shards like any other type.

**A declaration table is a fifth thing, and it takes none of these routes** (ruled 2026-08-16).
`core/features.txt` and `core/profile.txt` join `core/hooks/limits.env`, `core/tools/deps.txt`,
`core/hooks/vendored.txt`, `core/hooks/generated.txt` and `core/hooks/extensionless.txt`:
tab-separated or `key=value` data, authored by hand, read by exactly one law module, and **never
prose**. It is not an `UPPERCASE.md` awaiting classification — the type allowlist stays closed and
untouched, which is the whole reason the shape is worth naming. The two sitting at `core/` root
rather than beside their reader are placed by the rule above: they govern everything, so they do not
live inside one of the things they govern.

**The extension names the shape** (ruled 2026-08-17, Lucas: *"`.txt` seems too naive"*). The class
is one idea but not one format, and `.txt` was carrying three jobs while saying "unstructured text"
about a file with a closed seven-column header:

| shape | extension | files |
|---|---|---|
| tab-separated table with a header row | `.tsv` | `core/features.tsv`, `core/profile.tsv`, `core/tools/deps.tsv` |
| one value per line, no columns | `.txt` | `core/hooks/vendored.txt`, `generated.txt`, `extensionless.txt`, `gitignore-exceptions.txt` |
| `key=value` | `.env` | `core/hooks/limits.env` |

`.tsv` is a registered media type (`text/tab-separated-values`), so this buys editor and diff
support as well as honesty. The rule is what makes the two that did **not** move right *by the
rule* rather than by accident, which is the half worth keeping: a one-value list genuinely is plain
text, and only the tables were mislabelled.

`SPEC.md` is **not** a type: it collapses into `SPECS.md` (decided 2026-07-30, Lucas). The
singular/plural pair was the sharpest asymmetry in the corpus — two spellings, one meaning — and it
had leaked into enforcement, so the `> spec:` convention, `core/hooks/pre-commit` §1d,
`core/hooks/read/spec-read-gate.py`, `core/hooks/read/context-tracker.py`, `core/tools/wos/spec-scan` and
`core/tools/wos/spec-contract-check` all move with it.

### A type that outgrows the cap is cut

**Cutting is the rule; a sibling file is the exception and needs Lucas's explicit OK** — the
[`cap`](norms/cap.md) norm, stated once here for every type. Delete what repeats, what nobody
reads, and what a generator already derives. A split preserves the mass across more files, which
is the fix that only looks like one, and it is how this workspace reached nine roadmaps.

Two traps when cutting: a deleted file's row in the transient-exemption table keeps its exemption
alive, because every backticked name there is parsed as one; and the document you are deleting can
be the sole record of something live, so read it out before it goes.

**When a sibling is approved it is `TYPE-<slug>.md`, with the unsuffixed file as the index**, slug
in lowercase kebab-case. That shape is not a style preference — three gates assume it and reject
any other. `type-gate.py` reads `^[A-Z][A-Z0-9_.-]*\.md$` as a *type name*, so `ROADMAP-F4.md` is
rejected as an unknown type while `ROADMAP-verify.md` passes as an instance;
`entropy_naming.TYPE_SLUG` accepts a suffix only as `[a-z0-9]+(?:-[a-z0-9]+)*`; and
`citation-gate.LEDGER_NAMES` matches `^ROADMAP(-[a-z0-9-]+)?\.md$` on filename rather than path,
so a suffix it does not match turns every item number inside the sibling into a blocking violation.

The index then keeps three things and nothing else: what is true of every sibling, any list the
type's own rule says lives in exactly one place, and the generated routing table. The check that
makes "as small as possible" checkable: **a reader who has read only the index names the sibling
that answers their question, and is never wrong.**

### What a shard publishes about itself

A shard's header exists for one reader — the index's generated table — and every field earns its
place by answering *should I open this file?*, never *what does it say?*

**The decision is binary and its two errors are not symmetric.** Skipping a shard that held what the
task needed is silent: the session duplicates work, contradicts a settled decision, or reopens a
rejected idea. Opening one that was not needed costs a read and is visible. So the header is tuned
against the silent error, and a field that only saves a read is cut.

**The header is `>` lines under the H1, not YAML frontmatter.** Frontmatter is the contract for the
agent-library *layers* — skill, flow, agent, norm — which are loaded as prompts. A shard belongs to
the document family, and every type in it declares itself the same way `CONTEXT.md` does: `#` name,
then `> ` description, then `> key: value` — the shape `code/`'s `> spec:` already rides on, and,
unlike frontmatter, one that renders where a human can see it.

| field | ROADMAP | SCHEMA | SPECS | SETUP | value |
|-------|:---:|:---:|:---:|:---:|-------|
| line 2 onward, no key | ✅ | ✅ | ✅ | ✅ | **two to three sentences** — see § What a description must say |
| `priority` | ✅ | — | — | — | `essential` \| `important` \| `desirable` |
| `blocked-by` | ✅ | — | — | — | shard filenames, comma list |
| `answers` | — | ✅ | — | — | the questions this law settles |
| `governs` | — | — | ✅ | — | the paths or modules it constrains, same job as a `> spec:` line |
| `feature` | — | — | — | ✅ | an install step or feature the registry carries — the join `SETUP.md` already declares |
| `enforced-by` | — | ✅ | ✅ | — | the gates that apply it |

**A wrapped field is one field** — a `>` line that is not itself a `key:` continues the one above it.
It did not until 2026-08-24: the third enforcer `SCHEMA-vocabulary.md` names sat on the wrapped line
and was dropped, so the index published two where the law declares three. One parser reads this
shape for everyone, [`core/hooks/routing/header.py`](hooks/routing/header.py).

#### Every field that names our own code is verified

**Ruled 2026-08-24 (Lucas).** `enforced-by`, `blocked-by`, `governs` and `spec` name
paths; `feature` names the registry. [`entropy_fields.py`](hooks/entropy/entropy_fields.py) checks
each against the tree — blocking through `type-gate.py` on what a commit adds, reporting through the
dashboard on everything. Numbers already had *"re-run it, never quote it"*; claims about our own
tree, cheaper to check than any number, had nothing and kept being inherited as fact. A field a
parser already reads needs **no new habit and reaches backwards**: it charged every declaration the
day it landed, and three were wrong — including this table's own line claiming the generator checked
`blocked-by`. **Its accepted limits:** it never reaches prose, the price of the option nobody has to
remember, and inside `governs`, which mixes paths with qualifiers, only path-shaped tokens are read
— matching a shape rather than a word is what keeps a check like this from being switched off.

### What a description must say

**Ruled 2026-08-19 (Lucas): *"as 'Description' tão bem sucintas e muitas vezes não explicam de que
se trata o arquivo de forma minimamente decente."*** Both halves of that were true and they had one
cause. The bound was **80 characters**, which cannot hold a question and its object, so it wrote the
prose: thirty-odd shard descriptions were shaped to fit it, and `core/tools/wos/session/reads`
published itself as *"which files a"* — the literal end of its first comment line, not a truncation.

Three rules, and the first is the one that matters:

1. **Name the question the file answers, not its topic.** *"Tier 0 checks, the ratchet, and rules
   declared but unbuilt"* names a neighbourhood; *"does the tree still have the shape we said it
   has, and does anything check?"* tells a reader whether their answer is inside. A topic makes the
   open-or-skip decision a coin flip, which is the whole failure.
2. **Add the discriminator** — what is in here as opposed to the file next door. Most wrong opens
   are between two plausible neighbours, and one clause settles it.
3. **Two to three sentences**, bounded by `hoist.DESC_LIMIT`. The generator reads the whole `>`
   block and stops at the first `key:` field, so prose comes first and fields after; a code file's
   description is read the same way from its leading `#` comment paragraph. A routing block is
   exempt from the 120-column cap, so length here costs no violation.

**A truncated description is a finding, not a rendering.** The `…` means an author wrote past the
bound and the table published half a sentence — fix the source, never the cut.

**Everything countable is counted, never declared.** The generator derives open items, the
needs-Lucas count, the item slugs (`entropy_ledger.ITEM_SLUG`), line count and last touch, and writes
them into the index's table. A declared count is a second copy of a fact, and this workspace has the
receipts: `ROADMAP.md` § How to read this carried a hand-kept count that **went stale four times**,
twice while the paragraph asking to keep it true sat directly above it. Deriving it deletes the
paragraph and the failure mode together.

**The table names the marker in words, not the emoji.** `🔴` is defined only inside the file that
uses it, so a column headed `🔴` asks the reader to have already read the thing they are deciding
whether to read. The column is `Needs Lucas`. Body markers are a separate question, untouched here.

**A column empty for every shard is not emitted**, the rule `build_file_rows` already follows, which
is what lets one generator serve all three types without knowing which it is looking at.

`MEMORY.md` earns its row on symmetry: `~/.claude/projects/<slug>/memory` is a symlink to
`brain/memory/`, so it stands to [`brain/memory/`](../brain/memory/CONTEXT.md) exactly as `GOALS.md`
stands to `brain/goals/` — an index and router over a directory of instances, one line each, loaded
every session. The instances themselves are lowercase and need no type. **It is the one type written
by the agent rather than authored**, which is why its content is checked like any other file.

`SETUP.md` earns its row on the evidence: `README.md` is **repo-root only**, and several instances
sit in directories that are not repos — the workspace root, `academy/`, `code/`, `code/_templates/`.
"How do I make this work" is not "what is this and how do I run it". **The type survives — ruled
2026-08-16 (Lucas), and the question is closed.** The install path does not stop being prose, it
becomes *executable* prose: the harness the newcomer already opened is what performs the install,
reading this file as a procedure. That makes `SETUP.md` the deliverable rather than the thing an
installer replaces. The per-directory instances answer a question no installer covers — `code/`
holds per-language setup, `academy/` the LaTeX toolchain — so they are not install steps that a
root-level script absorbs.
