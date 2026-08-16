# Gate: what a code/ project must declare — verify contract, goal link, spec, branch, .md type, gitlink.
# Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script:
# it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher.

# ── 1a. Verification contract gate — every code/ project must declare + pass verify:fast ──
# Discovery is stack-agnostic: npm script (package.json) or Makefile target — either
# satisfies the contract. code/ projects with neither are hard-blocked (code/VERIFY.md G2);
# a passing stub is enough until real coverage lands (code/VERIFY.md G5).
TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null || true)
HAS_NPM_CONTRACT=0
HAS_MAKE_CONTRACT=0
[ -f "package.json" ] && grep -q '"verify:fast"' package.json && HAS_NPM_CONTRACT=1
[ -f "Makefile" ] && grep -qE '^verify-fast:' Makefile && HAS_MAKE_CONTRACT=1

CODE_STAGED=$(echo "$STAGED" | grep -E '\.(js|jsx|ts|tsx|py|dart)$' | grep -v '\.d\.ts$' || true)

if [ -n "$CODE_STAGED" ]; then
  case "$TOPLEVEL" in
    /mnt/workspace/code/*)
      if [ "$HAS_NPM_CONTRACT" != "1" ] && [ "$HAS_MAKE_CONTRACT" != "1" ]; then
        printf "⛔ No verify:fast contract found — every code/ project needs one.\n"
        printf "   Declare package.json \"verify:fast\" (npm) or a Makefile \"verify-fast:\" target (any stack).\n"
        printf "   No real tests yet? A passing stub is enough — see code/VERIFY.md G5.\n"
        exit 1
      fi
      ;;
  esac

  if [ "$HAS_NPM_CONTRACT" = "1" ] || [ "$HAS_MAKE_CONTRACT" = "1" ]; then
    printf "→ verify:fast…\n"
    if [ "$HAS_NPM_CONTRACT" = "1" ]; then RUN_CMD="npm run --silent verify:fast"; else RUN_CMD="make verify-fast"; fi
    if ! $RUN_CMD >/tmp/verify-fast.$$ 2>&1; then
      tail -30 /tmp/verify-fast.$$
      rm -f /tmp/verify-fast.$$
      printf "⛔ verify:fast is red — fix before committing. Full output: %s\n" "$RUN_CMD"
      exit 1
    fi
    rm -f /tmp/verify-fast.$$
    printf "✓ verify:fast green\n"
  fi
fi

# ── 1c. CONTEXT.md project-goal-link gate — code/<proj>/CONTEXT.md line 3 ─────
case "$TOPLEVEL" in
  /mnt/workspace/code/*)
    if echo "$STAGED" | grep -qx 'CONTEXT.md'; then
      GOAL_LINE3=$(sed -n '3p' "CONTEXT.md" 2>/dev/null)
      if ! printf '%s' "$GOAL_LINE3" | grep -qE '^>\s*goal:\s*(\[[^]]+\]\([^)]+\)|none)\s*$'; then
        printf "⛔ %s/CONTEXT.md missing '> goal:' link on line 3.\n" "$(basename "$TOPLEVEL")"
        printf "   Add '> goal: [slug](../../brain/goals/<slug>.md)' or '> goal: none'.\n"
        exit 1
      fi
    fi
    ;;
esac

# ── 1d. Spec-driven module gate — new module CONTEXT.md must declare '> spec:' ──
# Ratchet/boy-scout: fires ONLY for newly-added CONTEXT.md under code/ (existing modules
# are grandfathered). '> spec: <file>' must point to an existing SPEC.md; '> spec: none'
# opts out. Mirrors the 1c goal-link convention. See code/SPEC-DRIVE.md.
case "$TOPLEVEL" in
  /mnt/workspace/code/*)
    NEW_CONTEXTS=$(git diff --cached --name-only --diff-filter=A 2>/dev/null | grep -E '(^|/)CONTEXT\.md$' || true)
    if [ -n "$NEW_CONTEXTS" ]; then
      while IFS= read -r ctx; do
        [ -f "$ctx" ] || continue
        SPEC_DECL=$(grep -m1 -E '^>\s*spec:\s*\S' "$ctx" 2>/dev/null | sed -E 's/^>[[:space:]]*spec:[[:space:]]*//' | tr -d '\r' | xargs)
        if [ -z "$SPEC_DECL" ]; then
          printf "⛔ %s missing '> spec:' declaration (new module under code/).\n" "$ctx"
          printf "   Add '> spec: SPEC.md' (author it from code/_templates/module.SPEC.md),\n"
          printf "   or '> spec: none' to opt out. See code/SPEC-DRIVE.md.\n"
          exit 1
        fi
        if [ "$SPEC_DECL" != "none" ]; then
          CTX_DIR=$(dirname "$ctx")
          if [ ! -f "$CTX_DIR/$SPEC_DECL" ]; then
            printf "⛔ %s declares '> spec: %s' but %s/%s is missing.\n" "$ctx" "$SPEC_DECL" "$CTX_DIR" "$SPEC_DECL"
            printf "   Create it from code/_templates/module.SPEC.md, or use '> spec: none'.\n"
            exit 1
          fi
        fi
      done <<< "$NEW_CONTEXTS"
    fi
    ;;
esac

# ── 1e. Git Flow branch gate (code/ repos) ────────────────────────────────────
if [ -x /mnt/workspace/core/hooks/git/gitflow-gate.sh ]; then
  /mnt/workspace/core/hooks/git/gitflow-gate.sh || exit 1
fi

# ── 1g. Tier 0 type gate — .md type allowlist + CONTEXT.md hand-inventory ─────
# Ratchet/boy-scout, same shape as 1c/1d: fires only on files this commit ADDS, so a
# repo that inherited violations is not blocked on every commit. The allowlist is
# parsed from core/SCHEMA.md, never restated. See core/hooks/SPECS.md.
python3 /mnt/workspace/core/hooks/checks/type-gate.py || exit 1

# ── 1h. Tier 0 citation gate — roadmap item numbers cited outside a roadmap ───
# NOT a ratchet: the corpus was swept to zero, so every staged file is checked, not only
# the ones a commit adds. A closed item is deleted, so its number becomes a dead pointer.
python3 /mnt/workspace/core/hooks/checks/citation-gate.py || exit 1

# ── 1f. Nested-gitlink gate (workspace repo) ──────────────────────────────────
if [ -x /mnt/workspace/core/hooks/git/nested-gitlink-gate.sh ]; then
  /mnt/workspace/core/hooks/git/nested-gitlink-gate.sh || exit 1
fi

