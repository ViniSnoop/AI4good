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

# ── 2. Missing first-line description comment ─────────────────────────────────
# Moved into the Tier 0 gate (checks/type-gate.py, via entropy_context.check_description),
# which already runs over exactly this commit's added files from gates/project-contract.sh.
# What was here was a shell case-list that only warned, only over code extensions, and was a
# third copy of a table now living once in file_law.py.

