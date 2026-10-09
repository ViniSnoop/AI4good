# Papers
> LaTeX papers, submissions, manuscript workflows

Each paper is its own subdirectory with its own git repo (Overleaf as remote). Local compilation is
primary; Overleaf is the sync/checkpoint for final validation.

Every rule that constrains a paper — naming, file size, first-line comments, the `.texif` interface,
the `refs/` schema and tag vocabulary, writing quality, evidence discipline, git — plus how to
scaffold a new paper and how to build one: [SPECS.md](SPECS.md).

## Research

`/research lit "topic"` · `/research review sections/03_related_work.tex` · plus the CLI tools in
[core/tools/CONTEXT.md](../../core/tools/CONTEXT.md) (`papers`, `search`, `fetch`). Workflow
protocols: [core/flows/](../../core/flows/CONTEXT.md).

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`ROADMAP.md`](ROADMAP.md) | Papers Roadmap |
| [`SPECS.md`](SPECS.md) | What must be true of every paper under `academy/papers/`, and why. Extracted from `CONTEXT.md` on 2026-07-30: `context-gate` forces the whole CONTEXT.md chain before any file access, so a constraint written there was a tax on every session in the subtree — opening one `.tex` cost 2.4k tokens. SPECS is loaded on demand. |
| [`history.txt`](history.txt) | ← add first-line comment |
| [`readme.txt`](readme.txt) | ← add first-line comment |
| [`samplepaper.tex`](samplepaper.tex) | This is samplepaper.tex, a sample chapter demonstrating the |
<!-- routing:end -->
