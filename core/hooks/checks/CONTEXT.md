# checks
> Standalone blocking checks the commit and edit hooks run.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`bugs-gate.py`](bugs-gate.py) | [`bugs-gate.pyi`](bugs-gate.pyi) | `fixed_ids`, `repo_root`, `has_spec`, `main` | PreToolUse: Edit|Write on BUGS.md — flipping a bug to FIXED requires a matching |
| [`check-duplication.py`](check-duplication.py) | [`check-duplication.pyi`](check-duplication.pyi) | `main` | Pre-commit duplication gate — jscpd over the repo; blocks when a clone involves a staged |
| [`check-line-counts.sh`](check-line-counts.sh) | — | — | Check workspace code file line counts and print warnings/errors. |
| [`citation-gate.py`](citation-gate.py) | [`citation-gate.pyi`](citation-gate.pyi) | `citation_exempt_paths`, `staged_files`, `citation_hits`, `main` | Tier 0: a roadmap item number is not a citable identifier outside the roadmap family. |
| [`heredoc-gate.py`](heredoc-gate.py) | [`heredoc-gate.pyi`](heredoc-gate.pyi) | `targets`, `in_workspace`, `written_paths`, `main` | PreToolUse: Bash — a shell heredoc that writes a workspace file meets none of the file gates. |
| [`pre-edit.py`](pre-edit.py) | [`pre-edit.pyi`](pre-edit.pyi) | `block` | PreToolUse: Edit|Write — size gate (200-line block), first-line comment, CONTEXT.md description. |
| [`type-gate.py`](type-gate.py) | [`type-gate.pyi`](type-gate.pyi) | `check_name`, `staged_added_files`, `failures_for`, `main` | Tier 0 gate (core/SCHEMA.md § The .md type system): a staged file must be a known .md type or a |
<!-- routing:end -->
