#!/usr/bin/env python3
# The entropy dashboard. Runs every Tier 0 check over the whole
# tree and writes ONE generated report, so agents and Lucas read a pre-computed file
# instead of re-scanning the workspace. Zero-token, no LLM.
#
# Division of labour with core/hooks/checks/type-gate.py: the gate is a ratchet and only blocks what
# a commit ADDS, which is why a repo that inherited violations is not blocked on every
# commit. Everything it lets through historically shows up here, once, with a count.
#
# Nothing here blocks. The cap that does live in checks/pre-edit.py; this file reports what the
# tree already carries, including the files a ratchet let through before the cap reached them.
# Crossing a threshold asks for a SPLIT, never for a summary — forced brevity is the trap, and
# core/SCHEMA-outgrowing.md § A type that outgrows the cap shards says what a split
# has to leave behind.
import subprocess
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

# The checks are one level up in entropy/; the law (file_law, schema_law) is two, at the root of
# the enforcement layer; git/ holds the one check that reads git state instead of file content.
_ENTROPY = Path(__file__).resolve().parents[1]
for _dir in (_ENTROPY, _ENTROPY.parent, _ENTROPY.parent / 'git',
             _ENTROPY.parent / 'routing'):
    sys.path.insert(0, str(_dir))

import feature_law  # noqa: E402
from blocks import replace_block  # noqa: E402
from branch_debt import merged_remote_branches, unmerged_branches  # noqa: E402
from entropy_context import check_goal_link, check_misplaced_answer  # noqa: E402
from entropy_corpus import (enforcement_paths, is_generated_mirror,  # noqa: E402
                            tracked_files, wiki_exempt_paths)
from entropy_fanout import fanout_signals  # noqa: E402
from entropy_ledger import (duplicate_slugs, finished_work_hits,  # noqa: E402
                            goal_vocabulary, retired_hits,
                            unanswered_placeholders, wiki_link_hits)
from entropy_naming import check_dirs, check_placement, check_shape  # noqa: E402
from entropy_report import END, SECTIONS, SEED, START, render  # noqa: E402
from entropy_stores import experiment_hits, ref_tier_hits  # noqa: E402
from file_law import (is_authored, is_authored_prose,  # noqa: E402
                      is_generated_artifact, is_vendored, load_limits,
                      over_column_cap)
from schema_law import (SCHEMA, WORKSPACE_ROOT, load_law,  # noqa: E402
                        load_retired, load_scopes)

# The measurements sit under the hand-written issues, in their own block: an entropy finding and a
# known bug answer the same question, and core/SCHEMA.md gives that question one file. This tool
# owns the block, never the file.
REPORT = WORKSPACE_ROOT / 'ISSUES.md'

LEDGERS = {
    # Every shard of the wos ledger is ONE namespace: criterion 2 forbids the same item in two
    # ledgers, and sharding a ledger does not make its own shards rivals.
    'wos-roadmap': [WORKSPACE_ROOT / 'ROADMAP.md',
                    *sorted(WORKSPACE_ROOT.glob('ROADMAP-*.md'))],
    'life-todo': [WORKSPACE_ROOT / 'brain/TODO.md'],
    'core-roadmap': [WORKSPACE_ROOT / 'core/ROADMAP.md'],
    'goals': sorted((WORKSPACE_ROOT / 'brain/goals').glob('*.md')),
}


