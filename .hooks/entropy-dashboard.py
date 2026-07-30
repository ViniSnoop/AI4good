#!/usr/bin/env python3
# The entropy dashboard (ROADMAP.md Frente 4.3). Runs every Tier 0 check over the whole
# tree and writes ONE generated report, so agents and Lucas read a pre-computed file
# instead of re-scanning the workspace. Zero-token, no LLM.
#
# Division of labour with .hooks/type-gate.py: the gate is a ratchet and only blocks what
# a commit ADDS, which is why a repo that inherited violations is not blocked on every
# commit. Everything it lets through historically shows up here, once, with a count.
#
# Size is reported as a SIGNAL, never a cap: crossing a threshold asks for a delta review,
# it does not ask anyone to summarize a document down. Forced brevity is the trap.
import subprocess
import sys
from datetime import date
from pathlib import Path

from entropy_ledger import (duplicate_slugs, enforcement_paths, retired_hits,
                            tracked_files)
from entropy_naming import check_dirs, check_placement, check_shape
from schema_law import SCHEMA, WORKSPACE_ROOT, load_law, load_retired, load_scopes

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib.util import module_from_spec, spec_from_file_location  # noqa: E402

REPORT = WORKSPACE_ROOT / 'entropy.md'
LIMITS = WORKSPACE_ROOT / '.hooks/line-limits.env'
# A curated doc past this asks for a delta review. Docs are long because thinking is long;
# this is the point where it is worth asking whether two documents are wearing one name.
DOC_SIGNAL_LINES = 300
CODE_SUFFIXES = {'.py', '.ts', '.tsx', '.js', '.jsx', '.dart', '.sh'}

LEDGERS = {
    'wos-roadmap': [WORKSPACE_ROOT / 'ROADMAP.md'],
    'life-todo': [WORKSPACE_ROOT / 'brain/TODO.md'],
    'core-roadmap': [WORKSPACE_ROOT / 'core/ROADMAP.md'],
    'goals': sorted((WORKSPACE_ROOT / 'brain/goals').glob('*.md')),
}


def _type_gate():
    spec = spec_from_file_location('type_gate', WORKSPACE_ROOT / '.hooks/type-gate.py')
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _block_lines() -> int:
    for line in LIMITS.read_text(encoding='utf-8').splitlines():
        if line.startswith('BLOCK_LINES='):
            return int(line.split('=', 1)[1])
    return 200


def _added_by(path: Path) -> str:
    """The commit that introduced a file — a --no-verify bypass leaves no other trace."""
    repo = next((p for p in path.parents if (p / '.git').exists()), WORKSPACE_ROOT)
    out = subprocess.run(
        ['git', '-C', str(repo), 'log', '--diff-filter=A', '--format=%h %an',
         '-1', '--', str(path.relative_to(repo))],
        capture_output=True, text=True).stdout.strip()
    return out or 'unknown'


def _rel(path) -> str:
    return str(path).replace(f'{WORKSPACE_ROOT}/', '')


def collect(files: list) -> dict:
    gate = _type_gate()
    allowed, exempt = load_law(SCHEMA)
    scopes = load_scopes(SCHEMA)
    findings = {'types': [], 'inventories': [], 'naming': []}
    for path in files:
        if failure := gate.check_name(path, allowed, exempt):
            findings['types'].append(failure)
        if path.name == 'CONTEXT.md' and (failure := gate.check_inventory(path)):
            findings['inventories'].append(failure)
        for failure in (check_shape(path, allowed), check_dirs(path, WORKSPACE_ROOT),
                        check_placement(path, scopes, WORKSPACE_ROOT)):
            if failure:
                findings['naming'].append(failure)
    findings['retired'] = retired_hits(files, load_retired(SCHEMA),
                                       enforcement_paths(WORKSPACE_ROOT))
    findings['duplicates'] = [f'`[{slug}]` claimed by {", ".join(sorted(claims))}'
                              for slug, claims in duplicate_slugs(LEDGERS).items()]
    findings['size'] = size_signals(files)
    # One directory-level finding is reported by every file under it; dedupe so a count
    # means "things to fix", not "files touched by a thing to fix".
    findings['naming'] = sorted(set(findings['naming']))
    return findings


def size_signals(files: list) -> list:
    block = _block_lines()
    signals = []
    for path in files:
        if path.suffix not in CODE_SUFFIXES and path.suffix != '.md':
            continue
        try:
            lines = len(path.read_text(encoding='utf-8').splitlines())
        except (OSError, UnicodeDecodeError):
            continue
        if path.suffix == '.md' and lines > DOC_SIGNAL_LINES:
            signals.append(f'{_rel(path)} — {lines} lines (doc signal, review the delta)')
        elif path.suffix in CODE_SUFFIXES and lines > block:
            signals.append(f'{_rel(path)} — {lines} lines, over the {block} cap; '
                           f'introduced by {_added_by(path)}')
    return signals


SECTIONS = (
    ('types', 'Off-allowlist `.md` types', 'route via core/SCHEMA.md § four disposal routes'),
    ('inventories', 'CONTEXT.md hand-written inventories', 'the routing block owns inventory'),
    ('naming', 'Naming and placement', 'kebab-case ASCII, types where their scope allows'),
    ('retired', 'Retired tokens still alive', 'a rename is unfinished until these are zero'),
    ('duplicates', 'Items claimed by two ledgers', 'v1 criterion 2 — an item lives in one place'),
    ('size', 'Size signals', 'a signal for review, never a cap — do not summarize to fit'),
)


def render(findings: dict, scanned: int) -> str:
    total = sum(len(findings[key]) for key, _, _ in SECTIONS)
    out = ['# entropy',
           '> Generated by `.hooks/entropy-dashboard.py` (ROADMAP.md Frente 4.3). Do not edit.',
           '',
           f'{date.today().isoformat()} · {scanned} tracked files scanned · '
           f'**{total} findings**', '',
           '| Check | Findings |', '|-------|----------|']
    out += [f'| {title} | {len(findings[key])} |' for key, title, _ in SECTIONS]
    for key, title, note in SECTIONS:
        items = findings[key]
        out += ['', f'## {title}', '', f'*{note}*', '']
        out += ['Clean.'] if not items else [
            f'- {_rel(i.splitlines()[0])}' for i in sorted(items)]
    return '\n'.join(out) + '\n'


def main() -> int:
    files = tracked_files(WORKSPACE_ROOT, nested=True)
    findings = collect(files)
    REPORT.write_text(render(findings, len(files)), encoding='utf-8')
    print(f'entropy dashboard → {_rel(REPORT)} '
          f'({sum(len(findings[k]) for k, _, _ in SECTIONS)} findings)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
