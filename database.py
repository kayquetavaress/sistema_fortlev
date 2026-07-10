import pandas as pd
import os

ARQUIVO = "dados.csv"

def salvar_dado(dado):

    if os.path.exists(ARQUIVO):
        df = pd.read_csv(ARQUIVO, sep=";")
    else:
        df = pd.DataFrame(columns=[
            "codigo", "material", "formulacao", "peso", "usuario"
        ])

    # =========================
    # 🔥 PADRONIZAÇÃO DOS DADOS
    # =========================
    codigo = str(dado["codigo"]).strip()
    material = str(dado["material"]).strip().upper()
    formulacao = str(dado["formulacao"]).strip().upper()
    peso = round(float(dado["peso"]), 2)

    # =========================
    # 🚫 VERIFICAR DUPLICADO
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
    # ✅ SALVAR
    # =========================
    novo = pd.DataFrame([{
        "codigo": codigo,
        "material": material,
        "formulacao": formulacao,
        "peso": peso,
        "usuario": dado["usuario"]
    }])

    df = pd.concat([df, novo], ignore_index=True)

    df.to_csv(ARQUIVO, index=False, sep=";")

    return True

    # =========================
    # 🚫 BLOQUEIO DE DUPLICADO
    # =========================

    if not df.empty:
        existe = (
            (df["codigo"] == dado["codigo"]) &
            (df["material"] == dado["material"]) &
            (df["formulacao"] == dado["formulacao"]) &
            (df["peso"] == dado["peso"])
        )

        if existe.any():
            return False  # duplicado encontrado

    # =========================
    # ✅ SALVAR NORMAL
    # =========================

    novo = pd.DataFrame([dado])
    df = pd.concat([df, novo], ignore_index=True)

    df.to_csv(ARQUIVO, index=False, sep=";")

    return True



def carregar_dados():
    if os.path.exists(ARQUIVO):
        return pd.read_csv(ARQUIVO, sep=";")
    else:
        return pd.DataFrame(columns=[
            "codigo", "material", "formulacao", "peso", "usuario", "tipo"
        ])


def limpar_banco():
    df = pd.DataFrame(columns=[
        "codigo", "material", "formulacao", "peso", "usuario", "tipo"
    ])
    df.to_csv(ARQUIVO, index=False, sep=";")