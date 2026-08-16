# test
> The verify-fast suite: every Tier 0 check plus the tool unit tests. Zero-token, no network.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`law/`](law/CONTEXT.md) | Tier 0: what a file is, what a name may be, and how big a session may get. |
| [`video/`](video/CONTEXT.md) | T1 unit tests for the video tool. Fixtures live here; network-marked cases are… |
| [`workspace/`](workspace/CONTEXT.md) | Tier 0 workspace-wide invariants: pointers resolve, .gitignore self-heals… |
| [`wos/`](wos/CONTEXT.md) | Guards on the session-close ritual: the roundup tool's git behavior and the two… |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`conftest.py`](conftest.py) | [`conftest.pyi`](conftest.pyi) | `pytest_configure` | conftest.py — the one place the suite learns where things are: workspace root, core/tools, |
| [`test_gauth.py`](test_gauth.py) | [`test_gauth.pyi`](test_gauth.pyi) | `accounts`, `boom` | T1 auth recovery: a dead Google token must hand Lucas a runnable fix, not a traceback. |
| [`test_notion.py`](test_notion.py) | [`test_notion.pyi`](test_notion.pyi) | `block`, `fake_paged` | T1 notion: an id survives any form it is pasted in, and a failure hands back a runnable fix. |
| [`test_slides.py`](test_slides.py) | [`test_slides.pyi`](test_slides.pyi) | — | T1 slides: the geometry a deck reports must be the geometry the write path accepts. |
<!-- routing:end -->
