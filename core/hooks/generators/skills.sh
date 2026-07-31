# Generate: skill-library mirrors, then validate their frontmatter.
# Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script:
# it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher.

# ── 10a. Skill library sync + frontmatter validation ──────────────────────────
# When a skill source changes, regenerate mirrors (prunes orphans, the failure that
# dangles symlinks and breaks opencode startup) and validate frontmatter. See core/SCHEMA.md.
SKILL_SRC_STAGED=$(echo "$STAGED" | grep -E '^core/skills/.*\.md$' || true)
if [ -n "$SKILL_SRC_STAGED" ]; then
  printf "→ sync-skills…\n"
  if ! /mnt/workspace/core/tools/sync-skills >/tmp/sync-skills.$$ 2>&1; then
    cat /tmp/sync-skills.$$; rm -f /tmp/sync-skills.$$
    printf "⛔ sync-skills failed — invalid skill frontmatter (see core/SCHEMA.md). Fix before committing.\n"
    exit 1
  fi
  cat /tmp/sync-skills.$$; rm -f /tmp/sync-skills.$$
  git add -A /mnt/workspace/.claude/skills /mnt/workspace/.claude/commands /mnt/workspace/.opencode/skills 2>/dev/null || true
  if ! /mnt/workspace/core/tools/sync-skills --check >/tmp/sync-check.$$ 2>&1; then
    cat /tmp/sync-check.$$; rm -f /tmp/sync-check.$$
    printf "⛔ skill mirrors out of sync after regeneration.\n"; exit 1
  fi
  rm -f /tmp/sync-check.$$
  printf "✓ skills synced + validated\n"
fi

