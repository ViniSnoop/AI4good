# test
> The verify-fast suite: every Tier 0 check plus the tool unit tests. Zero-token, no network.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`law/`](law/CONTEXT.md) | Tier 0: the file law, the type gate, and the four entropy checks that read it. |
| [`video/`](video/CONTEXT.md) | T1 unit tests for the video tool. Fixtures live here; network-marked cases are e |
| [`workspace/`](workspace/CONTEXT.md) | Tier 0 workspace-wide invariants — pointers resolve, routing regenerates, .gitig |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`conftest.py`](conftest.py) | [`conftest.pyi`](conftest.pyi) | `pytest_configure` | conftest.py — the one place the suite learns where things are: workspace root, core/tools, |
<!-- routing:end -->
