# workspace
> Tier 0 workspace-wide invariants: pointers resolve, .gitignore self-heals, imports do not shadow.

Split 2026-08-15 at 8 files. What stayed is what holds for the **whole tree** rather than for one
piece of machinery: every relative link resolves, a new domain subdirectory does not fall out of the
`.gitignore` allowlist, and the suite's `sys.path` cannot silently shadow a module. The two
machineries moved into subdirectories named for the code they cover, so a surface and its coverage
are one word apart: [`gates/`](gates/CONTEXT.md) and [`generators/`](generators/CONTEXT.md), mirroring
`core/hooks/gates/` and `core/hooks/generators/`.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`gates/`](gates/CONTEXT.md) | What a blocking gate must say, and who it must fire for. Mirrors… |
| [`generators/`](generators/CONTEXT.md) | What the generators must produce, and what they must never produce. Mirrors… |

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`test_corpus_ratchet.py`](test_corpus_ratchet.py) | [`test_corpus_ratchet.pyi`](test_corpus_ratchet.pyi) | — | T0 corpus ratchets (core/SCHEMA.md § Placement): the .md corpus may not accumulate more of the three |
| [`test_gitignore_self_heal.py`](test_gitignore_self_heal.py) | [`test_gitignore_self_heal.pyi`](test_gitignore_self_heal.pyi) | — | T0 self-healing .gitignore allowlist check (core/hooks/SPECS.md): a new domain subdir with a |
| [`test_import_paths.py`](test_import_paths.py) | [`test_import_paths.pyi`](test_import_paths.pyi) | — | T0 harness invariant: the suite's sys.path cannot silently shadow a module. |
| [`test_pointer_integrity.py`](test_pointer_integrity.py) | [`test_pointer_integrity.pyi`](test_pointer_integrity.pyi) | `check_pointers` | T0 pointer-integrity check (Tier 0): every relative |
<!-- routing:end -->
