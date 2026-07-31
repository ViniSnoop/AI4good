# conftest.py — the one place the suite learns where things are: workspace root, core/tools,
# and the enforcement layer. Also registers the network marker for the video tests.
#
# Every test used to spell out `parents[3]` for the workspace root — nine copies of a depth,
# which is a number that changes the moment a test moves into a subdirectory. Import it from
# here instead; pytest loads this file before any test module.
import sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
WORKSPACE_ROOT = HERE.parents[2]

# Own directory first, so tests in subdirectories can `from conftest import WORKSPACE_ROOT`.
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(WORKSPACE_ROOT / 'core/tools'))

# core/hooks is one flat root (the law) plus one directory per responsibility. Derived by
# scan, never listed: a spelled-out list would go stale the next time a hook is split, and
# the tests would fail for a reason that has nothing to do with the law they assert.
HOOKS = WORKSPACE_ROOT / 'core/hooks'
for _dir in [HOOKS, *sorted(p for p in HOOKS.iterdir()
                            if p.is_dir() and not p.name.startswith(('.', '_')))]:
    sys.path.insert(0, str(_dir))


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "network: hits real network/models; excluded from verify:fast")
