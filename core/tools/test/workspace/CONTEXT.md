# workspace
> Tier 0 workspace-wide invariants — pointers resolve, routing regenerates, .gitignore self-heals.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`test_gitignore_self_heal.py`](test_gitignore_self_heal.py) | [`test_gitignore_self_heal.pyi`](test_gitignore_self_heal.pyi) | — | T0 self-healing .gitignore allowlist check (Frente 6 item 2): a new domain subdir with a |
| [`test_pointer_integrity.py`](test_pointer_integrity.py) | [`test_pointer_integrity.pyi`](test_pointer_integrity.pyi) | `check_pointers` | T0 pointer-integrity check (Frente 4 Tier 0, subsumes Frente 2): every relative |
| [`test_routing_table.py`](test_routing_table.py) | [`test_routing_table.pyi`](test_routing_table.pyi) | — | The routing table's generated columns (Frente 3.2). Zero-token, runs in verify-fast. |
<!-- routing:end -->
