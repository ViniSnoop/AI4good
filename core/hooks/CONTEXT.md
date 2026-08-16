# hooks
> The enforcement layer: git hooks, agent lifecycle hooks, and the Tier 0 checks they run.

Wired globally via `git config --global core.hooksPath /mnt/workspace/core/hooks`, so
`pre-commit` fires in **every** repo under this workspace, and by absolute path from
`.claude/settings.json` for the agent-side gates.

## The law lives in this directory's root, not in any checker

Two modules answer the two questions — [`file_law.py`](file_law.py) what a file **is**,
[`schema_law.py`](schema_law.py) what a name **may be** — and each reads its answer out of a
data file beside it rather than holding one: the numbers, the vendored trees, the
extensionless names, the `.gitignore` exceptions. The routing table below names all six.

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
| [`SPECS.md`](SPECS.md) | — | — | What must be true of the enforcement layer, and why: what each gate blocks, and… |
| [`extensionless.txt`](extensionless.txt) | — | — | Files allowed to have no extension because something OUTSIDE this workspace dictates the |
| [`file_law.py`](file_law.py) | [`file_law.pyi`](file_law.pyi) | `is_code_file`, `load_limits`, `allowed_extensionless`, `is_vendored`, `main` | What a file IS, and which rules apply to it. The numeric-law sibling of schema_law.py: |
| [`gitignore-exceptions.txt`](gitignore-exceptions.txt) | — | — | One "<domain>/<dir>" per line: a CONTEXT.md-bearing subdir Lucas deliberately wants left |
| [`hook_input.py`](hook_input.py) | [`hook_input.pyi`](hook_input.pyi) | `parse_stdin`, `is_subagent`, `seen_file`, `load_seen`, `mark_seen` | Shared parser for Claude Code hook stdin JSON — nested (current) and flat (legacy shim) schemas. |
| [`limits.env`](limits.env) | — | — | Every numeric limit in the workspace, in one file. Read by core/hooks/file_law.py |
| [`post-commit`](post-commit) | — | — | auto-push feature/* so work survives a dead session |
| [`post-edit.sh`](post-edit.sh) | — | — | PostToolUse: Edit, Write — regenerates interfaces, checks first-line comment, syncs CONTEXT.md |
| [`pre-commit`](pre-commit) | — | — | the dispatcher. |
| [`schema_law.py`](schema_law.py) | [`schema_law.pyi`](schema_law.pyi) | `load_law`, `load_scopes`, `load_retired` | The law parser. Every Tier 0 check reads core/SCHEMA.md through this module, and none |
| [`vendored.txt`](vendored.txt) | — | — | Third-party files we did not author. Excluded from the line cap, the fanout signal and |
<!-- routing:end -->
