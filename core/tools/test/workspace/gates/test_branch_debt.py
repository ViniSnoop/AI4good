# T0 the unmerged-branch signal: a repo is a finding when its branch is ahead of the branch it
# promotes into, and never otherwise. Zero-token, runs in verify-fast.
#
# The silences are the design. A repo sitting on its own base has nothing open; a repo with no
# base branch has nowhere to promote to and would otherwise be reported forever with no action
# available. Both look like "no finding" from outside and mean different things, so both are
# asserted rather than assumed — that is the boundary this file owns.
import subprocess
from pathlib import Path

import pytest

from branch_debt import merged_remote_branches, unmerged_branches


def git(repo: Path, *args):
	subprocess.run(['git', '-C', str(repo), *args], check=True,
	               capture_output=True, text=True)


def commit(repo: Path, name: str):
	(repo / name).write_text(name)
	git(repo, 'add', name)
	git(repo, 'commit', '-qm', name, '--no-verify')


@pytest.fixture
def repo(tmp_path):
	"""A repo with a `main` carrying one commit, ready to branch off."""
	subprocess.run(['git', 'init', '-q', '-b', 'main', str(tmp_path)], check=True)
	git(tmp_path, 'config', 'user.email', 'test@test')
	git(tmp_path, 'config', 'user.name', 'test')
	commit(tmp_path, 'base.txt')
	return tmp_path


def test_a_branch_ahead_of_its_base_is_a_finding(repo):
	git(repo, 'checkout', '-q', '-b', 'feature/x')
	commit(repo, 'work.txt')
	signal, = unmerged_branches(repo)
	assert 'feature/x' in signal and '1 ahead of main' in signal, signal


def test_a_branch_level_with_its_base_is_not(repo):
	"""Ahead-by-zero is the whole test — the same one `git branch -d` applies before refusing."""
	git(repo, 'checkout', '-q', '-b', 'feature/merged')
	assert unmerged_branches(repo) == []


def test_a_repo_on_its_own_base_is_not(repo):
	assert unmerged_branches(repo) == []


def test_master_counts_as_a_base(repo):
	"""branches/instituto is on master, and its branches deserve the same question."""
	git(repo, 'branch', '-m', 'main', 'master')
	git(repo, 'checkout', '-q', '-b', 'feature/y')
	commit(repo, 'work.txt')
	signal, = unmerged_branches(repo)
	assert 'ahead of master' in signal, signal


def test_a_repo_with_no_base_branch_is_silent(repo):
	"""Nowhere to promote to means no action, and a finding with no action is noise."""
	git(repo, 'checkout', '-q', '-b', 'feature/z')
	commit(repo, 'work.txt')
	git(repo, 'branch', '-D', 'main')
	assert unmerged_branches(repo) == []


@pytest.fixture
def cloned(repo, tmp_path_factory):
	"""A clone, so `origin/*` refs are real rather than simulated."""
	work = tmp_path_factory.mktemp('clone')
	subprocess.run(['git', 'clone', '-q', str(repo), str(work / 'r')], check=True)
	clone = work / 'r'
	git(clone, 'config', 'user.email', 'test@test')
	git(clone, 'config', 'user.name', 'test')
	return clone


def test_a_remote_branch_already_in_base_is_offered_for_deletion(cloned):
	git(cloned, 'push', '-q', 'origin', 'main:refs/heads/feature/done')
	git(cloned, 'fetch', '-q', 'origin')
	signal, = merged_remote_branches(cloned)
	# The line must be the runnable action, not a description of one.
	assert 'push origin --delete feature/done' in signal, signal


def test_a_remote_branch_carrying_unmerged_work_is_left_alone(cloned):
	git(cloned, 'checkout', '-q', '-b', 'feature/live')
	commit(cloned, 'work.txt')
	git(cloned, 'push', '-q', 'origin', 'feature/live')
	git(cloned, 'fetch', '-q', 'origin')
	assert merged_remote_branches(cloned) == []


def test_a_repo_with_no_remote_is_silent(repo):
	"""Deleting nothing is not an action; a repo with no origin has nothing to offer."""
	assert merged_remote_branches(repo) == []
