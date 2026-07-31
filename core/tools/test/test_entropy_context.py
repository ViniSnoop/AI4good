# T0 CONTEXT.md rules (Frente 4.1 Tier 0). Zero-token, runs in verify-fast.
#
# The goal-link check was written AFTER the backfill, not before: all 14 projects already
# declared line 3, so the check could go straight to blocking instead of warning. That
# order is the point — a check introduced against a red tree teaches people to ignore it.
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE_ROOT / 'core/hooks'))

import entropy_context  # noqa: E402


def test_every_project_declares_its_goal():
    failures = [f for path in sorted((WORKSPACE_ROOT / 'code').glob('*/CONTEXT.md'))
                if (f := entropy_context.check_goal_link(path))]
    assert failures == [], '\n'.join(failures)


def _project(tmp_path, line3):
    project = tmp_path / 'code' / 'thing'
    (project / '../../brain/goals').resolve().mkdir(parents=True, exist_ok=True)
    project.mkdir(parents=True)
    target = project / 'CONTEXT.md'
    target.write_text(f'# thing\n> what it is\n{line3}\n', encoding='utf-8')
    return target


def test_a_declared_goal_passes(tmp_path):
    (tmp_path / 'brain/goals').mkdir(parents=True)
    (tmp_path / 'brain/goals/real.md').write_text('# g\n', encoding='utf-8')
    target = _project(tmp_path, '> goal: [real](../../brain/goals/real.md)')
    assert entropy_context.check_goal_link(target) is None


def test_a_deliberate_none_passes(tmp_path):
    assert entropy_context.check_goal_link(_project(tmp_path, '> goal: none')) is None


def test_a_missing_declaration_is_flagged(tmp_path):
    failure = entropy_context.check_goal_link(_project(tmp_path, 'some prose instead'))
    assert failure is not None and 'line 3 must declare' in failure


def test_a_dead_goal_link_is_flagged(tmp_path):
    """Worse than `none`, because it reads as an answer."""
    target = _project(tmp_path, '> goal: [gone](../../brain/goals/gone.md)')
    failure = entropy_context.check_goal_link(target)
    assert failure is not None and 'does not exist' in failure


def test_scaffolding_is_not_a_project(tmp_path):
    templates = tmp_path / 'code' / '_templates'
    templates.mkdir(parents=True)
    target = templates / 'CONTEXT.md'
    target.write_text('# t\n> templates\nno goal line\n', encoding='utf-8')
    assert entropy_context.check_goal_link(target) is None


def test_a_non_project_context_is_not_asked(tmp_path):
    other = tmp_path / 'brain' / 'goals'
    other.mkdir(parents=True)
    target = other / 'CONTEXT.md'
    target.write_text('# goals\n> one file per goal\n', encoding='utf-8')
    assert entropy_context.check_goal_link(target) is None
