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

## Shape

- **Gates** reject: `type-gate.py`, `gitflow-gate.sh`, `bugs-gate.py`, `facade-gate.py`,
  `spec-read-gate.py`, `nested-gitlink-gate.sh`, `check-line-counts.sh`.
- **Generators** write and stage: `context_synchronizer.py`, `dart-api-extract.py`,
  `tex-interface-gen.py`, `brain_stats.py`.
- **Reports**: `entropy-dashboard.py` → [`entropy.md`](../../entropy.md). Read the report;
  never re-scan the tree.

Reasoning behind each gate: [`code/VERIFY.md`](../../code/VERIFY.md). Setup and the
toolchain they depend on: [`SETUP.md`](../../SETUP.md).

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`bash-context-gate.py`](bash-context-gate.py) | [`bash-context-gate.pyi`](bash-context-gate.pyi) | `candidates`, `context_chain`, `main` | PreToolUse: Bash — close the cat/head/grep bypass: extract workspace file paths from the |
| [`brain_common.py`](brain_common.py) | [`brain_common.pyi`](brain_common.pyi) | `git`, `touch_count`, `last_touch_date`, `replace_block` | Brain stats — shared config, git helpers, and block replacement. |
| [`brain_dashboard.py`](brain_dashboard.py) | [`brain_dashboard.pyi`](brain_dashboard.pyi) | `bar`, `area_from_file`, `timing_display`, `parse_goal_file`, `update_goals_table` | Brain stats — GOALS.md dashboard rendering (area/goal bars, active-goals table). |
| [`brain_stats.py`](brain_stats.py) | [`brain_stats.pyi`](brain_stats.pyi) | `trend_label`, `build_stats_block`, `compress_done`, `load_goal_files`, `staged_goal_files` | Brain attention tracker — per-file stats, done compression, commit orchestration. |
| [`bugs-gate.py`](bugs-gate.py) | [`bugs-gate.pyi`](bugs-gate.pyi) | `fixed_ids`, `repo_root`, `has_spec`, `main` | PreToolUse: Edit|Write on BUGS.md — flipping a bug to FIXED requires a matching |
| [`check-duplication.py`](check-duplication.py) | [`check-duplication.pyi`](check-duplication.pyi) | `main`, `rel` | Pre-commit duplication gate — jscpd over the repo; blocks when a clone involves a staged |
| [`check-facade-imports.py`](check-facade-imports.py) | [`check-facade-imports.pyi`](check-facade-imports.pyi) | `ts_violations`, `py_violations`, `dart_violations`, `check` | Blocks cross-module imports that bypass facade files (index.ts / __init__.py). |
| [`check-line-counts.sh`](check-line-counts.sh) | — | — | ← add first-line comment |
| [`compass-nudge.py`](compass-nudge.py) | [`compass-nudge.pyi`](compass-nudge.pyi) | `main` | SessionStart — a soft, ignorable reminder that the compass review hasn't run in a while, so the |
| [`context-gate.py`](context-gate.py) | [`context-gate.pyi`](context-gate.pyi) | `target_path`, `context_chain`, `main` | PreToolUse: Read|Edit|Write|Grep|NotebookEdit — force-read the CONTEXT.md chain of the |
| [`context-tracker.py`](context-tracker.py) | [`context-tracker.pyi`](context-tracker.pyi) | `main` | PostToolUse: Read — record CONTEXT.md/SPEC.md reads (consumed by context-gate.py / |
| [`context_synchronizer.py`](context_synchronizer.py) | [`context_synchronizer.pyi`](context_synchronizer.pyi) | `migrate_legacy`, `sync` | Sync the Routing block in CONTEXT.md (or AGENTS.md at workspace root). |
| [`copilot-agent.sh`](copilot-agent.sh) | — | — | ← add first-line comment |
| [`copilot-post-tool.py`](copilot-post-tool.py) | [`copilot-post-tool.pyi`](copilot-post-tool.pyi) | `emit_allow`, `main` | Copilot PostToolUse hook: regenerate interfaces, sync context, record read-trackers. |
| [`copilot-pre-tool.py`](copilot-pre-tool.py) | [`copilot-pre-tool.pyi`](copilot-pre-tool.pyi) | `emit_allow`, `gate`, `main` | Copilot PreToolUse hook: enforce workspace read/edit/terminal policy via canonical .hooks scripts. |
| [`copilot-session-start.py`](copilot-session-start.py) | [`copilot-session-start.pyi`](copilot-session-start.pyi) | `load_input`, `read_workspace_excerpt`, `load_caveman_context`, `main` | Copilot SessionStart hook: inject workspace policy context + caveman rules. |
| [`copilot_shared.py`](copilot_shared.py) | [`copilot_shared.pyi`](copilot_shared.pyi) | `load_input`, `session_id`, `normalize_path`, `collect_paths`, `first_string` | Shared plumbing for the Copilot pre/post tool shims: payload extraction + canonical hook exec. |
| [`dart-api-extract.py`](dart-api-extract.py) | — | `extract`, `main` | Extract public Dart API surface into a compact .dart.api stub file |
| [`entropy-dashboard.py`](entropy-dashboard.py) | [`entropy-dashboard.pyi`](entropy-dashboard.pyi) | `collect`, `size_signals`, `main` | The entropy dashboard (ROADMAP.md Frente 4.3). Runs every Tier 0 check over the whole |
| [`entropy_context.py`](entropy_context.py) | [`entropy_context.pyi`](entropy_context.pyi) | `check_inventory`, `is_project`, `check_goal_link` | Tier 0 CONTEXT.md rules (ROADMAP.md Frente 4.1). Zero-token, deterministic. |
| [`entropy_corpus.py`](entropy_corpus.py) | [`entropy_corpus.pyi`](entropy_corpus.pyi) | `tracked_files`, `nested_repos`, `enforcement_paths`, `walk` | Which files the Tier 0 checks look at, and which of them are allowed to name what the |
| [`entropy_fanout.py`](entropy_fanout.py) | [`entropy_fanout.pyi`](entropy_fanout.pyi) | `fanout_counts`, `fanout_signals` | Directory fanout: how many files one directory asks a reader to hold at once. |
| [`entropy_ledger.py`](entropy_ledger.py) | [`entropy_ledger.pyi`](entropy_ledger.pyi) | `retired_hits`, `item_slugs`, `duplicate_slugs`, `goal_vocabulary`, `wiki_link_hits` | Tier 0 ledger and vocabulary checks (ROADMAP.md Frente 4.1). Zero-token, deterministic. |
| [`entropy_naming.py`](entropy_naming.py) | [`entropy_naming.pyi`](entropy_naming.pyi) | `check_shape`, `check_dirs`, `check_placement` | Tier 0 naming and placement (ROADMAP.md Frente 4.1). Zero-token, deterministic. |
| [`entropy_report.py`](entropy_report.py) | [`entropy_report.pyi`](entropy_report.pyi) | `render` | The entropy report: what the dashboard's findings look like on the page. |
| [`facade-gate.py`](facade-gate.py) | [`facade-gate.pyi`](facade-gate.pyi) | `facades_read`, `find_nearest_facade`, `main` | PreToolUse: Edit|Write — block code/ module edits until the module's facade has been read. |
| [`facade-scan.py`](facade-scan.py) | [`facade-scan.pyi`](facade-scan.pyi) | — | Pre-Write hook: list existing facade exports before creating a new file in the same module. |
| [`facade-tracker.py`](facade-tracker.py) | [`facade-tracker.pyi`](facade-tracker.pyi) | `main` | PostToolUse: Read — record facade file reads to session state for facade-gate.py. |
| [`file_law.py`](file_law.py) | [`file_law.pyi`](file_law.pyi) | `is_code_file`, `load_limits`, `allowed_extensionless`, `is_vendored`, `main` | What a file IS, and which rules apply to it. The numeric-law sibling of schema_law.py: |
| [`gates/duplication-and-terms.sh`](gates/duplication-and-terms.sh) | — | — | ← add first-line comment |
| [`gates/lint.sh`](gates/lint.sh) | — | — | ← add first-line comment |
| [`gates/project-contract.sh`](gates/project-contract.sh) | — | — | ← add first-line comment |
| [`gates/source-quality.sh`](gates/source-quality.sh) | — | — | ← add first-line comment |
| [`generators/interfaces.sh`](generators/interfaces.sh) | — | — | ← add first-line comment |
| [`generators/prepare.sh`](generators/prepare.sh) | — | — | ← add first-line comment |
| [`generators/routing.sh`](generators/routing.sh) | — | — | ← add first-line comment |
| [`generators/skills.sh`](generators/skills.sh) | — | — | ← add first-line comment |
| [`gitflow-gate.sh`](gitflow-gate.sh) | — | — | ← add first-line comment |
| [`gitignore-self-heal.sh`](gitignore-self-heal.sh) | — | — | ← add first-line comment |
| [`hook_input.py`](hook_input.py) | [`hook_input.pyi`](hook_input.pyi) | `parse_stdin`, `seen_file`, `load_seen`, `mark_seen` | Shared parser for Claude Code hook stdin JSON — nested (current) and flat (legacy shim) schemas. |
| [`inbox-nudge.py`](inbox-nudge.py) | [`inbox-nudge.pyi`](inbox-nudge.pyi) | `read_body`, `count_entries`, `main` | SessionStart — warn Lucas + agent when brain/INBOX.md has piled up past a threshold, |
| [`nested-gitlink-gate.sh`](nested-gitlink-gate.sh) | — | — | ← add first-line comment |
| [`paper-scaffold.py`](paper-scaffold.py) | [`paper-scaffold.pyi`](paper-scaffold.pyi) | `scaffold`, `main`, `put` | paper-scaffold.py: Initialize or adapt a paper directory to workspace standards. |
| [`post-commit`](post-commit) | — | — | auto-push feature/* so work survives a dead session |
| [`post-edit.sh`](post-edit.sh) | — | — | ← add first-line comment |
| [`pre-commit`](pre-commit) | — | — | the dispatcher. |
| [`pre-edit.py`](pre-edit.py) | [`pre-edit.pyi`](pre-edit.pyi) | — | PreToolUse: Edit|Write — size gate (200-line block), first-line comment, CONTEXT.md description. |
| [`pre-read.sh`](pre-read.sh) | — | — | ← add first-line comment |
| [`precompact-wipe.sh`](precompact-wipe.sh) | — | — | ← add first-line comment |
| [`schema_law.py`](schema_law.py) | [`schema_law.pyi`](schema_law.pyi) | `load_law`, `load_scopes`, `load_retired` | The law parser. Every Tier 0 check reads core/SCHEMA.md through this module, and none |
| [`session-prune.sh`](session-prune.sh) | — | — | ← add first-line comment |
| [`spec-read-gate.py`](spec-read-gate.py) | [`spec-read-gate.pyi`](spec-read-gate.pyi) | `find_spec_module`, `block`, `nudge`, `main` | PreToolUse: Edit|Write — a spec-locked module (its CONTEXT.md carries `> spec:` and the referenced |
| [`start-session.sh`](start-session.sh) | — | — | ← add first-line comment |
| [`tex-interface-gen.py`](tex-interface-gen.py) | [`tex-interface-gen.pyi`](tex-interface-gen.pyi) | `write_interface`, `check_relationships`, `regenerate_labels`, `bib_check`, `main` | tex-interface-gen.py: Generate .texif interfaces, labels.md, and bib/review checks. |
| [`tex_interface_parser.py`](tex_interface_parser.py) | [`tex_interface_parser.pyi`](tex_interface_parser.pyi) | `line_of`, `extract_braced`, `extract_caption`, `first_prose_snippet`, `find_paper_root` | tex_interface_parser.py: LaTeX source parser for tex-interface-gen.py. |
| [`type-gate.py`](type-gate.py) | [`type-gate.pyi`](type-gate.pyi) | `check_name`, `staged_added_files`, `failures_for`, `main` | Tier 0 gate (ROADMAP.md Frente 4.1): a staged file must be a known .md type or a |
| [`workspace_meta.py`](workspace_meta.py) | [`workspace_meta.pyi`](workspace_meta.pyi) | `file_description`, `python_api`, `js_api`, `extract_api`, `interface_for` | Workspace metadata extraction: file descriptions, public APIs, and interface links. |
| [`workspace_scanner.py`](workspace_scanner.py) | [`workspace_scanner.pyi`](workspace_scanner.pyi) | `code_files`, `has_code_content`, `subdir_scan`, `parse_preserved_files`, `parse_preserved_subs` | Workspace scanner: directory discovery and CONTEXT.md routing-table assembly. |
<!-- routing:end -->
