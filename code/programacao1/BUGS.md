# programacao1 — Known Bugs

## BUG-001 — `ordenar()` crash em lista vazia

**Arquivo:** `src/ordenacao.py`, linha 3  
**Sintoma:** `IndexError: list index out of range` ao chamar `ordenar([])`.  
**Causa:** `lista_ordenada.append(lista_entrada[0])` antes de checar se lista não está vazia.  
**Status:** Não corrigido.  
**Fix sugerido:** Adicionar `if not lista_entrada: return []` no início da função.
