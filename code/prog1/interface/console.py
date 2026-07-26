import os
from negocio import util
from classes.pessoa import Pessoa
from classes.empresa import Empresa

# Códigos das cores de texto em Python
R = '\033[31m' # vermelho
G = '\033[32m' # verde
B = '\033[34m' # azul
Y = '\033[33m' # amarelo
P = '\033[35m' # roxo
C = '\033[36m' # ciano
W = '\033[37m' # branco
i = '\033[3m'  # itálico
n = '\033[7m'  # negativo
r = '\033[0m'  # resetar
p = "\033[F"   # mover o cursor para o começo da linha anterior
u = "\033[A"   # mover o cursor para cima uma linha

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_categorias(categorias):
    print()
    print("[CATEGORIAS]")
    
    soma = 0.0
    print(f"{i}Divisão da renda mensal ", end="")    
    for categoria, percentual in categorias.items(): 
        print(f"| {categoria} ", end="")
        print(f"{Y}{percentual * 100:3.1f}%{r}{i} ", end="")
        soma += percentual
    print(f"{i} | Totalizando {Y}{soma * 100:3.1f}%{r}{i} da renda mensal total.{r}")

def mostrar_pessoas(pessoas, categorias):
    print()
    print("[PESSOAS]")

    # Imprimir as pessoas e seus patrimônios
    max_renda_total = int(max(util.calc_renda_mensal(p) for p in pessoas))
    max_renda_total = 10000
    step = max_renda_total // 10

    print(f"{i}Gráfico de Barras | Legenda: {B}Conforto{r}{i}, {G}Salário{r}{i}, {P}Rendimentos{r}", end="")
    print(f"{i} | Cada traço = R${step:.2f}{r}{B}")

    for conforto in range(10, 1, -1):
        for pessoa in pessoas:
            char = " "
            if pessoa.conforto // len(categorias) >= conforto:
                char = "|"
            print(char, end="")
        print()

    print(f"{r}", end="")
    for pessoa in pessoas:
        print("-", end="")
    print()

    for renda_total in range(step, max_renda_total, step):
        for pessoa in pessoas:
            char = " "
            if util.calc_renda_mensal(pessoa) >= renda_total:
                if pessoa.salario >= renda_total:
                    char = f"{G}|{r}"
                else:
                    char = f"{P}|{r}"
            print(char, end="")
        print()
    print(f"{r}", end="")

def mostrar_empresas(empresas):
    print()
    print("[EMPRESAS]")

    for empresa in empresas:
        print(f"|{empresa.categoria:<11}| "
              f"{empresa.nome:<15}: {empresa.produto:<15} "
              f"{C}Q={empresa.qualidade}{r} Margem: {Y}{empresa.margem * 100:3.1f}%{r}\t"
              f"Custo: {R}R$ {empresa.custo:.2f}{r}\t"
              f"Preço: {G}R$ {util.calc_preco(empresa):.2f}{r}\t"
              f"Lucro T.: {G}R$ {(empresa.vendas * empresa.custo * empresa.margem):.2f}{r}\t"
              f"Vendas: ", end="")
        
        for i in range(empresa.vendas // 5):
            print(f"{G}${r}", end="")

        print()