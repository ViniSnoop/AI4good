import laya

agent = laya.Agent()

posts = [
    "URGENTE: Compartilhem antes que apaguem! O governo vai confiscar a poupança e fechar igrejas a partir de amanhã se ninguém protestar hoje!!",
    "Esse economistazinho de meia-tigela não passa de um vendido e incompetente, não tem moral para opinar sobre nada neste país.",
    "Ou você apoia incondicionalmente o nosso projeto agora, ou você é a favor do caos e quer destruir a nossa cidade.",
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

for i, post in enumerate(posts, 1):
    out = agent.predict(post, questions)
    tatica = out["answers"]["tatica"]
    intensidade = out["answers"]["intensidade"]
    urgencia = out["answers"]["urgencia_fabricada"]

    print(f"--- Post {i} ---")
    print(f"Texto: {post}")
    print(f"  [Diagnóstico]: {tatica['choice']} (prob: {tatica['probabilities'][tatica['choice']]:.2f})")
    print(f"  [Intensidade de Apelo]: score {intensidade['score']:.2f} ({intensidade['probabilities']})")
    print(f"  [Urgência Fabricada]: {urgencia['noul']:.2f}")
    print()
