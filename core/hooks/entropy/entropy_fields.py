#!/usr/bin/env python3
# Does a header field that names our own code name something that exists? Zero-token, deterministic.
#
# Ruled 2026-08-24 (Lucas): a structural claim about our own tree must live in a FIELD A PARSER
# ALREADY READS. Every specimen behind that ruling — "nothing calls X", "there is nowhere
# to put Y", "Z is unbuilt", "these groups match the tree" — was written into a durable file, refuted
# by one grep, and then inherited by a later session as settled fact. The header fields are the half
# of that claim-space a parser can reach today: shard_table.py already renders `enforced-by`,
# `governs`, `feature` and `blocked-by` into every sharded index, and nothing ever asked whether what
# they name is there. Chosen for RETROACTIVE reach — it charges all ~100 declarations the day it
# lands, and asks nobody to remember a new habit.
#
# WHAT IT CANNOT DO, said here so it is not rediscovered as a gap: it never reaches prose. A claim
# written into a paragraph stays unchecked, which is the price of the option that needs no discipline.
#
# MATCH A SHAPE, NOT A TOKEN — the constraint every candidate had to meet, for the reason
# entropy_vendor.py and checks/citation-gate.py already carry: "Z is unbuilt" is ordinary English, so
# a keyword check over prose is switched off within a week. This reads only declared fields, and
# inside `governs` only the tokens SHAPED like paths; prose there is skipped in silence, by design.
#
# Total, like entropy_stores.py: no allowlist, no ratchet inside the module. The ratchet is the
# CALLER's — type-gate.py asks only about files a commit adds, the dashboard asks about all of them.
import re
import sys
from pathlib import Path

# The header parser is one directory over and is deliberately the source of truth for the shape:
# a second copy of it inside a checker is the drift this family exists to catch.
_HOOKS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_HOOKS / 'routing'))

import feature_law  # noqa: E402
from header import header_fields  # noqa: E402

WORKSPACE_ROOT = _HOOKS.parents[1]

# Fields whose every comma item is a path to something we author. `parsed-by` carries no
# declarations at all today and is checked anyway: a field that is charged from the day it is
# declared never accumulates the backlog the charged ones had.
PATH_FIELDS = ('enforced-by', 'parsed-by', 'blocked-by', 'spec')
# `governs` mixes paths with prose in one list — `engine/runtime/, libraries/` beside
# `frontend/ streaming` and `every file under code/`. Only the first token of an item can be a path,
# and only if it is shaped like one; the rest is a human qualifier and is none of this check's
# business.
MIXED_FIELDS = ('governs',)
# `feature` names the registry, not paths.
SLUG_FIELDS = ('feature',)

# A field that declares there is nothing to name. `spec: none` is the common one and is an ANSWER —
# the author was asked and said no — which is why it reads as a word rather than as an empty value.
SENTINELS = {'none', '-', '—', 'n/a'}
# A path token: no spaces, no markdown, and either a directory separator or an extension. `latex`
# and `yes` are words; `core/hooks/` and `eslint.shared.js` are paths.
PATH_TOKEN = re.compile(r'^[\w./~-]+$')
HAS_EXTENSION = re.compile(r'\.[a-z]{1,5}$')
# `code/<project>/` and `core/skills/*.md` name a SHAPE, not a file. Charging them would report a
# finding whose only fix is to delete a placeholder that is doing its job.
PLACEHOLDER = re.compile(r'[<>*?]')


def _declared() -> set:
    """What a `> feature:` line may name, read from the registry rather than restated.

    The INSTALL column first, because that is the join core/features.txt declares in its own header:
    *"Every `> feature:` slug in SETUP.md appears in this column"*. A SETUP shard names install
    steps, and `git-hooks` is a step that four features share — it is not a feature slug and never
    was. The slug column is accepted too: a field naming a real feature is not a false claim about
    this tree, and refusing it would make the check pickier than the fact it is checking.
    """
    rows = feature_law.load_registry()
    return ({r['slug'] for r in rows} | {r['install'] for r in rows}) - SENTINELS


