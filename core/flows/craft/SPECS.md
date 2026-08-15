# Craft Flows — Specs
> Why `craft.md` stays one file instead of splitting further.

`craft.md` was one ~52 KB file mixing the always-loaded protocol with tables and history each loop
paid for eight times. The 2026-07-23 split follows what is actually read when: always-needed stays
in one file; per-chain and never-needed content became the subfiles beside it (`routing.md`,
`runtimes.md`, `prior-art.md`, the trunk `route.md`, the map `tree.md`). This is deliberately not
blind fragmentation — the whole spine (Core Principle, Carry, Autorouting, Return Flags, Loops
0–6.5, Cost Gate, Field Practice) stays one file, because a loop executor needs all of it in a
single read.
