import csv


def carregar_pessoas(endereco):
    pessoas = []

    arquivo = open(endereco, 'r', encoding='utf-8')
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        pessoa = {
            'nome': linha['nome'],
            'patrimonio': float(linha['patrimonio']),
            'salario': float(linha['salario'])
        }
        pessoas.append(pessoa)

    arquivo.close()
    return pessoas


def adicionar_pessoa(nome, patrimonio, salario, pessoas):
    pessoa = {
        'nome': nome,
        'patrimonio': patrimonio,
        'salario': salario
    }
    pessoas.append(pessoa)


def remover_pessoa(nome, pessoas):
    for i in range(len(pessoas)):
        if pessoas[i]['nome'].lower() == nome.lower():
            pessoas.pop(i)
            print(f"'{nome}' removido(a).")
            return
    print(f"Pessoa '{nome}' não encontrada.")


def salvar_pessoas(endereco, pessoas):
    arquivo = open(endereco, 'w', encoding='utf-8', newline='')
    escritor = csv.DictWriter(arquivo, fieldnames=['nome', 'patrimonio', 'salario'])
    escritor.writeheader()

    for pessoa in pessoas:
        escritor.writerow(pessoa)

    arquivo.close()
