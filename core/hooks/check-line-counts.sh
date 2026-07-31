#!/usr/bin/env bash
# Check workspace code file line counts and print warnings/errors.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/limits.env"

: "${WARN_LINES:=150}"
: "${BLOCK_LINES:=200}"

# Which files are code is decided by core/hooks/file_law.py, never by a regex here — this
# script carrying its own list is what let .sh and extensionless scripts past the gate for
# months (core/hooks/pre-commit reached 385 lines unblocked).
is_code() {
  printf '%s\n' "$1" | python3 "$SCRIPT_DIR/file_law.py" --filter-code | grep -q .
}

check_file() {
  local f="$1"
  [ -f "$f" ] || return 0

  is_code "$f" || return 0

  local lines
  lines=$(wc -l < "$f")
  if [ "$lines" -ge "$BLOCK_LINES" ]; then
    printf "🚨 BLOCK: %s (%s lines)\n" "$f" "$lines"
    return 1
  fi

  if [ "$lines" -ge "$WARN_LINES" ]; then
    printf "⚠ WARN: %s (%s lines)\n" "$f" "$lines"
  fi

  return 0
}

found_warn=0
found_block=0
files=()

if [ "${1:-}" = "--from-stdin" ]; then
  while IFS= read -r f; do
    [ -n "$f" ] && files+=("$f")
  done
elif [ "$#" -gt 0 ]; then
  files=("$@")
else
  # No argument: every tracked file, filtered by the same law check_file uses.
  mapfile -t files < <(git ls-files | python3 "$SCRIPT_DIR/file_law.py" --filter-code)
fi

for f in "${files[@]}"; do
  if check_file "$f"; then
    if [ -f "$f" ]; then
      lines=$(wc -l < "$f")
      if [ "$lines" -ge "$WARN_LINES" ] && [ "$lines" -lt "$BLOCK_LINES" ]; then
        found_warn=1
      fi
    fi
  else
    found_block=1
  fi
done

if [ "$found_block" -eq 1 ]; then
  printf "\nOne or more code files exceed the block threshold (%s lines).\n" "$BLOCK_LINES"
  exit 1
fi

if [ "$found_warn" -eq 1 ]; then
  printf "\nOne or more code files exceed the warn threshold (%s lines).\n" "$WARN_LINES"
  exit 0
fi

printf "No code files exceed thresholds.\n"
exit 0
