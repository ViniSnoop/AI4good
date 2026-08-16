# generators
> What the generators must produce, and what they must never produce. Mirrors `core/hooks/generators/`.

A generator writes an artifact and stages it, so its failures are **silent by construction** — it
exits 0 having written nothing, or having written the right thing in the wrong place. That is why
these tests ask *"what does this produce, and is it there?"* rather than watching for an exception.

Every case here is a bug that shipped. The JS declaration path emitted nothing **for years**, and
stubgen wrote into a mirror of its own path; neither ever failed loudly. See
[/ROADMAP.md](../../../../../ROADMAP.md) § *Silent failure is the failure mode this workspace
actually has*.

<!-- routing:start -->
## Routing

| File | Interface | Description |
|------|-----------|-------------|
| [`test_interface_generators.py`](test_interface_generators.py) | [`test_interface_generators.pyi`](test_interface_generators.pyi) | T0 interface-generator invariants: a generated stub must land beside its source, and a |
| [`test_routing_sync_bugs.py`](test_routing_sync_bugs.py) | [`test_routing_sync_bugs.pyi`](test_routing_sync_bugs.pyi) | T0 routing-generator invariants (ROADMAP Batch B item 1): four ways the CONTEXT.md routing |
| [`test_routing_table.py`](test_routing_table.py) | [`test_routing_table.pyi`](test_routing_table.pyi) | The routing table's generated columns (Frente 3.2). Zero-token, runs in verify-fast. |
<!-- routing:end -->
