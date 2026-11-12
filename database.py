import pandas as pd
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db import engine, registros

COLUNAS = ["id", "codigo", "material", "formulacao", "peso", "usuario"]


def salvar_dado(dado):
    """Grava um registro. Retorna False se já existir um idêntico."""
    novo = {
        "codigo": str(dado["codigo"]).strip(),
        "material": str(dado["material"]).strip().upper(),
        "formulacao": str(dado["formulacao"]).strip().upper(),
        "peso": round(float(dado["peso"]), 2),
        "usuario": dado.get("usuario"),
    }
    try:
        with engine.begin() as conn:
            conn.execute(registros.insert().values(**novo))
    except IntegrityError:
        return False
    return True


def carregar_dados():
    query = select(*[registros.c[c] for c in COLUNAS]).order_by(registros.c.id)
    with engine.connect() as conn:
        df = pd.DataFrame(conn.execute(query).fetchall(), columns=COLUNAS)
    if not df.empty:
        df["peso"] = df["peso"].astype(float)
    return df


def excluir_registro(registro_id):
    with engine.begin() as conn:
        conn.execute(registros.delete().where(registros.c.id == int(registro_id)))


def limpar_banco():
    with engine.begin() as conn:
        conn.execute(registros.delete())
