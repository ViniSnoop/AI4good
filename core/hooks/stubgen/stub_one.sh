# Generate the interface for ONE file. Sourced by core/hooks/generators/interfaces.sh and
# core/hooks/postedit/interfaces.sh — a FRAGMENT, not a standalone script.
#
# `interface-stubs` is the one feature that needs two wired paths where routing-tables needs none,
# and the reason was never the trigger — both triggers are real and both stay. Pre-commit stages the
# stub and sweeps stubless siblings; post-edit keeps it current inside the session, which is what
# read/pre-read.sh depends on, since it blocks a source read only while the stub beside it is
# current. What was duplicated is the INVOCATION: two copies of the stubgen call and four
# near-identical tsc calls, drifting one flag at a time. One copy each, here.
#
# Each function is silent and returns the tool's own status; the caller owns what to print and
# whether to `git add`, because that is the one thing the two paths really do differently.

# shellcheck source=/dev/null
source /mnt/workspace/core/hooks/stubgen/stub_paths.sh

# emit_pyi <file> — mypy stubgen, into the output root stub_paths.sh computes.
# $STUBGEN wins when the caller set it (post-edit names the venv binary by path); otherwise
# whatever is on PATH. Absent either way is a caller's problem to report, not a silent pass.
emit_pyi() {
	local stubgen="${STUBGEN:-}"
	[ -n "$stubgen" ] && [ ! -x "$stubgen" ] && return 127
	[ -z "$stubgen" ] && { stubgen=$(command -v stubgen) || return 127; }
	"$stubgen" "$1" -o "$(stub_out_dir "$1")" --quiet 2>/dev/null
}

# emit_dts <file> <tsc> — declarations BESIDE the source, one file at a time.
#
# Per file, never `tsc -p <config>`. The project path was silently emitting nothing for years and
# needed two independent fixes to emit once: jsconfig.json implies noEmit:true (it is an editor aid),
# and "outDir": "." lands in tsc's default exclude list, so the config excluded its own directory.
# Forced past both it then hit TS5055 on every module with a sibling .d.ts — our declarations sit
# beside their sources, so a project build reads its own previous output as an input. The per-file
# call has none of that and is idempotent.
#
# The .js arm differs by exactly two flags, which is why this is one function and not two: a second
# copy is how the four calls drifted apart in the first place.
emit_dts() {
	local file="$1" tsc="$2" dir
	dir=$(dirname "$file")
	case "$file" in
		*.js)
			"$tsc" --allowJs --checkJs false --declaration --emitDeclarationOnly \
			       --declarationDir "$dir" --target ES2020 "$file" 2>/dev/null
			;;
		*)
			"$tsc" --declaration --emitDeclarationOnly \
			       --declarationDir "$dir" --target ES2020 --skipLibCheck "$file" 2>/dev/null
			;;
	esac
}
