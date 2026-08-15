# hooks
> The enforcement layer: git hooks, agent lifecycle hooks, and the Tier 0 checks they run.

Wired globally via `git config --global core.hooksPath /mnt/workspace/core/hooks`, so
`pre-commit` fires in **every** repo under this workspace, and by absolute path from
`.claude/settings.json` for the agent-side gates. Moved here from `.hooks/` on 2026-07-31 —
nothing about it was Claude-specific, and hidden meant unmonitored by its own checks.

## The law lives in two files, never in a checker

| File | Owns |
|------|------|
| [`file_law.py`](file_law.py) | what a file **is** — `is_code_file`, `is_vendored`, `allowed_extensionless`, `load_limits` |
| [`schema_law.py`](schema_law.py) | what a name **may be** — parsed from [`core/SCHEMA.md`](../SCHEMA.md) |
| [`limits.env`](limits.env) | every number: `WARN_LINES`/`BLOCK_LINES`, `WARN_FILES`/`BLOCK_FILES` |
| [`vendored.txt`](vendored.txt) | third-party trees exempt from our authoring rules |
| [`extensionless.txt`](extensionless.txt) | names an external tool dictates (git hooks, `Makefile`) |

**A checker that restates any of these is the drift the checkers exist to catch.** It has
happened twice: five separate definitions of "a code file" (fixed 2026-07-31, guarded by
`test_no_checker_carries_its_own_extension_list`) and a hard-coded sibling path that stopped
exempting the retired-token checker the moment this directory moved.

## Shape — the root holds the law, every subdirectory holds one responsibility

Split 2026-07-31 at 50 files in one flat directory. Only four things stay at the root: the
two law modules, the shared hook-stdin parser, and the three entrypoints whose names are
dictated (`pre-commit` and `post-commit` by git, `post-edit.sh` by `.claude/settings.json`).
Everything else routes through the table below.

The split is real, not cosmetic: a subdirectory under `WARN_FILES` folds back into this
table unless it carries its own `CONTEXT.md`, so each one declares itself and the parent
table went 50 rows → 19. **Moving files without paying that cost would satisfy the fanout
count while leaving the reader exactly as much to hold** — the check would have been gamed
rather than answered.

Two axes worth knowing before you route:

- **Sourced vs executed.** `gates/`, `generators/` and `postedit/` hold *fragments* that are
  `source`d by `pre-commit` / `post-edit.sh` and share their shell state. Every other
  directory holds standalone programs, run by path.
- **Reject vs write.** A gate exits non-zero and stops the commit or the edit; a generator
  writes an artifact and stages it. `entropy/` does neither — it reports, into
  [`entropy.md`](../../entropy.md). Read that report; never re-scan the tree.

Python modules in a subdirectory reach the root law with
`sys.path.insert(0, str(Path(__file__).resolve().parents[1]))`. The test suite gets the same
path set once, from `core/tools/test/conftest.py`, derived by scanning this directory.

Reasoning behind each gate: [`code/VERIFY.md`](../../code/VERIFY.md). Setup and the
toolchain they depend on: [`SETUP.md`](../../SETUP.md).

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`brain/`](brain/CONTEXT.md) | brain/ attention stats and the GOALS.md dashboard. |
| [`checks/`](checks/CONTEXT.md) | Standalone blocking checks the commit and edit hooks run. |
| [`copilot/`](copilot/CONTEXT.md) | Provider shim: translates Copilot hook payloads onto the canonical gates. |
| [`entropy/`](entropy/CONTEXT.md) | The entropy dashboard and the Tier 0 checks it runs over the whole tree. |
| [`facade/`](facade/CONTEXT.md) | The facade discipline: read the facade before editing, never import around it. |
| [`gates/`](gates/CONTEXT.md) | Sourced pre-commit stages that may reject the commit. |
| [`generators/`](generators/CONTEXT.md) | Sourced pre-commit stages that write artifacts and stage them. |
| [`git/`](git/CONTEXT.md) | Gates and self-heals about git state itself: branch shape, gitlinks, .gitignore. |
| [`postedit/`](postedit/CONTEXT.md) | Sourced post-edit stages: regenerate interfaces, remind, sync, lint. |
| [`read/`](read/CONTEXT.md) | Force-a-read gates: the CONTEXT.md chain, the interface stub, the module spec. |
| [`routing/`](routing/CONTEXT.md) | The CONTEXT.md routing-table generator. |
| [`session/`](session/CONTEXT.md) | Session lifecycle: start, prune, precompact wipe, and the SessionStart nudges. |
| [`stubgen/`](stubgen/CONTEXT.md) | Interface stubs and paper scaffolding, generated on save and on commit. |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`file_law.py`](file_law.py) | [`file_law.pyi`](file_law.pyi) | `is_code_file`, `load_limits`, `allowed_extensionless`, `is_vendored`, `main` | What a file IS, and which rules apply to it. The numeric-law sibling of schema_law.py: |
| [`hook_input.py`](hook_input.py) | [`hook_input.pyi`](hook_input.pyi) | `parse_stdin`, `is_subagent`, `seen_file`, `load_seen`, `mark_seen` | Shared parser for Claude Code hook stdin JSON — nested (current) and flat (legacy shim) schemas. |
| [`post-commit`](post-commit) | — | — | auto-push feature/* so work survives a dead session |
| [`post-edit.sh`](post-edit.sh) | — | — | ← add first-line comment |
| [`pre-commit`](pre-commit) | — | — | the dispatcher. |
| [`schema_law.py`](schema_law.py) | [`schema_law.pyi`](schema_law.pyi) | `load_law`, `load_scopes`, `load_retired` | The law parser. Every Tier 0 check reads core/SCHEMA.md through this module, and none |
<!-- routing:end -->
