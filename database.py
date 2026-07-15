import pandas as pd
import os

ARQUIVO = "dados.csv"


def salvar_dado(dado):

    if os.path.exists(ARQUIVO):
        df = pd.read_csv(ARQUIVO, sep=";")
    else:
        df = pd.DataFrame(columns=[
            "codigo",
            "material",
            "formulacao",
            "peso",
            "turno",
            "data",
            "hora",
            "usuario"
        ])

    # =========================
    # PADRONIZAÇÃO DOS DADOS
    # =========================

    codigo = str(dado["codigo"]).strip()
    material = str(dado["material"]).strip().upper()
    formulacao = str(dado["formulacao"]).strip().upper()
    peso = round(float(dado["peso"]), 2)

    # =========================
    # VERIFICAR DUPLICADO
    # =========================

    if not df.empty:

        df["codigo"] = df["codigo"].astype(str)
        df["material"] = df["material"].astype(str).str.upper()
        df["formulacao"] = df["formulacao"].astype(str).str.upper()
        df["peso"] = df["peso"].astype(float).round(2)

        existe = (
            (df["codigo"] == codigo) &
            (df["material"] == material) &
            (df["formulacao"] == formulacao) &
            (df["peso"] == peso)
        )

        if existe.any():
            return False

    # =========================
    # SALVAR
    # =========================

    novo = pd.DataFrame([{
        "codigo": codigo,
        "material": material,
        "formulacao": formulacao,
        "peso": peso,
        "turno": dado["turno"],
        "data": dado["data"],
        "hora": dado["hora"],
        "usuario": dado["usuario"]
    }])

    df = pd.concat([df, novo], ignore_index=True)

    df.to_csv(
        ARQUIVO,
        index=False,
        sep=";"
    )

    return True


def carregar_dados():

    if os.path.exists(ARQUIVO):
        return pd.read_csv(ARQUIVO, sep=";")

    return pd.DataFrame(columns=[
        "codigo",
        "material",
        "formulacao",
        "peso",
        "turno",
        "data",
        "hora",
        "usuario"
    ])


def limpar_banco():

    df = pd.DataFrame(columns=[
        "codigo",
        "material",
        "formulacao",
        "peso",
        "turno",
        "data",
        "hora",
        "usuario"
    ])

    df.to_csv(
        ARQUIVO,
        index=False,
        sep=";"
    )