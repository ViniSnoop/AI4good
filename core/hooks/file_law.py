#!/usr/bin/env python3
# What a file IS, and which rules apply to it. The numeric-law sibling of schema_law.py:
# that module parses core/SCHEMA.md, this one owns the file-shape law every size, fanout
# and line-count check reads.
#
# Why it exists (2026-07-31): "a code file" was defined FOUR times — check-line-counts.sh,
# entropy-dashboard.py, workspace_meta.py and workspace_scanner.py each carried their own
# extension list, and no two agreed. `.sh` and extensionless executables were invisible to
# the BLOCKING gate, which is how core/hooks/pre-commit reached 385 lines and
# core/tools/wos/sync-skills 341 without ever being stopped. One definition, one home.
import fnmatch
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIMITS_FILE = HERE / 'limits.env'
VENDORED_FILE = HERE / 'vendored.txt'
EXTENSIONLESS_FILE = HERE / 'extensionless.txt'

# Things the line cap and the fanout signal apply to. Prose types (.md, .yaml, .toml) are
# NOT here: their size is a signal, never a cap. `.tex` is code on purpose — a paper
# section file is authored under the same 200-line rule (academy/papers/SPECS.md § File size).
CODE_EXTS = {'.js', '.jsx', '.ts', '.tsx', '.py', '.dart', '.sh',
             '.html', '.css', '.scss', '.tex'}

# A stub is generated FROM its source and rides in the routing table's Interface column.
GENERATED = ('.pyi', '.d.ts', '.dart.api', '.texif')


def is_code_file(path: Path) -> bool:
    """One definition. Extension, or an extensionless file carrying a shebang.

    The shebang arm is what closes the old blind spot: `core/hooks/pre-commit` and the
    core/tools CLIs are real code whose names are dictated by git or by ergonomics.
    """
    if path.name.endswith(GENERATED):
        return False
    if path.suffix in CODE_EXTS:
        return True
    if path.suffix:
        return False
    try:
        return path.open('rb').read(2) == b'#!'
    except OSError:
        return False


def load_limits() -> dict:
    """Every numeric limit, from the one file that holds them."""
    limits = {}
    for line in LIMITS_FILE.read_text(encoding='utf-8').splitlines():
        line = line.split('#', 1)[0].strip()
        if '=' in line:
            key, value = line.split('=', 1)
            limits[key.strip()] = int(value.strip())
    return limits


def _lines(path: Path) -> list:
    if not path.exists():
        return []
    return [ln.strip() for ln in path.read_text(encoding='utf-8').splitlines()
            if ln.strip() and not ln.startswith('#')]


def _patterns() -> list:
    return _lines(VENDORED_FILE)


def allowed_extensionless() -> set:
    """Basenames an external tool dictates, so they cannot carry an extension."""
    return set(_lines(EXTENSIONLESS_FILE))


def is_vendored(path: Path, root: Path) -> bool:
    """True for third-party files we did not author and must not police.

    17 of the 28 files over the line cap are conference templates (sigconf, iclr). Holding
    someone else's LaTeX class to our authoring rules makes the finding list 60% noise and
    would make every paper uncommittable. Same shape as gitignore-exceptions.txt: a named,
    reviewed list, never a heuristic.
    """
    try:
        rel = str(path.resolve().relative_to(root))
    except ValueError:
        return False
    return any(fnmatch.fnmatch(rel, pattern) for pattern in _patterns())


def main() -> int:
    """`--filter-code` keeps stdin paths that are code, so the shell gate shares this law."""
    if '--filter-code' not in sys.argv:
        print('usage: file_law.py --filter-code < paths', file=sys.stderr)
        return 2
    root = HERE.parents[1]
    for line in sys.stdin:
        candidate = Path(line.strip())
        if not line.strip():
            continue
        full = candidate if candidate.is_absolute() else root / candidate
        if is_code_file(full) and not is_vendored(full, root):
            print(line.strip())
    return 0


if __name__ == '__main__':
    sys.exit(main())
