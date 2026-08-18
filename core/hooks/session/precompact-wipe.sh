#!/usr/bin/env bash
# PreCompact — wipe the session CONTEXT.md seen-markers so the chain is re-read after
# compaction (injected context may be summarized away). See code/ROADMAP-verify.md W1.
# Switched off: the seen-markers survive compaction, so the chain is not re-read.
python3 /mnt/workspace/core/hooks/feature_law.py --enabled precompact-wipe || exit 0
sid=$(python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id',''))" 2>/dev/null)
[ -n "$sid" ] && rm -f "/tmp/claude_ctx_seen_${sid}.txt"
exit 0
