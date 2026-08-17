#!/usr/bin/env python3
# What the entropy dashboard counts about branches: repos on unmerged work, and remote labels
# whose commits already landed.
#
# It sits in git/ rather than beside the other entropy checks because it is the one that reads
# git state instead of file content — every module in entropy/ takes a list of files, this one
# takes a root and shells out. That difference is also what put entropy/ over the fanout cap
# when it briefly lived there, which is the check doing its job.
#
# /roundup Phase 5 already rules that a session promotes whenever the work is green and coherent,
# and says which of the three reasons applies when it does not. What was missing is the number the
# ruling exists to reduce: nothing counted repos left on an open branch, so branches accumulated
# across repos with nobody able to see it. Warn-only, like every other dashboard section.
import subprocess
from pathlib import Path

from entropy_corpus import nested_repos

# In base order. `master` is not legacy noise here: branches/instituto is on it, and a repo whose
# base is master has the same question asked of it as one on main.
BASES = ('main', 'master', 'develop')


def _git(repo: Path, *args) -> str:
    done = subprocess.run(['git', '-C', str(repo), *args],
                          capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else ''


def _rel(repo: Path, root: Path) -> str:
    return '.' if repo == root else str(repo).replace(f'{root}/', '')


def _base_of(repo: Path) -> str:
    """The branch this repo promotes into, or '' when it has none to compare against."""
    for base in BASES:
        if _git(repo, 'rev-parse', '--verify', '--quiet', f'refs/heads/{base}'):
            return base
    return ''


def unmerged_branches(root: Path) -> list:
    """One line per repo whose current branch is ahead of the branch it promotes into.

    Ahead-by-zero is the whole test and it is cheap — the same test `git branch -d` applies before
    it refuses. A repo already on its base, or with no base branch to promote into, is not a
    finding: the first has nothing open and the second has nowhere to put it.
    """
    signals = []
    for repo in sorted([root] + nested_repos(root)):
        branch = _git(repo, 'branch', '--show-current')
        if not branch or branch in BASES:
            continue
        base = _base_of(repo)
        if not base:
            continue
        ahead = _git(repo, 'rev-list', '--count', f'{base}..{branch}')
        if ahead.isdigit() and int(ahead) > 0:
            signals.append(f'{_rel(repo, root)} — {branch} is {ahead} ahead of {base}')
    return signals


def merged_remote_branches(root: Path) -> list:
    """Remote `feature/*` labels whose every commit is already in the base branch.

    Deleting one is an outward-facing act, so this counts and never acts. It was a ledger note
    saying eleven such branches were waiting for Lucas; by the time anything read it again the
    real number was six times that, across seventeen repos. A count that regenerates cannot rot
    the way that note did.
    """
    signals = []
    for repo in sorted([root] + nested_repos(root)):
        base = _base_of(repo)
        if not base or not _git(repo, 'rev-parse', '--verify', '--quiet',
                                f'refs/remotes/origin/{base}'):
            continue
        merged = [ln.strip() for ln in
                  _git(repo, 'branch', '-r', '--merged', f'origin/{base}').splitlines()]
        stale = [b for b in merged
                 if b.startswith(('origin/feature/', 'origin/release/', 'origin/hotfix/'))]
        if stale:
            # The line IS the command. One action per repo, because one push deletes many
            # branches, and a report that names the action beats one that names the problem.
            names = ' '.join(b.replace('origin/', '') for b in stale)
            signals.append(f'{_rel(repo, root)} — {len(stale)} merged into {base}: '
                           f'git -C {_rel(repo, root)} push origin --delete {names}')
    return signals
