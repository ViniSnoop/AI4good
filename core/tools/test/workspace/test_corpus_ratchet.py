# T0 corpus ratchets (Frente 13): the .md corpus may not accumulate more of the two
# defects no link-checker can see. Zero-token, runs in verify-fast.
#
# These sit here rather than beside the checks they call because they assert something
# about the WHOLE TREE, not about one piece of machinery: test_entropy_ledger.py and
# test_entropy_context.py own whether each check fires correctly, this owns whether the
# backlog is shrinking. Same split as test_pointer_integrity.py beside it.
#
# Both ceilings only ever go down. Each is paired with a staleness test, because a ratchet
# nobody lowers is just a baseline, and a baseline is where drift hides.
import entropy_context
import entropy_ledger
from conftest import WORKSPACE_ROOT
from file_law import load_limits

HEAD_WARN = load_limits()['CONTEXT_HEAD_WARN']

# Inherited backlog, drained by ROADMAP.md Frente 13.
FINISHED_CEILING = 105
MISPLACED_CEILING = 28

# The margin lets one cut land without forcing a test edit; a real drain pass trips it.
FINISHED_SLACK = 10
MISPLACED_SLACK = 5


def _files() -> list:
    return entropy_ledger.tracked_files(WORKSPACE_ROOT, nested=True)


def _finished() -> int:
    return len(entropy_ledger.finished_work_hits(
        _files(), entropy_ledger.enforcement_paths(WORKSPACE_ROOT)))


def _misplaced() -> int:
    return sum(1 for path in _files()
               if entropy_context.check_misplaced_answer(path, HEAD_WARN))


def test_prose_describing_finished_work_does_not_grow():
    live = _finished()
    assert live <= FINISHED_CEILING, (
        f'{live} corpses, up from {FINISHED_CEILING}. Cut the prose describing work that '
        f'landed, or rewrite it as present-tense state — entropy.md § Prose describing '
        f'finished work')


def test_constraints_in_context_heads_do_not_grow():
    live = _misplaced()
    assert live <= MISPLACED_CEILING, (
        f'{live} constrained heads, up from {MISPLACED_CEILING}. CONTEXT.md is the only '
        f'enforced-read type — move the contract to a sibling SPECS.md and leave one '
        f'pointer (core/SCHEMA.md § Placement)')


def test_the_ceilings_are_not_stale():
    finished, misplaced = _finished(), _misplaced()
    assert FINISHED_CEILING - finished <= FINISHED_SLACK, (
        f'finished-work is down to {finished} — lower FINISHED_CEILING to match, so the '
        f'ratchet keeps holding the new ground')
    assert MISPLACED_CEILING - misplaced <= MISPLACED_SLACK, (
        f'misplaced is down to {misplaced} — lower MISPLACED_CEILING to match')
