def agrupar(lista_ordenada, qtd_grupos):
    tamanho = len(lista_ordenada)
    qtd_elementos_grupo = tamanho // qtd_grupos

    lista_agrupamentos = []
    grupo = []

    for elemento in lista_ordenada:
        if len(grupo) < qtd_elementos_grupo:
            grupo.append(elemento)
        else:
            media = sum(grupo) / len(grupo)
            lista_agrupamentos.append(media)
            grupo = [elemento]

    if len(grupo) > 0:
        media = sum(grupo) / len(grupo)
        lista_agrupamentos.append(media)

    return lista_agrupamentos
