# A sharded type's index table: what each TYPE-<slug>.md publishes, rendered so the index answers
# "open or skip" without anything being opened.
#
# Its own module rather than a third job for workspace_scanner.py, whose sentence is *directory*
# discovery and assembly — a sharded index is not a directory, and the scanner was two lines from
# the cap. render_table came with it: both builders drop a column that is empty on every row, and
# that rule was about to exist twice.
#
# The law it serves: core/SCHEMA-outgrowing.md § What a shard publishes about itself.
import re
from pathlib import Path

from hoist import hoist, md_blurb

# `> key: value` under the H1 — the shape CONTEXT.md already uses for `> spec:`, so no new parser
# and, unlike frontmatter, it renders where a person can see it.
SHARD_FIELD = re.compile(r'^>\s*([a-z][a-z-]*):\s*(.+)$')
# An open item is a NUMBERED one — `1.`, `10b.` — which is the shape a roadmap actually uses and
# the same one entropy_ledger.TICKED_ITEM recognises. Counting `[slug]` instead would have read
# most fronts as empty: the bracketed id is optional and most items carry prose alone.
# The MARK IS PART OF THE SHAPE, and requiring it corrected two counts on 2026-08-19. Without it
# this matched `1. **Fold**` — a nested sub-step inside one ledger item — and the two numbered
# rules inside a legibility front's opening paragraph, so the index advertised 6 open where 4 were
# and 8 where 6 were. A numbered line in prose looks exactly like an item; a marked one does not,
# and ROADMAP.md § How to read this requires the mark on every item. LUCAS_ITEM already assumed it.
ITEM = re.compile(r'^\d+[a-z]?\.[ \t]*[🔴🟡🟢]', re.M)
# The marker counts only in ITEM position. A bare substring count read 13 where the ledger holds
# 12, because one shard has a sentence ABOUT the count with the marker inside it — the same
# confusion between a mark and a mention that made the hand-kept count wrong four times.
LUCAS_ITEM = re.compile(r'^[ \t]*\d+[a-z]?\.[ \t]*🔴', re.M)
# The optional id, when an item declares one. Narrower than entropy_ledger's copy on purpose: an
# index only needs to NAME items, never to decide whether two ledgers claim the same one.
SLUG = re.compile(r'^\s*(?:[-*>]+\s*)*(?:\d+[a-z]?\.\s*)?(?:\[[ xX]\]\s*)*[^\S\n]*'
                  r'(?:[🔴🟡🟢]\s*)?\**`?\[([a-z0-9][a-z0-9-]+)\](?!\()', re.M)
EMPTY_CELL = {'—', '-', ''}
# The headline an item already carries: the bold lead-in right after its number and mark. This is
# the column the index was missing — `Items` reads the optional `[slug]` id, which almost no item
# declares, so it rendered empty for every shard but one while the generator was ALREADY parsing
# the item text to produce Open and Needs Lucas. It read what would let a reader skip a shard and
# threw it away. Ruled 2026-08-19 (Lucas), after a session opened all seven shards to answer one
# question. Bold is not decoration here: every item in the family opens with it, so it is an
# authored one-line summary and the generator never has to write prose.
#
# The MARK IS REQUIRED and the item must start at column 0, which is what separates an item from
# prose that merely looks like one. Without both, this listed `1. **Fold**` — a nested sub-step
# inside one item — and `1. **Language is the thing.**`, two numbered rules inside a front's
# opening paragraph. Every real item carries a mark by ROADMAP.md § How to read this, and
# LUCAS_ITEM above already depends on that being true.
ITEM_HEADLINE = re.compile(r'^(\d+[a-z]?)\.[ \t]*([🔴🟡🟢])[ \t]*\*\*(.+?)\*\*', re.M | re.S)

# Column order is reading order: what it is, then how much is live, then what stops you.
SHARD_COLUMNS = (('Shard', None), ('Description', 'description'), ('Prio', 'priority'),
                 ('Open', 'open'), ('Needs Lucas', 'needs-lucas'), ('Answers', 'answers'),
                 ('Governs', 'governs'), ('Feature', 'feature'), ('Parsed by', 'parsed-by'),
                 ('Enforced by', 'enforced-by'), ('Blocked by', 'blocked-by'),
                 ('Items', 'items'))


