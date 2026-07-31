# Gate: ESLint on staged TypeScript. Runs LAST — it needs the .d.ts the generators just wrote.
# Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script:
# it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher.

# ── 10. ESLint hard block — TypeScript projects under code/ with eslint.config.js ──
TS_CODE_STAGED=$(echo "$STAGED" | grep -E '^code/[^/]+/.*\.(ts|tsx)$' | grep -v '\.d\.ts$' || true)
if [ -n "$TS_CODE_STAGED" ]; then
  declare -A _eslint_proj_seen
  while IFS= read -r staged_file; do
    [ -f "$staged_file" ] || continue
    proj_name=$(echo "$staged_file" | cut -d/ -f2)
    [ -n "${_eslint_proj_seen[$proj_name]+x}" ] && continue
    proj_dir="/mnt/workspace/code/$proj_name"
    [ -f "$proj_dir/eslint.config.js" ] || continue
    _eslint_proj_seen["$proj_name"]=1
    ESLINT_BIN="$proj_dir/node_modules/.bin/eslint"
    if [ ! -x "$ESLINT_BIN" ]; then
      printf "⚠  eslint not found in %s — run: npm install\n\n" "$proj_name"
      continue
    fi
    # Relative paths for this project
    PROJ_FILES_REL=$(echo "$TS_CODE_STAGED" | grep "^code/$proj_name/" | sed "s|^code/$proj_name/||")
    printf "→ ESLint (%s)…\n" "$proj_name"
    if ! (cd "$proj_dir" && echo "$PROJ_FILES_REL" | xargs "$ESLINT_BIN" 2>&1); then
      printf "❌ ESLint violations in %s block commit. Fix before committing.\n\n" "$proj_name"
      exit 1
    fi
  done <<< "$TS_CODE_STAGED"
  unset _eslint_proj_seen
fi
