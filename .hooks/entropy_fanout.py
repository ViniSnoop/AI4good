#!/usr/bin/env python3
# Directory fanout: how many files one directory asks a reader to hold at once.
#
# The rule is not new. `workspace_scanner.SPLIT_THRESHOLD` has always been the number, and
# `context_synchronizer.sync` has always warned when a directory crosses it — but it warned
# to stdout, during a sync nobody reads, so the tail grew unopposed. This module is that
# same law, surfaced where the other Tier 0 checks are read. The threshold is imported,
# never restated: a second copy of a limit is the drift these checks exist to catch.
#
# Why it belongs next to the size signals: a large routing table is not a formatting
# problem, it is the directory telling you it holds more than one responsibility. Splitting
# it costs one routing hop, so this is a SIGNAL, never a cap — see core/SCHEMA.md
# § Routing depth and locality for when the hop is worth paying.
from collections import Counter
from pathlib import Path

from workspace_meta import CODE_EXTS
from workspace_scanner import SPLIT_THRESHOLD

# A stub rides in the routing table's Interface column of its own source row, so it is not
# a separate thing for a reader to hold.
PAIRED = ('.pyi', '.d.ts')


def fanout_counts(files: list) -> Counter:
    """Directory -> number of CODE files, the same population SPLIT_THRESHOLD always meant.

    Deliberately not every file: a flat collection of documents is a legitimate shape
    (`brain/goals/` is 57 goal files and splitting it would be wrong), while a directory
    holding dozens of modules is one responsibility too many. The existing warning in
    `context_synchronizer.sync` counts exactly this population; matching it is what keeps
    one law with one meaning.
    """
    counts = Counter()
    for path in files:
        if path.suffix in CODE_EXTS and not path.name.endswith(PAIRED):
            counts[path.parent] += 1
    return counts


def fanout_signals(files: list, root: Path, limit: int = SPLIT_THRESHOLD) -> list:
    """Directories whose routing table is large because the directory is."""
    signals = []
    for directory, count in fanout_counts(files).items():
        if count <= limit:
            continue
        rel = str(directory).replace(f'{root}/', '')
        signals.append(f'{rel} — {count} files in one directory, over the {limit} fanout '
                       f'signal; split by responsibility if the split removes more table '
                       f'than the extra hop adds')
    return sorted(signals)
