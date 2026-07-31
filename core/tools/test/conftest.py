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

# core/hooks and core/tools are each one root plus one directory per responsibility. Both
# are derived by scan, never listed: a spelled-out list would go stale the next time either
# is split, and the tests would fail for a reason that has nothing to do with what they
# assert. That is exactly what happened when core/tools/test itself was split.
HOOKS = WORKSPACE_ROOT / 'core/hooks'
TOOLS = WORKSPACE_ROOT / 'core/tools'


def _tree(root):
    """The root, then every directory under it that holds importable modules."""
    yield root
    for child in sorted(root.rglob('*')):
        if child.is_dir() and not any(part.startswith(('.', '_')) for part in
                                      child.relative_to(root).parts):
            yield child


for _dir in [*_tree(HOOKS), *_tree(TOOLS)]:
    sys.path.insert(0, str(_dir))


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "network: hits real network/models; excluded from verify:fast")
