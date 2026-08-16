# Prepare: brain stats + self-healing .gitignore allowlist. Runs first — both stage files.
# Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script:
# it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher.

# ── 0. Brain stats (update goal stats, stage changes into this commit) ─────────
# Only runs when Brain/goals/ files are staged — avoids polluting unrelated commits.
# Absolute, like every other invocation in the chain: this hook fires in every repo under
# the workspace, and a cwd-relative path only happens to work in the one repo that has
# brain/GOALS.md. The guard hid that, which is why it survived the 2026-07-31 split.
if [ -f "brain/GOALS.md" ]; then
  echo "$STAGED" | grep -q '^brain/goals/' && python3 /mnt/workspace/core/hooks/brain/brain_stats.py
fi


# ── 0b. Self-healing .gitignore allowlist (decided 2026-07-24) ─
/mnt/workspace/core/hooks/git/gitignore-self-heal.sh .

