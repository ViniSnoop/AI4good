# programacao1 — SPECS

## Projeto

Simulador de sociedade em Python puro. Objetivo: simular comportamento social emergente (trabalho, estudo, consumo, empreendedorismo).

**Constraints hard:** só funções, loops, condicionais, listas e dicionários. Sem classes. Sem libs externas.

---

## Architecture Decisions

### AD-01 — Estrutura de arquivos

```
programacao1/
├── main.py                      # entry point + simular_dia/mes
├── rsc/
│   ├── setores.json
│   ├── habilidades.json
│   ├── prod-serv.json
│   ├── populacao_minima.json    # teste mínimo
│   └── populacao_completa.json  # teste completo
└── src/
    ├── setup.py       # carregar_catalogo, criar_pessoa/empresa, criar_simulacao
    ├── qualidade.py   # bonus_qualidade, calcular_qualidade_empresa
    ├── mercado.py     # atualizar_mercado, ajustar_preco_empresa, calcular_custo_sobrevivencia
    ├── decisao.py     # decidir, avaliar_emprego/estudo/empreendimento
    ├── pessoa.py      # trabalhar, estudar, consumir, calcular_bem_estar
    ├── empresa.py     # abrir_empresa, contratar, demitir, produzir
    └── relatorio.py   # relatorio_pessoa/mercado/simulacao
```

### AD-02 — Estruturas de dados principais

**`simulacao`** — wrapper global passado para quase todas as funções:
```python
{
    'dia': 1, 'mes': 1, 'ano': 1,
    'pessoas':  { 'p001': pessoa, ... },   # dict por id — escala para 10k
    'empresas': { 'e001': empresa, ... },  # dict por id
    'mercado':  mercado,
    'catalogo': catalogo,                  # estático, carregado dos JSONs
    'config': {
        'horizonte_decisao_anos': 10,
        'horas_sono_padrao': 8,
        'reserva_meses_seguranca': 3,
    }
}
```

**`catalogo`** — carregado dos JSONs, não muda durante simulação:
```python
{
    'setores':    { 'alimentacao': { 'nome': ..., 'percentual_renda': 0.25 }, ... },
    'habilidades':{ 'cozinheiro':  { 'nome': ..., 'setor_principal': ... }, ... },
    'prodservs':  {
        'refeicao': {
            'setor': 'alimentacao', 'consumidor': 'pessoa',
            'duracao_horas': 8,
            'dependencias': ['processamento_alimentos', 'distribuicao_energia'],
            'homem_hora': {
                'cozinheiro': { 'horas': 0.5, 'nivel_minimo': 1 },
                'atendente':  { 'horas': 0.15, 'nivel_minimo': 1 }
            }
        }
    }
}
```

**`pessoa`**:
```python
{
    'id': 'p001', 'nome': 'Ana',
    'patrimonio': 5000.0,
    'bem_estar': 7,                        # 0-10
    'habilidades': { 'cozinheiro': 3 },    # hab_id: nivel (float via gradiente)
    'empregos': [
        { 'empresa_id': 'e001', 'habilidade_id': 'cozinheiro',
          'horas_dia': 8, 'salario_hora': 20.0 }
    ],
    'estudando': {
        'empresa_id': 'e005', 'habilidade_alvo': 'cozinheiro',
        'horas_totais': 800, 'horas_completadas': 0, 'qualidade_curso': 6
    },                                      # None se não estuda
    'empresa_propria_id': None,
    'prodservs_ativos': [
        { 'prodserv_id': 'aluguel', 'qualidade': 4, 'horas_restantes': 400 }
    ]
}
```

**`empresa`**:
```python
{
    'id': 'e001', 'nome': 'Restaurante X',
    'dono_id': 'p001',
    'prodserv_id': 'refeicao',
    'habilidade_ensinada': None,            # só empresas de educação
    'preco': 25.0,
    'fator_esforco': 1.0,                   # multiplica horas mínimas → bonus qualidade
    'vagas': [
        { 'habilidade_id': 'cozinheiro', 'nivel_minimo': 3,
          'horas_dia': 8, 'salario_hora': 20.0, 'funcionario_id': 'p002' }
    ],
    'estoque_horas': 0.0,                   # horas de produto disponível para venda
    'vendas_30_dias': 0,
}
```

**`mercado`**:
```python
{
    'alimentacao': {
        3: { 'demanda_horas': 1000.0, 'oferta_horas': 800.0, 'preco_medio': 15.0 },
        5: { 'demanda_horas': 600.0,  'oferta_horas': 700.0, 'preco_medio': 25.0 },
    }, ...
}
```

### AD-03 — Regra de qualidade (única, reutilizada em tudo)

