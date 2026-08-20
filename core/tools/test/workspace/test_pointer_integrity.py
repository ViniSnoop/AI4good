# T0 pointer-integrity check (Tier 0): every relative
# ](path) link across CONTEXT.md / ROADMAP*.md / SCHEMA.md / AGENTS.md (repo) and
# MEMORY.md (auto-memory) must resolve. Zero-token, runs in verify-fast.
#
# [[slug]] resolution is intentionally NOT gated here: the memory spec allows a
# dangling [[slug]] as a "planned, not yet written" memory, and the corpus mixes
# kebab-case `name:` fields with underscore filenames as the link target, so there
# is no single rule to enforce yet. The entropy dashboard counts them instead.
import re
from pathlib import Path

from conftest import WORKSPACE_ROOT  # the depth lives in one file, not nine

# The auto-memory store lives IN the workspace as of 2026-08-15; the harness path
# ~/.claude/projects/<slug>/memory is a symlink to this directory, so every memory the
# harness writes lands in git and can be trimmed like any other file. This used to reach
# into $HOME and hardcode the project slug — a Tier 0 gate that read a path outside the
# repo it guards, and that no clone of this workspace could satisfy.
MEMORY_DIR = WORKSPACE_ROOT / "brain/memory"

# Deleted content still on disk is not workspace structure. A file manager moves a
# deleted project into .Trash-<uid>/, whose stale relative links then fail the check
# and block every commit until the trash is emptied — a gate nobody can fix by editing
# the workspace. Trash is excluded by prefix because the uid varies per machine.
EXCLUDE_DIRS = {".git", "node_modules", ".venv", "__pycache__", ".craft"}
EXCLUDE_PREFIXES = (".Trash",)
STRUCTURAL_NAME = re.compile(r"^(CONTEXT|SCHEMA|AGENTS|ROADMAP|ROADMAP-.*)\.md$")

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
FENCE_RE = re.compile(r"^\s*```")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
ROUTING_BLOCK_RE = re.compile(
    r"<!-- routing:start -->.*?<!-- routing:end -->", re.DOTALL
)


def _strip_fences(text: str) -> str:
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    text = "\n".join(out)
    # Auto-generated routing tables (AGENTS.md: "do not edit manually") hoist a
    # child CONTEXT.md's line-2 description verbatim, links and all; staleness
    # there is a sync-tool bug (dead pointer, or an unrewritten relative path
    # one level up), not a hand-authored one — out of scope for this Tier-0 gate.
    text = ROUTING_BLOCK_RE.sub(" ", text)
    # Inline single-backtick spans quote literal syntax for documentation
    # (e.g. `` `[[slug]]` `` describing the convention itself) — not real refs.
    return INLINE_CODE_RE.sub(" ", text)


def _structural_files(root: Path, memory_dir: Path):
    for path in root.rglob("*.md"):
        if any(part in EXCLUDE_DIRS or part.startswith(EXCLUDE_PREFIXES)
               for part in path.parts):
            continue
        if STRUCTURAL_NAME.match(path.name):
            yield path
    if memory_dir.is_dir():
        yield from memory_dir.glob("*.md")


def check_pointers(root: Path, memory_dir: Path) -> list:
    """Return a list of human-readable broken-pointer messages (empty = clean)."""
    failures = []
    for path in _structural_files(root, memory_dir):
        text = _strip_fences(path.read_text(encoding="utf-8"))
        for link in LINK_RE.findall(text):
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            if "<" in link:  # template placeholder, e.g. brain/goals/<slug>.md
                continue
            target = link.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                failures.append(f"{path}: broken link -> {link}")
    return failures


def test_pointer_integrity():
    failures = check_pointers(WORKSPACE_ROOT, MEMORY_DIR)
    assert not failures, "Pointer integrity broken:\n" + "\n".join(failures)


def test_dangling_relative_link_is_detected(tmp_path):
    # Regression fixture for the `../.vendor` dangling-link class of bug
    # (core/skills/caveman/scripts/CONTEXT.md, fixed f3d837f-era).
    sub = tmp_path / "scripts"
    sub.mkdir()
    (sub / "CONTEXT.md").write_text(
        "attribution in [`../.vendor`](../.vendor).\n", encoding="utf-8"
    )
    failures = check_pointers(tmp_path, tmp_path / "no-memory-here")
    assert len(failures) == 1
    assert "../.vendor" in failures[0]


def test_clean_fixture_has_no_failures(tmp_path):
    (tmp_path / "target.md").write_text("target\n", encoding="utf-8")
    (tmp_path / "CONTEXT.md").write_text("see [target](target.md).\n", encoding="utf-8")
    assert check_pointers(tmp_path, tmp_path / "no-memory-here") == []
