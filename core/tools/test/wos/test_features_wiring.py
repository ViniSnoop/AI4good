# T0 the feature registry's honesty half (core/SPECS.md § AD-14): a row claiming a switch must
# really have one, and throwing the switch must move the observable.
#
# WHY THIS IS A FILE OF ITS OWN. test_features.py answers "is the declaration complete and in its
# closed sets" — a question about data. These answer "does the declaration correspond to anything
# that runs" — a question about behaviour, and the one that costs the first ablation run its whole
# signal when it goes unasked. A row claiming to be wired while nothing reads the switch would make
# the ablation report "no effect" for a feature that was never disabled.
import os
import subprocess

import feature_law as law
from conftest import WORKSPACE_ROOT

SKILL_MIRROR = 'core/tools/wos/skills/mirror.sh'
NORMS_GENERATOR = 'core/hooks/routing/norms.py'
TOOL_LAW = 'core/tools/tool_law.py'

# A whole group can share one publisher, and then no row can name itself there: the mirror
# cannot spell fourteen skill slugs and the generator cannot spell ten norm slugs. Those rows
# are held honest by a BEHAVIOURAL probe instead — below for skills, test_norms.py for norms.
# `symmetry` passed the grep by accident, on the word "asymmetry" in a comment, which is the
# whole argument against a grep in one line.
GROUP_PUBLISHERS = {SKILL_MIRROR, NORMS_GENERATOR}


def _published_skills(off: str = '') -> set:
    """What the mirror would publish — the skills group's one observable. Sourced, not imported:
    the dispatcher is a shell fragment, and these are the variables `sync-skills` supplies."""
    script = (f'WORKSPACE={WORKSPACE_ROOT}; SRC=$WORKSPACE/core/skills; '
              f'COMMANDS_DIR=$WORKSPACE/.claude/commands; MIRRORS=(); '
              f'source {WORKSPACE_ROOT / SKILL_MIRROR}; list_skills')
    env = {**os.environ, law.OFF_ENV: off} if off else os.environ
    out = subprocess.run(['bash', '-c', script], capture_output=True, text=True, env=env)
    assert out.returncode == 0, out.stderr
    return set(out.stdout.split())


def test_a_row_claiming_to_be_wired_really_is():
    """The honesty check: would turning this off change anything? Answered the strongest way each
    row allows, which is what lets a group share one wiring point. A group with an invocable seam
    is switched off for real and its observable must move — which a guard on an unreachable branch
    cannot fake. A row owning its call site must name the slug there.

    EVERY path is checked, not the first: a feature spanning layers names one file per layer, and
    `latex` is the case that forced it — a gate that calls a tool it has also switched off would
    read the tool's refusal as a violation and block the commit the switch meant to relax.
    """
    broken = []
    for row in law.load_registry():
        for target in law.wired_paths(row):
            path = WORKSPACE_ROOT / target
            if not path.exists():
                broken.append(f"{row['slug']}: {target} does not exist")
            elif target not in GROUP_PUBLISHERS and row['slug'] not in path.read_text(encoding='utf-8'):
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


def test_the_wired_gates_actually_consult_the_law():
    """Both seams, end to end: a shell gate and a node hook reach the same law module.

    They are in different languages on purpose — the `--enabled` CLI arm is what lets a third
    harness wire a gate without a second implementation of the registry. A `core/tools`
    tool reaches the law through `tool_law`, which carries the sys.path hop; that hop is
    asserted itself, or the indirection becomes a place for the chain to go quietly dead.
    """
    assert 'feature_law' in (WORKSPACE_ROOT / TOOL_LAW).read_text(encoding='utf-8'), (
        f'{TOOL_LAW} is the tools-layer hop and must reach feature_law itself')
    for row in law.load_registry():
        for target in law.wired_paths(row):
            body = (WORKSPACE_ROOT / target).read_text(encoding='utf-8')
            assert 'feature_law' in body or 'tool_law' in body, (
                f"{target} names {row['slug']} but never asks feature_law whether it is on")


def test_a_switched_off_tool_refuses_to_run():
    """A tool stops at invocation, with its own exit code.

    AD-14 files skills and tools together as the rows with nowhere to put a call. True of
    a skill — markdown, switched off only by the mirror declining to publish it. A tool is
    a CLI this workspace owns, so it has a moment of its own, and this probe answers per row
    where a shared publisher answers once for the group. `OFF_EXIT` is asserted rather than
    "non-zero": every tool exits 1 on a real failure, so any-non-zero would pass on a broken one.
    """
    import tool_law
    probed = []
    for row in law.load_registry():
        for target in law.wired_paths(row):
            # Scoped by wiring point, not by group. `rtk-compaction` is wired to a hook, whose
            # observable is what it rewrites; the skills mirror is a sourced fragment probed
            # above. AD-14 exactly — the wiring point decides how a row is probed.
            if target == SKILL_MIRROR or not target.startswith('core/tools/'):
                continue
            out = subprocess.run([str(WORKSPACE_ROOT / target)], capture_output=True, text=True,
                                 cwd=WORKSPACE_ROOT,
                                 env={**os.environ, law.OFF_ENV: row['slug']})
            assert out.returncode == tool_law.OFF_EXIT, (
                f"{row['slug']}: exits {out.returncode} under {law.OFF_ENV}, so the switch does "
                f"not stop {target}")
            assert row['slug'] in out.stderr, f'{row["slug"]} stops without naming itself'
            probed.append(row['slug'])
    assert probed, 'no tool is wired to an entrypoint yet — this probe proves nothing'
