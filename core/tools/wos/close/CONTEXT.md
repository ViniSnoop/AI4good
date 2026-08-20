# close
> What a session close writes, and what it does with each artifact afterwards.

Fragments sourced by [`../roundup`](../roundup), the same shape
[`../skills/mirror.sh`](../skills/mirror.sh) has for `sync-skills`: the caller keeps the sequence and
the decisions, a fragment keeps the work one step does. Nothing here runs on its own — each relies on the caller's variables and would be
meaningless without them.

**One rule governs every artifact a close regenerates**: write it, then commit it — unless the tree
holds another session's work, in which case report the number and roll the write back. A
regenerated file left behind rides into that session's next `git add -A`, which is the incident
this directory's `settle` exists to make unrepeatable.

<!-- routing:start -->
## Routing

| File | Description |
|------|-------------|
| [`artifacts.sh`](artifacts.sh) | The generated artifacts a session close regenerates, and what happens to each one afterwards. Sourced by core/tools/wos/roundup — a FRAGMENT, not a standalone script: it relies on $WORKSPACE, $LEAVE_DIRTY, $VERIFY, $VERIFY_CMD and $LOG from the caller. |
<!-- routing:end -->
