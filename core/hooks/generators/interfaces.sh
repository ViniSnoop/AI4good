# Generate: language interface stubs — .pyi, .d.ts (js + ts), .dart.api.
# Sourced by core/hooks/pre-commit — a FRAGMENT, not a standalone script:
# it shares $STAGED and may `exit` to reject the commit. Order is fixed by the dispatcher.

# ── 6. Python → .pyi stubs (mypy stubgen) ─────────────────────────────────────
PY_FILES=$(echo "$STAGED" | grep '\.py$' | grep -v '__pycache__' || true)
if [ -n "$PY_FILES" ]; then
  if ! command -v stubgen &>/dev/null; then
    printf "⚠  stubgen not found — .pyi stubs skipped. Install: pip install mypy\n\n"
  else
    while IFS= read -r f; do
      [ -f "$f" ] || continue
      dir=$(dirname "$f")
      if stubgen "$f" -o "$dir" --quiet 2>/dev/null; then
        pyi="${f%.py}.pyi"
        [ -f "$pyi" ] && git add "$pyi"
      else
        printf "⚠  stubgen failed for $f — .pyi not staged\n\n"
      fi
    done <<< "$PY_FILES"
  fi
fi

# ── 7. JavaScript → .d.ts (tsc --allowJs via jsconfig.json) ───────────────────
JS_FILES=$(echo "$STAGED" | grep '\.js$' | grep -v '\.min\.js$' | grep -v '\.config\.js$' || true)
if [ -n "$JS_FILES" ]; then
  if ! command -v tsc &>/dev/null; then
    printf "⚠  tsc not found — .d.ts not generated for JS files.\n"
    printf "   Install: npm install -g typescript\n\n"
  else
    SEEN_DIRS=""
    while IFS= read -r f; do
      [ -f "$f" ] || continue
      cfg=""
      d=$(dirname "$f")
      while [ "$d" != "." ] && [ "$d" != "/" ]; do
        [ -f "$d/jsconfig.json" ] && cfg="$d/jsconfig.json" && break
        [ -f "$d/tsconfig.json" ] && cfg="$d/tsconfig.json" && break
        d=$(dirname "$d")
      done
      if [ -z "$cfg" ]; then
        printf "⚠  No jsconfig.json for $f — .d.ts not generated.\n"
        printf "   Create jsconfig.json with allowJs + declaration settings.\n\n"
        continue
      fi
      proj_dir=$(dirname "$cfg")
      echo "$SEEN_DIRS" | grep -qF "$proj_dir" && continue
      SEEN_DIRS="$SEEN_DIRS $proj_dir"
      if tsc -p "$cfg" --emitDeclarationOnly 2>/dev/null; then
        git add "$proj_dir"/**/*.d.ts 2>/dev/null || true
      else
        printf "⚠  tsc failed in $proj_dir — .d.ts not generated\n\n"
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
    if python3 /mnt/workspace/core/hooks/dart-api-extract.py "$f" 2>/dev/null; then
      dartapi="${f%.dart}.dart.api"
      [ -f "$dartapi" ] && git add "$dartapi"
    else
      printf "⚠  dart-api-extract failed for $f — .dart.api not staged\n\n"
    fi
  done <<< "$DART_FILES"
fi