```
qualidade_base = min(qualidade de todas as deps + níveis de todos os funcionários)
esforco_ratio  = horas_investidas / horas_minimas_catalogo
bonus          = floor(log2(esforco_ratio))   # cada 2× de esforço = +1 qualidade
qualidade      = min(10, qualidade_base + bonus)
```

Implementação sem lib externa:
```python
def bonus_qualidade(horas_investidas, horas_minimas):
    if horas_investidas <= horas_minimas:
        return 0
    ratio = horas_investidas / horas_minimas
    bonus = 0
    threshold = 2.0
    while ratio >= threshold:
        bonus += 1
        threshold *= 2
    return bonus
```

**Rationale:** qualidade 10 com base 1 custa 512× o mínimo — efetivamente impossível sem bons inputs, mas sem hard cap explícito. 10× para +9 níveis é realista (restaurante Michelin vs fast food).

### AD-04 — Regra de qualidade do estudo (gradiente)

Enquanto estuda:
```python
nivel_atual = qualidade_curso * (horas_completadas / horas_totais)  # float
```
Ao terminar: `habilidades[habilidade_alvo] = qualidade_curso`

**Rationale:** skill aumenta gradualmente, não no fim do curso. Mais realista e evita cliff effects na simulação.

### AD-05 — Regra de decisão (emprego vs estudo vs empreendimento)

```
# Filtro 1 — sobrevivência
reserva_meses = patrimonio / custo_mensal_minimo
se reserva_meses < 3:
    → aceita melhor emprego disponível (modo sobrevivência)

# Fora do modo sobrevivência: projeta 10 anos
horas_livres = 24 - horas_sono - horas_consumo_basico - horas_transporte

melhor_emprego  → avalia vagas disponíveis para habilidades atuais
melhor_estudo   → avalia cursos que maximizam (salario_pos - salario_pre) / duracao
empreendimento  → só se tem capital mínimo E demanda_insatisfeita > 0 no mercado

# Trabalho e estudo são simultâneos (podem coexistir nas 24h)
se ganho_estudo + ganho_emprego > ganho_empreendimento:
    → trabalha + estuda (se horas couberem)
senão se ganho_empreendimento > ganho_emprego:
    → empreende (+ estuda se couber)
senão:
    → só emprego
```

### AD-06 — Fluxo de simulação

- **Decisão:** 1× por dia, bloco (todos decidem antes de qualquer um agir)
- **Ação:** execução do dia inteiro (não hora a hora no MVP)
- **Mês:** fecha contas, atualiza mercado, calcula bem-estar

```
main.py → simular_mes()
  └── simular_dia()
        ├── FASE DECISÃO: para cada pessoa → decidir()
        │     ├── calcular_horas_disponiveis()
        │     ├── calcular_reserva_meses() → calcular_custo_sobrevivencia()
        │     ├── avaliar_emprego()
        │     ├── avaliar_estudo()
        │     └── avaliar_empreendimento()
        └── FASE AÇÃO:
              ├── para cada pessoa: trabalhar, estudar, consumir,
              │                     atualizar_prodservs_ativos, calcular_bem_estar
              └── para cada empresa: produzir → calcular_qualidade_empresa
                                              → bonus_qualidade
                                    ajustar_preco_empresa

  FIM MÊS: atualizar_mercado, relatorio_simulacao
```

### AD-07 — Bem-estar

`bem_estar` (0–10). Decresce quando:
- horas de sono < mínimo
- setor de saúde não atendido
- setor de lazer zerado por muito tempo
- qualquer setor básico não coberto

### AD-08 — Git e repositório

- Projeto mora em `/mnt/workspace/code/programacao1/`
- Repositório GitHub próprio a criar (`lsfcin/programacao1-simulador` ou similar)
- `lsfcin/programming-101` é o repo de referência da disciplina (mp01-mp10), diferente
- Git flow: `main` → `develop` → `funcionalidade/nome` por missão/feature

### AD-09 — Bootstrap de qualidade

Seed population com habilidades 1–9 distribuídas. Sem seed, ninguém chega em qualidade alta porque precisaria de educação de qualidade alta para ter professores de qualidade alta (galinha-ovo).

### AD-10 — Escala

Pessoas/empresas como dicts `{ id: dict }` (não listas). Permite lookup O(1) por id. Essencial para 10k pessoas.

---

## Conventions

- Toda função que modifica estado recebe o dict completo (pessoa, empresa, simulacao) por referência — Python mutates dicts in-place.
- Funções de avaliação (`avaliar_*`) retornam dict `{ganho_10_anos: float, ...detalhes}` — nunca modificam estado.
- `simulacao` é passado inteiro para funções que precisam de cross-reference (empresa precisa de pessoa, etc.).
- Dados estáticos (catalogo) nunca modificados durante simulação.
- IDs gerados como strings (`'p001'`, `'e001'`) — simples, legíveis, sem dependência de lib.
