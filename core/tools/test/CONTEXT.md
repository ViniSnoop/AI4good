# test
> The verify-fast suite: every Tier 0 check plus the tool unit tests. Zero-token, no network.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`conftest.py`](conftest.py) | [`conftest.pyi`](conftest.pyi) | `pytest_configure` | conftest.py — put core/tools on sys.path and register the network marker for video tests |
| [`test_entropy_context.py`](test_entropy_context.py) | [`test_entropy_context.pyi`](test_entropy_context.pyi) | — | T0 CONTEXT.md rules (Frente 4.1 Tier 0). Zero-token, runs in verify-fast. |
| [`test_entropy_fanout.py`](test_entropy_fanout.py) | [`test_entropy_fanout.pyi`](test_entropy_fanout.pyi) | — | T0 directory fanout (Frente 4.1 Tier 0). Zero-token, runs in verify-fast. |
| [`test_entropy_ledger.py`](test_entropy_ledger.py) | [`test_entropy_ledger.pyi`](test_entropy_ledger.pyi) | — | T0 ledger and vocabulary checks (Frente 4.1 Tier 0). Zero-token, runs in verify-fast. |
| [`test_entropy_naming.py`](test_entropy_naming.py) | [`test_entropy_naming.pyi`](test_entropy_naming.pyi) | — | T0 naming and placement (Frente 4.1 Tier 0). Zero-token, runs in verify-fast. |
| [`test_gitignore_self_heal.py`](test_gitignore_self_heal.py) | [`test_gitignore_self_heal.pyi`](test_gitignore_self_heal.pyi) | — | T0 self-healing .gitignore allowlist check (Frente 6 item 2): a new domain subdir with a |
| [`test_pointer_integrity.py`](test_pointer_integrity.py) | [`test_pointer_integrity.pyi`](test_pointer_integrity.pyi) | `check_pointers` | T0 pointer-integrity check (Frente 4 Tier 0, subsumes Frente 2): every relative |
| [`test_routing_table.py`](test_routing_table.py) | [`test_routing_table.pyi`](test_routing_table.pyi) | — | The routing table's generated columns (Frente 3.2). Zero-token, runs in verify-fast. |
| [`test_type_gate.py`](test_type_gate.py) | [`test_type_gate.pyi`](test_type_gate.pyi) | — | T0 type gate (Frente 4.1 Tier 0): the uppercase allowlist and the CONTEXT.md |
| [`test_video_core.py`](test_video_core.py) | [`test_video_core.pyi`](test_video_core.pyi) | `FakeProc`, `FakeMedia`, `download_audio`, `transcribe`, `download_video` | test_video_core.py — T0/T1 unit tests for video_core (no network; fixtures + injected runners) |
| [`test_video_images.py`](test_video_images.py) | [`test_video_images.pyi`](test_video_images.pyi) | `FakeProc`, `FakeMedia`, `FakeImages`, `ocr_image`, `caption_image` | test_video_images.py — T1 unit tests for the image-post path (no network, injected runners) |
<!-- routing:end -->
