#!/usr/bin/env python3
# Which files the Tier 0 checks look at, and which of them are allowed to name what the
# checks forbid. Split from entropy_ledger.py 2026-07-30 at the 150-line warn: enumerating
# the corpus is a different job from asserting things about it.
import subprocess
from pathlib import Path

SCANNED = {'.md', '.py', '.ts', '.tsx', '.js', '.jsx', '.sh', '.dart',
           '.yaml', '.yml', '.json', '.css', '.scss', '.tex', ''}

# Never walked: build output, caches, and the two directories that inflated every earlier
# measurement of this workspace (.venv 7.6 GB, .Trash-1000 6.6 GB).
SKIP_DIRS = {'.venv', 'node_modules', '.mypy_cache', '.pytest_cache', '.Trash-1000',
             '$RECYCLE.BIN', 'System Volume Information', 'outputs', 'tmp', 'models',
             'Downloads'}

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
