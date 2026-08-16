#!/usr/bin/env python3
# Tier 0 gate (core/SCHEMA.md § The .md type system): a staged file must be a known .md type or a
# well-shaped instance, must sit where its type is allowed to live, and a CONTEXT.md must
# not hand-list files. Zero-token, deterministic, no LLM.
#
# The law is PARSED from core/SCHEMA.md by schema_law.py, never restated here. It was
# already duplicated across three files before this gate existed, which is the exact drift
# class the gate is meant to catch — a second copy in the checker would be the same bug
# wearing a lab coat.
#
# Ratchet, like the spec-drive gate (core/hooks/pre-commit 1d): only files this commit ADDS
# are blocked. Pre-existing violations are reported by the entropy dashboard
# (entropy-dashboard.py), not by failing every commit in a repo that
# inherited them.
import re
import subprocess
import sys
from pathlib import Path

# The law is one level up; the checks this gate runs live in entropy/.
_HOOKS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_HOOKS))
sys.path.insert(0, str(_HOOKS / 'entropy'))

from entropy_context import check_goal_link, check_inventory  # noqa: E402
from entropy_corpus import enforcement_paths, wiki_exempt_paths  # noqa: E402
from entropy_ledger import goal_vocabulary, wiki_link_hits  # noqa: E402
from entropy_naming import check_dirs, check_placement, check_shape  # noqa: E402
from schema_law import SCHEMA, WORKSPACE_ROOT, load_law, load_scopes  # noqa: E402

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


def failures_for(path: Path, allowed: set, exempt: set, scopes: dict,
                 vocabulary: set) -> list:
    found = [f for f in (check_name(path, allowed, exempt),
                         check_inventory(path) if path.name == 'CONTEXT.md' else None,
                         check_goal_link(path),
                         check_shape(path, allowed),
                         check_dirs(path, WORKSPACE_ROOT),
                         check_placement(path, scopes, WORKSPACE_ROOT)) if f]
    return found + wiki_link_hits([path], vocabulary, wiki_exempt_paths(WORKSPACE_ROOT))


def main() -> int:
    if not SCHEMA.exists():
        return 0  # not the workspace repo; nothing to enforce against
    allowed, exempt = load_law(SCHEMA)
    scopes = load_scopes(SCHEMA)
    vocabulary = goal_vocabulary(WORKSPACE_ROOT / 'brain/goals')
    failures = []
    for path in staged_added_files():
        if path.exists():
            failures.extend(failures_for(path, allowed, exempt, scopes, vocabulary))
    if failures:
        print('⛔ type gate:')
        for failure in failures:
            print(f'   {failure}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
