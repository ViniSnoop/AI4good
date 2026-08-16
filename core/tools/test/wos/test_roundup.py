# T1 roundup tool (core/SPECS.md § AD-09): the deterministic half of the session-close ritual.
# Zero-token, no network — every case builds its own throwaway repo.
#
# The one thing worth guarding hardest is the dirty stop. It used to assert that uncommitted work
# was work *this* session forgot to commit, and asked for a commit that would have swept a parallel
# session's half-finished goal merge into main. Dirt has two possible owners and the script cannot
# tell them apart, so it names both and lets --leave-dirty answer.
import os
import shutil
import subprocess

from conftest import WORKSPACE_ROOT

ROUNDUP = WORKSPACE_ROOT / 'core/tools/wos/roundup'

MAKEFILE = 'verify-fast:\n\t@echo "3 passed"\n\nentropy:\n\t@echo "**7 findings**" > entropy.md\n'
RED_MAKEFILE = 'verify-fast:\n\t@exit 1\n\nentropy:\n\t@echo "**7 findings**" > entropy.md\n'


def _git(repo, *args):
    return subprocess.run(('git',) + args, cwd=repo, capture_output=True, text=True)


def _workspace(tmp_path, makefile=MAKEFILE):
    """A fake workspace: the real script at its real relative path, so ROOT == WORKSPACE and the
    gitflow and entropy branches of the code are reachable. main == develop, feature one ahead."""
    ws = tmp_path / 'ws'
    (ws / 'core/tools/wos').mkdir(parents=True)
    dest = ws / 'core/tools/wos/roundup'
    shutil.copy(ROUNDUP, dest)
    os.chmod(dest, 0o755)
    (ws / 'Makefile').write_text(makefile, encoding='utf-8')
    (ws / 'entropy.md').write_text('**9 findings**\n', encoding='utf-8')

    _git(ws, 'init', '-q', '-b', 'main')
    _git(ws, 'config', 'user.email', 'test@example.com')
    _git(ws, 'config', 'user.name', 'test')
    _git(ws, 'config', 'core.hooksPath', '/dev/null')  # the real hooks are not under test
    _git(ws, 'add', '-A')
    _git(ws, 'commit', '-q', '--no-verify', '-m', 'init')

    origin = tmp_path / 'origin.git'
    _git(tmp_path, 'init', '-q', '--bare', str(origin))
    _git(ws, 'remote', 'add', 'origin', str(origin))
    _git(ws, 'branch', 'develop')
    _git(ws, 'checkout', '-q', '-b', 'feature/x')
    (ws / 'shipped.txt').write_text('work\n', encoding='utf-8')
    _git(ws, 'add', '-A')
    _git(ws, 'commit', '-q', '--no-verify', '-m', 'feat: work')
    _git(ws, 'push', '-q', 'origin', 'main', 'develop', 'feature/x')
    return ws


def _run(ws, *args):
    return subprocess.run([str(ws / 'core/tools/wos/roundup'), *args],
                          cwd=ws, capture_output=True, text=True)


def _dirty(ws):
    """A parallel session's work in progress: one staged add, one unstaged edit."""
    (ws / 'theirs.md').write_text('their draft\n', encoding='utf-8')
    _git(ws, 'add', 'theirs.md')
    (ws / 'shipped.txt').write_text('their edit\n', encoding='utf-8')


def test_dirty_stop_prints_the_paths_and_asks_whose(tmp_path):
    ws = _workspace(tmp_path)
    _dirty(ws)
    r = _run(ws)
    assert r.returncode == 2
    assert 'theirs.md' in r.stdout, 'the agent cannot judge ownership without the paths'
    assert '--leave-dirty' in r.stdout and 'commit' in r.stdout


