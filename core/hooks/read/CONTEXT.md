# read
> Force-a-read gates: the CONTEXT.md chain, the interface stub, the module spec.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`bash-context-gate.py`](bash-context-gate.py) | [`bash-context-gate.pyi`](bash-context-gate.pyi) | `candidates`, `context_chain`, `main` | PreToolUse: Bash — close the cat/head/grep bypass: extract workspace file paths from the |
| [`context-gate.py`](context-gate.py) | [`context-gate.pyi`](context-gate.pyi) | `target_path`, `context_chain`, `main` | PreToolUse: Read|Edit|Write|Grep|NotebookEdit — force-read the CONTEXT.md chain of the |
| [`context-tracker.py`](context-tracker.py) | [`context-tracker.pyi`](context-tracker.pyi) | `main` | PostToolUse: Read — record CONTEXT.md/SPEC.md reads (consumed by context-gate.py / |
| [`pre-read.sh`](pre-read.sh) | — | — | ← add first-line comment |
| [`spec-read-gate.py`](spec-read-gate.py) | [`spec-read-gate.pyi`](spec-read-gate.pyi) | `find_spec_module`, `block`, `nudge`, `main` | PreToolUse: Edit|Write — a spec-locked module (its CONTEXT.md carries `> spec:` and the referenced |
<!-- routing:end -->
