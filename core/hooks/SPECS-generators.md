# Generated artifacts
> What the hooks write rather than reject, and what must be true of each artifact.
> governs: core/hooks/generators/, core/hooks/routing/, core/hooks/stubgen/

## Generated artifacts

### Interface files

Every save of a supported source file produces its interface unconditionally — universal, no
per-project config.

| Language | Output | Tool | Notes |
|----------|--------|------|-------|
| Python | `.pyi` | `stubgen` | on every edit and every commit |
| JavaScript | `.d.ts` | `tsc --allowJs --emitDeclarationOnly` | `jsconfig.json` auto-scaffolded if missing (IDE use only) |
| TypeScript | `.d.ts` | `tsc --emitDeclarationOnly` | `tsconfig.json` auto-scaffolded if no ancestor config is found |
| Dart | `.dart.api` | `stubgen/dart-api-extract.py` | public class/mixin/method signatures; needs Python 3 only, no Dart SDK |
| LaTeX | `.texif` | `stubgen/tex-interface-gen.py` | structure, full equations, floats, citations, TODOs, section opening sentences. Also regenerates `labels.md` (cross-file label registry + dangling-ref check). A `.bib` edit warns about missing `reviews/<key>.yaml` |

**To bypass the size gate temporarily**, edit `BLOCK_LINES` in [`limits.env`](limits.env), do the
operation, revert. Both `checks/pre-edit.py` and `checks/check-line-counts.sh` read it immediately.

### A file a tool writes is not a file anyone authored

`ARCHITECTURE.html` forced the third answer (2026-08-18). Until then a file was either **ours and
authored** — every size, shape and first-line rule applies — or **vendored**, listed in
[`vendored.txt`](vendored.txt) and exempt because upstream chose its layout. A generated page is
neither: `.html` is in `CODE_EXTS`, so the 200-line cap blocked the commit that first carried it,
and filing our own output under "third-party we did not author" would have bought the exemption with
a lie that misleads every later reader of both lists.

So [`generated.txt`](generated.txt) declares what our tools write, on the same contract as its
sibling — a **named, reviewed glob list, never a heuristic**, each entry naming its generator — and
`file_law.is_authored()` is now the one question every size and shape gate asks: code, ours, and
written by a person. It replaced the same condition spelled out at four call sites
(`checks/pre-edit.py`, `entropy/entropy-dashboard.py`, `entropy/entropy_fanout.py`, and
`file_law.py --filter-code`, which is how the shell gate inherits it), which is where the three
answers would otherwise have started disagreeing.

**Why the exemption is safe here and not in general:** the artifact has a test that its generator
can reproduce it byte for byte (`--check`), so nothing hides behind the exemption. An entry without
that property is a hand-edited file wearing a generated file's coat.

### The `CONTEXT.md` routing block

`routing/context_synchronizer.py` runs on every edit (via `post-edit.sh`, which also re-syncs the
parent directory) and every commit. It keeps each directory's `## Routing` block true without
anyone maintaining it:

- **adds** a new file, taking its description from the first source that answers, in this order:
  the first-line comment (code, below any shebang), a module docstring's first line (`.py`, per
  PEP 257), `description:` frontmatter then the line-2 `> ` blurb (`.md`), or the ` — ` usage
  comment (extensionless scripts)
- **removes** entries for deleted files, and **links** interfaces to their source
- **folds** a leaf directory under `WARN_FILES` into the parent block; **links** one at or above it,
  or one that carries its own `CONTEXT.md`
- **warns** when a directory exceeds `WARN_FILES` direct files

**Never edit inside the `<!-- routing:start/end -->` sentinels** — the next sync overwrites it.
**Renames are not tracked**: the old entry disappears and the new file arrives with a placeholder,
so the description is rewritten by hand after a rename.

**A `← add` marker is a claim about the generator before it is a claim about the file.** Four times
out of four (2026-08-15) the text was already there and this list was not reaching for it: `.sh` and
`.jsx` had no `COMMENT_RE` pattern, `.py` matched only a single-line docstring, `.env`/`.txt` were
outside `CONTENT_EXTS`, and `.md` rows read the H1 instead of the blurb. **Check the extension's
entry in `routing/workspace_meta.py` before writing a description by hand** — and when a whole
extension is undescribable, fix it there, because a sweep re-fills.

**Hoisted text is bounded and rebased; authored text is not.** A `.md` blurb and a subdirectory
blurb were written to sit under their own heading, in their own directory, so
[`routing/hoist.py`](routing/hoist.py) rebases their links and cuts them at `DESC_LIMIT`. A code
file's first-line comment goes in untouched: it was authored as this table's one-liner and cutting
it would lose text nothing else carries.

### First-line descriptions

Every scanned file begins with a one-line description, because `context_synchronizer.py` reads it as
the canonical description and writes it into `CONTEXT.md`. Enforced at **Write** (`pre-edit.py`
blocks), at **Edit** (a reminder prints, the edit stands), and at **commit** —
`entropy_context.check_description`, run by `checks/type-gate.py` over the files the commit adds.

**The commit gate is the load-bearing one, and it was the missing one.** `pre-edit.py` only fires
under `if not os.path.exists(file_path)`, so it covers creation through Edit/Write and nothing else:
a file written by a generator, a shell heredoc, `git checkout`, or an agent not running our hooks
was never asked. 150 markers across 54 `CONTEXT.md` accumulated under a rule that was already in
force — **an edit-time check only covers the harness path; the staged set is what covers everyone.**

**The check asks the generator, never its own pattern table.** `check_description` calls
`workspace_meta.file_description()` — the same call whose empty return makes the generator write
`← add first-line comment` — and `workspace_scanner.is_scanned()` to decide who is even asked, so
the gate's scope and the table's scope are one definition. The alternative was tried by accident and
cost a session: `ALL_EXTS` and `COMMENT_RE` disagreed, `.sh` and `.jsx` were scanned with no comment
pattern, and 59 well-commented files were marked undescribable — one of them inside this directory,
which was read as proof of a discipline hole until the generator was asked. **A marker is not
evidence of a discipline problem until the generator has been asked whether it can answer it.**

### Finished-work prose is blocked on what a commit adds

`entropy/entropy_ledger.py` carries the detector — strikethrough, a dated completion report, a
settled-marker, and a ticked item inside a ledger — and `checks/type-gate.py` calls it on
`staged_added_files()`. So a file **arriving** with a corpse in it is rejected, while the inherited
queue stays the dashboard's and rides the ceiling in `test_corpus_ratchet.py` instead of failing
every commit. That split is the rule for every Tier 0 check here, not a concession to this one:
a gate that fails on the day it lands trains its reader to ignore it.

Completion is deletion (`core/SCHEMA.md` § No archive types), and
[`core/SPECS-discipline.md`](../SPECS-discipline.md) § AD-15 makes blocking — not the mere existence of a detector —
what licenses deleting the prose.
