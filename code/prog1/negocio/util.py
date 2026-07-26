def calc_preco(empresa):
    return empresa.custo * (1 + empresa.margem)

def calc_disponibilidade(empresa):
    if empresa.oferta > 0:
        return True
    else:
        return False

def comprar(pessoa, empresa):
    empresa.vendas += 1
    empresa.oferta -= 1
    pessoa.patrimonio -= calc_preco(empresa)
    pessoa.conforto += empresa.qualidade

# Pesquisar melhor produto de uma categoria 
def escolher_melhor(categoria, empresas, orcamento):
    melhor_empresa = None
    for empresa in empresas:
        if empresa.categoria == categoria and empresa.oferta > 0:
            preco = calc_preco(empresa)
            if preco <= orcamento:
                if melhor_empresa is None or empresa.qualidade > melhor_empresa.qualidade:
                    melhor_empresa = empresa
                elif empresa.qualidade == melhor_empresa.qualidade:
                    if calc_preco(empresa) < calc_preco(melhor_empresa):
                        melhor_empresa = empresa

    return melhor_empresa

# Pesquisar produto mais barato de uma categoria 
def escolher_barato(categoria, empresas, orcamento):
    melhor_empresa = None
    for empresa in empresas:
        if empresa.categoria == categoria and empresa.oferta > 0:
            preco = calc_preco(empresa)
            if preco <= orcamento:
                if melhor_empresa is None or preco < calc_preco(melhor_empresa):
                    melhor_empresa = empresa

    return melhor_empresa

# Calcular a renda mensal total da pessoa, incluindo renda passiva
def calc_renda_mensal(pessoa):
    return pessoa.salario + (pessoa.patrimonio * 0.005)

def distribuir_produtos(empresas, governo, produtos):
    for instituicao, produto in produtos:
        if instituicao == governo:
            governo.produtos.append(produto)
        else:
            for empresa in empresas:
                if empresa.nome == instituicao:
                    empresa.produtos.append(produto)
                    break