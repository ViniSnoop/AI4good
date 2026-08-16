# session
> Session lifecycle: start, prune, precompact wipe, and the SessionStart nudges.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`compass-nudge.py`](compass-nudge.py) | [`compass-nudge.pyi`](compass-nudge.pyi) | `main` | SessionStart — a soft, ignorable reminder that the compass review hasn't run in a while, so the |
| [`context-meter.py`](context-meter.py) | [`context-meter.pyi`](context-meter.pyi) | `state_file`, `announced`, `mark`, `find_transcript`, `last_context` | UserPromptSubmit — say what the next turn costs, once per threshold crossed. |
| [`inbox-nudge.py`](inbox-nudge.py) | [`inbox-nudge.pyi`](inbox-nudge.pyi) | `read_body`, `count_entries`, `main` | SessionStart — warn Lucas + agent when brain/INBOX.md has piled up past a threshold, |
| [`precompact-wipe.sh`](precompact-wipe.sh) | — | — | PreCompact — wipe the session CONTEXT.md seen-markers so the chain is re-read after |
| [`session-prune.sh`](session-prune.sh) | — | — | SessionStart — prune stale session marker files (context seen-markers, facade reads, |
| [`start-session.sh`](start-session.sh) | — | — | Neutral session-start entrypoint |
<!-- routing:end -->
