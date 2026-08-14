# wos
> Guards on the session-close ritual: the roundup tool's git behavior and the two skills' prose contracts.

One ritual, two layers, two files. [`test_roundup.py`](test_roundup.py) runs the real script
against throwaway workspaces — a fake `core/tools/wos/roundup` inside a tmp repo, so `ROOT`
equals `WORKSPACE` and the gitflow and entropy paths are reachable at all.
[`test_roundup_skills.py`](test_roundup_skills.py) guards what cannot be asserted in bash: that
the skill does not re-inline the work the script took over, and that the hand-off template keeps
the shape agreed in ROADMAP Frente 9.2.

Zero-token, no network. Each test builds its own repo and bare origin; nothing touches the real
workspace.

<!-- routing:start -->
## Routing

| File | Interface | Description |
|------|-----------|-------------|
| [`test_roundup.py`](test_roundup.py) | [`test_roundup.pyi`](test_roundup.pyi) | T1 roundup tool (Frente 9.2): the deterministic half of the session-close ritual. |
| [`test_roundup_skills.py`](test_roundup_skills.py) | [`test_roundup_skills.pyi`](test_roundup_skills.pyi) | T0 the session-close skills (Frente 9.2): what bash cannot assert about the other layer. |
<!-- routing:end -->
