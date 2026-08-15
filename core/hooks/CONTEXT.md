# hooks
> The enforcement layer: git hooks, agent lifecycle hooks, and the Tier 0 checks they run.

Wired globally via `git config --global core.hooksPath /mnt/workspace/core/hooks`, so
`pre-commit` fires in **every** repo under this workspace, and by absolute path from
`.claude/settings.json` for the agent-side gates.

## The law lives in these files, not in any checker

| File | Owns |
|------|------|
| [`file_law.py`](file_law.py) | what a file **is** — `is_code_file`, `is_vendored`, `allowed_extensionless`, `load_limits` |
| [`schema_law.py`](schema_law.py) | what a name **may be** — parsed from [`core/SCHEMA.md`](../SCHEMA.md) |
| [`limits.env`](limits.env) | every number: `WARN_LINES`/`BLOCK_LINES`, `WARN_FILES`/`BLOCK_FILES` |
| [`vendored.txt`](vendored.txt) | third-party trees exempt from our authoring rules |
| [`extensionless.txt`](extensionless.txt) | names an external tool dictates (git hooks, `Makefile`) |

**A checker that restates any of these is the drift the checkers exist to catch.** Two
incidents that shape this rule, and the test that guards the first: [`SPECS.md`](SPECS.md).

## Shape — the root holds the law, every subdirectory holds one responsibility

Only the two law modules, the shared hook-stdin parser, and the three entrypoints whose
names are dictated by git/`.claude/settings.json` (`pre-commit`, `post-commit`,
`post-edit.sh`) stay at the root. Everything else lives in a subdirectory with its own
responsibility, routed through the table below.

Two axes worth knowing before you route:

- **Sourced vs executed.** `gates/`, `generators/` and `postedit/` hold *fragments* that are
  `source`d by `pre-commit` / `post-edit.sh` and share their shell state. Every other
  directory holds standalone programs, run by path.
- **Reject vs write.** A gate exits non-zero and stops the commit or the edit; a generator
  writes an artifact and stages it. `entropy/` does neither — it reports, into
  [`entropy.md`](../../entropy.md); read that report instead of re-scanning the tree.

Python modules in a subdirectory reach the root law with
`sys.path.insert(0, str(Path(__file__).resolve().parents[1]))`. The test suite gets the same
path set once, from `core/tools/test/conftest.py`, derived by scanning this directory.

Gate behavior and the agent-shim contract: [`SPECS.md`](SPECS.md). Why the `code/` gates
exist: [`code/VERIFY.md`](../../code/VERIFY.md). Installing the toolchain they depend on:
[`SETUP.md`](../../SETUP.md).

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
| [`read/`](read/CONTEXT.md) | Who must read what before touching a subtree — and who gets handed it instead. |
| [`routing/`](routing/CONTEXT.md) | The CONTEXT.md routing-table generator. |
| [`session/`](session/CONTEXT.md) | Session lifecycle: start, prune, precompact wipe, and the SessionStart nudges. |
| [`stubgen/`](stubgen/CONTEXT.md) | Interface stubs and paper scaffolding, generated on save and on commit. |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | Hooks — Specs |
| [`file_law.py`](file_law.py) | [`file_law.pyi`](file_law.pyi) | `is_code_file`, `load_limits`, `allowed_extensionless`, `is_vendored`, `main` | What a file IS, and which rules apply to it. The numeric-law sibling of schema_law.py: |
| [`hook_input.py`](hook_input.py) | [`hook_input.pyi`](hook_input.pyi) | `parse_stdin`, `is_subagent`, `seen_file`, `load_seen`, `mark_seen` | Shared parser for Claude Code hook stdin JSON — nested (current) and flat (legacy shim) schemas. |
| [`post-commit`](post-commit) | — | — | auto-push feature/* so work survives a dead session |
| [`post-edit.sh`](post-edit.sh) | — | — | PostToolUse: Edit, Write — regenerates interfaces, checks first-line comment, syncs CONTEXT.md |
| [`pre-commit`](pre-commit) | — | — | the dispatcher. |
| [`schema_law.py`](schema_law.py) | [`schema_law.pyi`](schema_law.pyi) | `load_law`, `load_scopes`, `load_retired` | The law parser. Every Tier 0 check reads core/SCHEMA.md through this module, and none |
<!-- routing:end -->
