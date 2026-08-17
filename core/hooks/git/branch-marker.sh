#!/usr/bin/env bash
# Branch drift warning — HEAD is shared mutable state between parallel sessions, and nothing said so.
# `record` stores the branch a session started on; `check` warns at commit time when HEAD has moved
# since. Warn only, never block: a deliberate mid-session switch is legitimate and common.
# Decided 2026-08-14 (Lucas) over one-worktree-per-session, which fights the branch sweep in
# core/skills/roundup.md Phase 5 — a checked-out worktree makes `git branch -d` refuse.
#
# One marker per repo, not per session: `record` runs at SessionStart, where only the repo is known,
# and `check` runs inside a git hook, which has no session id to pair with.

MODE="${1:-}"
REPO=$(git rev-parse --show-toplevel 2>/dev/null || true)
[ -z "$REPO" ] && exit 0

# --show-current, not rev-parse: it names a branch that has no commit yet, and it prints nothing
# on a detached HEAD — which is a rebase or a bisect, where a branch warning is noise.
BRANCH=$(git branch --show-current 2>/dev/null || true)
[ -z "$BRANCH" ] && exit 0

MARKER="/tmp/claude_branch_$(printf '%s' "$REPO" | tr -c 'A-Za-z0-9' '_').txt"

case "$MODE" in
  record)
    printf '%s\n' "$BRANCH" > "$MARKER"
    ;;
  check)
    [ -f "$MARKER" ] || exit 0
    STARTED=$(cat "$MARKER" 2>/dev/null)
    if [ -n "$STARTED" ] && [ "$STARTED" != "$BRANCH" ]; then
      printf "[Git] ⚠ HEAD moved since this session started: '%s' → '%s'.\n" "$STARTED" "$BRANCH"
      printf "   A parallel session may have switched the shared checkout, and this commit is\n"
      printf "   about to land on their branch. If it should be yours:\n"
      printf "   git merge-base --is-ancestor %s HEAD  &&  git branch -f %s HEAD\n" "$STARTED" "$STARTED"
      printf "   Never reset or force-push theirs. See core/hooks/SPECS.md § Branch drift.\n"
      # Re-record so a deliberate switch warns once, not on every commit that follows —
      # a warning that repeats after being understood is one people learn to skip.
      printf '%s\n' "$BRANCH" > "$MARKER"
    fi
    ;;
  *)
    printf 'usage: branch-marker.sh record|check\n' >&2
    exit 2
    ;;
esac
exit 0
