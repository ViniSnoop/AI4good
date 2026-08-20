# entropy
> What each entropy check counts, and where it must stay silent. Mirrors `core/hooks/entropy/`.

Split from `law/` 2026-08-15 at 8 files, the same way `test/workspace/` split into `gates/` and
`generators/`: a surface and its coverage stay one word apart, so the file that tests
`entropy_ledger.py` is found by knowing the name of the thing it tests.

These own whether each check **fires correctly** — the boundaries are the design, and every one of
them is a case where two things look identical and mean opposite things: a tick is a corpse in a
ledger and a legend marker in a spec, a date without a completion verb is a citation, a generator's
unfilled marker is a question rather than history. Whether the **backlog is shrinking** is a
different question, owned by the ratchets in [`../../workspace/`](../../workspace/CONTEXT.md).

Write the glyphs these checks hunt for **only inside a test**, never in this head: the checks read
prose literally, and a `CONTEXT.md` quoting a marker is indistinguishable from one that never
answered it — to the check and to a reader skimming it. That is not a false positive to exempt away;
it is the same ambiguity the reader has.

<!-- routing:start -->
## Routing

| File | Interface | Description |
|------|-----------|-------------|
| [`test_entropy_context.py`](test_entropy_context.py) | [`test_entropy_context.pyi`](test_entropy_context.pyi) | T0 CONTEXT.md rules (Tier 0, law in core/SCHEMA.md). Zero-token, runs in verify-fast. |
| [`test_entropy_fanout.py`](test_entropy_fanout.py) | [`test_entropy_fanout.pyi`](test_entropy_fanout.pyi) | T0 directory fanout (Tier 0, law in core/SCHEMA.md). Zero-token, runs in verify-fast. |
| [`test_entropy_inventory.py`](test_entropy_inventory.py) | [`test_entropy_inventory.pyi`](test_entropy_inventory.pyi) | T0 no-hand-inventory rule (Tier 0, law in core/SCHEMA.md). Zero-token, runs in verify-fast. |
| [`test_entropy_ledger.py`](test_entropy_ledger.py) | [`test_entropy_ledger.pyi`](test_entropy_ledger.pyi) | T0 ledger and vocabulary checks (Tier 0, law in core/SCHEMA.md). Zero-token, runs in verify-fast. |
| [`test_entropy_naming.py`](test_entropy_naming.py) | [`test_entropy_naming.pyi`](test_entropy_naming.pyi) | T0 naming and placement (Tier 0, law in core/SCHEMA.md). Zero-token, runs in verify-fast. |
| [`test_entropy_placeholders.py`](test_entropy_placeholders.py) | [`test_entropy_placeholders.pyi`](test_entropy_placeholders.pyi) | T0 unanswered scaffold placeholders (first-line-comment rule, core/hooks/SPECS.md). Zero-token, runs in verify-fast. |
| [`test_entropy_stores.py`](test_entropy_stores.py) | [`test_entropy_stores.pyi`](test_entropy_stores.pyi) | T0 the two doubt stores (core/SPECS-discipline.md § AD-16 band 1): an experiment states its own format, and a judged reference carries a source tier. Zero-token, runs in verify-fast. |
| [`test_entropy_vendor.py`](test_entropy_vendor.py) | [`test_entropy_vendor.pyi`](test_entropy_vendor.pyi) | T0 the vendor-name guard (core/SCHEMA-vocabulary.md): a ledger assigns a TIER, never a model. Zero-token, runs in verify-fast. |
<!-- routing:end -->
