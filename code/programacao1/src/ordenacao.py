def ordenar(lista_entrada, ascendente=True):
    lista_ordenada = []
    lista_ordenada.append(lista_entrada[0])

    for i in range(1, len(lista_entrada)):
        valor_entrada = lista_entrada[i]
        inserido = False

        for j in range(len(lista_ordenada)):
            if ascendente and valor_entrada < lista_ordenada[j]:
                lista_ordenada.insert(j, valor_entrada)
                inserido = True
                break
            elif not ascendente and valor_entrada > lista_ordenada[j]:
                lista_ordenada.insert(j, valor_entrada)
                inserido = True
                break

        if not inserido:
            lista_ordenada.append(valor_entrada)

    return lista_ordenada
