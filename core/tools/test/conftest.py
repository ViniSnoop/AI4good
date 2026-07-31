# conftest.py — put core/tools and the enforcement layer on sys.path, and register the
# network marker for video tests.
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

# core/hooks is one flat root (the law) plus one directory per responsibility. Derived by
# scan, never listed: a spelled-out list would go stale the next time a hook is split, and
# the tests would fail for a reason that has nothing to do with the law they assert.
HOOKS = pathlib.Path(__file__).resolve().parents[3] / 'core/hooks'
for _dir in [HOOKS, *sorted(p for p in HOOKS.iterdir()
                            if p.is_dir() and not p.name.startswith(('.', '_')))]:
    sys.path.insert(0, str(_dir))


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "network: hits real network/models; excluded from verify:fast")
