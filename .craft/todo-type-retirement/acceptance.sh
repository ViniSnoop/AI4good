#!/usr/bin/env bash
# Acceptance script for todo-type-retirement (Loop 4a).
# Throwaway — dies with .craft/. Not a pytest, not committed to core/tools/test/.
# Exits 0 only when every check passes. Prints one PASS/FAIL line per criterion.
set -u
ROOT=/mnt/workspace
cd "$ROOT" || { echo "FAIL setup: cannot cd to $ROOT"; exit 1; }
FAIL_COUNT=0
report() { # name ok why
  if [ "$2" -eq 0 ]; then echo "PASS $1"; else echo "FAIL $1: $3"; FAIL_COUNT=$((FAIL_COUNT+1)); fi
}

# C1 — every non-DELETE Fold Map row landed at its destination (pairs from 1-plan.md, hardcoded).
SHORTID_PAIRS=(
  "excalidraw-aula02|brain/goals/teaching-materials.md" "video-carrinho|brain/goals/teaching-materials.md"
  "medir-redesenho|brain/goals/teaching-materials.md" "questionarios-sextas|brain/goals/teaching-materials.md"
  "responder-time|brain/goals/paper-megatruth.md" "aluguel-dia-10|brain/goals/finances.md"
  "gastos-catalogar|brain/goals/home-casinhas.md" "ai4good-book-burning|brain/goals/teaching-materials.md"
  "checkup-metodo|brain/goals/workspace-os.md" "ai4good-pacing-frontier|brain/goals/teaching-materials.md"
  "arxiv-visuals|brain/goals/teaching-materials.md" "brave-conta-padrao|brain/goals/google-migration.md"
  "bolsa-ic|brain/goals/career-ufrpe.md" "progressao-cta|brain/goals/career-ufrpe.md"
  "ppc-ementas-3|brain/goals/burocracia-academica.md" "or-gate-shape|brain/goals/teaching-materials.md"
  "auth-recovery|brain/goals/google-migration.md" "fable-credito|brain/goals/workspace-os.md"
  "nvidia-imagegen|brain/goals/rpg-isoroll.md" "sbc-cotas|brain/goals/burocracia-academica.md"
  "calendar-migrar|brain/goals/google-migration.md" "calendario-ufrpe|brain/goals/teaching-materials.md"
  "drive-sync-method|brain/goals/google-migration.md" "ensino-mapa|brain/goals/google-migration.md"
  "fila-academy|brain/goals/google-migration.md" "fila-branches|brain/goals/google-migration.md"
  "fila-triagem|brain/goals/google-migration.md" "mandato-coletivo|brain/goals/cria.md"
  "plan-mode-default|brain/goals/workspace-os.md" "security-gates|brain/goals/workspace-os.md"
  "graph-native|brain/goals/craft-flows.md" "jcode-custo|brain/goals/workspace-os.md"
  "finetune-libs|brain/goals/local-ai.md"
  "papéis fixos|brain/goals/teaching-materials.md" "jatobá|brain/goals/ecovila.md"
  "gerador de animações|brain/goals/teaching-materials.md"
)
INBOX_PHRASES=("__probe_delete_me" "artigo do svr" "Jake Van Clief" "aceleração de buscas")

C1_FAILS=()
for pair in "${SHORTID_PAIRS[@]}"; do
  id="${pair%%|*}"; dest="${pair#*|}"
  [ -f "$ROOT/$dest" ] && grep -q -- "$id" "$ROOT/$dest" 2>/dev/null || C1_FAILS+=("'$id' not in $dest")
done
for phrase in "${INBOX_PHRASES[@]}"; do
  [ -f "$ROOT/brain/INBOX.md" ] && grep -q -- "$phrase" "$ROOT/brain/INBOX.md" 2>/dev/null || C1_FAILS+=("INBOX phrase '$phrase' missing")
