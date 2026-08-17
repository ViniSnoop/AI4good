# T0 the feature registry (core/SPECS.md § AD-14): every capability is declared, answered,
# and honest about whether it can actually be switched off.
#
# WHY THE HONESTY TEST IS THE POINT: the registry exists so an ablation can turn one feature off at
# a time. A row claiming to be wired while nothing reads the switch would make the ablation report
# "no effect" for a feature that was never disabled — the exact silent failure that cost the first
# ablation run its whole signal. So `wired` is checked against the file it names, not trusted.
import os
import re
import subprocess
import sys

import feature_law as law
from conftest import WORKSPACE_ROOT

SETUP = WORKSPACE_ROOT / 'SETUP.md'
DEPS = WORKSPACE_ROOT / 'core' / 'tools' / 'deps.txt'


def _setup_slugs():
    return set(re.findall(r'^> feature: `([a-z0-9-]+)`', SETUP.read_text(), re.M))


def _deps_slugs():
    lines = [ln for ln in DEPS.read_text().splitlines()
             if ln.strip() and not ln.startswith('#')]
    header = lines[0].split('\t')
    return {dict(zip(header, ln.split('\t')))['feature'] for ln in lines[1:]}


def test_every_setup_step_maps_to_a_declared_feature():
    """SETUP.md's slugs are install-shaped, so they join on the `install` column.

    This is half of what keeps three files one vocabulary instead of three. Adding an install step
    with a new slug fails here until the registry says which capability that step installs.
    """
    installs = {r['install'] for r in law.load_registry()} - {'-', ''}
    missing = sorted(_setup_slugs() - installs)
    assert not missing, (
        'SETUP.md declares install steps no registry row claims:\n  ' + '\n  '.join(missing))


def test_every_dependency_feature_is_a_declared_feature():
    """deps.txt's slugs are breakage-shaped: each names a capability, so they join on `slug`."""
    missing = sorted(_deps_slugs() - law.slugs())
    assert not missing, (
        'core/tools/deps.txt names features absent from core/features.txt:\n  ' +
        '\n  '.join(missing))


def test_a_skill_slug_names_the_skill_file():
    """A slug and the file it governs carry the same name (Lucas, 2026-08-17).

    Only the skills group can be checked this way — a hook's slug names a behavior spread over
    several files, not one path. The failure this catches is the one that produced it: the slug
    was `craft-flow`, the file was `loops.md`, and the flow was `craft`, so nothing disagreed
    with anything *adjacent* and the drift stayed legible at every single site.
    """
    skills = WORKSPACE_ROOT / 'core' / 'skills'
    orphans = [r['slug'] for r in law.load_registry() if r['group'] == 'skills'
               and not (skills / f"{r['slug']}.md").exists()
               and not (skills / r['slug']).is_dir()]
    assert not orphans, (
        'these skill slugs name no file in core/skills/:\n  ' + '\n  '.join(orphans))


def test_every_row_is_complete_and_in_its_closed_set():
    for row in law.load_registry():
        assert row['group'] in law.GROUPS, row
        assert row['enforcement'] in law.ENFORCEMENT, row
        assert row['scope'] in law.SCOPES, row
        assert len(row['buys'].split()) >= 8, (
            f"{row['slug']}'s `buys` must say what the feature buys you, not restate its name — "
            'nobody accepts an enforcement layer whose value they cannot see')


def test_every_declared_feature_has_an_answer():
    """A slug added to the registry and never answered would default silently to on."""
    declared, answered = law.slugs(), set(law.load_profile()['toggle'])
    assert declared == answered, (
        f'unanswered: {sorted(declared - answered)}\n'
        f'answered but undeclared: {sorted(answered - declared)}')


SKILL_MIRROR = 'core/tools/wos/skills/mirror.sh'