def shard_facts(path: Path) -> dict:
    """What a shard publishes about itself, plus what can be counted instead of published.

    The declared half is the `> key: value` lines. The derived half is everything countable,
    because a declared count is a second copy of a fact: ROADMAP.md kept one by hand and it went
    stale four times, twice while the paragraph asking to keep it true sat above it.
    """
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return {}
    lines = text.splitlines()
    facts = {'lines': str(len(lines))}
    for line in lines[2:]:
        if not line.startswith('>'):
            break
        if match := SHARD_FIELD.match(line.strip()):
            facts[match.group(1)] = match.group(2).strip()
    # The three counts are ROADMAP-only, as core/SCHEMA.md's field table says. Deriving them for
    # every type read a SPECS shard as having 13 open items, because a numbered list in prose looks
    # exactly like a numbered item — a count that is meaningless is worse than no column.
    if path.stem.split('-')[0] != 'ROADMAP':
        return facts
    if items := ITEM.findall(text):
        facts['open'] = str(len(items))
    if slugs := SLUG.findall(text):
        facts['items'] = ' '.join(f'`{slug}`' for slug in slugs)
    if red := LUCAS_ITEM.findall(text):
        facts['needs-lucas'] = str(len(red))
    return facts


def render_table(headers: tuple, rows: list, always: tuple) -> str:
    """A markdown table minus every column that is EMPTY_CELL on every row.

    Measured 2026-07-30: 773 of 1242 rows workspace-wide carried an em-dash Interface, paying table
    width in every read to say "nothing here". A column that says nothing for every row is not
    information about the thing it describes.
    """
    if not rows:
        return ''
    keep = [i for i in range(len(headers))
            if i in always or any(r[i] not in EMPTY_CELL for r in rows)]
    out = ['| ' + ' | '.join(headers[i] for i in keep) + ' |',
           '|' + '|'.join('-' * (len(headers[i]) + 2) for i in keep) + '|']
    out += ['| ' + ' | '.join(r[i] for i in keep) + ' |' for r in rows]
    return '\n'.join(out)


def shards_of(index: Path) -> list:
    """Every `TYPE-<slug>.md` beside `TYPE.md`, in name order. Empty when the type has not split."""
    return sorted(index.parent.glob(f'{index.stem}-*{index.suffix}'))


def index_for(path: Path) -> Path | None:
    """The index a `.md` belongs to, when it is part of a sharded type — else None.

    Answers for a shard AND for the index itself, so editing either one re-syncs the same table.
    A type with shards but no index (`code/` holds ROADMAP-verify.md and ROADMAP-spec-drive.md
    and no ROADMAP.md) returns None rather than inventing a file: an index nobody wrote is a
    decision, not a side effect of saving.
    """
    if path.suffix != '.md' or not path.stem.split('-')[0].isupper():
        return None
    index = path.parent / f'{path.stem.split("-")[0]}{path.suffix}'
    return index if index.exists() and shards_of(index) else None


def item_headlines(path: Path) -> list:
    """`(mark, headline)` per open item — what the index needs so a shard can be skipped.

    Only for a sharded ROADMAP, for the same reason the counts are: a numbered list in prose is
    shaped exactly like a numbered item, and headlines for those would be noise presented as an
    index. Whitespace is collapsed because a headline may wrap across lines in the source.
    """
    if path.stem.split('-')[0] != 'ROADMAP':
        return []
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return []
    out = []
    for _number, mark, headline in ITEM_HEADLINE.findall(text):
        out.append((mark or '·', ' '.join(headline.split())))
    return out


def build_open_items(shards: list) -> str:
    """The open items of every shard, one line each, under the table that names the shards.

    A list rather than a table cell: fourteen headlines in one cell is not something anybody
    reads, and this section is the whole point — it is what lets a session answer a question
    without opening a shard, which the Description column alone never did.
    """
    blocks = []
    for shard in shards:
        rows = item_headlines(shard)
        if not rows:
            continue
        lines = [f'**[`{shard.name}`]({shard.name})**', '']
        lines += [f'- {mark} {headline}' for mark, headline in rows]
        blocks.append('\n'.join(lines))
    if not blocks:
        return ''
    return ('### What is open, per shard\n\n'
            '*Generated from each shard\'s item headlines — open a shard only when one of these '
            'is the thing you came for.*\n\n' + '\n\n'.join(blocks))


def build_shard_rows(shards: list) -> str:
    """One row per shard. Which columns survive is what tells a reader which type this index is:
    a sharded ROADMAP keeps Prio/Open/Needs Lucas, a sharded SPECS keeps Governs/Enforced by, and
    neither builder had to be told which one it was looking at."""
    rows = []
    for shard in shards:
        facts = shard_facts(shard)
        facts['description'] = hoist(md_blurb(shard), '') or '← add description'
        rows.append([f'[`{shard.name}`]({shard.name})']
                    + [facts.get(key, '—') or '—' for _, key in SHARD_COLUMNS[1:]])
    headers = tuple(name for name, _ in SHARD_COLUMNS)
    table = render_table(headers, rows, (0, 1))
    items = build_open_items(shards)
    return f'{table}\n\n{items}' if items else table
