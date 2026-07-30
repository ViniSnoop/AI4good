# T0 ledger and vocabulary checks (Frente 4.1 Tier 0). Zero-token, runs in verify-fast.
#
# Two of these tests assert against the LIVE workspace and are meant to be green at all
# times, not baselined: a surviving retired token means a rename is unfinished, and a
# cross-ledger duplicate slug means v1 criterion 2 is false. Both were red when written,
# and the fix was to finish the work, not to widen the test.
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE_ROOT / '.hooks'))

import entropy_ledger  # noqa: E402
import schema_law  # noqa: E402

# The four wos ledgers (ROADMAP.md header: "an item lives in exactly one of the four").
# All goal files share one namespace because their achievement slugs are per-goal
# vocabulary — six startapps each having a [build-mvp] is not six copies of one item.
LEDGERS = {
    'wos-roadmap': [WORKSPACE_ROOT / 'ROADMAP.md'],
    'life-todo': [WORKSPACE_ROOT / 'brain/TODO.md'],
    'core-roadmap': [WORKSPACE_ROOT / 'core/ROADMAP.md'],
    'goals': sorted((WORKSPACE_ROOT / 'brain/goals').glob('*.md')),
}


def test_retired_tokens_come_from_schema():
    """Declared, not hardcoded — the same design as the type allowlist."""
    retired = schema_law.load_retired()
    assert retired['loop-engineering'] == 'craft'
    assert retired['KNOWN-BUGS'] == 'BUGS.md'
    assert 'SPEC.md' not in retired, 'that rename has not landed yet (Frente 12.1)'


def test_no_retired_token_survives():
    """A rename is finished only when its old spelling appears nowhere."""
    hits = entropy_ledger.retired_hits(
        entropy_ledger.tracked_files(WORKSPACE_ROOT),
        schema_law.load_retired(),
        entropy_ledger.enforcement_paths(WORKSPACE_ROOT))
    assert hits == [], '\n'.join(hits)


def test_the_law_may_name_what_it_retires(tmp_path):
    law = tmp_path / 'SCHEMA.md'
    law.write_text('| `gone-token` | `kept` | 2026-01-01 |\n', encoding='utf-8')
    assert entropy_ledger.retired_hits([law], {'gone-token': 'kept'}, {law}) == []


def test_retired_token_in_a_filename_is_a_hit(tmp_path):
    """The `fable-loop-engineering.md` shape: hyphen is a boundary, so a retired token
    hiding inside a compound name is still found. That is where a half-done rename
    survives longest."""
    target = tmp_path / 'prefix-gone-token.md'
    target.write_text('clean body\n', encoding='utf-8')
    hits = entropy_ledger.retired_hits([target], {'gone-token': 'kept'}, set())
    assert len(hits) == 1
    assert 'filename' in hits[0]


def test_a_longer_word_is_not_a_substring_hit(tmp_path):
    """Retired `gone-token` must not fire on `gone-tokenizer` — a different word."""
    target = tmp_path / 'note.md'
    target.write_text('the gone-tokenizer module is unrelated\n', encoding='utf-8')
    assert entropy_ledger.retired_hits([target], {'gone-token': 'kept'},
                                       set()) == []


def test_item_slugs_read_item_position_only(tmp_path):
    target = tmp_path / 'ROADMAP.md'
    target.write_text(
        '- [ ] [real-item] do the thing\n'
        '> [x] [done-item] finished\n'
        '- **`[parked-item]`** — out of scope\n'
        'prose mentioning [a-reference] mid-sentence\n'
        '- see [a-link](http://x) for details\n', encoding='utf-8')
    assert entropy_ledger.item_slugs(target) == {'real-item', 'done-item', 'parked-item'}


def test_sibling_namespaces_may_repeat_a_slug(tmp_path):
    for name in ('goal-a.md', 'goal-b.md'):
        (tmp_path / name).write_text('> [ ] [build-mvp] ship it\n', encoding='utf-8')
    namespaces = {'goals': [tmp_path / 'goal-a.md', tmp_path / 'goal-b.md']}
    assert entropy_ledger.duplicate_slugs(namespaces) == {}


def test_same_slug_in_two_ledgers_is_a_duplicate(tmp_path):
    (tmp_path / 'ROADMAP.md').write_text('- [ ] [thing] do it\n', encoding='utf-8')
    (tmp_path / 'TODO.md').write_text('- [ ] [thing] do it\n', encoding='utf-8')
    dups = entropy_ledger.duplicate_slugs(
        {'roadmap': [tmp_path / 'ROADMAP.md'], 'todo': [tmp_path / 'TODO.md']})
    assert set(dups) == {'thing'}
    assert set(dups['thing']) == {'roadmap', 'todo'}


def test_no_item_lives_in_two_ledgers():
    """v1 criterion 2, verified by scan rather than eyeball."""
    dups = entropy_ledger.duplicate_slugs(LEDGERS)
    assert dups == {}, '; '.join(
        f'[{slug}] in {sorted(claims)}' for slug, claims in dups.items())
