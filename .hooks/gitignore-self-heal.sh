#!/usr/bin/env bash
# Self-healing .gitignore allowlist (decided 2026-07-24, ROADMAP.md Frente 6 item 2).
# Every domain folder (core/, code/, academy/, branches/, brain/, models/, datasets/) uses a
# denylist-first .gitignore pattern (`<domain>/*` + explicit `!<domain>/<dir>/` allow lines),
# so a brand-new domain subdir is silently untracked until someone remembers to add its line
# — already bit core/refs/. A subdir with a CONTEXT.md is structural by construction (the
# existing "this is workspace scaffold" signal): add its allow line and stage it, no human
# action. A subdir with no CONTEXT.md stays ignored (correctly project-internal/scratch). A
# subdir listed in gitignore-exceptions.txt is a deliberate, reviewed exception — skipped.
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
EXCEPTIONS="$ROOT/.hooks/gitignore-exceptions.txt"

[ -f "$GITIGNORE" ] || exit 0

for domain in $(grep -oE '^[a-zA-Z0-9_-]+/\*$' "$GITIGNORE" | sed 's#/\*$##'); do
  [ -d "$ROOT/$domain" ] || continue
  for dir in "$ROOT/$domain"/*/; do
    [ -f "${dir}CONTEXT.md" ] || continue
    name="$domain/$(basename "$dir")"
    grep -qxF "$name" "$EXCEPTIONS" 2>/dev/null && continue
    grep -qxF "!$name/" "$GITIGNORE" && continue
    if [ -e "${dir}.git" ]; then
      # Own git repo (AGENTS.md: internal projects use their own repos) — track only the
      # routing stub, same shape as the existing code/laplata|gira|cria entries.
      printf '!%s/\n%s/*\n!%s/CONTEXT.md\n' "$name" "$name" "$name" >> "$GITIGNORE"
    else
      printf '!%s/\n' "$name" >> "$GITIGNORE"
    fi
    git -C "$ROOT" add "$GITIGNORE" 2>/dev/null || true
  done
done
