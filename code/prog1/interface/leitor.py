import csv
import json
from classes.pessoa import Pessoa
from classes.empresa import Empresa
from classes.produto import Produto
from classes.governo import Governo

def ler_categorias(caminho='/mnt/workspace/code/prog1/recursos/categorias.json'):
    with open(caminho, 'r', encoding="utf-8") as file:
        categorias = json.load(file)
    return categorias

def ler_pessoas(caminho='/mnt/workspace/code/prog1/recursos/pessoas.txt'):
    with open(caminho, 'r', encoding="utf-8") as file:
        linhas = file.readlines()
        linhas = linhas[1:]  # Ignorar cabeçalho
        pessoas = []
        for linha in linhas:
            nome, patrimonio, salario = linha.strip().split(',')
            pessoa = Pessoa(nome, float(patrimonio), float(salario))
            pessoas.append(pessoa)
        return pessoas

def ler_governo(caminho='/mnt/workspace/code/prog1/recursos/governo.json'):
    with open(caminho, 'r', encoding="utf-8") as file:
        governo_dicionario = json.load(file)

    caixa = governo_dicionario["Caixa"]
    imposto_investimentos = governo_dicionario["Imposto sobre Investimentos"]
    imposto_consumo = governo_dicionario["Imposto sobre Consumo"]
    imposto_renda = governo_dicionario["Imposto de Renda"]
    produtos = governo_dicionario["Produtos"]

    governo = Governo(
        caixa,
        imposto_investimentos,
        imposto_consumo,
        imposto_renda,
        produtos
    )

    return governo

def ler_empresas(caminho='mp8/recursos/empresas.csv'):
    with open(caminho, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Ignorar cabeçalho
        empresas = []
        for row in reader:
            nome, caixa = row
            empresa = Empresa(nome, float(caixa))
            empresas.append(empresa)
        return empresas

def ler_produtos(caminho='mp8/recursos/produtos.csv'):
    with open(caminho, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Ignorar cabeçalho
        produtos = []
        for row in reader:
            instituicao, categoria, nome, custo, preco, qualidade = row
            produto = Produto(categoria, nome, float(custo), float(preco), float(qualidade))
            produtos.append((instituicao, produto))
        return produtos


