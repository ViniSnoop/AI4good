# Prepare: brain stats + self-healing .gitignore allowlist. Runs first — both stage files.
# Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script:
# it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher.

# ── 0. Brain stats (update goal stats, stage changes into this commit) ─────────
# Only runs when Brain/goals/ files are staged — avoids polluting unrelated commits
if [ -f "brain/GOALS.md" ]; then
  echo "$STAGED" | grep -q '^brain/goals/' && python3 core/hooks/brain/brain_stats.py
fi


# ── 0b. Self-healing .gitignore allowlist (Frente 6 item 2, decided 2026-07-24) ─
/mnt/workspace/core/hooks/git/gitignore-self-heal.sh .

