# Gate: copy-paste (jscpd), facade boundaries, and paper term consistency.
# Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script:
# it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher.

# ── 1b. Duplication gate (jscpd) — blocks clones involving staged files ───────
DUP_FILES=$(echo "$STAGED" | grep -E '\.(js|jsx|ts|tsx|py|dart)$' | grep -vE '\.(d\.ts|pyi|min\.js)$' || true)
if [ -n "$DUP_FILES" ]; then
  if ! echo "$DUP_FILES" | python3 /mnt/workspace/core/hooks/checks/check-duplication.py; then
    exit 1
  fi
fi

# ── 2b. Facade boundary check ─────────────────────────────────────────────────
FACADE_FILES=$(echo "$STAGED" | grep -E '\.(ts|tsx|js|jsx|py|dart)$' | grep -v '\.d\.ts$' || true)
if [ -n "$FACADE_FILES" ]; then
  if ! echo "$FACADE_FILES" | python3 /mnt/workspace/core/hooks/facade/check-facade-imports.py; then
    exit 1
  fi
fi

# ── 3. Term consistency check (papers with terms.yaml) ────────────────────────
TEX_STAGED=$(echo "$STAGED" | grep '\.tex$' || true)
if [ -n "$TEX_STAGED" ]; then
  PAPER_ROOTS=$(echo "$TEX_STAGED" | xargs -I{} dirname {} | sort -u | while read -r d; do
    # Walk up to the directory that contains terms.yaml
    curr="$d"
    while [ "$curr" != "." ] && [ "$curr" != "/" ]; do
      [ -f "$curr/terms.yaml" ] && echo "$curr" && break
      curr=$(dirname "$curr")
    done
  done | sort -u)
  if [ -n "$PAPER_ROOTS" ]; then
    TERMS_TOOL="/mnt/workspace/core/tools/terms"
    while IFS= read -r paper_root; do
      if [ -x "$TERMS_TOOL" ]; then
        if ! "$TERMS_TOOL" "$paper_root" >/tmp/terms-check.$$ 2>&1; then
          cat /tmp/terms-check.$$
          rm -f /tmp/terms-check.$$
          printf "⛔ Fix terminology inconsistencies before committing.\n"
          printf "   Edit the .tex file, or update terms.yaml if the term was intentionally revised.\n"
          printf "   Override: git commit --no-verify\n\n"
          exit 1
        else
          cat /tmp/terms-check.$$
          rm -f /tmp/terms-check.$$
        fi
      fi
    done <<< "$PAPER_ROOTS"
  fi
fi

