#!/usr/bin/env python3
# Tier 0 type gate (ROADMAP Frente 4.1): every staged .md must be a known type or an
# instance, and a CONTEXT.md must not hand-list files. Zero-token, deterministic, no LLM.
#
# The allowlist is PARSED from core/SCHEMA.md, never restated here. It was already
# duplicated across three files before this gate existed, which is the exact drift class
# the gate is meant to catch — a second copy in the checker would be the same bug wearing
# a lab coat.
#
# Ratchet, like the spec-drive gate (.hooks/pre-commit 1d): only files this commit ADDS
# are blocked. Pre-existing violations are reported by the entropy dashboard (Frente 4.3),
# not by failing every commit in a repo that inherited them.
import re
import subprocess
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SCHEMA = WORKSPACE_ROOT / 'core/SCHEMA.md'

# CLAUDE.md is mandated by the harness, not chosen by us; a gate cannot un-invent it.
HARNESS_MANDATED = {'CLAUDE.md'}

# core/SCHEMA.md § The one exception: transient initiative docs. Parsed, not restated,
# for the same reason as the allowlist.
TRANSIENT_HEADING = '### The one exception: transient initiative docs'
TYPE_ROW = re.compile(r'^\|\s*`([A-Z][A-Z0-9_-]*\.md)`\s*\|', re.M)
BACKTICKED_MD = re.compile(r'`([^`]+\.md)`')

UPPERCASE_MD = re.compile(r'^[A-Z][A-Z0-9_.-]*\.md$')

# A CONTEXT.md head that re-lists the files below it. The generated routing block owns
# inventory (core/SCHEMA.md § Boundaries where types nearly touch).
ROUTING_START = '<!-- routing:start -->'
TREE_GLYPH = re.compile(r'[├└│]──')
PATH_BULLET = re.compile(r'^\s*[-*]\s+[`\[]([\w./-]+\.\w+|[\w./-]+/)', re.M)
INVENTORY_HEADING = re.compile(
    r'^#+\s+.*\b(file map|repository shape|project layout|file list|directory structure|'
    r'folder structure|files?\s+in\s+this|inventory)\b', re.I)


def _section(text: str, heading: str) -> str:
    """Body of one '### ...' section, up to the next heading of the same or higher level."""
    start = text.find(heading)
    if start < 0:
        return ''
    body = text[start + len(heading):]
    end = re.search(r'^#{1,3}\s', body, re.M)
    return body[:end.start()] if end else body


def load_law(schema_path: Path) -> tuple[set, set]:
    """(allowed type names, exempt transient-doc names) read straight from the law."""
    text = schema_path.read_text(encoding='utf-8')
    allowed = set(TYPE_ROW.findall(text))
    exempt = set()
    for name in BACKTICKED_MD.findall(_section(text, TRANSIENT_HEADING)):
        exempt.add(Path(name).name)
    return allowed, exempt


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


def check_inventory(path: Path) -> str | None:
    """CONTEXT.md must not hand-list files above its generated routing block."""
    if path.name != 'CONTEXT.md':
        return None
    text = path.read_text(encoding='utf-8')
    head = text.split(ROUTING_START, 1)[0]
    reasons = []
    heading = next((l for l in head.splitlines() if INVENTORY_HEADING.match(l)), None)
    if heading:
        reasons.append(f'inventory heading {heading.strip()!r}')
    if TREE_GLYPH.search(head):
        reasons.append('an ASCII directory tree')
    # A bullet counts only when the path REALLY EXISTS beside the CONTEXT.md. Documenting
    # a naming convention with globs (`grav_cam2_gXX_sq.png` in a paper's images/) is
    # legitimate CONTEXT content — describing the directory, which is its whole job. Only
    # a list of actual files duplicates the generated block.
    bullets = [b for b in PATH_BULLET.findall(head) if (path.parent / b).exists()]
    if len(bullets) >= 3:
        reasons.append(f'{len(bullets)} bullets listing real files')
    if not reasons:
        return None
    return (f"{path}: hand-written file inventory ({', '.join(reasons)}).\n"
            f"   The generated routing block owns inventory (core/SCHEMA.md § Boundaries\n"
            f"   where types nearly touch). Describe the directory; do not list it.")


def staged_added_files() -> list:
    """Only files this commit ADDS — the ratchet. Renames count as adds of the new name."""
    out = subprocess.run(['git', 'diff', '--cached', '--name-only', '--diff-filter=AR'],
                         capture_output=True, text=True).stdout
    return [Path(line) for line in out.splitlines() if line.endswith('.md')]


def main() -> int:
    if not SCHEMA.exists():
        return 0  # not the workspace repo; nothing to enforce against
    allowed, exempt = load_law(SCHEMA)
    failures = []
    for path in staged_added_files():
        if not path.exists():
            continue
        for failure in (check_name(path, allowed, exempt), check_inventory(path)):
            if failure:
                failures.append(failure)
    if failures:
        print('⛔ type gate:')
        for failure in failures:
            print(f'   {failure}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
