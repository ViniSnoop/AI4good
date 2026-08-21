# zcode
> ZCode-side instruments: the hook-protocol probes, and the future home of the adapter if direct registration fails fidelity.

The registration itself lives outside this tree, in
[`.zcode/config.json`](../../../.zcode/config.json) — direct spawns of the canonical gates,
mirroring `.claude/settings.json` one-to-one (no adapter, no second copy of a rule). What is
true of it, including the measured trust gate that holds it inert and the open protocol
questions: [`../../../.zcode/CONTEXT.md`](../../../.zcode/CONTEXT.md) and the experiment
[`experiments/zcode-hook-protocol.md`](../../experiments/zcode-hook-protocol.md). The shim
contract every runtime owes: [`SPECS-shim.md`](../SPECS-shim.md).

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`probe.sh`](probe.sh) | Dumps what a ZCode hook event delivers (stdin, filtered env, cwd, ppid) to /tmp/zcode_probe/. Temporary instrument — kept for the post-trust re-run. |
| [`probe-deny.sh`](probe-deny.sh) | Exit-2 fidelity probe: plain-text stdout + block, registered on a sacrificial matcher. Temporary instrument. |
<!-- routing:end -->
