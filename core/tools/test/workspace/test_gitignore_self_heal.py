# T0 self-healing .gitignore allowlist check (core/hooks/SPECS.md): a new domain subdir with a
# CONTEXT.md must get its `!<domain>/<dir>/` allow line added automatically, no human action.
import subprocess
from pathlib import Path

from conftest import WORKSPACE_ROOT

SCRIPT = WORKSPACE_ROOT / "core/hooks/git" / "gitignore-self-heal.sh"


def _make_fixture(tmp_path: Path) -> Path:
    (tmp_path / ".gitignore").write_text(
        "core/*\n!core/CONTEXT.md\n!core/tools/\n", encoding="utf-8"
    )
    (tmp_path / "core/hooks").mkdir(parents=True)
    (tmp_path / "core/hooks" / "gitignore-exceptions.txt").write_text(
        "core/excluded\n", encoding="utf-8"
    )
    (tmp_path / "core" / "tools").mkdir(parents=True)
    (tmp_path / "core" / "tools" / "CONTEXT.md").write_text("tools\n", encoding="utf-8")
    (tmp_path / "core" / "newdir").mkdir()
    (tmp_path / "core" / "newdir" / "CONTEXT.md").write_text("newdir\n", encoding="utf-8")
    (tmp_path / "core" / "scratch").mkdir()  # no CONTEXT.md — correctly ignored
    (tmp_path / "core" / "excluded").mkdir()
    (tmp_path / "core" / "excluded" / "CONTEXT.md").write_text("excluded\n", encoding="utf-8")
    (tmp_path / "core" / "ownrepo" / ".git").mkdir(parents=True)
    (tmp_path / "core" / "ownrepo" / "CONTEXT.md").write_text("ownrepo\n", encoding="utf-8")
    return tmp_path


def _run(tmp_path: Path) -> str:
    subprocess.run(["bash", str(SCRIPT), str(tmp_path)], check=True)
    return (tmp_path / ".gitignore").read_text(encoding="utf-8")


def test_new_context_bearing_subdir_gets_allowlisted(tmp_path):
    gitignore = _run(_make_fixture(tmp_path))
    assert "!core/newdir/" in gitignore


def test_context_free_subdir_is_left_ignored(tmp_path):
    gitignore = _run(_make_fixture(tmp_path))
    assert "!core/scratch/" not in gitignore


def test_exception_listed_subdir_is_never_added(tmp_path):
    gitignore = _run(_make_fixture(tmp_path))
    assert "!core/excluded/" not in gitignore


def test_already_allowed_subdir_is_untouched(tmp_path):
    fixture = _make_fixture(tmp_path)
    before = (fixture / ".gitignore").read_text(encoding="utf-8")
    gitignore = _run(fixture)
    assert gitignore.count("!core/tools/") == before.count("!core/tools/") == 1


def test_running_twice_is_idempotent(tmp_path):
    fixture = _make_fixture(tmp_path)
    _run(fixture)
    gitignore = _run(fixture)
    assert gitignore.count("!core/newdir/") == 1


def test_own_repo_subdir_is_never_touched(tmp_path):
    # A nested git repo is unreachable from the outer repo: git cannot track files inside it
    # without submodules, killed by the 2026-07-22 nested-gitlink-gate decision. Any allow line
    # tracks nothing and leaves a permanent `?? <dir>` in git status — which is what the first
    # version of this hook did to 13 code/ projects. Routing reads their CONTEXT.md off-disk.
    gitignore = _run(_make_fixture(tmp_path))
    assert "core/ownrepo" not in gitignore
