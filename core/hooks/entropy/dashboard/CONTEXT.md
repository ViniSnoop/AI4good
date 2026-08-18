# dashboard
> The entropy report: running every check over the whole tree, and what the findings look like.

Split from [`../`](../CONTEXT.md) 2026-08-18, when an eighth check pushed that directory past the
fanout signal. The seam was already the parent's own one-line description — *the dashboard **and**
the checks it runs* — so the split cost no new idea, only the hop.

**The checks stay next door and this directory owns nobody's rule.** Every module in
[`../`](../CONTEXT.md) answers one question about the tree; these two ask all of them and render the
answer. A check that moved in here would become invisible to the commit gate, which imports the
checks directly and never touches the dashboard.

Run it with `make entropy`; the report is [`entropy.md`](../../../../entropy.md) at the workspace
root. It is a **report, never a gate** — nothing here exits non-zero on a finding, and the ratchet
that keeps the counts falling lives in `core/tools/test/workspace/test_corpus_ratchet.py`.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`entropy-dashboard.py`](entropy-dashboard.py) | [`entropy-dashboard.pyi`](entropy-dashboard.pyi) | `collect`, `size_signals`, `stub_signals`, `main` | The entropy dashboard. Runs every Tier 0 check over the whole |
| [`entropy_report.py`](entropy_report.py) | [`entropy_report.pyi`](entropy_report.pyi) | `render` | The entropy report: what the dashboard's findings look like on the page. |
<!-- routing:end -->
