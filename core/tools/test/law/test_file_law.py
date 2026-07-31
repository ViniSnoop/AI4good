# T0 file law (Frente 3.2 close-out). Zero-token, runs in verify-fast.
#
# Why this file exists: "a code file" was defined FIVE times — check-line-counts.sh,
# entropy-dashboard.py, workspace_meta.py, pre-edit.py and facade-gate.py each carried an
# extension list, and no two agreed. `.sh` and extensionless executables were invisible to
# the BLOCKING gate, which is how core/hooks/pre-commit reached 385 lines and
# core/tools/wos/sync-skills 341 without ever being stopped.
#
# test_no_checker_carries_its_own_extension_list is the one that makes that unrepeatable.
import subprocess
import sys
from pathlib import Path

from conftest import WORKSPACE_ROOT  # the depth lives in one file, not nine
# sys.path for the enforcement layer is set once, by conftest.py — a second copy
# here would go stale the next time core/hooks is split.

from file_law import (CODE_EXTS, allowed_extensionless,  # noqa: E402
                      is_code_file, is_vendored, load_limits)

HOOKS = WORKSPACE_ROOT / 'core/hooks'


def test_an_extensionless_executable_is_code(tmp_path) -> None:
    """The blind spot that let a 385-line pre-commit through, closed."""
    script = tmp_path / 'pre-commit'
    script.write_text('#!/usr/bin/env bash\necho hi\n', encoding='utf-8')
    assert is_code_file(script)


def test_an_extensionless_plain_file_is_not_code(tmp_path) -> None:
    plain = tmp_path / 'LICENSE'
    plain.write_text('MIT\n', encoding='utf-8')
    assert not is_code_file(plain)


def test_shell_scripts_are_code(tmp_path) -> None:
    assert is_code_file(tmp_path / 'deploy.sh')


def test_generated_stubs_are_not_code(tmp_path) -> None:
    """A stub is produced FROM its source; policing it would double-count the source."""
    for name in ('mod.pyi', 'mod.d.ts'):
        assert not is_code_file(tmp_path / name)


def test_prose_is_not_code(tmp_path) -> None:
    """Doc length is a signal, never a cap — .md must never enter the blocking population."""
    for name in ('ROADMAP.md', 'data.yaml', 'pyproject.toml'):
        assert not is_code_file(tmp_path / name)


def test_tex_is_code_because_papers_say_so() -> None:
    """academy/papers/SPECS.md § File size puts section files under the same 200-line rule."""
    assert '.tex' in CODE_EXTS


def test_vendored_templates_are_exempt() -> None:
    """17 of 28 over-cap files are conference templates. Upstream's layout is not ours."""
    template = WORKSPACE_ROOT / 'academy/papers/ai4good/sigconf-i13n.tex'
    ours = WORKSPACE_ROOT / 'core/hooks/file_law.py'
    assert is_vendored(template, WORKSPACE_ROOT)
    assert not is_vendored(ours, WORKSPACE_ROOT)


def test_every_extensionless_tracked_file_is_explained() -> None:
    """Extensionless is allowed but never accidental: shebang, or a tool-mandated name.

    This is the check that answers "can we require extensions everywhere?" — no, because
    git names its own hooks and make names its own file. Making the exemption a named list
    is what stops extensionless files being a blind spot again.
    """
    mandated = allowed_extensionless()
    out = subprocess.run(['git', 'ls-files'], cwd=WORKSPACE_ROOT,
                         capture_output=True, text=True).stdout
    unexplained = []
    for rel in out.splitlines():
        path = WORKSPACE_ROOT / rel
        if Path(rel).suffix or not path.is_file() or path.name in mandated:
            continue
        if is_vendored(path, WORKSPACE_ROOT):
            continue
        try:
            if path.open('rb').read(2) != b'#!':
                unexplained.append(rel)
        except OSError:
            continue
    assert not unexplained, (
        f'extensionless files that are neither executable, vendored, nor listed in '
        f'core/hooks/extensionless.txt: {unexplained}')


def test_no_checker_carries_its_own_extension_list() -> None:
    """The defect this whole module exists to prevent: a second definition of "code"."""
    checkers = ['entropy/entropy-dashboard.py', 'entropy/entropy_fanout.py',
                'routing/workspace_meta.py', 'checks/pre-edit.py',
                'routing/context_synchronizer.py', 'checks/check-line-counts.sh']
    checkers += [f'gates/{p.name}' for p in sorted((HOOKS / 'gates').glob('*.sh'))]
    checkers += [f'generators/{p.name}' for p in sorted((HOOKS / 'generators').glob('*.sh'))]
    offenders = []
    for name in checkers:
        source = (HOOKS / name).read_text(encoding='utf-8')
        restates = ("'.py'" in source and "'.ts'" in source) or 'js|ts|tsx|py' in source
        if restates and 'file_law' not in source:
            offenders.append(name)
    assert not offenders, f'these restate the code-file law instead of importing it: {offenders}'


def test_every_limit_has_one_home() -> None:
    """Four numbers, one file. A checker hard-coding one of them is drift."""
    limits = load_limits()
    assert set(limits) == {'WARN_LINES', 'BLOCK_LINES', 'WARN_FILES', 'BLOCK_FILES'}
    assert limits['WARN_LINES'] < limits['BLOCK_LINES']
    assert limits['WARN_FILES'] < limits['BLOCK_FILES']
    scanner = (HOOKS / 'routing/workspace_scanner.py').read_text(encoding='utf-8')
    assert 'SPLIT_THRESHOLD = 7' not in scanner