def _repo_root(path: Path) -> Path:
    """The repo a file belongs to — the workspace root for most of the tree, a nested repo under
    code/ for the rest. A field in a nested repo names paths inside THAT repo."""
    for parent in path.resolve().parents:
        if (parent / '.git').exists():
            return parent
    return WORKSPACE_ROOT


def _items(value: str, field: str) -> list:
    """The comma list, as the tokens this field can be held to. Empty for prose.

    A path and a slug are each ONE word, so an item is its first token and whatever follows is a
    human qualifier: `frontend/ streaming` names `frontend/`, and `substrate — nothing else runs
    until these do` claims the slug `substrate`. Reading the whole item would put a sentence in
    the finding and make the same wrong claim harder to see.
    """
    out = []
    for item in value.split(','):
        words = item.strip().split()
        if field in PATH_FIELDS:
            item = item.strip()
        else:
            item = words[0] if words else ''
        out.append(item.strip('`').rstrip('.,;:'))
    return [i for i in out if i and i.lower() not in SENTINELS]


def _is_path(token: str) -> bool:
    if PLACEHOLDER.search(token) or not PATH_TOKEN.match(token):
        return False
    return '/' in token or bool(HAS_EXTENSION.search(token))


def _resolves(path: Path, token: str) -> bool:
    """Tried against the document's own directory, then its repo, then the workspace.

    Forgiving on purpose: `code/SPECS-git.md` names a workspace path and `code/flows/SPECS-data.md`
    names a repo-relative one, both correctly. A finding is only worth printing when NO reading of
    the token finds anything — otherwise the check would be enforcing a base nobody agreed on.
    """
    bases = (path.parent, _repo_root(path), WORKSPACE_ROOT)
    return any((base / token).exists() for base in bases)


def field_hits(files: list, mixed: bool = True) -> list:
    """Every header field naming a path or a slug that is not there.

    `mixed=False` drops `governs`, and the commit gate is the caller that passes it: that field's
    list mixes paths with prose, so a token this module misreads there would stop a commit rather
    than print a line. The dashboard reads it, where being wrong costs a reader ten seconds.

    The slug half runs only where the registry lives. core/features.txt is the WORKSPACE's registry;
    a nested repo under code/ declares its own install steps against no registry at all, and holding
    its `feature:` line to our slugs would report `comfyui` and `blender` as undeclared features of a
    workspace that never claimed them — the category error this front is named after.
    """
    checked = PATH_FIELDS + SLUG_FIELDS + (MIXED_FIELDS if mixed else ())
    hits, registry = [], None
    for path in files:
        if path.suffix != '.md':
            continue
        try:
            lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for field, value in header_fields(lines[2:]).items():
            if field not in checked:
                continue
            if field in SLUG_FIELDS:
                if _repo_root(path) != WORKSPACE_ROOT:
                    continue
                if registry is None:
                    registry = _declared()
                hits += [f'{path}: `{field}: {token}` is not declared in core/features.txt.\n'
                         f'   The field names an install step or a feature the registry carries\n'
                         f'   (core/SCHEMA-outgrowing.md § the field table). A word that is\n'
                         f'   neither is a claim about this workspace the registry does not make.'
                         for token in _items(value, field) if token not in registry]
                continue
            for token in _items(value, field):
                if not _is_path(token):
                    if field in MIXED_FIELDS:
                        continue  # prose in a mixed list; not this check's business
                    hits.append(f'{path}: `{field}: {token}` is not a path.\n'
                                f'   Every item in this field names a file or a directory\n'
                                f'   (core/SCHEMA-outgrowing.md § the field table).')
                elif not _resolves(path, token):
                    hits.append(f'{path}: `{field}` names {token}, which does not exist.\n'
                                f'   A field naming our own code is a claim about our own tree,\n'
                                f'   and it is checked so it cannot be inherited as fact\n'
                                f'   (core/SCHEMA-outgrowing.md § the field table).')
    return hits
