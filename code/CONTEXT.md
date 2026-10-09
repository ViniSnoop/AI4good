# Code
> Software projects developed under this workspace

You are a SENIOR software architect, your code WILL be evaluated!

**Before editing any file:**
1. Read it first. Before modifying a function, grep for all callers. Research before you edit.
2. Read the facade (`index.ts` / `__init__.py`) of every module you'll touch.

**You enforce this — no hook can:**
- REUSE always. NEVER copy-paste: refactor, extract a function or class.
- ONE responsibility per file — SMALL IS BETTER.
- REFACTOR after each coding prompt, and report only *after* refactoring.
- Names must be guessable without reading files, functions, or inspecting variables.

**Language rules, file templates, and the R1–R6 style table:** [SPECS-style.md](SPECS-style.md) § Style Rules (R1-R6).

**Git Flow**, the branch gate's scope, and the push policy: [SPECS-git.md](SPECS-git.md).

**Hooks block automatically** — each explains itself and names the fix when it fires, so only the numbers you need
*while writing* are here: files warn at **150 lines**, hard-block at **200**. The rest (facade boundaries, missing
first-line comments, duplicated blocks, the CONTEXT.md chain, interface stubs, `verify:fast` green, an ISSUES FIXED flip
needing a `test/**/b<N>-*` spec) surface at the moment they apply. Reasoning behind them:
[ROADMAP-verify.md](ROADMAP-verify.md).

**New project**: needs `CONTEXT.md` + `README.md`. Templates: [`_templates/`](_templates/).

**CONTEXT.md files**: line 2 = `> description`, line 3 = `> spec:` for a module. The routing block is auto-managed —
never edit it by hand.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`_templates/`](_templates/CONTEXT.md) | Project scaffolding templates — CONTEXT.md, README.md, SPECS.md, ROADMAP.md skeletons |
| [`mlp-heart-disease/`](mlp-heart-disease/CONTEXT.md) | Classificação de risco de doença cardíaca com MLP do zero e visualizador Streamlit |

| File | API | Description |
|------|-----|-------------|
| [`ROADMAP-spec-drive.md`](ROADMAP-spec-drive.md) | — | Enforcement rollout making the spec the contract for `code/` modules: verifiable inputs/outputs/invariants that precede and govern the code. Goal: [spec-driven-development](../brain/goals/spec-driven-development.md). |
| [`ROADMAP-verify.md`](ROADMAP-verify.md) | — | Testing-discipline rollout for `code/` projects: make agents verify their own results (no human eye per prompt) and enforce code centralization. Pilot: isoroll-module. Second: apptime. |
| [`SETUP.md`](SETUP.md) | — | Per-language setup, facade templates, and project scaffolding reference |
| [`SPECS-git.md`](SPECS-git.md) | — | Which branches exist, what may be committed where, and when work is pushed. |
| [`SPECS-structure.md`](SPECS-structure.md) | — | How a project is laid out: its files, its module specs, and its facade. |
| [`SPECS-style.md`](SPECS-style.md) | — | How a file is written, how big it may get, and when a directory splits. |
| [`SPECS.md`](SPECS.md) | — | Engineering conventions, architecture decisions, and process rules for all code/ projects. |
| [`eslint.shared.js`](eslint.shared.js) | `localPlugin`, `sharedRules`, `countCallsInSubtree`, `getChainDepth` | Shared ESLint rules for all TypeScript/JavaScript projects under code/ — R1-R6 style enforcement. |
| [`scaffold.sh`](scaffold.sh) | — | Scaffold a new code project directory with course template files. Usage: ./scaffold.sh <project-name> |
<!-- routing:end -->
