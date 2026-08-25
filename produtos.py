import pandas as pd
import os

ARQUIVO_PRODUTOS = "produtos.csv"


def carregar_produtos():

    if os.path.exists(ARQUIVO_PRODUTOS):

        return pd.read_csv(
            ARQUIVO_PRODUTOS,
            sep=";"
        )

    return pd.DataFrame(
        columns=[
            "codigo",
            "descricao"
        ]
    )


def salvar_produto(
    codigo,
    descricao
):

    df = carregar_produtos()

    codigo = str(codigo).strip()

    if codigo in df["codigo"].astype(str).tolist():

        return False

    novo = pd.DataFrame([{

        "codigo": codigo,
        "descricao": descricao

    }])

    df = pd.concat(
        [df, novo],
        ignore_index=True
    )

    df.to_csv(
        ARQUIVO_PRODUTOS,
        sep=";",
        index=False
    )

    return True