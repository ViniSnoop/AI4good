#!/usr/bin/env python3
# Tier 0 CONTEXT.md rules (ROADMAP.md Frente 4.1). Zero-token, deterministic.
#
# Split out of type-gate.py 2026-07-30 when the goal-link check joined the inventory
# check: type-gate.py is the ratchet that decides WHEN to run a check, these are the
# rules about what a CONTEXT.md must and must not say.
import re
from pathlib import Path

from entropy_corpus import is_generated_mirror

# core/SCHEMA.md § Boundaries where types nearly touch: CONTEXT never hand-lists files.
ROUTING_START = '<!-- routing:start -->'
TREE_GLYPH = re.compile(r'[├└│]──')
PATH_BULLET = re.compile(r'^\s*[-*]\s+[`\[]([\w./-]+\.\w+|[\w./-]+/)', re.M)
INVENTORY_HEADING = re.compile(
    r'^#+\s+.*\b(file map|repository shape|project layout|file list|directory structure|'
    r'folder structure|files?\s+in\s+this|inventory)\b', re.I)

GOAL_LINE = re.compile(r'^>\s*goal:\s*(none|\[([^\]]+)\]\(([^)]+)\))\s*$')


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


# A constraint reads as an obligation, which is the SPECS question. Answering it in a
# CONTEXT.md head charges every session in the subtree, because this is the only
# enforced-read type — core/SCHEMA.md § Placement, the REDIRECT cell.
CONSTRAINT = re.compile(
    r'\b(?:must|never|always|required|forbidden|blocked|do not|don\'t)\b', re.I)


def context_head(path: Path) -> str:
    """The curated prose above the generated routing block — the part a human wrote."""
    try:
        return path.read_text(encoding='utf-8').split(ROUTING_START, 1)[0]
    except (OSError, UnicodeDecodeError):
        return ''


def check_misplaced_answer(path: Path, head_warn: int) -> str | None:
    """A contract trapped in an over-size CONTEXT.md head.

    core/SCHEMA.md says each type answers exactly one question, but nothing verified that a
    file answers only *its own*. Size alone is a weak signal — a long head may be honest
    navigation — so this fires only where an over-size head is also *shaped* like a
    contract. The sibling's existence decides whether the fix is a move or a create.
    """
    if path.name != 'CONTEXT.md' or is_generated_mirror(path):
        return None
    head = context_head(path)
    tokens, modals = len(head) // 4, len(CONSTRAINT.findall(head))
    if tokens <= head_warn or not modals:
        return None
    sibling = path.parent / 'SPECS.md'
    verb = 'move them to the' if sibling.exists() else 'create a'
    return (f'{path}: head is {tokens} tok carrying {modals} constraint(s).\n'
            f'   CONTEXT.md is the only enforced-read type, so this is charged to every\n'
            f'   session in the subtree. {verb} sibling SPECS.md and leave one pointer\n'
            f'   (core/SCHEMA.md § Placement, REDIRECT).')


def is_project(path: Path) -> bool:
    """A project = a directory sitting directly under code/. Scaffolding is not one."""
    return (path.name == 'CONTEXT.md' and path.parent.parent.name == 'code'
            and not path.parent.name.startswith('_'))


def check_goal_link(path: Path) -> str | None:
    """Every project declares on line 3 which goal it serves, or `none` deliberately.

    The link is what stops a project from quietly outliving the reason it was started —
    the one question a repo cannot answer about itself.
    """
    if not is_project(path):
        return None
    lines = path.read_text(encoding='utf-8').splitlines()
    line = lines[2] if len(lines) > 2 else ''
    match = GOAL_LINE.match(line.strip())
    if not match:
        return (f'{path}: line 3 must declare the goal this project serves.\n'
                f'   Write `> goal: [<slug>](../../brain/goals/<slug>.md)`, or\n'
                f'   `> goal: none` if it deliberately serves no goal. Found: {line[:60]!r}')
    if match.group(1) == 'none':
        return None
    target = (path.parent / match.group(3)).resolve()
    if not target.exists():
        return (f'{path}: line 3 points at a goal file that does not exist.\n'
                f'   {match.group(3)} — a dead goal link is worse than `none`, because it\n'
                f'   reads as an answer.')
    return None
