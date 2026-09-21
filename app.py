import streamlit as st
import os
import pandas as pd
import io


from ocr import ler_imagem
from parser import extrair_dados
from database import salvar_dado, carregar_dados, limpar_banco, ARQUIVO
from produtos import (
    carregar_produtos,
    salvar_produto
)

st.set_page_config(page_title="Sistema Fortlev", layout="wide")

# =========================
# 🎨 ESTILO COMPLETO
# =========================
st.markdown("""
<style>

/* FUNDO */
.main {
    background: linear-gradient(180deg, #1f4e8c, #0f172a);
    color: white;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #0b1a33;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* LOGO GRANDE */
.logo-box {
    border: 3px solid #1F4E8C;
    padding: 20px;
    display: inline-block;
    border-radius: 10px;
    background-color: rgba(31, 78, 140, 0.2);
}

.logo-fortlev {
    font-size: 62px;
    font-weight: bold;
    color: white;
}


.slogan {
    font-size: 14px;
    color: #cbd5e1;
}


/* BOTÕES */
.stButton button {
    background: #1F4E8C;
    color: white;
    border-radius: 10px;
}

/* CARDS */
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

.dev {
    font-size: 11px;
    color: #94a3b8;
    text-align: center;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 🔐 LOGIN
# =========================
USUARIOS = {
    "admin": {
        "senha": "123456",
        "nome": "Administrador"
    },

    "kayque.tg": {
        "senha": "8150",
        "nome": "Kayque Tavares"
    },

    "cia.brunabcs": {
        "senha": "123456",
        "nome": "Bruna"
    },

    "visitante": {
        "senha": "123456",
        "nome": "Visitante"
    }
}


def tela_login():

    st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg, #011F5B, #102a43);
    }

    .login-card {
        background: #ffffff;
        padding: 35px;
        border-radius: 8px;
        box-shadow: 0px 8px 30px rgba(0,0,0,0.4);
    }

    .titulo {
        font-size: 28px;
        font-weight: bold;
        color: #FEFEFA;
        margin-bottom: 10px;
    }

    .subtitulo {
        font-size: 16px;
        color: #FEFEFA;
        margin-bottom: 15px;
    }

    .stButton button {
        background-color: #1F4E8C !important;
        color: white !important;
        width: 100%;
        height: 40px;
        border-radius: 4px;
    }

    div[data-testid="stTextInput"] input {
        background-color: #FEFEFA !important;
        color: black !important;
        border-radius: 4px;
    }

    </style>
    """, unsafe_allow_html=True)


    col_esq, col_centro, col_dir = st.columns([1, 2, 1])

    with col_centro:

        st.markdown(
            "<div class='titulo'>FORTLEV</div>",
            unsafe_allow_html=True
        )

        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        # BOTÃO DE LOGIN
        if st.button("Entrar", key="btn_login"):

            if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:

                st.session_state["logado"] = True
                st.session_state["usuario"] = usuario
                st.session_state["nome_usuario"] = USUARIOS[usuario]["nome"]

                st.rerun()

            else:
                st.error("Credenciais inválidas")


        st.markdown("""
        <div style='font-size:12px; margin-top:10px; color:#666'>
            Desenvolvido por Kayque Tavares Gomes<br>
            2026
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# =========================
# 📂 MENU
# =========================
def menu():

    st.sidebar.markdown("## 💼 Sistema Fortlev")

    st.sidebar.markdown("""
📦 Controle de Inventário  
🏭 Ambiente Industrial  
📊 Monitoramento de Produção
""")

    opcao = st.sidebar.radio(
    "Selecione uma opção",
    [
        "📸 Leitura de Etiqueta",
        "📊 Painel",
        "📋 Inventário",
        "📦 Cadastro de Produtos"
    ]
)

    st.sidebar.markdown("---")

    st.sidebar.write(f"👤 Usuário atual: {st.session_state.get('usuario')}")

    if st.sidebar.button("🔄 Trocar usuário"):
        st.session_state["logado"] = False
        st.session_state["usuario"] = ""
        st.rerun()

    st.sidebar.markdown("""""", unsafe_allow_html=True)

    return opcao

# =========================
# 📸 UPLOAD
# =========================
def tela_upload():

    st.markdown("### 📸 Leitura de Etiqueta")

    modo = st.radio(
        "Modo de Entrada",
        [
            "📸 Anexar Imagem",
            "⌨️ Digitação Manual"
        ]
    )

    # =========================
    # OCR
    # =========================

    if modo == "📸 Anexar Imagem":

        arquivo = st.file_uploader(
            "Selecione ou tire uma foto",
            type=["jpg", "png", "jpeg"]
        )

        if arquivo:

            if not os.path.exists("imagens"):
                os.makedirs("imagens")

            caminho = os.path.join(
                "imagens",
                arquivo.name
            )

            with open(caminho, "wb") as f:
                f.write(
                    arquivo.getbuffer()
                )

            st.image(
                caminho,
                width=300
            )

            texto = ler_imagem(
                caminho
            )

            dados = extrair_dados(
                texto
            )

            st.subheader(
                "📊 Dados Extraídos"
            )

            st.write(dados)

            if (
                dados
                and dados.get("codigo")
                and dados.get("peso")
            ):

                dados["usuario"] = st.session_state.get(
                    "usuario"
                )

                salvou = salvar_dado(
                    dados
                )

                if salvou:

                    st.success(
                        "✅ Registro salvo"
                    )

                else:

                    st.error(
                        "⚠️ Registro duplicado!"
                    )

            else:

                st.error(
                    "Erro na leitura"
                )
    
# =========================
# MANUAL
# =========================

    else:

        st.subheader(
            "⌨️ Digitação Manual"
        )

        codigo = st.text_input(
            "Código do Produto"
        )

        material_padrao = ""

        try:

            df_produtos = carregar_produtos()

            produto = df_produtos[
                df_produtos["codigo"].astype(str)
                == codigo.strip()
            ]

            if not produto.empty:

                material_padrao = str(
                    produto.iloc[0]["descricao"]
                )

        except:
            pass

        material = st.text_input(
            "Material",
            value=material_padrao,
            disabled=True
        )

        formulacao = st.text_input(
            "Formulação"
        )

        peso = st.number_input(
            "Peso",
            min_value=0.0,
            step=0.01
        )

        operador = st.text_input(
            "Operador"
        )

        turno = st.selectbox(
            "Turno",
            ["", "A", "B", "C", "D"]
        )

        col1, col2 = st.columns(2)

        with col1:

            data = st.date_input(
                "Data de Produção"
            )

        with col2:

            hora = st.time_input(
                "Hora de Produção"
            )

        if st.button(
            "💾 Salvar Registro Manual"
        ):

            dados = {

                "codigo": codigo,
                "material": material,
                "formulacao": formulacao,
                "peso": peso,
                "operador": operador,
                "turno": turno,
                "data": str(data),
                "hora": str(hora),
                "usuario": st.session_state.get(
                    "usuario"
                )

            }

            salvou = salvar_dado(
                dados
            )

            if salvou:

                st.success(
                    "✅ Registro salvo"
                )

            else:

                st.error(
                    "⚠️ Registro duplicado!"
                )
   # =========================
# 📦 PRODUTOS
# =========================

def tela_produtos():

    st.markdown(
        "### 📦 Cadastro de Produtos"
    )

    codigo = st.text_input(
        "Código"
    )

    descricao = st.text_input(
        "Descrição"
    )

    if st.button(
        "Salvar Produto"
    ):

        salvou = salvar_produto(
            codigo,
            descricao
        )

        if salvou:

            st.success(
                "✅ Produto cadastrado!"
            )

        else:

            st.warning(
                "⚠️ Código já existe!"
            )

    st.markdown("---")

    df = carregar_produtos()

    st.dataframe(
        df,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader(
        "🗑️ Excluir Produto"
    )

    if not df.empty:

        produto = st.selectbox(
            "Selecione o código",
            df["codigo"].astype(str)
        )

        if st.button(
            "Excluir Produto"
        ):

            df = df[
                df["codigo"].astype(str)
                != produto
            ]

            df.to_csv(
                "produtos.csv",
                sep=";",
                index=False
            )

            st.success(
                "✅ Produto excluído!"
            )

            st.rerun()     
            
# =========================
# 📊 DASHBOARD
# =========================

def tela_dashboard():

    st.markdown("## 📊 Painel de Controle")
    st.caption("Visão geral dos registros e da produção")

    df = carregar_dados()

    # ==========================================
    # VERIFICAÇÃO
    # ==========================================

    if df.empty:
        st.warning("⚠️ Nenhum dado disponível para exibir no painel.")
        return

    # ==========================================
    # PADRONIZAÇÃO DOS DADOS
    # ==========================================

    df["peso"] = pd.to_numeric(
        df["peso"],
        errors="coerce"
    ).fillna(0)

    df["material"] = (
        df["material"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    df["codigo"] = (
        df["codigo"]
        .astype(str)
        .str.strip()
    )

    if "formulacao" in df.columns:
        df["formulacao"] = (
            df["formulacao"]
            .astype(str)
            .str.upper()
            .str.strip()
        )

    # ==========================================
    # FILTROS
    # ==========================================

    st.markdown("### 🔎 Filtros")

    col1, col2, col3 = st.columns(3)

    with col1:

        produtos = ["Todos"] + sorted(
            df["material"]
            .dropna()
            .unique()
            .tolist()
        )

        produto_selecionado = st.selectbox(
            "📦 Produto",
            produtos
        )

    with col2:

        codigos = ["Todos"] + sorted(
            df["codigo"]
            .dropna()
            .unique()
            .tolist()
        )

        codigo_selecionado = st.selectbox(
            "🔢 Código",
            codigos
        )

    with col3:

        if "formulacao" in df.columns:

            formulacoes = ["Todos"] + sorted(
                df["formulacao"]
                .dropna()
                .unique()
                .tolist()
            )

            formulacao_selecionada = st.selectbox(
                "🧪 Formulação",
                formulacoes
            )

        else:

            formulacao_selecionada = "Todos"

    # ==========================================
    # APLICAÇÃO DOS FILTROS
    # ==========================================

    df_filtrado = df.copy()

    if produto_selecionado != "Todos":

        df_filtrado = df_filtrado[
            df_filtrado["material"]
            == produto_selecionado
        ]

    if codigo_selecionado != "Todos":

        df_filtrado = df_filtrado[
            df_filtrado["codigo"]
            == codigo_selecionado
        ]

    if (
        formulacao_selecionada != "Todos"
        and "formulacao" in df_filtrado.columns
    ):

        df_filtrado = df_filtrado[
            df_filtrado["formulacao"]
            == formulacao_selecionada
        ]

    # ==========================================
    # INDICADORES PRINCIPAIS
    # ==========================================

    total_registros = len(df_filtrado)

    peso_total = df_filtrado["peso"].sum()

    peso_total_ton = peso_total / 1000

    total_produtos = (
        df_filtrado["material"]
        .nunique()
    )

    peso_medio = (
        df_filtrado["peso"].mean()
        if not df_filtrado.empty
        else 0
    )

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "📦 Registros",
            f"{total_registros:,}".replace(",", ".")
        )

    with c2:

        st.metric(
            "⚖️ Peso Total",
            f"{peso_total:,.2f} kg".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    with c3:

        st.metric(
            "🏭 Produção",
            f"{peso_total_ton:,.2f} Ton".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    with c4:

        st.metric(
            "📊 Média por Registro",
            f"{peso_medio:,.2f} kg".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    # ==========================================
    # ALERTA QUANDO NÃO HÁ RESULTADOS
    # ==========================================

    if df_filtrado.empty:

        st.warning(
            "⚠️ Nenhum registro encontrado com os filtros selecionados."
        )

        return

    # ==========================================
    # PRODUÇÃO POR PRODUTO
    # ==========================================

    st.markdown("---")

    st.markdown("### 📦 Produção por Produto")

    producao_produto = (
        df_filtrado
        .groupby("material")["peso"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    st.bar_chart(
        producao_produto,
        height=350
    )

    # ==========================================
    # DUAS COLUNAS DE ANÁLISE
    # ==========================================

    col_esq, col_dir = st.columns(2)

    # ==========================================
    # RANKING
    # ==========================================

    with col_esq:

        st.markdown("### 🏆 Ranking de Produção")

        ranking = (
            df_filtrado
            .groupby(
                ["codigo", "material"]
            )["peso"]
            .sum()
            .reset_index()
            .sort_values(
                "peso",
                ascending=False
            )
        )

        ranking["peso_ton"] = (
            ranking["peso"] / 1000
        )

        ranking["participacao"] = (
            ranking["peso"]
            / ranking["peso"].sum()
            * 100
        )

        ranking = ranking.rename(
            columns={
                "codigo": "Código",
                "material": "Produto",
                "peso": "Peso (kg)",
                "peso_ton": "Peso (Ton)",
                "participacao": "% Total"
            }
        )

        ranking["Peso (kg)"] = ranking[
            "Peso (kg)"
        ].round(2)

        ranking["Peso (Ton)"] = ranking[
            "Peso (Ton)"
        ].round(2)

        ranking["% Total"] = ranking[
            "% Total"
        ].round(2)

        st.dataframe(
            ranking,
            use_container_width=True,
            hide_index=True
        )

    # ==========================================
    # DISTRIBUIÇÃO DOS REGISTROS
    # ==========================================

    with col_dir:

        st.markdown("### 📋 Registros por Produto")

        quantidade_produto = (
            df_filtrado
            .groupby("material")
            .size()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            quantidade_produto,
            height=350
        )

    # ==========================================
    # ANÁLISE POR USUÁRIO
    # ==========================================

    if "usuario" in df_filtrado.columns:

        st.markdown("---")

        st.markdown("### 👤 Registros por Usuário")

        usuario_df = (
            df_filtrado
            .groupby("usuario")
            .agg(
                Registros=("peso", "count"),
                Peso_Total_kg=("peso", "sum")
            )
            .reset_index()
            .sort_values(
                "Peso_Total_kg",
                ascending=False
            )
        )

        usuario_df["Peso_Total_ton"] = (
            usuario_df["Peso_Total_kg"] / 1000
        )

        usuario_df = usuario_df.rename(
            columns={
                "usuario": "Usuário",
                "Peso_Total_kg": "Peso Total (kg)",
                "Peso_Total_ton": "Peso Total (Ton)"
            }
        )

        usuario_df["Peso Total (kg)"] = (
            usuario_df["Peso Total (kg)"]
            .round(2)
        )

        usuario_df["Peso Total (Ton)"] = (
            usuario_df["Peso Total (Ton)"]
            .round(2)
        )

        st.dataframe(
            usuario_df,
            use_container_width=True,
            hide_index=True
        )

    # ==========================================
    # FORMULAÇÕES
    # ==========================================

    if "formulacao" in df_filtrado.columns:

        st.markdown("---")

        st.markdown("### 🧪 Produção por Formulação")

        formulacao_df = (
            df_filtrado
            .groupby("formulacao")["peso"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            formulacao_df,
            height=300
        )

    # ==========================================
    # RESUMO DOS DADOS
    # ==========================================

    st.markdown("---")

    st.markdown("### 📋 Resumo dos Registros")

    col1, col2, col3 = st.columns(3)

    with col1:

        maior_registro = df_filtrado["peso"].max()

        st.metric(
            "⬆️ Maior Peso",
            f"{maior_registro:.2f} kg"
        )

    with col2:

        menor_registro = df_filtrado["peso"].min()

        st.metric(
            "⬇️ Menor Peso",
            f"{menor_registro:.2f} kg"
        )

    with col3:

        produtos_ativos = (
            df_filtrado["material"]
            .nunique()
        )

        st.metric(
            "📦 Produtos Produzidos",
            produtos_ativos
        )

    # ==========================================
    # TABELA DETALHADA
    # ==========================================

    st.markdown("---")

    with st.expander("🔎 Visualizar registros detalhados"):

        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True
        )

# =========================
# 📋 INVENTÁRIO
# =========================
def tela_inventario():

    st.markdown("### 📋 Inventário")

    df = carregar_dados()

    if not df.empty:

        filtro = st.text_input(
            "🔍 Pesquisar Produto"
        )

        if filtro:

            df = df[
                df["material"].astype(str)
                .str.contains(
                    filtro,
                    case=False,
                    na=False
                )
            ]

        st.markdown("### Inventário")

        df_editado = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic"
        )

        st.markdown("---")

        if st.button(
            "🗑️ Apagar TODOS os registros"
        ):

            limpar_banco()

            st.warning(
                "Todos os registros apagados"
            )

            st.rerun()

        st.markdown("---")

        st.subheader(
            "🗑️ Remover Registro"
        )

        indice = st.number_input(
            "Número da linha",
            min_value=0,
            max_value=len(df)-1,
            step=1
        )

        if st.button(
            "Excluir Registro"
        ):

            df = df.drop(indice)

            df.reset_index(
                drop=True,
                inplace=True
            )

            df.to_csv(
                ARQUIVO,
                index=False,
                sep=";"
            )

            st.success(
                "Registro removido"
            )

            st.rerun()
        st.markdown("---")

        output = io.BytesIO()

        df_editado.to_excel(
            output,
            index=False,
            engine="openpyxl"
        )

        st.download_button(
            "📥 Baixar Excel",
            data=output.getvalue(),
            file_name="inventario.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:

        st.info(
            "Sem registros"
        )

# =========================
# 🚀 CONTROLE PRINCIPAL
# =========================

if "logado" not in st.session_state:
    st.session_state["logado"] = False

# 👉 SE NÃO ESTIVER LOGADO → MOSTRA LOGIN
if not st.session_state["logado"]:
    tela_login()
    st.stop()  # 🔥 ESSA LINHA RESOLVE TUDO


# 👉 SE ESTIVER LOGADO  → MOSTRA SISTEMA
else:
    opcao = menu()

    if opcao == "📸 Leitura de Etiqueta":
        tela_upload()

    elif opcao == "📊 Painel":
        tela_dashboard()

    elif opcao == "📋 Inventário":
        tela_inventario()
        
    elif opcao == "📦 Cadastro de Produtos":
        tela_produtos() 
        
    