def _gate(name: str):
    """Load a kebab-named gate from checks/ — the dashboard reports what the gates block."""
    spec = spec_from_file_location(
        name.replace('-', '_'), WORKSPACE_ROOT / f'core/hooks/checks/{name}.py')
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    gate = _gate("type-gate")
    allowed, exempt = load_law(SCHEMA)
    scopes = load_scopes(SCHEMA)
    head_warn = load_limits()['CONTEXT_HEAD_WARN']
    findings = {'types': [], 'inventories': [], 'naming': [], 'goals': [],
                'misplaced': []}
    for path in files:
        if failure := gate.check_name(path, allowed, exempt):
            findings['types'].append(failure)
        if path.name == 'CONTEXT.md' and (failure := gate.check_inventory(path)):
            findings['inventories'].append(failure)
        if failure := check_misplaced_answer(path, head_warn):
            findings['misplaced'].append(failure)
        if failure := check_goal_link(path):
            findings['goals'].append(failure)
        for failure in (check_shape(path, allowed), check_dirs(path, WORKSPACE_ROOT),
                        check_placement(path, scopes, WORKSPACE_ROOT)):
            if failure:
                findings['naming'].append(failure)
    exempt = enforcement_paths(WORKSPACE_ROOT)
    findings['retired'] = retired_hits(files, load_retired(SCHEMA), exempt)
    citations = _gate('citation-gate')
    findings['citations'] = citations.citation_hits(
        files, citations.citation_exempt_paths(WORKSPACE_ROOT))
    findings['wiki'] = wiki_link_hits(
        files, goal_vocabulary(WORKSPACE_ROOT / 'brain/goals'),
        wiki_exempt_paths(WORKSPACE_ROOT))
    findings['duplicates'] = [f'`[{slug}]` claimed by {", ".join(sorted(claims))}'
                              for slug, claims in duplicate_slugs(LEDGERS).items()]
    findings['size'] = size_signals(files)
    findings['stubs'] = stub_signals(files)
    findings['fanout'] = fanout_signals(files, WORKSPACE_ROOT)
    findings['branches'] = unmerged_branches(WORKSPACE_ROOT)
    findings['remotes'] = merged_remote_branches(WORKSPACE_ROOT)
    findings['finished'] = finished_work_hits(files, exempt)
    findings['undescribed'] = unanswered_placeholders(files, exempt)
    findings['stores'] = experiment_hits(files) + ref_tier_hits(files)
    # One directory-level finding is reported by every file under it; dedupe so a count
    # means "things to fix", not "files touched by a thing to fix".
    findings['naming'] = sorted(set(findings['naming']))
    return findings


def size_signals(files: list) -> list:
    """Authored files over the line cap, and .md lines over the column cap.

    One number for both kinds since 2026-08-18. Prose used to carry its own DOC_SIGNAL_LINES=300,
    a second number answering the question BLOCK_LINES already answers, which is the drift
    file_law.py exists to prevent — and it reported a file it never held to anything.
    """
    limits = load_limits()
    block, cols = limits['BLOCK_LINES'], limits['BLOCK_COLS']
    signals = []
    for path in files:
        if is_generated_mirror(path):
            continue
        prose = is_authored_prose(path, WORKSPACE_ROOT)
        if not prose and not is_authored(path, WORKSPACE_ROOT):
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        lines = text.splitlines()
        if len(lines) > block:
            signals.append(f'{_rel(path)} — {len(lines)} lines, over the {block} cap; '
                           f'introduced by {_added_by(path)}')
        long = over_column_cap(text, cols) if prose else []
        if long:
            signals.append(f'{_rel(path)} — {len(long)} line(s) over the {cols}-column cap '
                           f'(first at line {long[0]})')
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
        if not stub or is_vendored(path, WORKSPACE_ROOT) or \
                is_generated_artifact(path, WORKSPACE_ROOT):
            continue
        if path.name.endswith('.d.ts') or '__pycache__' in path.parts:
            continue
        if not path.with_name(path.stem + stub).exists():
            signals.append(f'{_rel(path)} — no {stub}')
    return signals


def main() -> int:
    if not feature_law.is_enabled('entropy-dashboard'):
        return 0  # switched off: no report is written, so the number stops existing rather than lying
    files = tracked_files(WORKSPACE_ROOT, nested=True)
    findings = collect(files)
    text = REPORT.read_text(encoding='utf-8') if REPORT.exists() else SEED
    block = render(findings, len(files), WORKSPACE_ROOT)
    REPORT.write_text(replace_block(text, block, START, END), encoding="utf-8")
    print(f'entropy dashboard → {_rel(REPORT)} '
          f'({sum(len(findings[k]) for k, _, _ in SECTIONS)} findings)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
