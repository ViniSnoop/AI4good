CORES = {
    'W': '\033[37m',
    'G': '\033[32m',
    'B': '\033[34m',
    'R': '\033[31m',
    'Y': '\033[33m',
    'C': '\033[36m',
    'M': '\033[35m',
}
RESET = '\033[0m'


def mostrar_tabela(pessoas):
    if len(pessoas) == 0:
        print("Nenhuma pessoa carregada.")
        return

    nomes = []
    patrimonios = []
    salarios = []

    for pessoa in pessoas:
        nomes.append(pessoa['nome'])
        patrimonio_str = "R$ " + f"{pessoa['patrimonio']:.2f}".replace('.', ',')
        salario_str = "R$ " + f"{pessoa['salario']:.2f}".replace('.', ',')
        patrimonios.append(patrimonio_str)
        salarios.append(salario_str)

    largura_nome = len("Nome")
    for nome in nomes:
        if len(nome) > largura_nome:
            largura_nome = len(nome)

    largura_patrimonio = len("Patrimônio")
    for p in patrimonios:
        if len(p) > largura_patrimonio:
            largura_patrimonio = len(p)

    largura_salario = len("Salário")
    for s in salarios:
        if len(s) > largura_salario:
            largura_salario = len(s)

    cabecalho = f"| {'Nome':<{largura_nome}} | {'Patrimônio':<{largura_patrimonio}} | {'Salário':<{largura_salario}} |"
    separador = f"|{'-' * (largura_nome + 2)}|{'-' * (largura_patrimonio + 2)}|{'-' * (largura_salario + 2)}|"

    print(cabecalho)
    print(separador)

    for i in range(len(pessoas)):
        linha = f"| {nomes[i]:<{largura_nome}} | {patrimonios[i]:<{largura_patrimonio}} | {salarios[i]:<{largura_salario}} |"
        print(linha)


def mostrar_grafico(valores, direcao_cima, linha_horizontal, rotulos_eixo_vertical, valor_base, cor='W', multiplicador_log=0):
    if multiplicador_log != 0:
        if not isinstance(multiplicador_log, int) or multiplicador_log == 1 or multiplicador_log < 0:
            print("Erro: o parâmetro multiplicador_log só é ativado por valores inteiros >= 2, valores diferentes serão ignorados e a escala linear será usada nestes casos.")
            multiplicador_log = 0

    if len(valores) == 0:
        print("Sem dados para mostrar.")
        return

    cor_codigo = CORES.get(cor, CORES['W'])

    valor_max = max(valores)

    niveis = []
    if multiplicador_log == 0:
        nivel = valor_base
        while nivel <= valor_max:
            niveis.append(nivel)
            nivel = nivel + valor_base
    else:
        nivel = valor_base
        while nivel <= valor_max:
            niveis.append(nivel)
            nivel = nivel * multiplicador_log

    if len(niveis) == 0:
        niveis.append(valor_base)

    def formatar_reais(valor):
        return "R$ " + f"{valor:.2f}".replace('.', ',')

    largura_label = 0
    if rotulos_eixo_vertical:
        for nivel in niveis:
            label = formatar_reais(nivel)
            if len(label) > largura_label:
                largura_label = len(label)

    prefixo_vazio = ""
    if rotulos_eixo_vertical:
        prefixo_vazio = " " * (largura_label + 1)

    linha_h = prefixo_vazio + "-" * len(valores)

    def imprimir_nivel(nivel):
        linha = ""
        if rotulos_eixo_vertical:
            label = formatar_reais(nivel)
            linha = label.rjust(largura_label) + " "
        for valor in valores:
            if valor >= nivel:
                linha = linha + cor_codigo + "|" + RESET
            else:
                linha = linha + " "
        print(linha)

    if direcao_cima:
        for i in range(len(niveis) - 1, -1, -1):
            imprimir_nivel(niveis[i])
        if linha_horizontal:
            print(linha_h)
    else:
        if linha_horizontal:
            print(linha_h)
        for i in range(len(niveis)):
            imprimir_nivel(niveis[i])
