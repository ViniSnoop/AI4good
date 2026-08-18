# wos
> What the workspace declares about itself, and what the session-close ritual really does.

Two responsibilities, after the instruments moved to [`session/`](session/CONTEXT.md) in 2026-08-17's
fanout split.

**Declaration** — three files that must agree, checked against each other and never trusted.
[`test_deps.py`](test_deps.py) on `core/tools/deps.txt`, and the feature registry split in two:
[`test_features.py`](test_features.py) asks whether the declaration is complete and inside its closed
sets, [`test_features_wiring.py`](test_features_wiring.py) asks whether a row claiming a switch has
one. Data and behaviour are different questions with different failure modes — a row can be
perfectly well-formed and still name a file that never reads the law, which is the failure that cost
the first ablation run its entire signal ([`core/SPECS.md`](../../../SPECS.md) § AD-14).

**The ritual** — one ritual, two layers, two files. [`test_roundup.py`](test_roundup.py) runs the
real script against throwaway workspaces — a fake `core/tools/wos/roundup` inside a tmp repo, so
`ROOT` equals `WORKSPACE` and the gitflow and entropy paths are reachable at all.
[`test_roundup_skills.py`](test_roundup_skills.py) guards what cannot be asserted in bash: that
the skill does not re-inline the work the script took over, and that the hand-off template keeps
the shape agreed in [`core/SPECS.md`](../../../SPECS.md) § AD-09.

Zero-token, no network. Each test builds its own repo and bare origin; nothing touches the real
workspace.

<!-- routing:start -->
## Routing

| Subdirectory | Description |
|--------------|-------------|
| [`session/`](session/CONTEXT.md) | The instruments: what a session costs, what fills its window, and what a read… |

| File | Interface | Description |
|------|-----------|-------------|
| [`test_deps.py`](test_deps.py) | [`test_deps.pyi`](test_deps.pyi) | T0 declared dependencies (core/tools/SPECS.md § Declared dependencies): a third-party import the |
| [`test_features.py`](test_features.py) | [`test_features.pyi`](test_features.pyi) | T0 the feature registry's declaration half (core/SPECS.md § AD-14): every feature is declared, |
| [`test_features_wiring.py`](test_features_wiring.py) | [`test_features_wiring.pyi`](test_features_wiring.pyi) | T0 the feature registry's honesty half (core/SPECS.md § AD-14): a row claiming a switch must |
| [`test_roundup.py`](test_roundup.py) | [`test_roundup.pyi`](test_roundup.pyi) | T1 roundup tool (core/SPECS.md § AD-09): the deterministic half of the session-close ritual. |
| [`test_roundup_skills.py`](test_roundup_skills.py) | [`test_roundup_skills.pyi`](test_roundup_skills.pyi) | T0 the session-close skills (core/SPECS.md § AD-09): what bash cannot assert about the other layer. |
<!-- routing:end -->
