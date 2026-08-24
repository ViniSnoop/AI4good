---
name: feedback-question-context
description: "toda pergunta de escolha ao Lucas carrega contexto, problema e tradeoffs na própria pergunta e em cada opção"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f8f7f3b9-9269-4185-8aea-130fb0062c3e
  modified: 2026-08-24T18:22:22.181Z
---

Quando eu apresento escolhas ao Lucas (AskUserQuestion, planos, verdicts), **a pergunta e cada
opção precisam explicar o contexto, o problema e os tradeoffs por completo, sem depender do que
foi dito antes na conversa**. Pode e deve sugerir que ele consulte o plano ou a conversa para se
aprofundar — mas o essencial tem que estar ali.

**Why:** capturado por ele em `brain/INBOX.md` em 2026-08-24. O momento da pergunta é um dos
poucos em que a atenção dele é forçada para a conversa; o resto (avanços intermediários, planos
gigantes) ele não consegue acompanhar por completo. Palavras dele: *"tem muitas vezes que
aparecem coisas nas respostas que eu simplesmente 'passo direto', não sei do que se trata."*
Uma opção que só faz sentido para quem leu os 40 turnos anteriores é uma decisão tomada no escuro.

**How to apply:** no texto da pergunta, dizer qual é a decisão e por que ela existe agora. Em
cada opção, dizer o que acontece se escolhida e o que se perde — nunca só o rótulo. Marcar a
recomendada e dizer por quê. Se a opção depende de algo decidido antes, repetir esse algo em uma
linha em vez de referenciar. Vale para qualquer harness, não só Claude Code.
Relacionado: [[feedback-plain-language]], [[feedback-explore-before-cutting]].
