# routing
> The CONTEXT.md routing-table generator.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`context_synchronizer.py`](context_synchronizer.py) | [`context_synchronizer.pyi`](context_synchronizer.pyi) | `migrate_legacy`, `sync` | Sync the Routing block in CONTEXT.md (or AGENTS.md at workspace root). |
| [`workspace_meta.py`](workspace_meta.py) | [`workspace_meta.pyi`](workspace_meta.pyi) | `file_description`, `python_api`, `js_api`, `extract_api`, `interface_for` | Workspace metadata extraction: file descriptions, public APIs, and interface links. |
| [`workspace_scanner.py`](workspace_scanner.py) | [`workspace_scanner.pyi`](workspace_scanner.pyi) | `code_files`, `has_code_content`, `subdir_scan`, `parse_preserved_files`, `parse_preserved_subs` | Workspace scanner: directory discovery and CONTEXT.md routing-table assembly. |
<!-- routing:end -->
