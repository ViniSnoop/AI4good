# Research Flows
> Research-workflow protocols owned by the `research` skill. Invoked as `research <verb>` — filename = command tail.

Each file here is one workflow of the `research` skill ([`core/skills/research.md`](../../skills/research.md)).
The skill is the dispatcher; these are the protocols it reads and executes. **The filename is the
command tail**: `core/flows/research/scout.md` ⟺ `research scout`. Do not invoke these directly —
go through the `research` skill so the shared tool-discipline and source-tier rules load.

Ownership rule (see [`core/SCHEMA.md`](../../SCHEMA.md)): a flow owned by a dispatcher skill lives in
`core/flows/<skill>/` and its filename equals the command tail; unowned flows stay flat at `core/flows/`.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`audit.md`](audit.md) | Compare a paper's claims against its public codebase and identify mismatches… |
| [`compare.md`](compare.md) | Compare multiple sources on a topic and produce a source-grounded matrix of… |
| [`draft.md`](draft.md) | Turn research findings into a polished paper-style draft with equations… |
| [`explore.md`](explore.md) | Autonomous experiment loop — try ideas, measure results, keep what works… |
| [`literature.md`](literature.md) | Run a literature review on a topic using paper search and primary-source… |
| [`recipe.md`](recipe.md) | Find ranked, implementable ML training recipes backed by papers, datasets, docs… |
| [`replicate.md`](replicate.md) | Plan or execute a replication workflow for a paper, claim, or benchmark. |
| [`review.md`](review.md) | Simulate an AI research peer review with likely objections, severity, and a… |
| [`scout.md`](scout.md) | Scout a topic across web + repos + academia in refined rounds, then convert the… |
| [`sota.md`](sota.md) | Map the state of the art of a field — fill refs/REFS.md plus one review yaml per… |
| [`summarize.md`](summarize.md) | Summarize any URL, local file, or PDF using the RLM pattern — source stored on… |
| [`watch.md`](watch.md) | Set up a recurring or deferred research watch on a topic, company, paper area… |
<!-- routing:end -->
