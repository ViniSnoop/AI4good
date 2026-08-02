# Frontmatter validation for every layer of the agent library — skills, flows, the
# flow composition DAG, and agents. The law itself is core/SCHEMA.md; these only enforce
# it. Sourced by core/tools/wos/sync-skills; relies on $SRC and $WORKSPACE from the caller.

# Every source skill must carry YAML frontmatter with name + description.
# This is what keeps a non-skill doc (status note, ADR) from leaking into the mirrors.
validate_skills() {
  local rc=0 f name fm
  for f in "$SRC"/*.md; do
    name="$(basename "$f" .md)"
    is_skill "$name" || continue
    if [[ "$(head -1 "$f")" != "---" ]]; then
      echo "INVALID skill (no YAML frontmatter — not a skill): $f"; rc=1; continue
    fi
    fm="$(awk 'NR==1&&/^---[[:space:]]*$/{f=1;next} f&&/^---[[:space:]]*$/{exit} f{print}' "$f")"
    grep -qE '^name:[[:space:]]*\S'        <<<"$fm" || { echo "INVALID skill (missing name:): $f"; rc=1; }
    grep -qE '^description:[[:space:]]*(\S|$)' <<<"$fm" || { echo "INVALID skill (missing description:): $f"; rc=1; }
  done
  return $rc
}

# Flow layer (core/SCHEMA.md): every flow carries description, args, type ∈ enum, confirm ∈ enum.
# Exempt: CONTEXT.md and everything under flows/craft/ — the engineering cluster is its own
# protocol (declares tier routing directly) and has no `type` in the current enum. See SCHEMA.
# Recursive: flows owned by a dispatcher skill live in core/flows/<skill>/ (e.g. research/).
validate_flows() {
  local rc=0 f name fm type confirm
  while IFS= read -r f; do
    name="$(basename "$f" .md)"
    case "$f" in
      */flows/craft/*) continue ;;
    esac
    case "$name" in
      CONTEXT) continue ;;
    esac
    if [[ "$(head -1 "$f")" != "---" ]]; then
      echo "INVALID flow (no YAML frontmatter): $f"; rc=1; continue
    fi
    fm="$(awk 'NR==1&&/^---[[:space:]]*$/{f=1;next} f&&/^---[[:space:]]*$/{exit} f{print}' "$f")"
    grep -qE '^description:[[:space:]]*\S' <<<"$fm" || { echo "INVALID flow (missing description:): $f"; rc=1; }
    grep -qE '^args:[[:space:]]*\S'        <<<"$fm" || { echo "INVALID flow (missing args:): $f"; rc=1; }
    type="$(sed -nE 's/^type:[[:space:]]*(\S+).*/\1/p' <<<"$fm")"
    confirm="$(sed -nE 's/^confirm:[[:space:]]*(\S+).*/\1/p' <<<"$fm")"
    case "$type" in
      research-brief|utility|domain) ;;
      *) echo "INVALID flow (type must be research-brief|utility|domain, got '${type:-<missing>}'): $f"; rc=1 ;;
    esac
    case "$confirm" in
      plan|none) ;;
      *) echo "INVALID flow (confirm must be plan|none, got '${confirm:-<missing>}'): $f"; rc=1 ;;
    esac
  done < <(find "$WORKSPACE/core/flows" -name '*.md')
  return $rc
}

# Composition layer (core/SCHEMA.md § Composition and cycles): the `uses:` graph must be a DAG.
# A definitional cycle never bottoms out — expanding it is infinite. This is the *definition-time*
# guard only; execution loops (a flow retrying its own step) are legal and are bounded by the
# runtime iteration cap declared in the flow, never by this check.
validate_flow_dag() {
  local rc=0 f name fm uses u
  declare -A USES=() KNOWN=() COLOR=()
  while IFS= read -r f; do
    name="$(basename "$f" .md)"
    case "$name" in
      CONTEXT|TREE) continue ;;
    esac
    KNOWN["$name"]=1
    [[ "$(head -1 "$f")" == "---" ]] || continue
    fm="$(awk 'NR==1&&/^---[[:space:]]*$/{f=1;next} f&&/^---[[:space:]]*$/{exit} f{print}' "$f")"
    uses="$(sed -nE 's/^uses:[[:space:]]*(.*)$/\1/p' <<<"$fm" | tr ',' ' ')"
    USES["$name"]="$uses"
  done < <(find "$WORKSPACE/core/flows" -name '*.md')

  for name in "${!USES[@]}"; do
    for u in ${USES[$name]}; do
      [[ -n "${KNOWN[$u]:-}" ]] || { echo "INVALID flow ($name uses unknown flow '$u'): core/flows/**/$name.md"; rc=1; }
    done
  done

  # Iterative DFS with a three-colour walk: 0 unvisited, 1 on the current path, 2 done.
  # Hitting a colour-1 node means the path returned to itself.
  local start stack node
  for start in "${!USES[@]}"; do
    [[ "${COLOR[$start]:-0}" == 0 ]] || continue
    stack=("$start")
    while ((${#stack[@]})); do
      node="${stack[-1]}"
      case "${COLOR[$node]:-0}" in
        0)
          COLOR["$node"]=1
          for u in ${USES[$node]:-}; do
            [[ -n "${KNOWN[$u]:-}" ]] || continue
            case "${COLOR[$u]:-0}" in
              1) echo "INVALID flow (uses: cycle — '$node' uses '$u', which leads back to '$node'): the uses: graph must be a DAG, see core/SCHEMA.md"; rc=1 ;;
              0) stack+=("$u") ;;
            esac
          done
          ;;
        *)
          COLOR["$node"]=2
          unset 'stack[-1]'
          ;;
      esac
    done
  done
  return $rc
}

# Agent layer (core/SCHEMA.md): name, description, tier ∈ enum; workers also need tools + output.
# `lead` is the one orchestrator (tier-only). _template excluded like skills.
validate_agents() {
  local rc=0 f name fm tier
  for f in "$WORKSPACE/core/agents"/*.md; do
    name="$(basename "$f" .md)"
    case "$name" in
      CONTEXT|_template) continue ;;
    esac
    if [[ "$(head -1 "$f")" != "---" ]]; then
      echo "INVALID agent (no YAML frontmatter): $f"; rc=1; continue
    fi
    fm="$(awk 'NR==1&&/^---[[:space:]]*$/{f=1;next} f&&/^---[[:space:]]*$/{exit} f{print}' "$f")"
    grep -qE '^name:[[:space:]]*\S'        <<<"$fm" || { echo "INVALID agent (missing name:): $f"; rc=1; }
    grep -qE '^description:[[:space:]]*\S' <<<"$fm" || { echo "INVALID agent (missing description:): $f"; rc=1; }
    tier="$(sed -nE 's/^tier:[[:space:]]*(\S+).*/\1/p' <<<"$fm")"
    case "$tier" in
      low|medium|high|max) ;;
      *) echo "INVALID agent (tier must be low|medium|high|max, got '${tier:-<missing>}'): $f"; rc=1 ;;
    esac
    if grep -qE '^(model|thinking):' <<<"$fm"; then
      echo "INVALID agent (model:/thinking: forbidden in core source — use tier:): $f"; rc=1
    fi
    if [[ "$name" != lead ]]; then
      grep -qE '^tools:[[:space:]]*\S'  <<<"$fm" || { echo "INVALID agent (worker missing tools:): $f"; rc=1; }
      grep -qE '^output:[[:space:]]*\S' <<<"$fm" || { echo "INVALID agent (worker missing output:): $f"; rc=1; }
    fi
  done
  return $rc
}

