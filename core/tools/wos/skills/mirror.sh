# Mirror generation for the skill library: listing, symlink mirrors, command-file
# copies, and orphan pruning. Sourced by core/tools/wos/sync-skills — a FRAGMENT that relies
# on $SRC, $MIRRORS and $COMMANDS_DIR from the caller.

# Skill name is the basename without .md, excluding non-skill files.
is_skill() {
  local name="$1"
  case "$name" in
    _template|CONTEXT) return 1 ;;
    *.original)        return 1 ;;
    *)                 return 0 ;;
  esac
}

# A command (slash command) is a top-level skill — NOT a sub-skill.
# Sub-skills have names like "foundry-canvas" where "foundry" is also a skill;
# they're reference docs loaded by the parent router, not invocable commands.
is_command() {
  local name="$1" prefix
  [[ "$name" == *-* ]] || return 0
  prefix="${name%%-*}"
  is_skill "$prefix" && [[ -f "$SRC/$prefix.md" ]] && return 1
  return 0
}

list_skills() {
  local f name
  for f in "$SRC"/*.md; do
    name="$(basename "$f" .md)"
    if is_skill "$name"; then
      printf '%s\n' "$name"
    fi
  done
}

list_commands() {
  local name
  while IFS= read -r name; do
    is_command "$name" && printf '%s\n' "$name"
  done < <(list_skills)
}

sync_mirror() {
  local mirror="$1"
  mkdir -p "$mirror"
  local name target link
  while IFS= read -r name; do
    target="$WORKSPACE/core/skills/$name.md"
    mkdir -p "$mirror/$name"
    link="$mirror/$name/SKILL.md"
    ln -sfn "$target" "$link"
  done < <(list_skills)
}

check_mirror() {
  local mirror="$1" rc=0 name link target existing
  while IFS= read -r name; do
    target="$WORKSPACE/core/skills/$name.md"
    link="$mirror/$name/SKILL.md"
    if [[ ! -L "$link" ]]; then
      echo "MISSING link: $link"; rc=1
    else
      existing="$(readlink "$link")"
      if [[ "$existing" != "$target" ]]; then
        echo "STALE link: $link -> $existing (want $target)"; rc=1
      fi
      if [[ ! -e "$link" ]]; then
        echo "BROKEN link (dangling): $link"; rc=1
      fi
    fi
  done < <(list_skills)
  return $rc
}

# A command file is the skill body relocated to a different directory depth, so a
# straight `cp` leaves every relative link pointing at nothing: `../flows/x.md` in
# core/skills/ means core/flows/x.md, but from .claude/commands/ it resolves to
# .claude/flows/x.md. All 6 relative links across the mirrors were dead this way
# (found 2026-07-30). Rewrite them against the source dir on the way out; the
# staleness check compares the same rendered form, or every file reads as stale.
render_command() {
  python3 - "$1" "$SRC" "$COMMANDS_DIR" <<'PY'
import os, re, sys

src_file, src_dir, dst_dir = sys.argv[1:4]


# Code spans and fences quote syntax rather than link to it — `[what it is](url)`
# in core/skills/inbox.md is the shape a ref entry must take, not a path to fix.
PROTECTED_OR_LINK = re.compile(r'(```.*?```|`[^`\n]+`)|\]\(([^)\s]+)\)', re.DOTALL)


def rewrite(match):
    if match.group(1):
        return match.group(0)
    path, sep, frag = match.group(2).partition('#')
    if not path or path.startswith(('http://', 'https://', 'mailto:')):
        return match.group(0)
    absolute = os.path.normpath(os.path.join(src_dir, path))
    return '](' + os.path.relpath(absolute, dst_dir) + sep + frag + ')'


text = open(src_file, encoding='utf-8').read()
sys.stdout.write(PROTECTED_OR_LINK.sub(rewrite, text))
PY
}

sync_commands() {
  mkdir -p "$COMMANDS_DIR"
  local name
  while IFS= read -r name; do
    render_command "$SRC/$name.md" > "$COMMANDS_DIR/$name.md"
  done < <(list_commands)
}

check_commands() {
  local rc=0 name cmd src
  while IFS= read -r name; do
    cmd="$COMMANDS_DIR/$name.md"
    src="$SRC/$name.md"
    if [[ ! -f "$cmd" ]]; then
      echo "MISSING command: $cmd"; rc=1
    elif ! diff -q <(render_command "$src") "$cmd" >/dev/null 2>&1; then
      echo "STALE command: $cmd (differs from rendered $src)"; rc=1
    fi
  done < <(list_commands)
  return $rc
}

# A mirror dir or command file with no corresponding source skill is an orphan.
# Orphans are the failure that dangles symlinks and breaks opencode startup.
orphans() {
  local action="$1" rc=0 mirror d c name
  for mirror in "${MIRRORS[@]}"; do
    [[ -d "$mirror" ]] || continue
    for d in "$mirror"/*/; do
      [[ -d "$d" ]] || continue
      name="$(basename "$d")"
      if ! is_skill "$name" || [[ ! -f "$SRC/$name.md" ]]; then
        if [[ "$action" == prune ]]; then rm -rf "$d"; echo "pruned orphan mirror: $d"
        else echo "ORPHAN mirror (no source skill): $d"; rc=1; fi
      fi
    done
  done
  for c in "$COMMANDS_DIR"/*.md; do
    [[ -f "$c" ]] || continue
    name="$(basename "$c" .md)"
    if [[ ! -f "$SRC/$name.md" ]] || ! is_command "$name"; then
      if [[ "$action" == prune ]]; then rm -f "$c"; echo "pruned orphan command: $c"
      else echo "ORPHAN command (no source skill): $c"; rc=1; fi
    fi
  done
  return $rc
}

