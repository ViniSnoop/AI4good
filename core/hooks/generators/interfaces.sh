# Generate: language interface stubs — .pyi, .d.ts (js + ts), .dart.api.
# Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script:
# it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher.
#
# `interface-stubs` names TWO paths in core/features.txt — this one and postedit/interfaces.sh
# (core/SPECS.md § AD-14). Not a duplicate trigger: this one stages the stub into the commit
# and sweeps stubless siblings, post-edit keeps the stub current inside the session so
# read/pre-read.sh never serves a stale interface. Guarding one would leave the other writing.
if python3 /mnt/workspace/core/hooks/feature_law.py --enabled interface-stubs; then

# ── 6. Python → .pyi stubs (mypy stubgen) ─────────────────────────────────────
# Staged files, PLUS any stubless sibling in the same directories. A .py that entered the
# repo outside Edit/Write — a bash heredoc, a bulk vendoring, a --no-verify commit — was
# never stubbed by anything, and nothing ever looked back: 182 files workspace-wide had no
# interface. Sweeping the touched directories catches the common shape (a directory that
# gained files in one go) without paying a whole-tree scan on every commit. The rest is
# counted in entropy.md so the number is visible instead of merely absent.
PY_FILES=$(echo "$STAGED" | grep '\.py$' | grep -v '__pycache__' || true)
if [ -n "$PY_FILES" ]; then
  if ! command -v stubgen &>/dev/null; then
    printf "⚠  stubgen not found — .pyi stubs skipped. Install: pip install mypy\n\n"
  else
    PY_SWEEP=$(
      { echo "$PY_FILES"
        echo "$PY_FILES" | xargs -I{} dirname {} | sort -u | while IFS= read -r d; do
          for sib in "$d"/*.py; do
            [ -f "$sib" ] && [ ! -f "${sib%.py}.pyi" ] && echo "$sib"
          done
        done
      } | grep -v '^$' | sort -u
    )
    # shellcheck source=/dev/null
    source /mnt/workspace/core/hooks/stubgen/stub_paths.sh
    while IFS= read -r f; do
      [ -f "$f" ] || continue
      if stubgen "$f" -o "$(stub_out_dir "$f")" --quiet 2>/dev/null; then
        pyi="${f%.py}.pyi"
        [ -f "$pyi" ] && git add "$pyi"
      else
        printf "⚠  stubgen failed for $f — .pyi not staged\n\n"
      fi
    done <<< "$PY_SWEEP"
  fi
fi

# ── 7. JavaScript → .d.ts (tsc --allowJs, one file at a time) ─────────────────
# Per file, NOT `tsc -p <jsconfig>`. The project path was silently emitting nothing
# for years and two independent defects had to be fixed for it to emit even once:
# jsconfig.json implies noEmit:true (it is an editor aid — see postedit/interfaces.sh),
# and "outDir": "." lands in tsc's default exclude list, excluding the config's own
# directory. Worse, once both were forced the project path hit TS5055 on every module
# with a sibling .d.ts — our declarations sit beside their sources, so a project build
# reads its own previous output as an input and refuses to overwrite it. The per-file
# call has none of that, is idempotent, and is already what post-edit runs.
JS_FILES=$(echo "$STAGED" | grep '\.js$' | grep -v '\.min\.js$' | grep -v '\.config\.js$' || true)
if [ -n "$JS_FILES" ]; then
  if ! command -v tsc &>/dev/null; then
    printf "⚠  tsc not found — .d.ts not generated for JS files.\n"
    printf "   Install: npm install -g typescript\n\n"
  else
    while IFS= read -r f; do
      [ -f "$f" ] || continue
      d=$(dirname "$f")
      if tsc --allowJs --checkJs false --declaration --emitDeclarationOnly \
             --declarationDir "$d" --target ES2020 "$f" 2>/dev/null; then
        dts="${f%.js}.d.ts"
        [ -f "$dts" ] && git add "$dts"
      else
        printf "⚠  tsc failed for $f — .d.ts not staged\n\n"
      fi
    done <<< "$JS_FILES"
  fi
fi

# ── 8. TypeScript → .d.ts (tsc --incremental, once per project) ───────────────
TS_FILES=$(echo "$STAGED" | grep -E '\.(ts|tsx)$' | grep -v '\.d\.ts$' || true)
if [ -n "$TS_FILES" ]; then
  TSC=""; command -v tsc &>/dev/null && TSC="tsc"
  [ -z "$TSC" ] && [ -x "$HOME/.local/bin/tsc" ] && TSC="$HOME/.local/bin/tsc"
  if [ -z "$TSC" ]; then
    printf "⚠  tsc not found — .d.ts not generated. Install: npm install -g typescript\n\n"
  else
    declare -A _ts_seen
    while IFS= read -r f; do
      [ -f "$f" ] || continue
      proj_root=""
      d=$(dirname "$f")
      while [ "$d" != "." ] && [ "$d" != "/" ]; do
        [ -f "$d/tsconfig.json" ] && proj_root="$d" && break
        d=$(dirname "$d")
      done
      [ -z "$proj_root" ] && continue
      [ -n "${_ts_seen[$proj_root]+x}" ] && continue
      _ts_seen["$proj_root"]=1
      # Pick declarations config
      cfg="$proj_root/tsconfig.json"
      [ -f "$proj_root/tsconfig.declarations.json" ] && cfg="$proj_root/tsconfig.declarations.json"
      # Ensure .tsbuildinfo-declarations is gitignored in this project
      gi="$proj_root/.gitignore"
      if ! grep -qF '.tsbuildinfo-declarations' "$gi" 2>/dev/null; then
        printf '\n.tsbuildinfo-declarations\n' >> "$gi"
        git add "$gi" 2>/dev/null || true
      fi
      # Generate declarations (incremental; || true — partial emit OK for bundler projects)
      "$TSC" -p "$cfg" --emitDeclarationOnly --incremental \
        --tsBuildInfoFile "$proj_root/.tsbuildinfo-declarations" >/dev/null 2>&1 || true
      find "$proj_root" -name '*.d.ts' ! -path '*/node_modules/*' \
        -exec git add {} \; 2>/dev/null || true
      printf "✓ .d.ts generated: %s\n" "$proj_root"
    done <<< "$TS_FILES"
    unset _ts_seen
  fi
fi

# ── 9. Dart → .dart.api stubs ─────────────────────────────────────────────────
DART_FILES=$(echo "$STAGED" | grep '\.dart$' || true)
if [ -n "$DART_FILES" ]; then
  while IFS= read -r f; do
    [ -f "$f" ] || continue
    if python3 /mnt/workspace/core/hooks/stubgen/dart-api-extract.py "$f" 2>/dev/null; then
      dartapi="${f%.dart}.dart.api"
      [ -f "$dartapi" ] && git add "$dartapi"
    else
      printf "⚠  dart-api-extract failed for $f — .dart.api not staged\n\n"
    fi
  done <<< "$DART_FILES"
fi

fi  # interface-stubs

