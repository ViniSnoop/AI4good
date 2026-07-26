from negocio import util
from classes.pessoa import Pessoa
from classes.empresa import Empresa

def simular_sociedade(pessoas, empresas, governo, categorias):
    for empresa in empresas:
        simular_empresa(empresa, governo)

    for pessoa in pessoas:
        simular_pessoa(pessoa, empresas, governo, categorias)
    

def simular_empresa(empresa):
    # Se a oferta zerou quer dizer que a empresa vendeu tudo
    if empresa.oferta == 0:
        empresa.reposicao += 1
        empresa.margem += 0.01

    # Se a oferta está alta, quer dizer que as vendas foram aquém
    elif empresa.oferta > 10:
        empresa.reposicao = max(0, empresa.reposicao - 1)
        if(empresa.margem > 0.01):
            empresa.margem -= 0.01

    # Repor o estoque de produtos
    empresa.oferta += empresa.reposicao  # Exemplo de reposição de estoque
    empresa.vendas = 0  # Resetar vendas após reposição

def simular_pessoa(pessoa, empresas, categorias):
    # Reinicializar conforto da pessoa
    pessoa.conforto = 0.0

    # Fazer compras dentro do orçamento para cada categoria
    # e atualizar o conforto da pessoa

    # Renda passiva
    # Aplicar o percentual de rendimento no patrimônio da pessoa como renda passiva
    renda_mensal = util.calc_renda_mensal(pessoa)

    pessoa.patrimonio += renda_mensal  # Atualizar patrimônio com a renda total

    for categoria, percentual in categorias.items():
        # Comprar o produto de melhor qualidade
        # que caiba no orçamento da pessoa para aquela categoria
        orcamento = renda_mensal * percentual
        patrimonio = pessoa.patrimonio
        empresa = util.escolher_melhor(categoria, empresas, orcamento)
        if empresa is None:
            empresa = util.escolher_barato(categoria, empresas, patrimonio)

        # Se encontrou um produto, comprar e atualizar o conforto
        if empresa is not None:
            util.comprar(pessoa, empresa)
