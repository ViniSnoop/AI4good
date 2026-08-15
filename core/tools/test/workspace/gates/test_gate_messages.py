# T0: a blocking gate must say WHY on stderr. Claude Code feeds a PreToolUse exit-2's
# stderr back to the model and drops stdout, so a gate printing to stdout blocks the edit
# with no reason attached — it reads as "No stderr output" (ROADMAP Batch B item 3).
import json
import re
import subprocess
from pathlib import Path

import pytest

from conftest import WORKSPACE_ROOT

PRE_EDIT = WORKSPACE_ROOT / "core/hooks/checks/pre-edit.py"

# Every gate wired as a blocking PreToolUse hook. pre-edit.py was the only one of the six
# on stdout, which is why this went unnoticed for so long: five siblings were correct.
BLOCKING_GATES = (
    "core/hooks/checks/pre-edit.py",
    "core/hooks/checks/bugs-gate.py",
    "core/hooks/read/context-gate.py",
    "core/hooks/read/bash-context-gate.py",
    "core/hooks/read/spec-read-gate.py",
    "core/hooks/facade/facade-gate.py",
)


def _run(payload: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(PRE_EDIT)], input=json.dumps(payload),
        capture_output=True, text=True,
    )


@pytest.mark.parametrize("gate", BLOCKING_GATES)
def test_every_blocking_gate_writes_its_reason_to_stderr(gate: str) -> None:
    body = (WORKSPACE_ROOT / gate).read_text(encoding="utf-8")
    # Five of the six block with `return 2` from main(), not sys.exit(2). Matching only
    # the latter skipped exactly the gates this test exists to check — a green run that
    # asserted nothing.
    assert re.search(r'(sys\.)?exit\(2\)|return 2', body), (
        f"{gate} is listed as a blocking gate but has no blocking path — either it "
        "stopped blocking or this list is stale"
    )
    assert "stderr" in body, (
        f"{gate} exits 2 without ever naming stderr — Claude Code drops stdout on a "
        "PreToolUse block, so the edit is refused with no reason attached"
    )


def test_no_bare_print_survives_in_pre_edit() -> None:
    """Every message here is a rejection; none of them belongs on stdout."""
    body = PRE_EDIT.read_text(encoding="utf-8")
    bare = [l.strip() for l in body.splitlines()
            if re.match(r'\s*print\(', l) and "stderr" not in l]
    assert not bare, f"pre-edit.py prints to stdout again: {bare}"


def test_first_line_rejection_lands_on_stderr(tmp_path: Path) -> None:
    r = _run({"tool_name": "Write",
              "tool_input": {"file_path": str(tmp_path / "p.py"), "content": "x = 1\n"}})
    assert r.returncode == 2
    assert "FIRST-LINE MISSING" in r.stderr
    assert not r.stdout.strip()


def test_context_description_rejection_lands_on_stderr(tmp_path: Path) -> None:
    r = _run({"tool_name": "Write",
              "tool_input": {"file_path": str(tmp_path / "CONTEXT.md"),
                             "content": "# t\nno blockquote\n"}})
    assert r.returncode == 2
    assert "CONTEXT.md DESCRIPTION MISSING" in r.stderr
    assert not r.stdout.strip()


def test_size_gate_rejection_lands_on_stderr(tmp_path: Path) -> None:
    r = _run({"tool_name": "Write",
              "tool_input": {"file_path": str(tmp_path / "big.py"),
                             "content": "# big\n" + "x = 1\n" * 400}})
    assert r.returncode == 2
    assert "SIZE GATE" in r.stderr
    assert not r.stdout.strip()


def test_an_allowed_edit_is_silent_and_exits_zero(tmp_path: Path) -> None:
    ok = tmp_path / "ok.py"
    ok.write_text("# ok\nx = 1\n", encoding="utf-8")
    r = _run({"tool_name": "Edit",
              "tool_input": {"file_path": str(ok), "old_string": "x", "new_string": "y"}})
    assert r.returncode == 0
    assert not r.stdout.strip() and not r.stderr.strip()
