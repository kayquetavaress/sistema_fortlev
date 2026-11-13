"""Conexão com o banco de dados.

Em produção (Railway) usa PostgreSQL via variável DATABASE_URL.
Localmente, sem DATABASE_URL, usa um arquivo SQLite (fortlev.db).
Na primeira execução as tabelas são criadas e populadas com os
CSVs existentes (dados.csv e produtos.csv).
"""

import os

import pandas as pd
from sqlalchemy import (
    Column, DateTime, Integer, MetaData, Numeric, String, Table,
    UniqueConstraint, create_engine, func, inspect,
)


def _url():
    url = os.getenv("DATABASE_URL", "sqlite:///fortlev.db")
    if url.startswith("postgres://"):
        url = "postgresql+psycopg://" + url[len("postgres://"):]
    elif url.startswith("postgresql://"):
        url = "postgresql+psycopg://" + url[len("postgresql://"):]
    return url


engine = create_engine(_url(), pool_pre_ping=True)
metadata = MetaData()

registros = Table(
    "registros", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("codigo", String, nullable=False),
    Column("material", String, nullable=False),
    Column("formulacao", String, nullable=False),
    Column("peso", Numeric(12, 2), nullable=False),
    Column("usuario", String),
    Column("criado_em", DateTime(timezone=True), server_default=func.now()),
    UniqueConstraint("codigo", "material", "formulacao", "peso",
                     name="uq_registro"),
)

produtos = Table(
    "produtos", metadata,
    Column("codigo", String, primary_key=True),
    Column("descricao", String),
)


def _semear(tabela, arquivo, colunas):
    if not os.path.exists(arquivo):
        return
    df = pd.read_csv(arquivo, sep=";", dtype=str).fillna("")
    df = df[[c for c in colunas if c in df.columns]]
    if df.empty:
        return
    if "peso" in df.columns:
        df["peso"] = df["peso"].astype(float).round(2)
    for c in ("material", "formulacao"):
        if c in df.columns:
            df[c] = df[c].str.strip().str.upper()
    df = df.drop_duplicates(
        subset=[c for c in df.columns if c != "usuario" and c != "descricao"]
    )
    with engine.begin() as conn:
        conn.execute(tabela.insert(), df.to_dict("records"))


def _inicializar():
    existentes = set(inspect(engine).get_table_names())
    metadata.create_all(engine)
    if "produtos" not in existentes:
        _semear(produtos, "produtos.csv", ["codigo", "descricao"])
    if "registros" not in existentes:
        _semear(registros, "dados.csv",
                ["codigo", "material", "formulacao", "peso", "usuario"])


_inicializar()
