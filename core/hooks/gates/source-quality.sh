# Gate: line counts and first-line description comments.
# Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script:
# it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher.

# ── 1. Line-count checks (code files only — not JSON, Markdown, binaries) ─────
CODE_FILES=$(echo "$STAGED" | python3 "$HOOKS_DIR/file_law.py" --filter-code || true)

if [ -n "$CODE_FILES" ]; then
  if ! printf '%s\n' "$CODE_FILES" | /mnt/workspace/core/hooks/checks/check-line-counts.sh --from-stdin >/tmp/workspace-line-counts.$$ 2>&1; then
    cat /tmp/workspace-line-counts.$$
    rm -f /tmp/workspace-line-counts.$$
    exit 1
  fi
  cat /tmp/workspace-line-counts.$$
  rm -f /tmp/workspace-line-counts.$$
fi

# ── 2. Missing first-line description comment (new files only) ─────────────────
NEW_CODE=$(git diff --cached --name-only --diff-filter=A 2>/dev/null \
  | python3 "$HOOKS_DIR/file_law.py" --filter-code || true)
if [ -n "$NEW_CODE" ]; then
  while IFS= read -r f; do
    [ -f "$f" ] || continue
    first=$(head -1 "$f")
    case "$f" in
      *.py)   echo "$first" | grep -qE '^\s*(#|"""|'"''')" || \
                printf "⚠  No first-line description: $f\n   Add: # Short description of this module\n\n" ;;
      *.js|*.ts|*.tsx|*.dart) echo "$first" | grep -qE '^\s*//' || \
                printf "⚠  No first-line description: $f\n   Add: // Short description of this module\n\n" ;;
      *.css|*.scss) echo "$first" | grep -qE '^\s*/\*' || \
                printf "⚠  No first-line description: $f\n   Add: /* Short description of this stylesheet */\n\n" ;;
      *.html) echo "$first" | grep -qE '^\s*<!--' || \
                printf "⚠  No first-line description: $f\n   Add: <!-- Short description of this template -->\n\n" ;;
      *.tex) echo "$first" | grep -qE '^\s*%' || \
                printf "⚠  No first-line description: $f\n   Add: %% Short description of this section\n\n" ;;
    esac
  done <<< "$NEW_CODE"
fi

