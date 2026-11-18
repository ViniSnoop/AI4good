#!/usr/bin/env python3
"""
Demonstração sem2: FiltroSoberano - Execução de ponta a ponta
AI for Good - Seminário 2 (Demonstração ao vivo)
Mede tempo total, tempo por post e pico de memória real (RSS).
"""

import time
import resource
import laya

print("=== FiltroSoberano · Demonstração sem2 ===")
print("Inicializando modelo Laya (Sistema 1)...")
t0 = time.perf_counter()
agent = laya.Agent()
t_load = time.perf_counter() - t0

posts = [
    {
        "id": 1,
        "tipo": "Alarme e pânico moral",
        "texto": "URGENTE: Compartilhem antes que apaguem! O governo vai confiscar a poupança e fechar igrejas a partir de amanhã se ninguém protestar hoje!!"
    },
    {
        "id": 2,
        "tipo": "Ataque pessoal (caso de falha selecionado)",
        "texto": "Esse economistazinho de meia-tigela não passa de um vendido e incompetente, não tem moral para opinar sobre nada neste país."
    },
    {
        "id": 3,
        "tipo": "Falso dilema",
        "texto": "Ou você apoia incondicionalmente o nosso projeto agora, ou você é a favor do caos e quer destruir a nossa cidade."
    }
]

questions = {
    "tatica": {
        "type": "choice",
        "instructions": "Qual a principal técnica de manipulação retórica presente no texto?",
        "criteria": {
            "panico_moral": "apelo ao medo, alarme social, urgência conspiratória ou ameaça existencial",
            "ataque_pessoal": "ad hominem, desqualificação pessoal, ofensas à honra do interlocutor",
            "falso_dilema": "bifurcação forçada, escolha binária artificial (ou apoia ou é inimigo)",
            "legitimo": "argumentação racional, debate fático sem falácia apelativa",
        },
    },
    "intensidade": {
        "type": "score",
        "instructions": "Qual o grau de apelo emocional apelativo do texto?",
        "criteria": ["baixo", "moderado", "alarmista"],
    },
    "urgencia_fabricada": {
        "type": "noul",
        "instructions": "O texto induz urgência artificial ou pânico para forçar compartilhamento imediato?",
    },
}

t_inferencias = []
for p in posts:
    tp0 = time.perf_counter()
    out = agent.predict(p["texto"], questions)
    duracao_post = time.perf_counter() - tp0
    t_inferencias.append(duracao_post)

    tatica = out["answers"]["tatica"]
    intensidade = out["answers"]["intensidade"]
    urgencia = out["answers"]["urgencia_fabricada"]

    print(f"\n--- Post {p['id']} [{p['tipo']}] ---")
    print(f"Texto: \"{p['texto']}\"")
    print(f"  → Diagnóstico: {tatica['choice']} (confiança: {tatica['probabilities'][tatica['choice']]:.2f})")
    print(f"  → Intensidade do apelo: score {intensidade['score']:.2f}")
    print(f"  → Urgência fabricada: {urgencia['noul']:.2f}")

t_total = time.perf_counter() - t0
mem_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
pico_mb = mem_kb / 1024
pico_gb = mem_kb / (1024 * 1024)

print("\n" + "=" * 50)
print(f"MÉTRICAS DA EXECUÇÃO (tag sem2):")
print(f"  Tempo total (carga + 3 posts): {t_total:.2f} s")
print(f"  Carga do modelo: {t_load:.2f} s")
print(f"  Inferência média por post: {sum(t_inferencias)/len(t_inferencias):.2f} s")
print(f"  Pico de memória real (RSS): {pico_mb:.1f} MB ({pico_gb:.2f} GB)")
print("=" * 50)
