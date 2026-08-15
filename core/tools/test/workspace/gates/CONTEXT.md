# gates
> What a blocking gate must say, and who it must fire for. Mirrors `core/hooks/gates/`.

Two questions, one per file, and they are independent — a gate can block the right agent for the
wrong reason, or the wrong agent with a perfect message.

| File | The one question it answers |
|------|-----------------------------|
| [`test_gate_messages.py`](test_gate_messages.py) | When a gate blocks, does it say **why**, on stderr? |
| [`test_subagent_gate.py`](test_subagent_gate.py) | **Who** is gated — and who is deliberately not? |

Both run the real gate as a subprocess against a synthetic payload, so they assert the wiring, not
the source text. The one exception is deliberate: `test_the_spec_gate_is_not_exempted` reads
`spec-read-gate.py` for the *absence* of the exemption helper, because proving a gate does **not**
opt out is easier structurally than constructing a spec-locked module in a tmp tree.

**Why stderr is the whole subject of the first file:** a `PreToolUse` exit-2's stderr is fed back to
the model and its stdout is dropped, so a gate printing to stdout blocks with no reason attached and
reads as "No stderr output".

**Why the second exists:** the subagent exemption was real before it was decided — a worker
inherited the parent's `session_id` and therefore its seen-set, leaving it ungated only for subtrees
the parent happened to visit. Ruled deliberate 2026-08-15; measured in
[`core/experiments/subagent-context-chain.md`](../../../../experiments/subagent-context-chain.md).

<!-- routing:start -->
## Routing

| File | Interface | Description |
|------|-----------|-------------|
| [`test_gate_messages.py`](test_gate_messages.py) | [`test_gate_messages.pyi`](test_gate_messages.pyi) | T0: a blocking gate must say WHY on stderr. Claude Code feeds a PreToolUse exit-2's |
| [`test_subagent_gate.py`](test_subagent_gate.py) | [`test_subagent_gate.pyi`](test_subagent_gate.pyi) | T0 the subagent exemption (ROADMAP Frente 3.1): a worker is not made to read the routing chain. |
<!-- routing:end -->
