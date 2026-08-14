# entropy
> The entropy dashboard and the Tier 0 checks it runs over the whole tree.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`entropy-dashboard.py`](entropy-dashboard.py) | [`entropy-dashboard.pyi`](entropy-dashboard.pyi) | `collect`, `size_signals`, `stub_signals`, `main` | The entropy dashboard (ROADMAP.md Frente 4.3). Runs every Tier 0 check over the whole |
| [`entropy_context.py`](entropy_context.py) | [`entropy_context.pyi`](entropy_context.pyi) | `check_inventory`, `is_project`, `check_goal_link` | Tier 0 CONTEXT.md rules (ROADMAP.md Frente 4.1). Zero-token, deterministic. |
| [`entropy_corpus.py`](entropy_corpus.py) | [`entropy_corpus.pyi`](entropy_corpus.pyi) | `tracked_files`, `nested_repos`, `enforcement_paths`, `walk` | Which files the Tier 0 checks look at, and which of them are allowed to name what the |
| [`entropy_fanout.py`](entropy_fanout.py) | [`entropy_fanout.pyi`](entropy_fanout.pyi) | `fanout_counts`, `fanout_signals` | Directory fanout: how many files one directory asks a reader to hold at once. |
| [`entropy_ledger.py`](entropy_ledger.py) | [`entropy_ledger.pyi`](entropy_ledger.pyi) | `retired_hits`, `item_slugs`, `duplicate_slugs`, `goal_vocabulary`, `wiki_link_hits` | Tier 0 ledger and vocabulary checks (ROADMAP.md Frente 4.1). Zero-token, deterministic. |
| [`entropy_naming.py`](entropy_naming.py) | [`entropy_naming.pyi`](entropy_naming.pyi) | `check_shape`, `check_dirs`, `check_placement` | Tier 0 naming and placement (ROADMAP.md Frente 4.1). Zero-token, deterministic. |
| [`entropy_report.py`](entropy_report.py) | [`entropy_report.pyi`](entropy_report.pyi) | `render` | The entropy report: what the dashboard's findings look like on the page. |
<!-- routing:end -->
