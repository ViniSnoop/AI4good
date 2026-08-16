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
  done
done
