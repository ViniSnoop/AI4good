from negocio   import simulador
from negocio   import util
from interface import leitor
from interface import console

def main():

    console.limpar()

    categorias = leitor.ler_categorias()
    pessoas    = leitor.ler_pessoas()
    governo    = leitor.ler_governo()
    empresas   = leitor.ler_empresas()
    produtos   = leitor.ler_produtos()
    util.distribuir_produtos(empresas, governo, produtos)

    simular = True
    while simular:
        console.limpar()
        print("[SIMULADOR DE RELAÇÕES DE MERCADO]")
    
        console.mostrar_categorias(categorias)
        console.mostrar_pessoas(pessoas, categorias)
        console.mostrar_empresas(empresas)

        # Aperte enter para avançar em 1 mês, digite um número para avançar N meses ou "sair" para encerrar
        resposta = input("\nDigite um número para avançar N meses, 'enter' para avançar 1 mês ou 'sair' para encerrar: ").strip().lower()
        
        if resposta.isdigit():
            meses = int(resposta)
            for _ in range(meses):
                simulador.simular_sociedade(pessoas, empresas, governo, categorias)

        elif resposta == "":
            simulador.simular_sociedade(pessoas, empresas, governo, categorias)

        elif resposta == "sair":
            simular = False

# Iniciar a simulação
if __name__ == "__main__":
    main()