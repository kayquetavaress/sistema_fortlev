import pandas as pd
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db import engine, produtos


def carregar_produtos():
    query = select(produtos.c.codigo, produtos.c.descricao).order_by(produtos.c.codigo)
    with engine.connect() as conn:
        return pd.DataFrame(conn.execute(query).fetchall(),
                            columns=["codigo", "descricao"])


def salvar_produto(codigo, descricao):
    """Cadastra um produto. Retorna False se o código já existir."""
    try:
        with engine.begin() as conn:
            conn.execute(produtos.insert().values(
                codigo=str(codigo).strip(), descricao=descricao))
    except IntegrityError:
        return False
    return True


def excluir_produto(codigo):
    with engine.begin() as conn:
        conn.execute(produtos.delete().where(produtos.c.codigo == str(codigo)))