def test_dirty_stop_does_not_assert_whose_work_it_is(tmp_path):
    """The defect, in one assertion: the old message said 'commit, then rerun' as a statement of
    fact about work it had not attributed."""
    ws = _workspace(tmp_path)
    _dirty(ws)
    first = _run(ws).stdout.splitlines()[0]
    assert 'whose' in first.lower(), f'the stop must ask, not assert: {first!r}'


def test_leave_dirty_promotes_without_touching_the_tree(tmp_path):
    ws = _workspace(tmp_path)
    _dirty(ws)
    before = _git(ws, 'status', '--porcelain').stdout
    r = _run(ws, '--leave-dirty')
    assert r.returncode == 0, r.stdout
    assert 'promoted' in r.stdout
    assert _git(ws, 'rev-parse', 'main').stdout == _git(ws, 'rev-parse', 'feature/x').stdout
    assert _git(ws, 'rev-parse', '--abbrev-ref', 'HEAD').stdout.strip() == 'feature/x'
    assert _git(ws, 'status', '--porcelain').stdout == before, 'a fast-forward must not touch files'


def test_leave_dirty_never_commits_the_foreign_dirt(tmp_path):
    """The hazard that made this flag necessary: the entropy commit stages the whole index, so
    committing it while another session has files staged carries them into chore(entropy)."""
    ws = _workspace(tmp_path)
    _dirty(ws)
    r = _run(ws, '--leave-dirty')
    assert 'not committed' in r.stdout
    log = _git(ws, 'log', '--name-only', '--pretty=format:', 'feature/x').stdout
    assert 'theirs.md' not in log
    assert 'theirs.md' in _git(ws, 'status', '--porcelain').stdout


def test_clean_tree_still_commits_entropy(tmp_path):
    ws = _workspace(tmp_path)
    r = _run(ws)
    assert r.returncode == 0, r.stdout
    assert '7 findings' in r.stdout and 'not committed' not in r.stdout
    assert 'chore(entropy)' in _git(ws, 'log', '--oneline', 'main').stdout


def test_a_real_merge_is_refused_while_the_tree_is_not_ours(tmp_path):
    """Only a fast-forward avoids a checkout. Moving HEAD under a live parallel session is what
    --leave-dirty exists to avoid, so a diverged target is reported, never merged."""
    ws = _workspace(tmp_path)
    _git(ws, 'checkout', '-q', 'develop')
    (ws / 'diverged.txt').write_text('elsewhere\n', encoding='utf-8')
    _git(ws, 'add', '-A')
    _git(ws, 'commit', '-q', '--no-verify', '-m', 'chore: diverge')
    _git(ws, 'push', '-q', 'origin', 'develop')
    _git(ws, 'checkout', '-q', 'feature/x')
    _dirty(ws)
    r = _run(ws, '--leave-dirty')
    assert r.returncode == 1
    assert 'real merge' in r.stdout and 'not promoted' in r.stdout


def test_red_verify_blocks_promotion(tmp_path):
    ws = _workspace(tmp_path, makefile=RED_MAKEFILE)
    r = _run(ws)
    assert r.returncode == 1
    assert 'verify: red' in r.stdout and 'not promoted' in r.stdout
    assert _git(ws, 'rev-parse', 'main').stdout != _git(ws, 'rev-parse', 'feature/x').stdout


def test_no_promote_needs_a_reason(tmp_path):
    ws = _workspace(tmp_path)
    assert _run(ws, '--no-promote').returncode != 0


def test_unknown_flag_is_a_usage_error(tmp_path):
    ws = _workspace(tmp_path)
    r = _run(ws, '--commit-everything')
    assert r.returncode == 64 and '--leave-dirty' in r.stderr


def test_the_flags_compose(tmp_path):
    ws = _workspace(tmp_path)
    _dirty(ws)
    r = _run(ws, '--leave-dirty', '--no-promote', 'branch is incoherent')
    assert r.returncode == 0, r.stdout
    assert 'branch is incoherent' in r.stdout and 'not promoted' in r.stdout
