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
import subprocess
from pathlib import Path

SCANNED = {'.md', '.py', '.ts', '.tsx', '.js', '.jsx', '.sh', '.dart',
           '.yaml', '.yml', '.json', '.css', '.scss', '.tex', ''}

# Never walked: build output, caches, and the two directories that inflated every earlier
# measurement of this workspace (.venv 7.6 GB, .Trash-1000 6.6 GB).
SKIP_DIRS = {'.venv', 'node_modules', '.mypy_cache', '.pytest_cache', '.Trash-1000',
             '$RECYCLE.BIN', 'System Volume Information', 'outputs', 'tmp', 'models',
             'Downloads'}

# A bracketed slug is an item ID only in item position: after the bullet and the optional
# checkbox, decoration allowed. Elsewhere in prose it is a reference to an item that lives
# somewhere else, which is exactly what a single ledger is supposed to produce.
ITEM_SLUG = re.compile(
    r'^\s*(?:[-*>]+\s*)*(?:\[[ xX]\]\s*)*\**`?\[([a-z0-9][a-z0-9-]+)\](?!\()', re.M)


def tracked_files(root: Path, nested: bool = False) -> list:
    """Text files git tracks, relative to root. git is the inventory; find is not.

    `nested` also walks the 24 repos living inside the workspace. The dashboard wants
    them — entropy does not stop at a repo boundary. Tests do NOT: an assertion in this
    repo about another repo's content fails for reasons this repo cannot fix, and each
    nested repo runs its own verify.
    """
    files = []
    for repo in [root] + (sorted(nested_repos(root)) if nested else []):
        out = subprocess.run(['git', '-C', str(repo), 'ls-files'],
                             capture_output=True, text=True).stdout
        files += [repo / line for line in out.splitlines()
                  if Path(line).suffix.lower() in SCANNED]
    return files


def nested_repos(root: Path, depth: int = 3) -> list:
    """Repos inside the workspace. Bounded walk — an unbounded one costs 14 GB of .venv
    and trash, which is how earlier counts of this workspace came out wrong twice."""
    found = []
    def walk(directory: Path, level: int):
        if level > depth:
            return
        for child in directory.iterdir():
            if not child.is_dir() or child.name.startswith('.') or child.name in SKIP_DIRS:
                continue
            if (child / '.git').exists():
                found.append(child)
            else:
                walk(child, level + 1)
    walk(root, 0)
    return found


# The law, the check that enforces it, that check's tests, and the report that quotes the
# findings all have to be able to NAME a retired token. Nothing else may.
ENFORCEMENT = ('core/SCHEMA.md', 'entropy.md',
               '.hooks/entropy_ledger.py', '.hooks/entropy_ledger.pyi',
               'core/tools/test/test_entropy_ledger.py',
               'core/tools/test/test_entropy_ledger.pyi')


def enforcement_paths(root: Path) -> set:
    return {(root / name).resolve() for name in ENFORCEMENT}


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
