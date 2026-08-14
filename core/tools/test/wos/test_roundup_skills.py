# T0 the session-close skills (Frente 9.2): what bash cannot assert about the other layer.
# Zero-token, no network.
#
# The split only holds if the skill keeps *not* doing the script's work. Prose has no compiler, so
# a later session re-inlining `make entropy` or the merges — the exact shape this frente deleted —
# would pass every other check in the suite. These guard the seam and the hand-off's agreed shape.
import re

from conftest import WORKSPACE_ROOT

ROUNDUP_SKILL = (WORKSPACE_ROOT / 'core/skills/roundup.md').read_text(encoding='utf-8')
HANDOFF_SKILL = (WORKSPACE_ROOT / 'core/skills/handoff.md').read_text(encoding='utf-8')


def _blocks(text):
    return re.findall(r'```(?:bash|sh)?\n(.*?)```', text, re.S)


def _phase_naming(text, needle):
    """The number of the `## Phase N` heading whose body first mentions `needle`."""
    phase = None
    for line in text.splitlines():
        heading = re.match(r'##\s*Phase\s*(\d+)', line)
        if heading:
            phase = heading.group(1)
        elif phase and needle in line:
            return phase
    return None


def test_the_skill_does_not_reinline_the_script():
    """Frente 9.2's whole point: these ran as prose at the session's most expensive turns."""
    for block in _blocks(ROUNDUP_SKILL):
        for inlined in ('make entropy', 'git merge', 'git push', 'verify-fast'):
            assert inlined not in block, (
                f'{inlined!r} is back in core/skills/roundup.md — it belongs to '
                'core/tools/wos/roundup, which the skill calls once')


def test_the_skill_calls_the_tool_by_path():
    assert 'core/tools/wos/roundup' in ROUNDUP_SKILL


def test_a_skipped_handoff_deletes_the_artifact():
    """Decided 2026-08-13: the file's existence means a thread is open. A stale block left in
    place would let the next window resume a thread that closed sessions ago."""
    assert re.search(r'rm -f\s+outputs/handoff\.md', HANDOFF_SKILL), (
        'core/skills/handoff.md must name the deletion — skipping is what makes the path a signal')


def test_the_handoff_may_decline_to_write_one():
    assert 'do not emit a resume prompt' in HANDOFF_SKILL
    assert 'manufactures' in HANDOFF_SKILL, 'keep the reason: a resume prompt invents a next action'


def test_the_roundup_skill_does_not_promise_a_handoff_that_may_not_exist():
    """Phase 5 closes by telling the next session to read the artifact. That instruction is wrong
    whenever /handoff declined to write it."""
    tail = ROUNDUP_SKILL.split('## Phase 5')[-1]
    assert 'skipped' in tail, 'Phase 5 still assumes a hand-off was always written'


def _template():
    for block in _blocks(HANDOFF_SKILL):
        if '## Resume' in block:
            return block
    raise AssertionError('core/skills/handoff.md no longer carries a resume template')


def test_the_template_has_no_placeholder_to_fill():
    """`Open threads` is omitted, not answered with a "none." placeholder — the output rule
    applied to a section. A placeholder is a shape the model fills rather than a fact it
    reports. Scoped to the template: the prose above it may quote what it forbids."""
    template = _template()
    assert '"none."' not in template
    assert 'Omit the whole section' in template


def test_the_state_block_is_the_tools_three_lines():
    """Re-deriving them costs a second round of git at the most expensive turn, and lets the two
    disagree — last session's block and the script's output already differed."""
    state = _template().split('### State')[-1]
    for line in ('verify:', 'entropy:', 'sync:'):
        assert line in state, f'{line} missing from the State block'
    assert 'verbatim' in state


def test_the_template_caps_what_it_repeats():
    """Last session's hand-off ran 48 lines, and 3 of its 5 open threads were already written in
    ROADMAP.md. The caps are the fix; losing them is how it grows back."""
    assert '≤3 bullets' in HANDOFF_SKILL
    assert re.search(r'≤2 files', HANDOFF_SKILL)
    assert 'no ledger already holds' in HANDOFF_SKILL


def test_both_skills_agree_on_which_phase_promotes():
    """/handoff points at the phase that promotes instead of merging itself. The pointer went
    stale once already when the skill collapsed six phases into three."""
    promoting = _phase_naming(ROUNDUP_SKILL, 'core/tools/wos/roundup')
    assert promoting, 'no phase of core/skills/roundup.md calls the tool'
    cited = re.search(r'/roundup`?\s*Phase\s*(\d+)', HANDOFF_SKILL)
    assert cited, 'core/skills/handoff.md no longer points anywhere for promotion'
    assert cited.group(1) == promoting, (
        f'handoff.md sends promotion to Phase {cited.group(1)}; the tool runs in Phase {promoting}')


def test_the_dirty_flag_is_documented_where_it_is_decided():
    """--leave-dirty answers a question only the agent can answer, so the script's own stop names
    it at the moment it applies. The skill must not pre-load it as a routine step."""
    for block in _blocks(ROUNDUP_SKILL):
        assert '--leave-dirty' not in block, (
            'the skill must not run --leave-dirty by default — the stop offers it when it applies')
