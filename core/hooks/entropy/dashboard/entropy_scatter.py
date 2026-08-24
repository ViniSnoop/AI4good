#!/usr/bin/env python3
# Which repo owns a finding, and the local ledger it is written into.
#
# Ruled 2026-08-20 (Lucas): every CODE repo keeps its own ISSUES.md, because the reader who can fix
# a finding is the one already inside that repo. Papers and branches/ stay pooled at the root —
# they are not code and their findings are few. core/ and brain/ are parts of WOS itself, so the
# workspace repo's own ledger covers them (his call, 2026-08-24). Fourteen ledgers, not twenty-six.
#
# The root SUMS, and the sum is recomputed here from the same scan that writes the locals — never
# hand-carried. A collected number that any repo could write into is precisely the copied-count
# drift these checks exist to catch, so one pass by one writer produces both halves or neither.
from pathlib import Path

from blocks import replace_block
from entropy_corpus import nested_repos
from entropy_report import END, START, local_seed, render

# Only code repos scatter. The directory is the declaration: a repo under code/ is a software
# project with its own verify suite, which is what makes a local ledger actionable there.
CODE = 'code'


def code_repos(root: Path) -> list:
    """The repos that get a local ledger, as paths relative to the workspace root."""
    rels = [str(repo.relative_to(root)) for repo in nested_repos(root)]
    return sorted(rel for rel in rels if rel.split('/')[0] == CODE)


def _head(finding: str, root: Path) -> str:
    """The path a finding names, relative to the workspace root.

    Every section leads with the thing it found — a file path, or a repo path for the two git
    checks — so the first whitespace-delimited token is the owner even when a colon or an em dash
    follows it.
    """
    token = finding.splitlines()[0].split()[0] if finding.split() else ''
    return token.replace(f'{root}/', '').rstrip(':').lstrip('./')


def owner(finding: str, root: Path, repos: list) -> str:
    """The repo whose ledger a finding belongs in, or '' for the root's own.

    Longest prefix wins, so a repo nested inside another lands in the innermost one.
    """
    head = _head(finding, root)
    matches = [r for r in repos if head == r or head.startswith(f'{r}/')]
    return max(matches, key=len) if matches else ''


def partition(findings: dict, root: Path, repos: list) -> tuple:
    """Split every section's findings into (the root's own, one dict per code repo)."""
    mine = {key: [] for key in findings}
    per_repo = {repo: {key: [] for key in findings} for repo in repos}
    for key, items in findings.items():
        for item in items:
            target = owner(item, root, repos)
            (per_repo[target] if target else mine)[key].append(item)
    return mine, per_repo


def write_local(repo: str, root: Path, findings: dict, scanned: int) -> int:
    """Write one repo's own entropy block into its own ISSUES.md. Returns its finding count."""
    ledger = root / repo / 'ISSUES.md'
    text = ledger.read_text(encoding='utf-8') if ledger.exists() else local_seed(repo)
    block = render(findings, scanned, root / repo, name=repo)
    ledger.write_text(replace_block(text, block, START, END, at_end=True), encoding='utf-8')
    return sum(len(items) for items in findings.values())


def scatter(findings: dict, root: Path, files: list) -> tuple:
    """Write every local ledger, and hand back (the root's own findings, count per repo).

    Each ledger reports the files scanned in ITS OWN repo. Handing every one of them the
    workspace-wide total would make each local file state something false about itself, which is
    the failure the self-description front exists to name.
    """
    repos = code_repos(root)
    mine, per_repo = partition(findings, root, repos)
    scanned = {repo: 0 for repo in repos}
    for path in files:
        if repo := owner(str(path), root, repos):
            scanned[repo] += 1
    counts = {repo: write_local(repo, root, per_repo[repo], scanned[repo]) for repo in repos}
    return mine, counts
