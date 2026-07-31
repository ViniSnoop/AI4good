# Generate: CONTEXT.md routing blocks and TeX .texif interfaces.
# Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script:
# it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher.

# ── 4. Sync CONTEXT.md Routing block — leaf dirs only ─────────────────────────
# Parent CONTEXT.md files list subdirectory entries (links), not individual files.
# They only need re-sync when a subdir is created/deleted, not on every file edit.
if [ -n "$CODE_FILES" ]; then
  declare -A _ctx_synced
  while IFS= read -r leaf_dir; do
    if [ -z "${_ctx_synced[$leaf_dir]+x}" ]; then
      _ctx_synced["$leaf_dir"]=1
      if [ -f "$leaf_dir/CONTEXT.md" ]; then
        python3 /mnt/workspace/core/hooks/routing/context_synchronizer.py "$leaf_dir" 2>/dev/null \
          && git add "$leaf_dir/CONTEXT.md" 2>/dev/null || true
      fi
    fi
  done < <(echo "$CODE_FILES" | xargs -I{} dirname {} | sort -u)
  unset _ctx_synced
fi

# ── 5b. TeX → .texif interfaces ───────────────────────────────────────────────
TEX_FILES=$(echo "$STAGED" | grep '\.tex$' || true)
if [ -n "$TEX_FILES" ]; then
  while IFS= read -r f; do
    [ -f "$f" ] || continue
    if python3 /mnt/workspace/core/hooks/stubgen/tex-interface-gen.py "$f" 2>/dev/null; then
      texif="${f%.tex}.texif"
      [ -f "$texif" ] && git add "$texif"
    else
      printf "⚠  tex-interface-gen failed for $f — .texif not staged\n\n"
    fi
  done <<< "$TEX_FILES"
fi

