#!/usr/bin/env bash
# Self-healing .gitignore allowlist (decided 2026-07-24). Contract: core/hooks/SPECS.md.
# Every domain folder (core/, code/, academy/, branches/, brain/, models/, datasets/) uses a
# denylist-first .gitignore pattern (`<domain>/*` + explicit `!<domain>/<dir>/` allow lines),
# so a brand-new domain subdir is silently untracked until someone remembers to add its line
# — already bit core/refs/. A subdir with a CONTEXT.md is structural by construction (the
# existing "this is workspace scaffold" signal): add its allow line and stage it, no human
# action. A subdir with no CONTEXT.md stays ignored (correctly project-internal/scratch). A
# subdir listed in gitignore-exceptions.txt is a deliberate, reviewed exception — skipped.
# A subdir that is its own git repo is skipped too (see the note in the loop).
#
# Usage: gitignore-self-heal.sh [workspace-root]   (default: cwd — a git hook's cwd is repo root)
set -euo pipefail

# Switched off: the allowlist stops repairing itself. A generator that is disabled writes
# nothing rather than writing an empty artifact, which would be worse than not running.
python3 /mnt/workspace/core/hooks/feature_law.py --enabled gitignore-self-heal || exit 0

# Scoped to the workspace repo — this hook file is wired globally (core.hooksPath), but the
# domain-denylist .gitignore pattern only exists at /mnt/workspace. Nested project repos
# (code/*, academy/papers/*, ...) have their own unrelated .gitignore; skip them.
if [ $# -eq 0 ]; then
  TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null || true)
  [ "$TOPLEVEL" = "/mnt/workspace" ] || exit 0
fi

ROOT="${1:-.}"
GITIGNORE="$ROOT/.gitignore"
EXCEPTIONS="$ROOT/core/hooks/gitignore-exceptions.txt"

[ -f "$GITIGNORE" ] || exit 0

HEALED=""

for domain in $(grep -oE '^[a-zA-Z0-9_-]+/\*$' "$GITIGNORE" | sed 's#/\*$##'); do
  [ -d "$ROOT/$domain" ] || continue
  for dir in "$ROOT/$domain"/*/; do
    # A nested git repo is unreachable from the outer repo: git cannot track files inside it
    # without submodules, which the 2026-07-22 nested-gitlink-gate decision deliberately killed.
    # An allow line would track nothing and leave a permanent `?? <dir>` in every git status,
    # which is exactly what the first version of this hook did to 13 code/ projects. Routing
    # reads their CONTEXT.md off-disk instead. Corrected 2026-07-29.
    [ -e "${dir}.git" ] && continue
    [ -f "${dir}CONTEXT.md" ] || continue
    name="$domain/$(basename "$dir")"
    grep -qxF "$name" "$EXCEPTIONS" 2>/dev/null && continue
    grep -qxF "!$name/" "$GITIGNORE" && continue
    printf '!%s/\n' "$name" >> "$GITIGNORE"
    git -C "$ROOT" add "$GITIGNORE" 2>/dev/null || true
    HEALED="$HEALED $name"
  done
done

# Heal, then STOP — the commit in flight cannot carry what it could not see.
#
# Staging happens before this hook runs, so every file under a directory healed above was
# ignored at `git add` time and is not in the index. Committing anyway ships a directory's
# CONTEXT.md without the files it describes, and a clone at that commit regenerates an empty
# artifact. That is what happened when core/norms/ landed: it self-corrected one commit later
# and nothing was lost, which is exactly why it would keep happening.
#
# The alternative was to `git add` the missing files here so one commit always suffices.
# Rejected 2026-08-19 (Lucas): a commit hook that stages files the caller did not stage is
# worse than the bug it fixes. Fail loud instead. Contract: core/hooks/SPECS.md.
[ -n "$HEALED" ] || exit 0

MISSING=""
for name in $HEALED; do
  if [ -n "$(git -C "$ROOT" ls-files --others --exclude-standard -- "$name" 2>/dev/null)" ]; then
    MISSING="$MISSING $name"
  fi
done

# Healed, but nothing was actually hidden — the allow line was merely absent. Let the commit run.
[ -n "$MISSING" ] || exit 0

echo "GITIGNORE HEALED -- rerun the commit" >&2
echo "  .gitignore now allows:$MISSING" >&2
echo "  Those files were ignored when this commit was staged, so it would ship without them." >&2
echo "  Run: git add$MISSING && git commit ..." >&2
exit 1
