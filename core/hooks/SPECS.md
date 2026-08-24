# Hooks — Specs
> What must be true of the enforcement layer, and why: what each gate blocks, and the contract a new agent's shim must
> satisfy.

Companion to [`CONTEXT.md`](CONTEXT.md), which says what this directory *is* and routes into it.
This file holds the constraints. Installing the toolchain these gates depend on is a third
question, answered by [`SETUP.md`](../../SETUP.md).

## The law lives in file_law.py / schema_law.py / limits.env, never in a checker

A checker that restates any of these is the drift the checkers exist to catch. This has bitten
twice: five separate definitions of "a code file" existed across different checkers before they
were unified behind `file_law.is_code_file`, guarded now by
`core/tools/test/law/test_file_law.py::test_no_checker_carries_its_own_extension_list`. And
`entropy_corpus.py`'s `_CHECKER` / `_CHECKER_TESTS` constants once spelled out a sibling path by
hand — a hard-coded path stops exempting the retired-token checker (and its own test file) from
itself the moment `core/hooks` moves. The fix derives both from `Path(__file__)` instead, so a
future move cannot break it the same way.

## What a working install looks like

Behavioural assertions — these are what the gates promise, and the list a new shim is tested
against. The commands that check the toolchain itself are in [`SETUP.md`](../../SETUP.md) § Verification.

- edit a `.py` / `.js` / `.ts` / `.dart` file → its interface regenerates immediately
- edit a `.tex` file → `.texif` **and** `labels.md` regenerate; a `.bib` edit warns about bib keys
  with no `reviews/<key>.yaml`
- read a source file whose interface is current → blocked, interface first
- grow a code file past 200 lines → the edit is blocked
- create a new file with no first-line comment → the Write is blocked
- edit a file already missing that comment → a reminder prints, the edit stands
- commit a new file the routing table could not describe → the commit is rejected
- commit a 200+ line code file → the commit is rejected
- commit any staged code file → its `CONTEXT.md` routing block is updated and staged

<!-- routing:start -->
## Routing

| Shard | Description | Governs |
|-------|-------------|---------|
| [`SPECS-gates.md`](SPECS-gates.md) | What each blocking gate rejects, at commit time and at edit time. | core/hooks/pre-commit, core/hooks/gates/, core/hooks/checks/, core/hooks/read/ |
| [`SPECS-generators.md`](SPECS-generators.md) | What the hooks write rather than reject, and what must be true of each artifact. | core/hooks/generators/, core/hooks/routing/, core/hooks/stubgen/ |
| [`SPECS-shim.md`](SPECS-shim.md) | One canonical behaviour, and what a new agent runtime must do to get it. | core/hooks/copilot/, core/hooks/hook_input.py, .opencode/plugins/ |
<!-- routing:end -->
