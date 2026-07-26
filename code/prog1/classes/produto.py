class Produto:
    def __init__(self, categoria, nome, custo, preco, qualidade):
        self.categoria = categoria
        self.nome = nome
        self.custo = custo
        self.preco = preco
        self.qualidade = qualidade
        self.margem = preco / custo - 1
        self.oferta = 0
        self.reposicao = 1
        self.aquisicoes = 0
