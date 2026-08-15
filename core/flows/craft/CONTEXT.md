# Craft Flows
> The engineering cluster owned by the `loops` skill — build work in file-relayed loops. Invoked as `/loops`.

Entry point: the `loops` skill ([`core/skills/loops.md`](../../skills/loops.md)) — it loads the
shared discipline before any file here is read directly.

Why `craft.md` stays one file instead of splitting further: [`SPECS.md`](SPECS.md).

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`SPECS.md`](SPECS.md) | Craft Flows — Specs |
| [`architect.md`](architect.md) | Architecture-decision subtree of the craft tree — turn a design/technology choice into a recorded decision (problem → options → trade-offs → decision → ADR). Produces a durable decision record, not code. |
| [`craft.md`](craft.md) | Looped engineering flow — development in file-relayed loops with model autorouting; each loop runs in a fresh, cheap session that reads exactly one file. |
| [`prior-art.md`](prior-art.md) | Craft — Prior Art, Provenance, and Case Study |
| [`route.md`](route.md) | Loop router — classify a /loops task by TYPE and dispatch to the right subtree flow (padaria · feature/SDD · research · architecture). Thin: it classifies and hands off, it does not do the work. |
| [`routing.md`](routing.md) | Craft — Provider Routing |
| [`runtimes.md`](runtimes.md) | Craft — Runtime Spawn Recipes |
| [`tree.md`](tree.md) | The Craft Tree |
<!-- routing:end -->
