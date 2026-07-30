# T0 type gate (Frente 4.1 Tier 0): the uppercase allowlist and the CONTEXT.md
# no-hand-inventory rule. Zero-token, runs in verify-fast.
#
# The point of these tests is that the checker reads core/SCHEMA.md as its single
# source. If someone edits the law, the gate follows without a code change; if
# someone hardcodes the names back into the checker, test_law_comes_from_schema
# stops proving anything and should be read as a warning, not deleted.
import sys
from pathlib import Path

import pytest

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE_ROOT / '.hooks'))

import importlib.util

spec = importlib.util.spec_from_file_location(
    'type_gate', WORKSPACE_ROOT / '.hooks/type-gate.py')
type_gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(type_gate)

SCHEMA = WORKSPACE_ROOT / 'core/SCHEMA.md'


def test_law_comes_from_schema():
    """The allowlist is parsed, not restated — the whole design of this gate."""
    allowed, exempt = type_gate.load_law(SCHEMA)
    # Types the workspace cannot function without; a parse regression drops them all.
    assert {'AGENTS.md', 'CONTEXT.md', 'ROADMAP.md', 'SPECS.md', 'README.md'} <= allowed
    assert 'SETUP.md' in allowed, 'SETUP.md was allowlisted 2026-07-30'
    # SPEC.md was deliberately collapsed into SPECS.md and must NOT be a type.
    assert 'SPEC.md' not in allowed
    # The transient-initiative exemption is parsed from its own section.
    assert 'VERIFY.md' in exempt
    assert 'MIGRATION-STATUS.md' in exempt


def test_allowlisted_name_passes(tmp_path):
    allowed, exempt = type_gate.load_law(SCHEMA)
    target = tmp_path / 'ROADMAP.md'
    target.write_text('# r\n', encoding='utf-8')
    assert type_gate.check_name(target, allowed, exempt) is None


def test_invented_type_is_blocked(tmp_path):
    allowed, exempt = type_gate.load_law(SCHEMA)
    target = tmp_path / 'LEXICON.md'
    target.write_text('# l\n', encoding='utf-8')
    failure = type_gate.check_name(target, allowed, exempt)
    assert failure is not None
    assert 'LEXICON.md' in failure
    assert 'four disposal routes' in failure


def test_lowercase_instance_is_never_checked(tmp_path):
    allowed, exempt = type_gate.load_law(SCHEMA)
    for name in ('tree.md', 'labels.md', 'draft.md', 'some-notes.md'):
        target = tmp_path / name
        target.write_text('# x\n', encoding='utf-8')
        assert type_gate.check_name(target, allowed, exempt) is None


def test_harness_mandated_name_is_exempt(tmp_path):
    allowed, exempt = type_gate.load_law(SCHEMA)
    target = tmp_path / 'CLAUDE.md'
    target.write_text('# c\n', encoding='utf-8')
    assert type_gate.check_name(target, allowed, exempt) is None


def _context(tmp_path, body):
    target = tmp_path / 'CONTEXT.md'
    target.write_text(body, encoding='utf-8')
    return target


def test_ascii_tree_is_flagged(tmp_path):
    # The code/isoroll-content/CONTEXT.md '## Repository Shape' class of violation.
    target = _context(tmp_path, '# d\n> desc\n\n## Repository Shape\n\n'
                                '```\nsrc/\n├── a.py\n└── b.py\n```\n')
    failure = type_gate.check_inventory(target)
    assert failure is not None
    assert 'ASCII directory tree' in failure


def test_inventory_heading_is_flagged(tmp_path):
    target = _context(tmp_path, '# d\n> desc\n\n## File Map\n\nprose only, no bullets\n')
    failure = type_gate.check_inventory(target)
    assert failure is not None
    assert 'File Map' in failure


def _with_files(tmp_path, *names):
    for name in names:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('x\n', encoding='utf-8')


def test_path_bullets_are_flagged(tmp_path):
    _with_files(tmp_path, 'src/a.py', 'src/b.py', 'src/c.py')
    target = _context(tmp_path, '# d\n> desc\n\n'
                                '- `src/a.py` — does a\n'
                                '- `src/b.py` — does b\n'
                                '- `src/c.py` — does c\n')
    failure = type_gate.check_inventory(target)
    assert failure is not None
    assert '3 bullets listing real files' in failure


def test_two_path_bullets_are_allowed(tmp_path):
    """Pointing at a couple of files in prose is navigation, not an inventory."""
    _with_files(tmp_path, 'src/a.py', 'src/b.py')
    target = _context(tmp_path, '# d\n> desc\n\n'
                                '- `src/a.py` — the entry point\n'
                                '- `src/b.py` — the parser\n')
    assert type_gate.check_inventory(target) is None


def test_naming_convention_globs_are_allowed(tmp_path):
    """academy/papers/*/images/CONTEXT.md documents filename PATTERNS, not files.

    This was a real false positive: five bullets of glob patterns read as an
    inventory until the check required the path to exist on disk.
    """
    target = _context(tmp_path, '# images\n> All manuscript figures\n\n'
                                'Naming conventions:\n'
                                '- `grav_cam2_gXX_sq.png` — gravity gradient panels\n'
                                '- `spin_s4_*.sq.png` — spin gradient panels\n'
                                '- `newton_sX_sq.png` — scene gallery\n'
                                '- `*_rk4_s3_front_480p.png` — metric comparison\n')
    assert type_gate.check_inventory(target) is None


def test_generated_routing_block_is_not_an_inventory(tmp_path):
    """Everything below routing:start is generated and owns inventory by design."""
    target = _context(tmp_path, '# d\n> desc\n\n<!-- routing:start -->\n## Routing\n\n'
                                '| File | Interface | API | Description |\n'
                                '|---|---|---|---|\n'
                                '| [`a.py`](a.py) | — | — | does a |\n'
                                '| [`b.py`](b.py) | — | — | does b |\n'
                                '| [`c.py`](c.py) | — | — | does c |\n'
                                '<!-- routing:end -->\n')
    assert type_gate.check_inventory(target) is None


def test_clean_context_passes(tmp_path):
    target = _context(tmp_path, '# thing\n> What this directory is, in one line.\n\n'
                                'Prose about the subtree and its rules.\n')
    assert type_gate.check_inventory(target) is None


def test_non_context_file_is_not_inventory_checked(tmp_path):
    target = tmp_path / 'ROADMAP.md'
    target.write_text('## File Map\n\n- `a.py` — a\n- `b.py` — b\n- `c.py` — c\n',
                      encoding='utf-8')
    assert type_gate.check_inventory(target) is None
