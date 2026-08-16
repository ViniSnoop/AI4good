# gates
> Sourced pre-commit stages that may reject the commit.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`duplication-and-terms.sh`](duplication-and-terms.sh) | Gate: copy-paste (jscpd), facade boundaries, and paper term consistency. |
| [`lint.sh`](lint.sh) | Gate: ESLint on staged TypeScript. Runs LAST — it needs the .d.ts the generators just wrote. |
| [`project-contract.sh`](project-contract.sh) | Gate: what a code/ project must declare — verify contract, goal link, spec, branch, .md type, gitlink. |
| [`source-quality.sh`](source-quality.sh) | Gate: line counts and first-line description comments. |
<!-- routing:end -->
