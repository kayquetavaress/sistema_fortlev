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

    st.markdown(
        "### 📊 Painel de Controle"
    )

    df = carregar_dados()

    if df.empty:

        st.warning(
            "Nenhum dado disponível"
        )

        return

    total_registros = len(df)

    peso_total_kg = df["peso"].sum()

    peso_total_t = (
        peso_total_kg / 1000
    )

    total_produtos = (
        df["material"].nunique()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Registros",
        total_registros
    )

    c2.metric(
        "Peso Total (Kg)",
        f"{peso_total_kg:.2f}"
    )

    c3.metric(
        "Peso Total (Ton)",
        f"{peso_total_t:.2f}"
    )

    c4.metric(
        "Produtos",
        total_produtos
    )

    st.markdown("---")

    producao_kg = (
        df.groupby(
            "material"
        )["peso"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    st.subheader(
        "Produção por Produto (Kg)"
    )

    st.bar_chart(
        producao_kg
    )

    producao_t = (
        producao_kg / 1000
    )

    st.subheader(
        "Produção por Produto (Ton)"
    )

    st.bar_chart(
        producao_t
    )

    st.subheader(
        "🏆 Ranking de Produção"
    )

    ranking = (
        producao_kg
        .reset_index()
    )

    st.dataframe(
        ranking.rename(
            columns={
                "material": "Produto",
                "peso": "Peso (Kg)"
            }
        )
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
        
    
