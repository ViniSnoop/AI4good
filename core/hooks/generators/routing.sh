# Generate: CONTEXT.md routing blocks and TeX .texif interfaces.
# Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script:
# it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher.

# ── 4. Sync CONTEXT.md Routing block — leaf dirs only ─────────────────────────
# Parent CONTEXT.md files list subdirectory entries (links), not individual files.
# They only need re-sync when a subdir is created/deleted, not on every file edit.
#
# $STAGED is --diff-filter=ACM, so a DELETED file is invisible to $CODE_FILES — and a
# directory that LOSES a file is exactly the one whose routing table now names something
# that is gone. The stale row then survived forever, because nothing else re-syncs that
# CONTEXT.md. $STAGED_DELETED is collected by the dispatcher for this one consumer.
# `--filter-code` classifies by name, so it does not need the file to still exist.
DELETED_CODE=$(echo "$STAGED_DELETED" | python3 "$HOOKS_DIR/file_law.py" --filter-code || true)
CTX_DIRTY=$(printf '%s\n%s\n' "$CODE_FILES" "$DELETED_CODE" | grep -v '^$' || true)

if [ -n "$CTX_DIRTY" ]; then
  declare -A _ctx_synced
  while IFS= read -r leaf_dir; do
    if [ -z "${_ctx_synced[$leaf_dir]+x}" ]; then
      _ctx_synced["$leaf_dir"]=1
      if [ -f "$leaf_dir/CONTEXT.md" ]; then
        python3 /mnt/workspace/core/hooks/routing/context_synchronizer.py "$leaf_dir" 2>/dev/null \
          && git add "$leaf_dir/CONTEXT.md" 2>/dev/null || true
      fi
    fi
  done < <(echo "$CTX_DIRTY" | xargs -I{} dirname {} | sort -u)
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

