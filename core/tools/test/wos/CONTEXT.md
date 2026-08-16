# wos
> Guards on the session-close ritual: the roundup tool's git behavior and the two skills' prose contracts.

One ritual, two layers, two files. [`test_roundup.py`](test_roundup.py) runs the real script
against throwaway workspaces — a fake `core/tools/wos/roundup` inside a tmp repo, so `ROOT`
equals `WORKSPACE` and the gitflow and entropy paths are reachable at all.
[`test_roundup_skills.py`](test_roundup_skills.py) guards what cannot be asserted in bash: that
the skill does not re-inline the work the script took over, and that the hand-off template keeps
the shape agreed in [`core/SPECS.md`](../../../SPECS.md) § AD-09.

Zero-token, no network. Each test builds its own repo and bare origin; nothing touches the real
workspace.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`test_context.py`](test_context.py) | [`test_context.pyi`](test_context.pyi) | `turn`, `result`, `use`, `transcript`, `build` | T1 the context instrument (core/hooks/SPECS.md): what fills the window, attributed from the transcript. |
| [`test_deps.py`](test_deps.py) | [`test_deps.pyi`](test_deps.pyi) | — | T0 declared dependencies (core/tools/SPECS.md § Declared dependencies): a third-party import the |
| [`test_features.py`](test_features.py) | [`test_features.pyi`](test_features.pyi) | — | T0 the feature registry (core/SPECS.md § AD-14): every capability is declared, answered, |
| [`test_roundup.py`](test_roundup.py) | [`test_roundup.pyi`](test_roundup.pyi) | — | T1 roundup tool (core/SPECS.md § AD-09): the deterministic half of the session-close ritual. |
| [`test_roundup_skills.py`](test_roundup_skills.py) | [`test_roundup_skills.pyi`](test_roundup_skills.pyi) | — | T0 the session-close skills (core/SPECS.md § AD-09): what bash cannot assert about the other layer. |
| [`test_usage.py`](test_usage.py) | [`test_usage.pyi`](test_usage.pyi) | `response`, `text`, `thinking`, `project`, `build` | T1 the cost instrument: what counts as one turn, and which half of output is re-read. |
<!-- routing:end -->
