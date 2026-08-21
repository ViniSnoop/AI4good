# ZCode hook-protocol probe: dump what a ZCode hook event delivers (stdin payload, filtered
# env, cwd, ppid) into /tmp/zcode_probe/, so the shim is designed on measured fact rather than
# documentation. Analysis lands in core/experiments/zcode-hook-protocol.md. Temporary — deleted
# once the shim replaces it.
event="${1:-unknown}"
out="/tmp/zcode_probe"
mkdir -p "$out"
n=$(ls "$out" 2>/dev/null | wc -l)
f="$out/$(printf '%03d' "$n")_${event}.txt"
{
  echo "== event:   $event"
  echo "== date:    $(date -Is)"
  echo "== cwd:     $(pwd)"
  echo "== ppid:    $PPID"
  echo "== stdin:"
  cat
  echo "== end stdin"
  echo "== env (filtered):"
  env | grep -iE '^(CLAUDE|ZCODE|SESSION|PROJECT|HOOK)' | sort
  echo "== end env"
} > "$f" 2>&1
exit 0