def _published_skills(off: str = '') -> set:
    """What the skills mirror would publish right now — the group's one observable.

    Sourced rather than imported because the dispatcher is a shell fragment; the caller's
    variables are exactly what `core/tools/wos/sync-skills` supplies.
    """
    script = (f'WORKSPACE={WORKSPACE_ROOT}; SRC=$WORKSPACE/core/skills; '
              f'COMMANDS_DIR=$WORKSPACE/.claude/commands; MIRRORS=(); '
              f'source {WORKSPACE_ROOT / SKILL_MIRROR}; list_skills')
    env = {**os.environ, law.OFF_ENV: off} if off else os.environ
    out = subprocess.run(['bash', '-c', script], capture_output=True, text=True, env=env)
    assert out.returncode == 0, out.stderr
    return set(out.stdout.split())


def test_a_row_claiming_to_be_wired_really_is():
    """The honesty check, and it asks one question: would turning this off change anything?

    It is answered the strongest way each row allows, which is the whole reason a group may share
    a wiring point. Where a group has an invocable seam, the feature is switched off for real and
    the observable must move — a probe a guard on an unreachable branch cannot pass. Where a row
    owns its own call site, the named file must name the slug and consult the law.

    `n/a` rows are skipped rather than failed: they have no in-process switch by ruling, and the
    ablation reaches them by building a clone variant instead (core/SPECS.md § AD-14).
    """
    broken = []
    for row in law.load_registry():
        if not law.is_wired(row):
            continue
        target = row['wired']
        path = WORKSPACE_ROOT / target
        if not path.exists():
            broken.append(f"{row['slug']}: {target} does not exist")
        elif target != SKILL_MIRROR and row['slug'] not in path.read_text(encoding='utf-8'):
            broken.append(f"{row['slug']}: {target} never mentions the slug")
    assert not broken, (
        'these rows claim to be switchable and are not:\n  ' + '\n  '.join(broken))

    group = {r['slug'] for r in law.load_registry() if r['wired'] == SKILL_MIRROR}
    live = _published_skills()
    assert group <= live, (
        f'the mirror does not publish {sorted(group - live)}, so switching them off proves '
        f'nothing — the registry and core/skills/ disagree about what exists')
    for slug in sorted(group):
        assert slug not in _published_skills(off=slug), (
            f'{slug} is still published with {law.OFF_ENV}={slug}: the row names {SKILL_MIRROR} '
            f'but the switch changes nothing there')


def test_an_unknown_slug_fails_open():
    """A gate must never stop enforcing because someone mistyped a row."""
    assert law.is_enabled('no-such-feature-anywhere')


def test_the_ablation_switch_turns_one_feature_off(monkeypatch):
    """WOS_FEATURES_OFF is what the ablation drives; without it there is nothing to measure."""
    slug = 'line-limit'
    assert law.is_enabled(slug)
    monkeypatch.setenv(law.OFF_ENV, f'something-else,{slug}')
    assert not law.is_enabled(slug)
    assert law.is_enabled('caveman'), 'the switch must remove one feature, not all of them'


def test_the_cli_agrees_with_this_file():
    """One parser, not two. If `features` drifts from the registry, the answers stop being real."""
    out = subprocess.run([sys.executable, str(WORKSPACE_ROOT / 'core/tools/wos/features'),
                          '--check'], capture_output=True, text=True, cwd=WORKSPACE_ROOT)
    assert out.returncode == 0, out.stdout + out.stderr


def test_the_wired_gates_actually_consult_the_law():
    """Both seams, end to end: a shell gate and a node hook reach the same law module.

    They are in different languages on purpose — the `--enabled` CLI arm is what lets a third
    harness wire a gate without a second implementation of the registry.
    """
    for row in law.load_registry():
        if not law.is_wired(row):
            continue
        body = (WORKSPACE_ROOT / row['wired']).read_text(encoding='utf-8')
        assert 'feature_law' in body, (
            f"{row['wired']} names {row['slug']} but never asks feature_law whether it is on")
