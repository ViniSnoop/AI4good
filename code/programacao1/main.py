import sys
sys.path.insert(0, 'src')

import gerenciador_arquivos
import visualizador
import ordenacao
import agrupamento

ARQUIVO_PESSOAS = 'rsc/pessoas_pequeno.csv'

pessoas = []

print("=== Simulador Social ===")
print()

while True:
    print("Opções: [carregar] [adicionar] [remover] [salvar] [tabela] [salarios] [patrimonios] [grupos] [sair]")
    opcao = input("> ")

    if opcao == "sair" or opcao == "Sair" or opcao == "SAIR":
        print("Encerrando o programa.")
        break

    elif opcao == "carregar":
        pessoas = gerenciador_arquivos.carregar_pessoas(ARQUIVO_PESSOAS)
        print(f"{len(pessoas)} pessoas carregadas.")

    elif opcao == "adicionar":
        nome = input("Nome: ")
        patrimonio = float(input("Patrimônio: "))
        salario = float(input("Salário: "))
        gerenciador_arquivos.adicionar_pessoa(nome, patrimonio, salario, pessoas)
        print(f"'{nome}' adicionado(a).")

    elif opcao == "remover":
        nome = input("Nome da pessoa a remover: ")
        gerenciador_arquivos.remover_pessoa(nome, pessoas)

    elif opcao == "salvar":
        gerenciador_arquivos.salvar_pessoas(ARQUIVO_PESSOAS, pessoas)
        print("Dados salvos.")

    elif opcao == "tabela":
        visualizador.mostrar_tabela(pessoas)

    elif opcao == "salarios":
        salarios = []
        for pessoa in pessoas:
            salarios.append(pessoa['salario'])
        visualizador.mostrar_grafico(salarios, True, True, True, 1250.0, 'W', 2)

    elif opcao == "patrimonios":
        patrimonios = []
        for pessoa in pessoas:
            patrimonios.append(pessoa['patrimonio'])
        visualizador.mostrar_grafico(patrimonios, True, True, True, 1250.0, 'W', 2)

    elif opcao == "grupos":
        patrimonios = []
        for pessoa in pessoas:
            patrimonios.append(pessoa['patrimonio'])
        patrimonios_ordenados = ordenacao.ordenar(patrimonios, True)
        grupos = agrupamento.agrupar(patrimonios_ordenados, 5)
        visualizador.mostrar_grafico(grupos, True, True, True, 1250.0, 'W', 2)

    else:
        print(f"Opção '{opcao}' não reconhecida.")

    print()
