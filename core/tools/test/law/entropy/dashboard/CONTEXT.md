# dashboard
> The two checks that are about the REPORT rather than about the tree: who owns a finding, and what
> the count was last time.

Split from [`../`](../CONTEXT.md) 2026-08-25, when the parent passed the hard file cap. The seam is
the one [`core/hooks/entropy/dashboard/`](../../../../../hooks/entropy/dashboard/CONTEXT.md) already
uses next door: every check in `core/hooks/entropy/` answers one question about the tree, and these
two modules ask all of them and render the answer. A test of the rendering belongs with the
rendering.

Each one recomputes the number it checks rather than reading what was written: the root's total is
re-added from every local ledger pulled back off disk, and the trend's baseline comes from git. That
is what makes them worth running — a count any repo could write into is the copied-count drift
these checks exist to catch.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`test_entropy_scatter.py`](test_entropy_scatter.py) | [`test_entropy_scatter.pyi`](test_entropy_scatter.pyi) | — | T0 the entropy scatter (ruled 2026-08-25): every nested repo keeps its own ledger and the root sums them. Zero-token, runs in verify-fast. |
| [`test_entropy_trend.py`](test_entropy_trend.py) | [`test_entropy_trend.pyi`](test_entropy_trend.pyi) | `git`, `commit`, `repo` | T0 the entropy trend (core/hooks/entropy/dashboard/entropy_trend.py): a bare count let every session write "flat" while the real number climbed, so the header carries a baseline instead. Zero-token, runs in verify-fast. |
<!-- routing:end -->
