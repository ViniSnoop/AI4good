# gates
> What a blocking gate must say, and who it must fire for. Mirrors `core/hooks/gates/`.

Three questions, one per file, and they are independent — a hook can block the right agent for the
wrong reason, the wrong agent with a perfect message, or rewrite shell it had no business touching.

| File | The one question it answers |
|------|-----------------------------|
| [`test_gate_messages.py`](test_gate_messages.py) | When a gate blocks, does it say **why**, on stderr? |
| [`test_subagent_gate.py`](test_subagent_gate.py) | **Who** is gated — and who is deliberately not? |
| [`test_bash_compact_rewrite.py`](test_bash_compact_rewrite.py) | When a hook rewrites, does it leave **unreadable shell alone**? |

Why each one exists, and the one place a test reads source instead of running it: [`SPECS.md`](SPECS.md).

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | Why each hook test exists, and the one structural exception to running the real… |
| [`test_agent_context.py`](test_agent_context.py) | [`test_agent_context.pyi`](test_agent_context.pyi) | `prompt_id` | T0 the agent-context briefing (core/hooks/SPECS.md): the orchestrator's duty, done by a hook. |
| [`test_bash_compact_rewrite.py`](test_bash_compact_rewrite.py) | [`test_bash_compact_rewrite.pyi`](test_bash_compact_rewrite.pyi) | `rtk_path` | T0 the multi-line rtk shim: it must reach lines 2+, and must never reshape shell it cannot read. |
| [`test_gate_messages.py`](test_gate_messages.py) | [`test_gate_messages.pyi`](test_gate_messages.pyi) | — | T0: a hook must speak on the channel its class is read on. Two mirrored rules, one subject. |
| [`test_heredoc_gate.py`](test_heredoc_gate.py) | [`test_heredoc_gate.pyi`](test_heredoc_gate.pyi) | `run` | T0 the heredoc gate: a shell write to a workspace file must not walk past the file gates. |
| [`test_subagent_gate.py`](test_subagent_gate.py) | [`test_subagent_gate.pyi`](test_subagent_gate.pyi) | — | T0 the subagent exemption (core/hooks/SPECS.md): a worker is not made to read the routing chain. |
<!-- routing:end -->
