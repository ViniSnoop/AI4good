# The routing table's generated columns (Frente 3.2). Zero-token, runs in verify-fast.
#
# Two rules, both measured on 2026-07-30 across 159 CONTEXT.md / 1242 rows:
#   1. A generated column empty on EVERY row is not emitted. 773 of 1242 rows carried an
#      em-dash Interface, paying table width to say "nothing here".
#   2. `test_*` symbols are not API. The test runner collects them; no module imports one.
#
# Rule 2 is keyed on the SYMBOL, never on the path. A `tests/`-directory exemption would
# be a door to walk production code through, dodging the facade and interface-stub gates.
# test_a_production_symbol_in_a_test_directory_still_appears is that guarantee — it must
# never be deleted to make another test pass.
import sys
from pathlib import Path

from conftest import WORKSPACE_ROOT  # the depth lives in one file, not nine
# sys.path for the enforcement layer is set once, by conftest.py — a second copy
# here would go stale the next time core/hooks is split.

from workspace_meta import ALL_EXTS, COMMENT_RE, extract_api, file_description  # noqa: E402
from workspace_scanner import build_file_rows, parse_preserved_files  # noqa: E402


def _table(tmp_path, **sources) -> str:
    files = []
    for name, body in sources.items():
        p = tmp_path / name
        p.write_text(body, encoding='utf-8')
        files.append((p, name))
    return build_file_rows(files, {}, tmp_path)


def test_an_all_empty_interface_column_is_dropped(tmp_path) -> None:
    table = _table(tmp_path, **{'a.py': '# alpha\n', 'b.py': '# beta\n'})
    assert '| Interface |' not in table
    assert '| File |' in table and 'Description |' in table


def test_a_column_with_one_real_value_survives(tmp_path) -> None:
    (tmp_path / 'a.pyi').write_text('def go() -> None: ...\n', encoding='utf-8')
    table = _table(tmp_path, **{'a.py': '# alpha\ndef go():\n    pass\n', 'b.py': '# beta\n'})
    assert '| Interface |' in table


def test_file_and_description_are_never_dropped(tmp_path) -> None:
    """Even when every description is the placeholder, the column is the table."""
    table = _table(tmp_path, **{'a.py': 'x = 1\n', 'b.py': 'y = 2\n'})
    assert table.splitlines()[0].startswith('| File |')
    assert table.splitlines()[0].rstrip().endswith('Description |')


def test_test_symbols_are_not_listed_as_api(tmp_path) -> None:
    p = tmp_path / 'test_thing.py'
    p.write_text('def test_a_thing_holds():\n    pass\n', encoding='utf-8')
    assert extract_api(p) == '—'


def test_a_shared_fixture_is_still_api(tmp_path) -> None:
    """Suppression must not swallow the helpers a conftest genuinely exports."""
    p = tmp_path / 'conftest.py'
    p.write_text('def make_scene():\n    pass\n\ndef test_ignored():\n    pass\n',
                 encoding='utf-8')
    assert '`make_scene`' in extract_api(p)
    assert 'test_ignored' not in extract_api(p)


def test_a_production_symbol_in_a_test_directory_still_appears(tmp_path) -> None:
    """The anti-circumvention guarantee: no path-shaped door out of the API column.

    Moving a module into `tests/` must not hide what it exports, or an agent could park
    production code there to escape the facade and interface-stub gates.
    """
    d = tmp_path / 'tests'
    d.mkdir()
    p = d / 'helpers.py'
    p.write_text('def build_payload():\n    pass\n', encoding='utf-8')
    assert '`build_payload`' in extract_api(p)


def test_every_scanned_extension_can_be_described() -> None:
    """The scanner's extension list and the comment-pattern table must agree.

    Two lists that have to match, with nothing checking that they did: `.sh` and `.jsx`
    were in ALL_EXTS and absent from COMMENT_RE, so 59 tracked files were undescribable by
    construction. Each got `← add first-line comment` in its routing row no matter how well
    it was commented — including `core/hooks/post-edit.sh`, inside the enforcement
    directory, which ROADMAP.md Frente 4.6 read as evidence of a discipline hole.
    """
    missing = sorted(ALL_EXTS - set(COMMENT_RE))
    assert not missing, (
        f'{missing} are scanned but have no comment pattern, so file_description() returns '
        f"'' for every one of them and the generator asks for a comment the file may "
        f'already carry. Add a pattern to COMMENT_RE in core/hooks/routing/workspace_meta.py')


def test_a_shell_script_is_described_below_its_shebang(tmp_path) -> None:
    """The concrete case: a shebang is not the description, the comment under it is."""
    p = tmp_path / 'thing.sh'
    p.write_text('#!/usr/bin/env bash\n# does the thing\n', encoding='utf-8')
    assert file_description(p) == 'does the thing'


def test_preserved_descriptions_survive_a_narrower_table() -> None:
    """Descriptions are re-read from tables of any arity — first cell file, last cell desc."""
    four = '| [`a.py`](a.py) | — | `go` | does the thing |'
    two = '| [`a.py`](a.py) | does the thing |'
    assert parse_preserved_files(four) == {'a.py': 'does the thing'}
    assert parse_preserved_files(two) == {'a.py': 'does the thing'}
