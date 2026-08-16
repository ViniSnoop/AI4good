#!/usr/bin/env python3
# What is switched ON. The third law module: file_law.py says what a file IS, schema_law.py says
# what a name MAY BE, this one says which capabilities are live. Like schema_law.py it reads its
# answer out of core/ rather than holding one — the registry is core/features.txt, the answers are
# core/profile.txt, and neither is restated here.
#
# Why it exists (2026-08-16): the ablation bench ran once and produced no signal because no single
# feature could be turned off. Every gate that consults this module becomes measurable; every gate
# that does not is counted as a finding by `core/tools/wos/features --findings`.
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORE = HERE.parent
REGISTRY_FILE = CORE / 'features.txt'
PROFILE_FILE = CORE / 'profile.txt'

# The closed sets the registry's columns may draw from. Kept here rather than in the data file for
# the same reason limits.env holds numbers and file_law.py holds the extension list: the values are
# data, the vocabulary is law.
GROUPS = {'hooks', 'context-tree', 'brain', 'capabilities', 'skills'}
ENFORCEMENT = {'blocks', 'warns', 'generates', 'advises', 'none'}
SCOPES = {'general', 'lucas'}

# One ablation switch, and it only ever REMOVES. There is no WOS_FEATURES_ON, and the asymmetry is
# deliberate: an ablation run answers "what does this workspace cost without X", so it subtracts.
# A feature that should be on is turned on in the profile, where the choice is versioned and
# reviewable, rather than in an environment variable that vanishes with the shell.
OFF_ENV = 'WOS_FEATURES_OFF'


def _rows(path: Path) -> list:
    """Tab-separated, '#' comments dropped, first surviving line is the header.

    The same shape core/tools/deps.txt uses, parsed the same way, on purpose: three declaration
    files that a reader can open without learning a third format.
    """
    if not path.exists():
        return []
    lines = [ln.rstrip('\n') for ln in path.read_text(encoding='utf-8').splitlines()
             if ln.strip() and not ln.lstrip().startswith('#')]
    if not lines:
        return []
    header = lines[0].split('\t')
    return [dict(zip(header, ln.split('\t'))) for ln in lines[1:]]


def load_registry() -> list:
    """Every declared feature, in file order."""
    return _rows(REGISTRY_FILE)


def slugs() -> set:
    return {r['slug'] for r in load_registry()}


def load_profile() -> dict:
    """The answers, split by kind: {'toggle': {slug: 'on'|'off'}, 'setting': {key: value}}."""
    out: dict = {'toggle': {}, 'setting': {}}
    for row in _rows(PROFILE_FILE):
        kind = row.get('kind', '')
        if kind in out:
            out[kind][row.get('key', '')] = row.get('value', '')
    return out


def _off_by_env() -> set:
    return {s.strip() for s in os.environ.get(OFF_ENV, '').split(',') if s.strip()}


def is_enabled(slug: str) -> bool:
    """Is this capability live right now?

    Fail-open on an unknown slug, and that is the load-bearing choice: a gate must never stop
    enforcing because someone mistyped a row. A feature nobody declared behaves exactly as it did
    before this module existed, so wiring a gate can only ever be safe.
    """
    if slug in _off_by_env():
        return False
    return load_profile()['toggle'].get(slug, 'on') != 'off'


def setting(key: str, default: str = '') -> str:
    """A profile answer that is not a switch — the interaction language, and its kind."""
    return load_profile()['setting'].get(key, default)


def findings() -> list:
    """Rows that declare no wiring: capabilities that cannot be switched off.

    This is the audit, not a warning list. A capability entangled with the scaffold rather than
    sitting on it is invisible to an ablation, so the count is the number the ablation study has
    to drive down before it can measure anything (core/SPECS.md § AD-14).
    """
    return [r for r in load_registry() if r.get('wired', '-') in ('-', '')]


def main() -> int:
    """`--enabled <slug>` exits 0 when live, 1 when off — so a shell gate or a node hook shares
    this law instead of reimplementing it. Same arm, same reason, as file_law.py --filter-code."""
    if len(sys.argv) == 3 and sys.argv[1] == '--enabled':
        return 0 if is_enabled(sys.argv[2]) else 1
    print('usage: feature_law.py --enabled <slug>', file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
