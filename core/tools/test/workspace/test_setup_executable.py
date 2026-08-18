# T0 the install is a procedure, not prose (core/SCHEMA.md § The .md type system): every SETUP.md
# step declares its feature and carries a precondition, an install and a verify probe.
#
# The harness is the installer — a newcomer's own agent reads SETUP.md and executes it. That only
# works if every step says how to tell it is already done and how to prove it worked. This file is
# what stops the next added step from being a paragraph.
import re

from conftest import WORKSPACE_ROOT

SETUP = WORKSPACE_ROOT / 'SETUP.md'
INSTALL_SKILL = WORKSPACE_ROOT / 'core/skills/install.md'


def _steps():
    """The `##` sections between the steps markers. Prose outside them is not a step."""
    body = SETUP.read_text().split('<!-- steps:start -->')[1].split('<!-- steps:end -->')[0]
    chunks = re.split(r'^## ', body, flags=re.M)[1:]
    return [(c.splitlines()[0].strip(), c) for c in chunks]


def test_the_steps_region_exists():
    assert '<!-- steps:start -->' in SETUP.read_text(), (
        'SETUP.md lost its steps markers; every check below reads them')
    assert _steps(), 'no steps found between the markers'


def test_every_step_declares_its_feature():
    """The join to the feature registry: skip a step, lose exactly the feature it names.

    `> substrate: yes` is the one alternative, and it is a ruling rather than an escape hatch
    (2026-08-17): the venv and the absolute shebang install what every feature RUNS ON, so
    they have no registry row to join to — switching off the interpreter the switch itself
    executes on cannot produce an ablation signal. Anything else must name its feature.
    """
    for name, body in _steps():
        marker = re.search(r'^> (?:feature: `[a-z0-9-]+`|substrate: yes) · agent: (yes|no)$',
                           body, flags=re.M)
        assert marker, (
            f'step "{name}" has no `> feature: ... · agent: yes|no` line '
            f'(or `> substrate: yes` if it installs no feature)')


def test_an_agent_runnable_step_has_all_three_parts():
    for name, body in _steps():
        if '· agent: yes' not in body:
            continue
        for part in ('**Precondition**', '**Install**', '**Verify**'):
            assert part in body, f'step "{name}" is agent-runnable but has no {part}'


def test_a_step_an_agent_cannot_finish_says_what_to_ask_for():
    """`agent: no` is a handover, not a dead end. It must name the thing only Lucas can supply."""
    for name, body in _steps():
        if '· agent: no' not in body:
            continue
        assert '**Needs Lucas:**' in body, (
            f'step "{name}" is marked agent: no but never says what to ask for')


def test_every_step_can_be_probed():
    """A Verify with no command is a claim. Each step's parts must carry a runnable block."""
    for name, body in _steps():
        assert '```' in body, f'step "{name}" contains no command block'


def test_the_install_skill_is_a_door_not_a_copy():
    """The file is the procedure; the skill only opens it.

    A stranger on opencode or copilot has no skill loaded — that is the population this is for — so
    SETUP.md must stand alone. The failure this guards is the skill slowly re-inlining the commands
    until there are two procedures that drift apart.
    """
    setup_blocks = re.findall(r'```(?:bash|powershell)\n(.*?)```', SETUP.read_text(), re.S)
    setup_lines = {ln.strip() for b in setup_blocks for ln in b.splitlines()
                   if ln.strip() and not ln.strip().startswith('#')}
    skill_blocks = re.findall(r'```(?:bash|powershell)\n(.*?)```', INSTALL_SKILL.read_text(), re.S)
    skill_lines = {ln.strip() for b in skill_blocks for ln in b.splitlines()
                   if ln.strip() and not ln.strip().startswith('#')}
    copied = setup_lines & skill_lines
    assert not copied, (
        'core/skills/install.md copies commands out of SETUP.md — the skill is a doorway, and a '
        'second copy is what core/SCHEMA.md calls a bug:\n  ' + '\n  '.join(sorted(copied)))


def test_the_skill_sends_the_agent_to_the_file():
    assert 'SETUP.md' in INSTALL_SKILL.read_text(), (
        'the /install skill never names the procedure it is a door to')
