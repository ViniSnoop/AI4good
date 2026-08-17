# compact
> Shrink tool output before it reaches the context — the input-side twin of caveman.

Caveman compresses what the agent *writes*; this directory compresses what the agent *reads back*.
The compaction itself is [rtk](https://github.com/rtk-ai/rtk)'s job (`SETUP.md` § RTK installs it);
what lives here is the wiring that decides which commands reach it.

The shim exists because rtk reads the first line of a Bash payload and nothing else, which left every
multi-line call uncompacted — 23.4% of them open with a `cd`. What it may split, what it hands back
untouched, and the two undocumented harness facts it rests on: [`SPECS.md`](SPECS.md).

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`SPECS.md`](SPECS.md) | — | — | What the rtk shim may rewrite, what it must leave alone, and the two harness… |
| [`bash-compact-rewrite.py`](bash-compact-rewrite.py) | [`bash-compact-rewrite.pyi`](bash-compact-rewrite.pyi) | `ask_rtk`, `rewritten_command`, `rtk_rewrite`, `delegate`, `record` | PreToolUse: Bash — send every line of a multi-line command through rtk, not just the first. |
<!-- routing:end -->
