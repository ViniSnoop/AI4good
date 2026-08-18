# entropy
> The Tier 0 checks that count what the tree has drifted into. One question each.

Each module here answers one question about the corpus and hands back findings; nothing here
prints, blocks or renders. Two callers consume them, and the split between those callers is the
design: [`../checks/type-gate.py`](../checks/CONTEXT.md) **blocks**, on what a commit adds, and
[`dashboard/`](dashboard/CONTEXT.md) **reports**, on everything, so a repo that inherited a
violation is visible without being unable to commit.

[`entropy_corpus.py`](entropy_corpus.py) is the odd one and stays: it answers *which files a check
may look at*, which every check needs before it can count anything.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`dashboard/`](dashboard/CONTEXT.md) | The entropy report: running every check over the whole tree, and what the… |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`entropy_context.py`](entropy_context.py) | [`entropy_context.pyi`](entropy_context.pyi) | `check_inventory`, `context_head`, `check_misplaced_answer`, `check_description`, `is_project` | Tier 0 CONTEXT.md rules, parsed from core/SCHEMA.md. Zero-token, deterministic. |
| [`entropy_corpus.py`](entropy_corpus.py) | [`entropy_corpus.pyi`](entropy_corpus.pyi) | `staged_added_files`, `tracked_files`, `nested_repos`, `is_generated_mirror`, `enforcement_paths` | Which files the Tier 0 checks look at, and which of them are allowed to name what the |
| [`entropy_fanout.py`](entropy_fanout.py) | [`entropy_fanout.pyi`](entropy_fanout.pyi) | `fanout_counts`, `fanout_signals` | Directory fanout: how many files one directory asks a reader to hold at once. |
| [`entropy_ledger.py`](entropy_ledger.py) | [`entropy_ledger.pyi`](entropy_ledger.pyi) | `retired_hits`, `item_slugs`, `duplicate_slugs`, `finished_work_hits`, `unanswered_placeholders` | Tier 0 ledger and vocabulary checks, parsed from core/SCHEMA.md. Zero-token, deterministic. |
| [`entropy_naming.py`](entropy_naming.py) | [`entropy_naming.pyi`](entropy_naming.pyi) | `check_shape`, `check_dirs`, `check_placement` | Tier 0 naming and placement, parsed from core/SCHEMA.md. Zero-token, deterministic. |
| [`entropy_stores.py`](entropy_stores.py) | [`entropy_stores.pyi`](entropy_stores.pyi) | `experiment_hits`, `ref_tier_hits` | Tier 0 for the two stores that record what we know and how sure we are: core/experiments/ and |
<!-- routing:end -->