done
n=${#C1_FAILS[@]}
report C1 "$([ "$n" -eq 0 ] && echo 0 || echo 1)" "$n missing — ${C1_FAILS[0]:-}$( [ "$n" -gt 1 ] && echo " (+$((n-1)) more)")"

# C2 — brain/TODO.md gone from disk and from git tracking.
c2r=""; c2bad=0
[ -e "$ROOT/brain/TODO.md" ] && { c2bad=1; c2r="still on disk"; }
git -C "$ROOT" ls-files --error-unmatch brain/TODO.md >/dev/null 2>&1 && { c2bad=1; c2r="${c2r:+$c2r; }still tracked"; }
report C2 "$c2bad" "$c2r"

# C3 — TODO.md gone from core/SCHEMA.md and core/SCHEMA-placement.md.
c3r=""; c3bad=0
grep -q 'TODO\.md' "$ROOT/core/SCHEMA.md" 2>/dev/null && { c3bad=1; c3r="in core/SCHEMA.md"; }
grep -q 'TODO\.md' "$ROOT/core/SCHEMA-placement.md" 2>/dev/null && { c3bad=1; c3r="${c3r:+$c3r; }in core/SCHEMA-placement.md"; }
report C3 "$c3bad" "$c3r"

# C4 — no TODO.md row in brain/CONTEXT.md.
if grep -q 'TODO\.md' "$ROOT/brain/CONTEXT.md" 2>/dev/null; then report C4 1 "row still present"; else report C4 0 ""; fi

# C4b — new files exist, non-trivial, ROADMAP.md has exactly 31 '- [ ]' rows.
c4bbad=0; c4br=""
for f in "brain/goals/google-migration.md" "branches/google-migration/CONTEXT.md" "branches/google-migration/ROADMAP.md"; do
  [ -s "$ROOT/$f" ] || { c4bbad=1; c4br="${c4br:+$c4br; }$f missing/empty"; }
done
if [ -f "$ROOT/branches/google-migration/ROADMAP.md" ]; then
  cnt=$(grep -c '^- \[ \]' "$ROOT/branches/google-migration/ROADMAP.md" 2>/dev/null || echo 0)
  [ "$cnt" -eq 31 ] || { c4bbad=1; c4br="${c4br:+$c4br; }ROADMAP.md has $cnt rows, want 31"; }
fi
report C4b "$c4bbad" "$c4br"

# C5 — no 'life-todo' in the entropy dashboard and its test mirror.
c5r=""; c5bad=0
grep -q 'life-todo' "$ROOT/core/hooks/entropy/dashboard/entropy-dashboard.py" 2>/dev/null && { c5bad=1; c5r="in entropy-dashboard.py"; }
grep -q 'life-todo' "$ROOT/core/tools/test/law/entropy/test_entropy_ledger.py" 2>/dev/null && { c5bad=1; c5r="${c5r:+$c5r; }in test_entropy_ledger.py"; }
report C5 "$c5bad" "$c5r"

# C6 — ROADMAP-ledger.md no longer says "four ledgers".
if grep -qi 'four ledgers' "$ROOT/ROADMAP-ledger.md" 2>/dev/null; then report C6 1 "still present"; else report C6 0 ""; fi

# C7 — pointer integrity: only allowlisted files still mention TODO.md.
ALLOWLIST=("ROADMAP.md" "ROADMAP-ledger.md" "ROADMAP-archive.md" "brain/goals/workspace-os.md"
  "brain/memory/feedback_parallel_sessions.md" "brain/memory/feedback_inbox_ref_task_pairing.md"
  "core/hooks/entropy/entropy_ledger.py")
FENCED_WARN=("brain/memory/feedback_inbox_ref_task_pairing.md" "core/hooks/entropy/entropy_ledger.py")
hits=$(git -C "$ROOT" grep -l 'TODO\.md' 2>/dev/null || true)
c7bad=0; offenders=()
while IFS= read -r f; do
  [ -z "$f" ] && continue
  case "$f" in .craft/todo-type-retirement/*) continue ;; esac
  allowed=0
  for a in "${ALLOWLIST[@]}"; do [ "$f" = "$a" ] && { allowed=1; break; }; done
  if [ "$allowed" -eq 1 ]; then
    for w in "${FENCED_WARN[@]}"; do [ "$f" = "$w" ] && echo "WARN C7: $f is fenced this session — follow-up still open"; done
  else
    c7bad=1; offenders+=("$f")
  fi
done <<< "$hits"
report C7 "$c7bad" "outside allowlist: ${offenders[*]:-}"

# C8 — make verify-fast is green.
if (cd "$ROOT" && make verify-fast) >/tmp/acceptance-verify-fast.log 2>&1; then
  report C8 0 ""
else
  report C8 1 "exited non-zero — see /tmp/acceptance-verify-fast.log"
fi

echo "---"
if [ "$FAIL_COUNT" -eq 0 ]; then echo "ALL CHECKS PASS"; exit 0; else echo "$FAIL_COUNT check(s) FAILED"; exit 1; fi
