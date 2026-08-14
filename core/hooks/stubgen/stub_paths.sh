# Where a generated stub must be written. Sourced by core/hooks/generators/interfaces.sh
# and core/hooks/postedit/interfaces.sh — a FRAGMENT, not a standalone script.
#
# stubgen mirrors PACKAGE structure under -o, so for a file inside a package it writes
# `<out>/<pkg>/<name>.pyi`, not `<out>/<name>.pyi`. Passing the file's own directory as -o
# therefore produced a mirror of the path inside itself — `scripts/scripts/*.pyi`,
# `engine/tests/unit/<subject>/unit/<subject>/*.pyi` — one per package directory, all
# untracked, deleted by hand three times before the cause was named. The output root has
# to be the directory ABOVE the package root; only then does the mirror land where the
# source is. A non-package directory walks zero times and keeps the old behaviour.

stub_out_dir() {
	local d
	d=$(dirname "$1")
	while [ -f "$d/__init__.py" ]; do
		d=$(dirname "$d")
	done
	printf '%s\n' "$d"
}
