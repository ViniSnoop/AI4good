# Papers
> LaTeX papers, submissions, manuscript workflows

Each paper is its own subdirectory with its own git repo (Overleaf as remote). Local compilation is
primary; Overleaf is the sync/checkpoint for final validation.

**Every rule that constrains a paper — naming, file size, first-line comments, the `.texif`
interface, the `refs/` schema and tag vocabulary, writing quality, evidence discipline, git —
lives in [SPECS.md](SPECS.md).** That file is loaded on demand, which is the whole point: this one
sits on the always-loaded path and SPECS does not.

## Starting a new paper

```bash
python3 /mnt/workspace/core/hooks/paper-scaffold.py new <paper-name>
```

Creates the full standard layout: `main.tex`, `.latexmkrc`, `.gitignore`, `labels.md`, and a
`CONTEXT.md` for the root and for `sections/`, `refs/`, `lib/`, `images/`, `tables/`, `outputs/` —
with `refs/CONTEXT.md` pre-filled with the tag schema and workflow.

Add missing scaffold files to an **existing** paper without overwriting:

```bash
python3 /mnt/workspace/core/hooks/paper-scaffold.py adapt <path-to-paper>
```

The `post-edit` hook warns with the `adapt` command if `refs/CONTEXT.md` is missing when a `.tex`
file is saved.

## Building

```bash
cd /mnt/workspace/academy/papers/<paper-folder>
latexmk -xelatex -halt-on-error -interaction=nonstopmode main.tex
latexmk -C && latexmk -xelatex -halt-on-error -interaction=nonstopmode main.tex  # clean rebuild
```

Use XeLaTeX for document classes that require `fontspec` (e.g. SBC/JBCS). Artifacts go to `build/`;
the PDF lands at the paper root.

## Research

`/research lit "topic"` · `/research review sections/03_related_work.tex` · plus the CLI tools in
[core/tools/CONTEXT.md](../../core/tools/CONTEXT.md) (`papers`, `search`, `fetch`). Workflow
protocols: [core/flows/](../../core/flows/CONTEXT.md).

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`2026-JBCS-relativistic_raytracer/`](2026-JBCS-relativistic_raytracer/CONTEXT.md) | JBCS special issue paper on relativistic raytracing benchmarking for SVR 2026 |
| [`2026-SIBGRAPI-relativistic_raytracer/`](2026-SIBGRAPI-relativistic_raytracer/CONTEXT.md) | SIBGRAPI 2026 paper on relativistic raytracing benchmarking |
| [`2027-CHI-cria/`](2027-CHI-cria/CONTEXT.md) | Hybrid human-AI ideation as mechanism design — classroom study. Targets: LBW CHI |
| [`2027-ICLR-dobra/`](2027-ICLR-dobra/CONTEXT.md) | Context folding + SLMs on consumer hardware — research twin of `code/dobra`. Tar |
| [`ai4good/`](ai4good/CONTEXT.md) | Visão + sistema + piloto: o papel moral da IA — da captura de atenção e da guerr |
| [`mechanism-search/`](mechanism-search/CONTEXT.md) | Paper embrião: busca de mecanismos sociais com LLMs ancorada em dados de fluxo f |
| [`megatruth/`](megatruth/CONTEXT.md) | Hybrid intelligence paper — crowd truth aggregation via mechanism design |
| [`mutual-credit-ai/`](mutual-credit-ai/CONTEXT.md) | Paper embrião: agentes de IA resolvendo a iliquidez de moedas complementares — c |
| [`pls-pix/`](pls-pix/CONTEXT.md) | Paper embrião: prize-linked savings via Pix contra o dreno das bets no Brasil —  |
| [`spacemantics/`](spacemantics/CONTEXT.md) | Benchmark+method paper: a verifiable spatial DSL lifts LLM spatial capability ac |

| File | Description |
|------|-------------|
| [`ROADMAP.md`](ROADMAP.md) | Papers Roadmap |
| [`SPECS.md`](SPECS.md) | Papers — Specs |
<!-- routing:end -->
