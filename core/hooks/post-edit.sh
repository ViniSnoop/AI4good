#!/usr/bin/env bash
# PostToolUse: Edit, Write — regenerates interfaces, checks first-line comment, syncs CONTEXT.md

input_json="${CLAUDE_TOOL_INPUT:-$(cat)}"
file=$(echo "$input_json" | python3 -c \
	"import sys,json; d=json.load(sys.stdin); ti=d.get('tool_input'); ti=ti if isinstance(ti,dict) else d; print(ti.get('file_path',''))" 2>/dev/null)

[ -z "$file" ] || [ ! -f "$file" ] && exit 0

dir=$(dirname "$file")

# Locate tsc (PATH or ~/.local/bin fallback)
TSC=""; command -v tsc &>/dev/null && TSC="tsc"
[ -z "$TSC" ] && [ -x "$HOME/.local/bin/tsc" ] && TSC="$HOME/.local/bin/tsc"

# Walk up to nearest tsconfig.json, stopping at git root
find_tsconfig() {
	local d="$1"
	while [ "$d" != "/" ]; do
		[ -f "$d/tsconfig.json" ] && echo "$d/tsconfig.json" && return
		{ [ -f "$d/.git" ] || [ -d "$d/.git" ]; } && return
		d=$(dirname "$d")
	done
}

HOOKS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Split 2026-07-31 at 208 lines (the cap is 200). It was never blocked because the
# line-count gate could not see .sh files until file_law.py landed. Parts are SOURCED —
# they share $file, $dir, $TSC and find_tsconfig. Order preserved: lint runs last, after
# interfaces.sh has written the .d.ts it needs.
for part in interfaces reminders sync lint; do
  # shellcheck source=/dev/null
  source "$HOOKS_DIR/postedit/$part.sh"
done
