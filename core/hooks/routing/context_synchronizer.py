#!/usr/bin/env python3
# Sync the Routing block in CONTEXT.md (or AGENTS.md at workspace root).
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import feature_law
from blocks import line_pos as _line_pos
from blocks import replace_block as _replace
from file_law import is_code_file
from shard_table import build_shard_rows, index_for, shards_of
from workspace_scanner import (
    SPLIT_THRESHOLD,
    code_files, has_code_content, subdir_scan,
    parse_preserved_files, parse_preserved_subs,
    build_sub_rows, build_file_rows, build_routing_block,
)

RS  = '<!-- routing:start -->'
RE  = '<!-- routing:end -->'



_ROUTING_HEAD = re.compile(r'^##\s+Routing\s*$', re.MULTILINE)
_NEXT_HEAD    = re.compile(r'^#{1,2}\s+\S', re.MULTILINE)


def _drop_unsentineled_routing(text: str) -> str:
    """Remove a hand-written `## Routing` section so the generated block replaces it.

    Without this the generator appended its block anyway and the file ended up with two
    Routing sections — one hand-maintained and going stale, one generated — with nothing
    saying which the reader should believe. The generator owns inventory (core/AGENTS.md),
    so the hand-written one loses; everything after it is kept untouched.
    """
    m = _ROUTING_HEAD.search(text)
    if not m:
        return text
    nxt = _NEXT_HEAD.search(text, m.end())
    end = nxt.start() if nxt else len(text)
    return (text[:m.start()].rstrip('\n') + '\n\n' + text[end:].lstrip('\n')).rstrip('\n')


def replace_block(text: str, new_block: str) -> str:
    """Swap the routing block for a new one, standardized to the end of the file.

    Shared by the two things that own a routing block — a directory's CONTEXT.md and a sharded
    type's index. They differ in what fills the block, never in where it sits.

    The marker mechanics live in blocks.py, shared with every other generated block; what stays
    here is the routing table's own two rules — it goes last, and a hand-written `## Routing`
    section it finds instead of markers is the block it is replacing.
    """
    if _line_pos(text, RS) == -1 or _line_pos(text, RE) == -1:
        text = _drop_unsentineled_routing(text)
    return _replace(text, new_block, RS, RE, at_end=True)


def sync_shards(target: Path) -> bool:
    """Rewrite the index table of the sharded type `target` belongs to; False when it is not one.

    Runs BESIDE the directory sync rather than instead of it: a shard is one of its type's files
    and one of its directory's, and both tables are meant to know about it.
    """
    index = index_for(target)
    if index is None:
        return False
    block = build_routing_block('', build_shard_rows(shards_of(index)), RS, RE)
    index.write_text(replace_block(index.read_text(encoding='utf-8'), block), encoding='utf-8')
    print(f'✓ shard-sync: {index}')
    return True


def sync(target: Path):
    # The one seam for `routing-tables` (core/SPECS.md § AD-14): pre-commit
    # (generators/routing.sh) and post-edit (postedit/sync.sh) both arrive here, so one
    # guard switches both moments off. The two fragments keep separate call sites because
    # only the pre-commit one stages the result — a difference in what they do with the
    # block, not in whether the block gets written.
    if not feature_law.is_enabled('routing-tables'):
        return
    if not target.is_dir():
        sync_shards(target)
    directory = target if target.is_dir() else target.parent

    ctx = directory / 'CONTEXT.md'
    workspace_mode = False
    if not ctx.exists():
        w = directory / 'AGENTS.md'
        if w.exists():
            ctx = w
            workspace_mode = True
        else:
            return

    text = ctx.read_text(encoding='utf-8')

    # Extract preserved descriptions first (workspace_mode uses them for link_list).
    si = _line_pos(text, RS)
    ei = _line_pos(text, RE)
    inner           = text[si + len(RS): ei] if si != -1 and ei != -1 else ''
    preserved_files = parse_preserved_files(inner)
    preserved_subs  = parse_preserved_subs(inner)

    # Scan directory.
    if workspace_mode:
        # Workspace root: include only subdirs with CONTEXT.md or preserved descriptions.
        # This excludes OS system dirs ($RECYCLE.BIN etc.) not in the curated list.
        all_files = []
        all_subdirs = sorted(p for p in directory.iterdir()
                             if p.is_dir() and not p.name.startswith('.'))
        link_list = [s for s in all_subdirs
                     if (s / 'CONTEXT.md').exists() or s.name in preserved_subs]
    else:
        direct_files = [(f, f.name) for f in code_files(directory)]
        fold_list, link_list = subdir_scan(directory, RS, RE)
        all_files = direct_files + fold_list

    # Build new block.
    sub_content  = build_sub_rows(link_list, preserved_subs)  if link_list  else ''
    file_content = build_file_rows(all_files, preserved_files, directory) if all_files else ''
    new_block    = build_routing_block(sub_content, file_content, RS, RE)

    ctx.write_text(replace_block(text, new_block), encoding='utf-8')
    print(f'✓ routing-sync: {ctx}')

    removed = set(preserved_files) - {rel for _, rel in all_files}
    for r in removed:
        print(f'  removed stale entry: {r}')

    if not workspace_mode:
        code_count = sum(1 for f, _ in direct_files if is_code_file(f))
        if code_count > SPLIT_THRESHOLD:
            print(f'⚠  {directory}: {code_count} code files — consider splitting')


if __name__ == '__main__':
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    sync(target)
