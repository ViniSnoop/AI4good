#!/usr/bin/env python3
"""Brain stats — shared config, git helpers, and block replacement."""

import re
import subprocess
from pathlib import Path

# Paths stay workspace-relative: the hooks run with cwd at the workspace root and git
# reports --name-only against the same origin, so a relative path compares directly to
# what git prints. WORKSPACE is the one absolute, needed to resolve an owned path to the
# nested repo that actually holds its history.
WORKSPACE  = Path(__file__).resolve().parents[3]
BRAIN      = Path("brain")
GOALS_FILE = BRAIN / "GOALS.md"
LOG_DIR    = BRAIN / ".log"        # runtime state only (compass-last.txt), never an archive
GOALS_DIR  = BRAIN / "goals"


def workspace_rel(path):
    """`path` as a workspace-relative string, whether it arrived absolute or relative."""
    p = Path(path)
    return str(p.relative_to(WORKSPACE)) if p.is_absolute() else str(p)

PERIODS = [
    ("month",     30),
    ("trimester", 90),
    ("semester",  180),
    ("year",      365),
    ("2-year",    730),
    ("4-year",    1460),
]

DONE_KEEP = 3

AREAS = ["health", "career", "finances", "fun", "spiritual"]


def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


# touch_count / last_touch_date lived here and counted commits against a goal's own .md
# file. That is the defect brain_attention.py exists to fix, and leaving them would leave a
# second, wrong definition of "a touch" for the next caller to reach for. Deleted 2026-08-13.


def replace_block(content, start, end, new_block):
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(content):
        return None
    return pattern.sub(lambda _: new_block, content)
