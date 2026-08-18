# routing
> The CONTEXT.md routing-table generator.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`context_synchronizer.py`](context_synchronizer.py) | [`context_synchronizer.pyi`](context_synchronizer.pyi) | `migrate_legacy`, `sync` | Sync the Routing block in CONTEXT.md (or AGENTS.md at workspace root). |
| [`hoist.py`](hoist.py) | [`hoist.pyi`](hoist.pyi) | `md_blurb`, `rebase_links`, `truncate_outside_links`, `hoist` | Text written for one file, made safe to show inside another file's table. |
| [`norms.py`](norms.py) | [`norms.pyi`](norms.pyi) | `body`, `published`, `block`, `sync` | Publish core/norms/*.md into AGENTS.md's rule block, in the registry's order. |
| [`workspace_meta.py`](workspace_meta.py) | [`workspace_meta.pyi`](workspace_meta.pyi) | `file_description`, `python_api`, `js_api`, `extract_api`, `interface_for` | Workspace metadata extraction: file descriptions, public APIs, and interface links. |
| [`workspace_scanner.py`](workspace_scanner.py) | [`workspace_scanner.pyi`](workspace_scanner.pyi) | `is_scanned`, `code_files`, `has_code_content`, `subdir_scan`, `parse_preserved_files` | Workspace scanner: directory discovery and CONTEXT.md routing-table assembly. |
<!-- routing:end -->
