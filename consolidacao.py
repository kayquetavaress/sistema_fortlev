from collections import defaultdict

def consolidar(df):
    agrupado = defaultdict(list)
    vistos = set()
    duplicados = []

    for _, linha in df.iterrows():
        material = linha["material"]
        codigo = linha["codigo"]
        peso = linha["peso"]

        identificador = (codigo, peso)

        if identificador in vistos:
            duplicados.append(linha.to_dict())
        else:
            vistos.add(identificador)

        chave = (material, codigo)
        agrupado[chave].append(peso)

    resultado = []

    for (material, codigo), pesos in agrupado.items():
        resultado.append({
            "material": material,
            "codigo": codigo,
            "quantidade": len(pesos),
            "peso_total": sum(pesos),
            "pesos": pesos
        })

    return resultado, duplicados
