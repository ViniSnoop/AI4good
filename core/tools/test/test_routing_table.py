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

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE_ROOT / '.hooks'))

from workspace_meta import extract_api  # noqa: E402
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


def test_preserved_descriptions_survive_a_narrower_table() -> None:
    """Descriptions are re-read from tables of any arity — first cell file, last cell desc."""
    four = '| [`a.py`](a.py) | — | `go` | does the thing |'
    two = '| [`a.py`](a.py) | does the thing |'
    assert parse_preserved_files(four) == {'a.py': 'does the thing'}
    assert parse_preserved_files(two) == {'a.py': 'does the thing'}
