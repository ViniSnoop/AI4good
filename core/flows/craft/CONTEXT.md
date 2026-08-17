# Craft Flows
> The engineering cluster owned by the `craft` skill — build work in file-relayed loops. Invoked as `/craft`.

Entry point: the `craft` skill ([`core/skills/craft.md`](../../skills/craft.md)) — it loads the
shared discipline before any file here is read directly.

Why `craft.md` stays one file instead of splitting further: [`SPECS.md`](SPECS.md).

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`SPECS.md`](SPECS.md) | Why `craft.md` stays one file instead of splitting further. |
| [`architect.md`](architect.md) | Architecture-decision subtree of the craft tree — turn a design/technology… |
| [`craft.md`](craft.md) | Looped engineering flow — development in file-relayed loops with model… |
| [`prior-art.md`](prior-art.md) | Where this flow comes from, what evidence backs its routing decisions, and one… |
| [`route.md`](route.md) | Loop router — classify a /craft task by TYPE and dispatch to the right subtree… |
| [`routing.md`](routing.md) | Which concrete model fills each tier, per provider; the availability probe; the… |
| [`runtimes.md`](runtimes.md) | How the orchestrator actually spawns a loop, per runtime. Verbatim recipes; no… |
| [`tree.md`](tree.md) | Canonical map of `/craft`: a router classifies each task and dispatches to a… |
<!-- routing:end -->
