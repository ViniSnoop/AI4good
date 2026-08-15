#!/usr/bin/env python3
# The entropy dashboard (ROADMAP.md Frente 4.3). Runs every Tier 0 check over the whole
# tree and writes ONE generated report, so agents and Lucas read a pre-computed file
# instead of re-scanning the workspace. Zero-token, no LLM.
#
# Division of labour with core/hooks/checks/type-gate.py: the gate is a ratchet and only blocks what
# a commit ADDS, which is why a repo that inherited violations is not blocked on every
# commit. Everything it lets through historically shows up here, once, with a count.
#
# Size is reported as a SIGNAL, never a cap: crossing a threshold asks for a delta review,
# it does not ask anyone to summarize a document down. Forced brevity is the trap.
import subprocess
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

# The law (file_law, schema_law) lives one level up, at the root of the enforcement layer;
# the checks below are siblings here in entropy/.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from entropy_context import check_goal_link  # noqa: E402
from entropy_corpus import enforcement_paths, tracked_files, wiki_exempt_paths  # noqa: E402
from entropy_fanout import fanout_signals  # noqa: E402
from entropy_ledger import (duplicate_slugs, goal_vocabulary,  # noqa: E402
                            retired_hits, wiki_link_hits)
from entropy_naming import check_dirs, check_placement, check_shape  # noqa: E402
from entropy_report import SECTIONS, render  # noqa: E402
from file_law import is_code_file, is_vendored, load_limits  # noqa: E402
from schema_law import (SCHEMA, WORKSPACE_ROOT, load_law,  # noqa: E402
                        load_retired, load_scopes)

REPORT = WORKSPACE_ROOT / 'entropy.md'
# A curated doc past this asks for a delta review. Docs are long because thinking is long;
# this is the point where it is worth asking whether two documents are wearing one name.
DOC_SIGNAL_LINES = 300

LEDGERS = {
    'wos-roadmap': [WORKSPACE_ROOT / 'ROADMAP.md'],
    'life-todo': [WORKSPACE_ROOT / 'brain/TODO.md'],
    'core-roadmap': [WORKSPACE_ROOT / 'core/ROADMAP.md'],
    'goals': sorted((WORKSPACE_ROOT / 'brain/goals').glob('*.md')),
}


def _type_gate():
    spec = spec_from_file_location(
        'type_gate', WORKSPACE_ROOT / 'core/hooks/checks/type-gate.py')
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _block_lines() -> int:
    return load_limits()['BLOCK_LINES']


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
    findings = {'types': [], 'inventories': [], 'naming': [], 'goals': []}
    for path in files:
        if failure := gate.check_name(path, allowed, exempt):
            findings['types'].append(failure)
        if path.name == 'CONTEXT.md' and (failure := gate.check_inventory(path)):
            findings['inventories'].append(failure)
        if failure := check_goal_link(path):
            findings['goals'].append(failure)
        for failure in (check_shape(path, allowed), check_dirs(path, WORKSPACE_ROOT),
                        check_placement(path, scopes, WORKSPACE_ROOT)):
            if failure:
                findings['naming'].append(failure)
    exempt = enforcement_paths(WORKSPACE_ROOT)
    findings['retired'] = retired_hits(files, load_retired(SCHEMA), exempt)
    findings['wiki'] = wiki_link_hits(
        files, goal_vocabulary(WORKSPACE_ROOT / 'brain/goals'),
        wiki_exempt_paths(WORKSPACE_ROOT))
    findings['duplicates'] = [f'`[{slug}]` claimed by {", ".join(sorted(claims))}'
                              for slug, claims in duplicate_slugs(LEDGERS).items()]
    findings['size'] = size_signals(files)
    findings['stubs'] = stub_signals(files)
    findings['fanout'] = fanout_signals(files, WORKSPACE_ROOT)
    # One directory-level finding is reported by every file under it; dedupe so a count
    # means "things to fix", not "files touched by a thing to fix".
    findings['naming'] = sorted(set(findings['naming']))
    return findings


def size_signals(files: list) -> list:
    block = _block_lines()
    signals = []
    for path in files:
        code = is_code_file(path) and not is_vendored(path, WORKSPACE_ROOT)
        if not code and path.suffix != '.md':
            continue
        try:
            lines = len(path.read_text(encoding='utf-8').splitlines())
        except (OSError, UnicodeDecodeError):
            continue
        if path.suffix == '.md' and lines > DOC_SIGNAL_LINES:
            signals.append(f'{_rel(path)} — {lines} lines (doc signal, review the delta)')
        elif code and lines > block:
            signals.append(f'{_rel(path)} — {lines} lines, over the {block} cap; '
                           f'introduced by {_added_by(path)}')
    return signals


_STUB_FOR = {'.py': '.pyi', '.ts': '.d.ts', '.tsx': '.d.ts', '.js': '.d.ts'}


def stub_signals(files: list) -> list:
    """Source files with no interface stub beside them.

    The read gate only fires when a stub EXISTS, so a missing one does not break —
    it silently switches the interface-first discipline off for that file, and nothing
    said so. The commit hook stubs what a commit stages; a file that arrived any other
    way was never stubbed and was never counted. This is the counting.
    """
    signals = []
    for path in files:
        stub = _STUB_FOR.get(path.suffix)
        if not stub or is_vendored(path, WORKSPACE_ROOT):
            continue
        if path.name.endswith('.d.ts') or '__pycache__' in path.parts:
            continue
        if not path.with_name(path.stem + stub).exists():
            signals.append(f'{_rel(path)} — no {stub}')
    return signals


def main() -> int:
    files = tracked_files(WORKSPACE_ROOT, nested=True)
    findings = collect(files)
    REPORT.write_text(render(findings, len(files), WORKSPACE_ROOT), encoding="utf-8")
    print(f'entropy dashboard → {_rel(REPORT)} '
          f'({sum(len(findings[k]) for k, _, _ in SECTIONS)} findings)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
