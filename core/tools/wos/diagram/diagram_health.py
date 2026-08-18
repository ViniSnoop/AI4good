# What the workspace's declarations say about its HEALTH, as opposed to its contents.
#
# The three drawings beside this one are inventories: they answer "what is there". Lucas asked a
# different question — "is WOS well tied, does it have loose ends, too much noise, discardable
# things, and what is MISSING" — and an inventory cannot answer it, which is why the first version
# of the page rendered correctly and still did not earn its read.
#
# Every finding here is DERIVED from the same declared sources the rest of the picture reads. None
# is a threshold somebody chose: a feature enforcing nothing is a fact the registry states, an
# orphan directory is a fact the routing blocks state by omission. A finding this module cannot
# support is absent rather than guessed.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import diagram_data as data  # noqa: E402
import feature_law  # noqa: E402
from diagram_data import WORKSPACE_ROOT  # noqa: E402
from entropy_corpus import tracked_files  # noqa: E402


def harness_owned(rel: str) -> bool:
    """A top-level dotted directory belongs to a HARNESS, not to this workspace.

    A RULE, deliberately, and not a list of `.claude` / `.opencode` / `.github` / `.vscode`.
    AGENTS.md's first structural claim is that the workspace owns its state and never a vendor's
    directory, so a dotted top level is by definition somebody else's tree — mirrored into, not
    authored here. A list would go stale the day a new provider is added, and would silently start
    reporting that provider's mirror as rot the workspace should fix.
    """
    return rel.startswith('.')


def orphans(root: Path = WORKSPACE_ROOT) -> list:
    """[(directory, tracked files)] — holds tracked files, and no routing block points at it.

    The strongest loose end the tree can state: the routing chain is how an agent reaches
    anything, so a directory outside it holds work nothing can navigate to. Sorted by name rather
    than by size, because every one of them is worth the same single line of attention.
    """
    routed, _edges, _coverage = data.containment(root)
    counts: dict = {}
    for path in tracked_files(root):
        rel = str(path.relative_to(root).parent)
        if rel != '.' and not harness_owned(rel):
            counts[rel] = counts.get(rel, 0) + 1
    return sorted((d, n) for d, n in counts.items() if d not in routed)


def _layers(rows: list) -> tuple:
    """(declared layers, layers holding at least one feature). A feature may name several with
    `+`, so the split goes through feature_law rather than through the raw column."""
    held = {group for row in rows for group in feature_law.groups(row)}
    return sorted(feature_law.GROUPS), sorted(feature_law.GROUPS & held)


def by_layer(rows: list) -> list:
    """[(layer, {enforcement: count}, total)] — every DECLARED layer, biggest first.

    A layer holding nothing is kept with a total of zero rather than dropped, and that is the
    whole point of iterating the declared set instead of the observed one: `agents` and `flows`
    are declared layers of this workspace that hold no feature, and a drawing built from what
    exists can never show what does not.
    """
    counts: dict = {layer: {} for layer in feature_law.GROUPS}
    for row in rows:
        for layer in feature_law.groups(row):
            strength = counts.setdefault(layer, {})
            strength[row['enforcement']] = strength.get(row['enforcement'], 0) + 1
    out = [(layer, strength, sum(strength.values())) for layer, strength in counts.items()]
    return sorted(out, key=lambda r: (-r[2], r[0]))


def findings(rows: list, coverage: dict, root: Path = WORKSPACE_ROOT) -> list:
    """Every health finding, biggest first: [{count, of, text, where, inferred}].

    `of` is the population the count is out of, or None when the finding has no denominator — it
    is what turns "7 directories" into "2 OF 6 layers", which is the difference between a number
    and a proportion a reader can judge. `inferred` marks a finding standing on convention rather
    than on a declaration, so the page can label it exactly like every other inferred edge.

    EVERY ROW HERE IS A GAP, and two candidates were cut on 2026-08-18 for failing that test.
    "28 of 68 features enforce nothing" reads as dead weight and is nothing of the kind: those 28
    are 15 skills, 7 tools and 6 recording hooks — features that serve when called instead of
    pushing on their own, which is a layer of this workspace and not a defect in it. "14 of 24
    sites carry exactly one feature" is the same mistake: a small directory is small. Both are
    facts about SHAPE, so the grid draws them and this list does not claim them. A findings list
    whose largest number is not a problem teaches its reader to stop believing the rest.
    """
    declared, held = _layers(rows)
    empty = [layer for layer in declared if layer not in held]
    loose = orphans(root)
    out = [
        _f(len(loose), None,
           'directories hold tracked files that no routing block points at',
           'the routing blocks, against git ls-files'),
        _f(len(data.INFERRED_TRIGGER), None,
           'hook firing moments are inferred — no registry declares them',
           'core/hooks/, by directory convention', inferred=True),
        _f(len(empty), len(declared),
           'declared layers hold no feature at all', 'core/features.txt § group'),
        _f(len(feature_law.findings()), len(rows),
           'features cannot be switched off at all', 'core/features.txt § wired'),
        _f(len(coverage['unparsed']), coverage['total'],
           'routing blocks could not be read', 'the routing sentinels'),
    ]
    return sorted(out, key=lambda f: -f['count'])


def _f(count: int, of, text: str, where: str, inferred: bool = False) -> dict:
    return {'count': count, 'of': of, 'text': text, 'where': where, 'inferred': inferred}


def detail(rows: list, root: Path = WORKSPACE_ROOT) -> dict:
    """The names behind the counts, for the findings that are short enough to name in full.

    A count tells Lucas there is rot; a name tells him where to go. Only the closed, short sets
    are listed — naming 28 features would rebuild the dense table this view exists to summarise.
    """
    declared, held = _layers(rows)
    return {
        'empty layers': [layer for layer in declared if layer not in held],
        'unswitchable': [row['slug'] for row in feature_law.findings()],
        'orphan directories': [d for d, _n in orphans(root)],
    }
