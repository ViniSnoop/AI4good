# Text written for one file, made safe to show inside another file's table.
#
# Split out of workspace_scanner.py 2026-08-15 at the size gate, and the split is the
# design: hoisting is one operation with three parts — FIND the sentence, REBASE its links,
# BOUND its length — and those parts had drifted into two modules that each did some of it.
# A subdirectory row hoisted a blurb and got all three; a `.md` file row hoisted nothing and
# showed its H1 instead (ROADMAP.md Frente 4.7). One module, one rule: everything hoisted
# goes through hoist().
import re
from pathlib import Path

DESC_LIMIT = 80
SCAFFOLD_BLURB = '← add description'
LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')


def md_blurb(path: Path) -> str:
    """A `.md` file's line-2 `> ` blurb — the sentence that says what the file IS.

    The `#` H1 is a *name*, not a description: `COMMENT_RE['.md']` captured it and stopped,
    so `tree.md` advertised "The Craft Tree" in every routing table while the sentence
    saying what it is sat one line below, unread. This line has always been read for a
    *child's* CONTEXT.md and for nothing else — same class as the missing `.sh` key in
    COMMENT_RE: the generator had the text and did not reach for it.
    """
    try:
        lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
    except OSError:
        return ''
    if len(lines) < 2:
        return ''
    match = re.match(r'^>\s*(.+)', lines[1].strip())
    if not match:
        return ''
    blurb = match.group(1).strip()
    return '' if blurb == SCAFFOLD_BLURB else blurb


def rebase_links(text: str, prefix: str) -> str:
    """Rewrite relative link targets so they resolve from the PARENT directory.

    A hoisted description travels verbatim into a table one directory up, where
    `[REFS.md](REFS.md)` silently names the *parent's* REFS.md — a different file, or none
    at all. Absolute paths, URLs and bare anchors already mean the same from either
    directory, so they are left alone.
    """
    # Underscored because `python_api` walks the whole AST, so a nested closure with a bare
    # name is advertised in the routing table as importable API. Real gap, written down in
    # ROADMAP.md Frente 4.7; the convention already carries the fix.
    def _fix(match):
        target = match.group(2)
        if target.startswith(('/', '#')) or '://' in target or target.startswith('mailto:'):
            return match.group(0)
        return f'[{match.group(1)}]({prefix}{target})'
    return LINK_RE.sub(_fix, text)


def truncate_outside_links(text: str, limit: int) -> str:
    """Cut to `limit`, never mid-link and never mid-word, and say that you cut.

    Mid-link, because a half-copied `[REFS.md](RE` is a broken pointer and the
    pointer-integrity check would be right to fail on it. Mid-word, because `Tier 0 checks
    t` reads as a typo rather than as a truncation — the reader cannot tell a cut from a
    mistake, which is half of why these descriptions read badly. The ellipsis is what makes
    the difference visible.
    """
    if len(text) <= limit:
        return text
    cut, at_link = limit, False
    for match in LINK_RE.finditer(text):
        if match.start() < cut < match.end():
            cut, at_link = match.start(), True
            break
    head = text[:cut]
    if not at_link and not text[cut].isspace():
        whole_words = head.rsplit(' ', 1)[0]
        if whole_words:
            head = whole_words
    return head.rstrip().rstrip('.,;:—-') + '…'


def hoist(text: str, prefix: str) -> str:
    """Rebase and bound in one call — the only way hoisted text enters a table.

    Both parts always, because either one alone is a bug that shipped: rebasing without
    bounding lets one file's paragraph set the width of somebody else's table, and bounding
    without rebasing leaves pointers aimed at the wrong directory.

    A code file's first-line comment does NOT come through here. It was authored as a
    one-liner, for this table, in this directory — there is nothing to rebase and cutting it
    would lose text that nothing else carries.
    """
    return truncate_outside_links(rebase_links(text, prefix), DESC_LIMIT)
