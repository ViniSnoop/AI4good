# T0 directory fanout (Frente 4.1 Tier 0). Zero-token, runs in verify-fast.
#
# The law is not new: workspace_scanner.SPLIT_THRESHOLD has always been the number and
# context_synchronizer.sync has always warned on it — to stdout, during a sync nobody
# reads, which is why the tail grew to 51 files in one directory. These tests hold the
# same law where it is visible.
#
# The whole-tree test is a RATCHET: live violations must be a subset of a named baseline,
# so a new one fails the build while the inherited ones stay visible. Shrinking the
# baseline is the only edit this test should ever get.
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE_ROOT / '.hooks'))

import entropy_fanout  # noqa: E402
import entropy_ledger  # noqa: E402
from workspace_scanner import SPLIT_THRESHOLD  # noqa: E402

# Inherited fanout, each a directory that owes a split. Nothing else may join.
BASELINE = {
    '.hooks',                                              # the enforcement layer itself
    'core/tools',
    'core/tools/test',
    'core/skills/caveman/scripts',
    'core/skills/caveman/hooks',
    'academy/administration/coordenacao-lc/novo-ppc-bcc/ementas',
}


def _live() -> set:
    counts = entropy_fanout.fanout_counts(entropy_ledger.tracked_files(WORKSPACE_ROOT))
    return {str(d).replace(f'{WORKSPACE_ROOT}/', '')
            for d, n in counts.items() if n > SPLIT_THRESHOLD}


def test_no_new_directory_exceeds_the_fanout_signal() -> None:
    assert _live() <= BASELINE, (
        f'new over-full directories: {sorted(_live() - BASELINE)} — split by '
        f'responsibility, or add to BASELINE with the item that retires it')


def test_baseline_is_not_stale() -> None:
    assert BASELINE <= _live(), (
        f'these are fixed and must leave BASELINE: {sorted(BASELINE - _live())}')


def test_a_small_directory_is_clean(tmp_path) -> None:
    files = [tmp_path / f'mod_{i}.py' for i in range(SPLIT_THRESHOLD)]
    assert entropy_fanout.fanout_signals(files, tmp_path) == []


def test_an_over_full_directory_is_flagged(tmp_path) -> None:
    files = [tmp_path / f'mod_{i}.py' for i in range(SPLIT_THRESHOLD + 1)]
    signals = entropy_fanout.fanout_signals(files, tmp_path)
    assert len(signals) == 1
    assert f'{SPLIT_THRESHOLD + 1} files' in signals[0]


def test_a_flat_document_collection_is_not_fanout(tmp_path) -> None:
    """brain/goals is 57 goal files and splitting it would be wrong. Only code counts."""
    files = [tmp_path / f'goal-{i}.md' for i in range(40)]
    assert entropy_fanout.fanout_signals(files, tmp_path) == []


def test_interface_stubs_do_not_count_toward_fanout(tmp_path) -> None:
    """A stub rides in its source's Interface column; it is not a second thing to hold."""
    files = []
    for i in range(SPLIT_THRESHOLD):
        files += [tmp_path / f'mod_{i}.py', tmp_path / f'mod_{i}.pyi']
    assert entropy_fanout.fanout_signals(files, tmp_path) == []


def test_the_threshold_has_exactly_one_home() -> None:
    """The number is imported from the scanner, never restated — a second copy is drift."""
    source = (WORKSPACE_ROOT / '.hooks/entropy_fanout.py').read_text(encoding='utf-8')
    assert 'from workspace_scanner import SPLIT_THRESHOLD' in source
    assert f'= {SPLIT_THRESHOLD}' not in source
