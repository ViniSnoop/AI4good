# generators
> Sourced pre-commit stages that write artifacts and stage them.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`interfaces.sh`](interfaces.sh) | Generate: language interface stubs — .pyi, .d.ts (js + ts), .dart.api. |
| [`prepare.sh`](prepare.sh) | Prepare: brain stats + self-healing .gitignore allowlist. Runs first — both stage files. |
| [`routing.sh`](routing.sh) | Generate: CONTEXT.md routing blocks and TeX .texif interfaces. |
| [`skills.sh`](skills.sh) | Generate: skill-library mirrors, then validate their frontmatter. |
<!-- routing:end -->
