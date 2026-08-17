# T0 type gate (Tier 0, law in core/SCHEMA.md): the uppercase allowlist. Zero-token, runs in verify-fast.
#
# The no-hand-inventory rule moved to entropy/test_entropy_inventory.py 2026-08-15 — it
# tests `entropy_context.py`, not this gate, which only decides WHEN a check runs.
#
# The point of these tests is that the checker reads core/SCHEMA.md as its single
# source. If someone edits the law, the gate follows without a code change; if
# someone hardcodes the names back into the checker, test_law_comes_from_schema
# stops proving anything and should be read as a warning, not deleted.
from conftest import WORKSPACE_ROOT  # the depth lives in one file, not nine
# sys.path for the enforcement layer is set once, by conftest.py — a second copy
# here would go stale the next time core/hooks is split.

import importlib.util

spec = importlib.util.spec_from_file_location(
    'type_gate', WORKSPACE_ROOT / 'core/hooks/checks/type-gate.py')
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
    assert 'REFACTOR.md' in exempt
    # Membership only shrinks; each is routed to a ROADMAP-<slug>.md or a SPECS.md. VERIFY.md left
    # on 2026-08-17 when its rename landed — the exemption covers the old name, never the new one.
    assert exempt == {'ROADMAP-spec-drive.md', 'REFACTOR.md', 'DECISIONS.md'}, (
        'the exemption is a closed list that only shrinks — a new name here means someone '
        'invented a type instead of using ROADMAP-<slug>.md'
    )


def test_scopes_come_from_schema():
    """The third parse of the law, and the only one whose loss is silent.

    A heading rename is already caught: it empties `load_retired` (KeyError in
    test_retired_tokens_come_from_schema) or `exempt` (the closed-list assert above).
    `load_scopes` has no such tripwire — it reads the type table's second column, so
    reformatting that table empties it, `check_placement` stops flagging anything, and
    the naming suite still passes because it only asserts findings stay within a baseline.
    Fewer findings is exactly what a broken parse looks like.
    """
    scopes = type_gate.load_scopes(SCHEMA)
    assert scopes == {'AGENTS.md': 'root', 'README.md': 'repo-root'}, (
        'the scope column of the type table stopped parsing — check_placement is now '
        'silently checking nothing'
    )


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
