# gates
> Sourced pre-commit stages that may reject the commit.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`duplication-and-terms.sh`](duplication-and-terms.sh) | Gate: copy-paste (jscpd), facade boundaries, and paper term consistency. Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script: it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher. |
| [`lint.sh`](lint.sh) | Gate: ESLint on staged TypeScript. Runs LAST — it needs the .d.ts the generators just wrote. Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script: it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher. |
| [`project-contract.sh`](project-contract.sh) | Gate: what a code/ project must declare — verify contract, goal link, spec, branch, .md type, gitlink. Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script: it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher. |
| [`source-quality.sh`](source-quality.sh) | Gate: line counts and first-line description comments. Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script: it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher. |
<!-- routing:end -->
