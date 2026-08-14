# T0 context meter (Frente 9.1): the session-size signal that decides when to hand off.
# Zero-token, runs in verify-fast.
#
# Two things are worth guarding here. The thresholds must come from limits.env, so the
# numbers can be re-tuned without touching the checker — the same rule that already binds
# every other checker to its law file. And the meter must announce each threshold exactly
# once: a warning that repeats every turn is one Lucas learns to skip, which costs the
# tokens without buying the decision.
import importlib.util
import json

from conftest import WORKSPACE_ROOT

spec = importlib.util.spec_from_file_location(
    'context_meter', WORKSPACE_ROOT / 'core/hooks/session/context-meter.py')
context_meter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context_meter)

LIMITS = WORKSPACE_ROOT / 'core/hooks/limits.env'


def _turn(ctx, sidechain=False, role='assistant'):
    return json.dumps({
        'type': role,
        'isSidechain': sidechain,
        'message': {'usage': {
            'input_tokens': 2,
            'cache_read_input_tokens': ctx - 2,
            'cache_creation_input_tokens': 0,
        }},
    })


def _transcript(tmp_path, lines):
    path = tmp_path / 'session.jsonl'
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return str(path)


def test_thresholds_come_from_limits_env():
    """The meter reads the numbers; it must not carry a copy of them."""
    limits = context_meter.load_limits()
    assert limits['CTX_WARN'] < limits['CTX_LOUD']
    source = (WORKSPACE_ROOT / 'core/hooks/session/context-meter.py').read_text()
    for value in (limits['CTX_WARN'], limits['CTX_LOUD']):
        assert str(value) not in source, (
            f'{value} is hardcoded in context-meter.py — it belongs only in limits.env')


def test_declared_in_limits_env():
    text = LIMITS.read_text(encoding='utf-8')
    assert 'CTX_WARN=' in text and 'CTX_LOUD=' in text


def test_reads_the_most_recent_turn(tmp_path):
    path = _transcript(tmp_path, [_turn(40_000), _turn(310_000)])
    assert context_meter.last_context(path) == 310_000


def test_subagent_turns_are_not_the_session(tmp_path):
    """A sidechain turn carries its own small context — it is not what the session holds."""
    path = _transcript(tmp_path, [_turn(310_000), _turn(9_000, sidechain=True)])
    assert context_meter.last_context(path) == 310_000


def test_missing_or_unreadable_transcript_is_silent(tmp_path):
    assert context_meter.last_context(str(tmp_path / 'absent.jsonl')) == 0
    garbage = tmp_path / 'garbage.jsonl'
    garbage.write_text('not json at all\n{"usage": broken\n', encoding='utf-8')
    assert context_meter.last_context(str(garbage)) == 0


def test_each_threshold_announces_once(tmp_path, monkeypatch):
    state = tmp_path / 'state.txt'
    monkeypatch.setattr(context_meter, 'state_file', lambda _sid: str(state))
    limits = context_meter.load_limits()
    warn, loud = limits['CTX_WARN'], limits['CTX_LOUD']

    assert context_meter.announced('s') == 0
    context_meter.mark('s', warn)
    assert context_meter.announced('s') == warn
    # Still inside the warn band on a later turn — already said, stay quiet.
    assert warn <= context_meter.announced('s')
    # Crossing the louder mark is new information, so it speaks again.
    assert loud > context_meter.announced('s')


def test_the_loud_message_names_the_way_out(tmp_path):
    limits = context_meter.load_limits()
    text = context_meter.message(300_000, limits['CTX_LOUD'], limits['CTX_LOUD'])
    assert '/roundup' in text and '300k' in text
    # Prepare, don't spawn: the way out is an artifact plus one line Lucas types.
    assert '/handoff' in text
    assert context_meter.HANDOFF_ARTIFACT in text


def test_the_warn_message_does_not_demand_action(tmp_path):
    """The first nudge exists to be ignorable — see brain/SPECS.md § Rationale."""
    limits = context_meter.load_limits()
    text = context_meter.message(160_000, limits['CTX_WARN'], limits['CTX_LOUD'])
    assert '160k' in text
    assert '/roundup' not in text
    assert '/handoff' not in text


def test_meter_and_skill_name_the_same_artifact():
    """The meter only names the path; /handoff writes it. Drift breaks the hand-off silently."""
    skill = (WORKSPACE_ROOT / 'core/skills/handoff.md').read_text(encoding='utf-8')
    assert context_meter.HANDOFF_ARTIFACT in skill, (
        f'context-meter.py points at {context_meter.HANDOFF_ARTIFACT}, '
        f'but core/skills/handoff.md never writes it')


def test_the_handoff_artifact_is_not_an_uppercase_type():
    """core/SCHEMA.md § types is a closed allowlist; a resume prompt is an instance."""
    name = context_meter.HANDOFF_ARTIFACT.rsplit('/', 1)[-1]
    assert name == name.lower(), f'{name} reads as a type — types are allowlisted in SCHEMA.md'


def test_the_meter_never_spawns_a_session():
    """Decided 2026-08-13 (Frente 9.1): a successor cannot take the terminal, so none is spawned."""
    source = (WORKSPACE_ROOT / 'core/hooks/session/context-meter.py').read_text(encoding='utf-8')
    for forbidden in ('--bg', 'subprocess', 'claude -p', 'os.system'):
        assert forbidden not in source, f'{forbidden} in a hook that must only ever print'
