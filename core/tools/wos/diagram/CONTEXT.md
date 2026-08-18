# diagram
> The workspace drawn from its own declarations: one generated HTML picture, zero tokens, no model.

`architecture` writes [`ARCHITECTURE.html`](../../../../ARCHITECTURE.html) at the workspace root —
three views of the same workspace, from three sources that already exist:

| View | Renders | Read from |
|------|---------|-----------|
| enforcement | every feature against every site that enforces it | [`core/features.txt`](../../../features.txt) |
| routing | the chain an agent walks, three levels deep | the generated routing blocks |
| mass | tracked bytes per directory | `git ls-files` |

**A hand-drawn map is the rot the routing tables exist to prevent**, so nothing here is drawn by
hand and no model runs at render time. The picture can be no more wrong than its sources: a wrong
edge means a wrong routing table, and fixing the drawing means fixing the source. The one thing it
cannot read is *when a hook fires* — no machine-readable trigger registry exists yet, so those are
derived from directory convention and labelled `inferred` in the page.

Total and fail-loud: every run prints `parsed N of M routing blocks`, and a block it cannot slice
is named rather than skipped — a picture that quietly drops a subtree is worse than no picture.

```
core/tools/wos/diagram/architecture              # regenerate ARCHITECTURE.html
core/tools/wos/diagram/architecture --check      # exit 1 if the committed file is stale
core/tools/wos/diagram/architecture --out /tmp/x.html
```

`/roundup` regenerates and commits it at every session close, which is what keeps a stale picture a
bug in the close rather than a fact of life. Output determinism is load-bearing for that: no
timestamp, no commit sha, so the file changes only when the workspace did.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`views/`](views/CONTEXT.md) | One drawing per file. A view renders data it is handed and computes nothing… |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`architecture`](architecture) | — | — | draw the workspace as it is (enforcement matrix, routing spine, folder mass) into one self-contained ARCHITECTURE.html; --check exits 1 when the committed file is stale |
| [`diagram_data.py`](diagram_data.py) | [`diagram_data.pyi`](diagram_data.pyi) | `area_of`, `trigger_of`, `lifecycle`, `features`, `matrix` | The canonical data behind ARCHITECTURE.html: what the workspace declares, what contains what, |
| [`diagram_health.py`](diagram_health.py) | [`diagram_health.pyi`](diagram_health.pyi) | `harness_owned`, `orphans`, `by_layer`, `findings`, `detail` | What the workspace's declarations say about its HEALTH, as opposed to its contents. |
| [`diagram_page.py`](diagram_page.py) | [`diagram_page.pyi`](diagram_page.pyi) | `render` | The page the three drawings live in: one self-contained HTML file, no script, no asset it does |
<!-- routing:end -->
