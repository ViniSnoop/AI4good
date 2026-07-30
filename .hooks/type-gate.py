#!/usr/bin/env python3
# Tier 0 gate (ROADMAP.md Frente 4.1): a staged file must be a known .md type or a
# well-shaped instance, must sit where its type is allowed to live, and a CONTEXT.md must
# not hand-list files. Zero-token, deterministic, no LLM.
#
# The law is PARSED from core/SCHEMA.md by schema_law.py, never restated here. It was
# already duplicated across three files before this gate existed, which is the exact drift
# class the gate is meant to catch — a second copy in the checker would be the same bug
# wearing a lab coat.
#
# Ratchet, like the spec-drive gate (.hooks/pre-commit 1d): only files this commit ADDS
# are blocked. Pre-existing violations are reported by the entropy dashboard
# (entropy-dashboard.py, Frente 4.3), not by failing every commit in a repo that
# inherited them.
import re
import subprocess
import sys
from pathlib import Path

from entropy_context import check_goal_link, check_inventory
from entropy_naming import check_dirs, check_placement, check_shape
from schema_law import SCHEMA, WORKSPACE_ROOT, load_law, load_scopes

# CLAUDE.md is mandated by the harness, not chosen by us; a gate cannot un-invent it.
HARNESS_MANDATED = {'CLAUDE.md'}

UPPERCASE_MD = re.compile(r'^[A-Z][A-Z0-9_.-]*\.md$')


def check_name(path: Path, allowed: set, exempt: set) -> str | None:
    name = path.name
    if not UPPERCASE_MD.match(name):
        return None
    if name in allowed or name in exempt or name in HARNESS_MANDATED:
        return None
    return (f"{path}: '{name}' is not a known .md type.\n"
            f"   Route it (core/SCHEMA.md § The four disposal routes): generated or plain\n"
            f"   content -> lowercase instance; a constraint -> SPECS.md; or add it to the\n"
            f"   allowlist in core/SCHEMA.md § The `.md` type system if you mean it.")


def staged_added_files() -> list:
    """Only files this commit ADDS — the ratchet. Renames count as adds of the new name."""
    out = subprocess.run(['git', 'diff', '--cached', '--name-only', '--diff-filter=AR'],
                         capture_output=True, text=True).stdout
    return [Path(line) for line in out.splitlines()]


def failures_for(path: Path, allowed: set, exempt: set, scopes: dict) -> list:
    return [f for f in (check_name(path, allowed, exempt),
                        check_inventory(path) if path.name == 'CONTEXT.md' else None,
                        check_goal_link(path),
                        check_shape(path, allowed),
                        check_dirs(path, WORKSPACE_ROOT),
                        check_placement(path, scopes, WORKSPACE_ROOT)) if f]


def main() -> int:
    if not SCHEMA.exists():
        return 0  # not the workspace repo; nothing to enforce against
    allowed, exempt = load_law(SCHEMA)
    scopes = load_scopes(SCHEMA)
    failures = []
    for path in staged_added_files():
        if path.exists():
            failures.extend(failures_for(path, allowed, exempt, scopes))
    if failures:
        print('⛔ type gate:')
        for failure in failures:
            print(f'   {failure}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
