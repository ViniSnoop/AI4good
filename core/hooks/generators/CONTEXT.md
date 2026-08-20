# generators
> Sourced pre-commit stages that write artifacts and stage them.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`interfaces.sh`](interfaces.sh) | Generate: language interface stubs — .pyi, .d.ts (js + ts), .dart.api. Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script: it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher. |
| [`prepare.sh`](prepare.sh) | Prepare: brain stats + self-healing .gitignore allowlist. Runs first — both stage files. Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script: it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher. |
| [`routing.sh`](routing.sh) | Generate: CONTEXT.md routing blocks and TeX .texif interfaces. Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script: it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher. |
| [`skills.sh`](skills.sh) | Generate: skill-library mirrors, then validate their frontmatter. Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script: it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher. |
<!-- routing:end -->
