# postedit
> Sourced post-edit stages: regenerate interfaces, remind, sync, lint.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`interfaces.sh`](interfaces.sh) | Regenerate the interface next to the file just edited — .pyi, .d.ts, .dart.api, .texif. |
| [`lint.sh`](lint.sh) | ESLint + Prettier for TypeScript under code/ (R1-R6). |
| [`reminders.sh`](reminders.sh) | Nudges, never blocks: first-line description, facade boundary, CONTEXT.md line 2 and goal link. |
| [`sync.sh`](sync.sh) | Keep generated indexes fresh: the CONTEXT.md routing block and the codegraph. |
<!-- routing:end -->
