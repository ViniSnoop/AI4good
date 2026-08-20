# T0 the entropy scatter (ruled 2026-08-20): every code repo keeps its own ledger and the root sums
# them. Zero-token, runs in verify-fast.
#
# The sum is the thing to get right. A collected number any repo could write into is the
# copied-count drift these checks exist to catch, so the test reads every local ledger BACK OFF
# DISK and re-adds it — proving the root's number was computed, not carried.
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'hooks/entropy/dashboard'))

from entropy_scatter import code_repos, owner, partition  # noqa: E402

ROOT = Path(__file__).resolve().parents[4].parent
TOTAL = re.compile(r'\*\*(\d+) findings\*\*')


def _reported(ledger: Path) -> int:
    """The finding count a ledger states in its own generated block."""
    match = TOTAL.search(ledger.read_text(encoding='utf-8'))
    return int(match.group(1)) if match else 0


def test_every_code_repo_has_its_own_ledger() -> None:
    for repo in code_repos(ROOT):
        assert (ROOT / repo / 'ISSUES.md').exists(), f'{repo} has no local ISSUES.md'


def test_the_root_total_equals_the_sum_of_the_local_ledgers() -> None:
    repos = code_repos(ROOT)
    root_text = (ROOT / 'ISSUES.md').read_text(encoding='utf-8')
    collected = int(TOTAL.search(root_text).group(1))
    here = int(re.search(r'\*\*\d+ findings\*\*, (\d+) of them here', root_text).group(1))
    scattered = sum(_reported(ROOT / repo / 'ISSUES.md') for repo in repos)
    assert collected == here + scattered


def test_the_index_lists_every_repo_that_has_a_ledger() -> None:
    root_text = (ROOT / 'ISSUES.md').read_text(encoding='utf-8')
    for repo in code_repos(ROOT):
        assert f'({repo}/ISSUES.md)' in root_text, f'{repo} is missing from the root index'


def test_a_finding_lands_in_the_repo_that_owns_its_path() -> None:
    repos = ['code/aiwbot', 'code/dobra']
    assert owner('code/aiwbot/bot.py — 3 lines over', ROOT, repos) == 'code/aiwbot'


def test_the_innermost_repo_wins_when_one_nests_inside_another() -> None:
    repos = ['code/outer', 'code/outer/inner']
    assert owner('code/outer/inner/thing.py: finding', ROOT, repos) == 'code/outer/inner'


def test_papers_and_branches_stay_pooled_at_the_root() -> None:
    """Lucas's ruling: they are not code and their findings are few."""
    repos = code_repos(ROOT)
    assert owner('academy/papers/wos-ablation/PLAN.md: finding', ROOT, repos) == ''
    assert owner('branches/casinhas/PROJETO.md: finding', ROOT, repos) == ''


def test_core_and_brain_stay_with_the_workspace_repo() -> None:
    """Ruled 2026-08-20: both are parts of WOS, so its own ledger covers them — 14 ledgers, not 16."""
    repos = code_repos(ROOT)
    assert owner('core/SCHEMA.md: finding', ROOT, repos) == ''
    assert owner('brain/GOALS.md: finding', ROOT, repos) == ''


def test_partition_loses_no_finding() -> None:
    findings = {'size': ['code/aiwbot/a.py x', 'core/b.md y'], 'naming': ['code/dobra/c: z']}
    repos = ['code/aiwbot', 'code/dobra']
    mine, per_repo = partition(findings, ROOT, repos)
    kept = sum(len(v) for v in mine.values())
    kept += sum(len(v) for repo in per_repo.values() for v in repo.values())
    assert kept == sum(len(v) for v in findings.values())
