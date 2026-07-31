#!/usr/bin/env python3
# Tier 0 ledger and vocabulary checks (ROADMAP.md Frente 4.1). Zero-token, deterministic.
#
# Two assertions that make two recurring bugs catchable instead of re-discovered:
#   retired tokens  — a rename is finished only when its old spelling appears nowhere
#                     (core/SCHEMA.md § Retired tokens). This is what makes an
#                     incomplete rename visible at the generator instead of at the leaves.
#   duplicate slugs — a work item lives in exactly one ledger; a copy is a bug
#                     (ROADMAP.md header). This is v1 criterion 2, verified by scan.
import re
from pathlib import Path

from entropy_corpus import enforcement_paths, tracked_files  # noqa: F401

# A bracketed slug is an item ID only in item position: after the bullet and the optional
# checkbox, decoration allowed. Elsewhere in prose it is a reference to an item that lives
# somewhere else, which is exactly what a single ledger is supposed to produce.
ITEM_SLUG = re.compile(
    r'^\s*(?:[-*>]+\s*)*(?:\[[ xX]\]\s*)*\**`?\[([a-z0-9][a-z0-9-]+)\](?!\()', re.M)


def retired_hits(files: list, retired: dict, exempt: set) -> list:
    """Every surviving occurrence of a retired token, in content or in a filename."""
    exempt = {path.resolve() for path in exempt}
    # Hyphen is a boundary, not a word character: a retired token survives just as much
    # inside `fable-loop-engineering.md` as it does standing alone, and that compound
    # form is how an unfinished rename actually hides at the leaves.
    patterns = {token: re.compile(rf'(?<!\w){re.escape(token)}(?!\w)')
                for token in retired}
    hits = []
    for path in files:
        if path.resolve() in exempt:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        for token, pattern in patterns.items():
            where = 'filename' if pattern.search(path.name) else None
            if not where and pattern.search(text):
                where = f'line {text[:pattern.search(text).start()].count(chr(10)) + 1}'
            if where:
                hits.append(f'{path}: retired token {token!r} survives ({where}).\n'
                            f'   Renamed to {retired[token]!r} — core/SCHEMA.md § Retired\n'
                            f'   tokens. If this line only *explains* the rename, delete it:\n'
                            f'   git holds the history.')
    return hits


def item_slugs(path: Path) -> set:
    """Slugs this file claims as items — bracketed, in item position."""
    try:
        return set(ITEM_SLUG.findall(path.read_text(encoding='utf-8')))
    except (OSError, UnicodeDecodeError):
        return set()


def duplicate_slugs(namespaces: dict) -> dict:
    """Slug -> the namespaces claiming it, for every slug claimed by more than one.

    Namespace, not file, is the unit. A goal file's achievement slugs (`build-mvp`,
    `mvp-scope`, `first-class`) are private vocabulary repeated across sibling goals by
    design — six startapps all having a `build-mvp` is not six copies of one item. What
    criterion 2 forbids is the *same work item* tracked in two different ledgers, so the
    caller declares the namespaces and all goal files share one.
    """
    owners = {}
    for namespace, ledgers in namespaces.items():
        for ledger in ledgers:
            for slug in item_slugs(ledger):
                owners.setdefault(slug, {})[namespace] = ledger
    return {slug: claims for slug, claims in owners.items() if len(claims) > 1}


WIKI_LINK = re.compile(r'\[\[([a-z0-9][a-z0-9-]*)\]\]')


def goal_vocabulary(goals_dir: Path) -> set:
    """Every name a `[[slug]]` is allowed to use: a goal file, or an item inside one.

    Decided 2026-07-30 (Lucas). Both halves are real pointers — `[[spec-driven-development]]`
    names the file, `[[prompt-dsl]]` names an item living inside `craft-flows.md` — and both
    are resolvable by scan, which is the only property a checker needs.
    """
    vocabulary = set()
    for goal in goals_dir.glob('*.md'):
        vocabulary.add(goal.stem)
        vocabulary |= item_slugs(goal)
    return vocabulary


def wiki_link_hits(files: list, vocabulary: set, exempt: set) -> list:
    """Every `[[slug]]` naming neither a goal file nor an item inside one."""
    exempt = {path.resolve() for path in exempt}
    hits = []
    for path in files:
        if path.suffix != '.md' or path.resolve() in exempt:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        for slug in sorted(set(WIKI_LINK.findall(text)) - vocabulary):
            hits.append(f'{path}: [[{slug}]] names no goal file and no item in one.\n'
                        f'   A `[[slug]]` points at brain/goals/<slug>.md or at a bracketed\n'
                        f'   item inside a goal file. Fix the slug, or write the goal.')
    return hits
