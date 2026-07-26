class Governo:
    def __init__(
            self, 
            caixa, 
            imposto_investimentos, 
            imposto_consumo, 
            imposto_renda, 
            produtos
            ):
        self.caixa = caixa
        self.produtos = produtos
        self.imposto_investimentos = imposto_investimentos
        self.imposto_consumo = imposto_consumo
        self.imposto_renda = imposto_renda