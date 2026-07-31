# Keep generated indexes fresh: the CONTEXT.md routing block and the codegraph.
# Sourced by core/hooks/post-edit.sh — a FRAGMENT, not a standalone script:
# it relies on $file, $dir, $TSC and find_tsconfig from the caller.

# ── Sync CONTEXT.md Routing block — leaf dir only ─────────────────────────────
[ -f "$dir/CONTEXT.md" ] \
    && python3 /mnt/workspace/core/hooks/routing/context_synchronizer.py "$dir" 2>/dev/null

# ── codegraph sync — keep index fresh after every source edit ─────────────────
if [[ "$file" == /mnt/workspace/code/* ]]; then
	case "$file" in
		*.pyi|*.d.ts|*.dart.api|*.texif|*.csvif) : ;;  # generated — skip
		*.py|*.js|*.ts|*.tsx|*.dart|*.jsx)
			cg_root=""; cg_dir=$(dirname "$file")
			while [ "$cg_dir" != "/" ]; do
				[ -d "$cg_dir/.codegraph" ] && cg_root="$cg_dir" && break
				cg_dir=$(dirname "$cg_dir")
			done
			if [ -n "$cg_root" ]; then
				codegraph sync "$cg_root" 2>&1 | head -1
			else
				proj_root=$(echo "$file" | grep -oP '^/mnt/workspace/code/[^/]+')
				[ -n "$proj_root" ] && printf "⚠️  no codegraph index — run: codegraph init %s\n" "$proj_root"
			fi
			;;
	esac
fi
