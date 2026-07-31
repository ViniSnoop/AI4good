#!/usr/bin/env python3
# Directory fanout: how many files one directory asks a reader to hold at once.
#
# The rule is not new. A files-per-directory threshold has always existed, and
# `context_synchronizer.sync` has always warned when a directory crosses it — but it warned
# to stdout, during a sync nobody reads, so the tail grew unopposed. This module is that
# same law, surfaced where the other Tier 0 checks are read. Both the threshold and the
# definition of "code file" are imported from limits.env / file_law.py, never restated:
# a second copy of a limit is the drift these checks exist to catch.
#
# Why it belongs next to the size signals: a large routing table is not a formatting
# problem, it is the directory telling you it holds more than one responsibility. Splitting
# it costs one routing hop, so this is a SIGNAL, never a cap — see core/SCHEMA.md
# § Routing depth and locality for when the hop is worth paying.
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from file_law import is_code_file, is_vendored, load_limits  # noqa: E402


def fanout_counts(files: list, root: Path) -> Counter:
    """Directory -> number of code files, using the one definition in file_law.

    Deliberately not every file: a flat collection of documents is a legitimate shape
    (`brain/goals/` is 57 goal files and splitting it would be wrong), while a directory
    holding dozens of modules is one responsibility too many. Vendored trees are excluded —
    upstream chose their layout and we are not going to split it.
    """
    counts = Counter()
    for path in files:
        if is_code_file(path) and not is_vendored(path, root):
            counts[path.parent] += 1
    return counts


def fanout_signals(files: list, root: Path, limit: int = None) -> list:
    """Directories whose routing table is large because the directory is."""
    limits = load_limits()
    warn = limits['WARN_FILES'] if limit is None else limit
    block = limits['BLOCK_FILES']
    signals = []
    for directory, count in fanout_counts(files, root).items():
        if count <= warn:
            continue
        rel = str(directory).replace(f'{root}/', '')
        level = 'over the BLOCK_FILES cap' if count > block else 'over the WARN_FILES signal'
        signals.append(f'{rel} — {count} code files in one directory, {level}; split by '
                       f'responsibility if the split removes more table than the hop adds')
    return sorted(signals)
