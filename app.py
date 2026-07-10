import streamlit as st
import os
import pandas as pd
import io

from ocr import ler_imagem
from parser import extrair_dados
from database import salvar_dado, carregar_dados, limpar_banco, ARQUIVO

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

def tela_login():

    # ✅ CSS LIMPO E PROFISSIONAL
    st.markdown("""
    <style>

    /* fundo */
    .stApp {
        background: linear-gradient(135deg, #011F5B, #102a43);
    }

    /* card */
    .login-card {
        background: #ffffff;
        padding: 35px;
        border-radius: 8px;
        box-shadow: 0px 8px 30px rgba(0,0,0,0.4);
    }

    /* título */
    .titulo {
        font-size: 28px;
        font-weight: bold;
        color: #FEFEFA;
        margin-bottom: 10px;
    }

    /* subtítulo */
    .subtitulo {
        font-size: 16px;
        color: #FEFEFA;
        margin-bottom: 15px;
    }

    /* botão */
    .stButton button {
        background-color: #1F4E8C !important;
        color: white !important;
        width: 100%;
        height: 40px;
        border-radius: 4px;
    }

    /* input */
    div[data-testid="stTextInput"] input {
        background-color: #FEFEFA !important;
        color: black !important;
        border-radius: 4px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ✅ CENTRALIZAÇÃO CORRETA
    col_esq, col_centro, col_dir = st.columns([1, 2, 1])

    with col_centro:

       
        st.markdown("<div class='titulo'>FORTLEV</div>", unsafe_allow_html=True)

        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if usuario == "admin" and senha == "1234":   
                st.session_state["logado"] = True
                st.session_state["usuario"] = usuario
                st.rerun()
            elif usuario == "kayque" and senha == "8150":
                st.session_state["logado"] = True
                st.session_state["usuario"] = usuario
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
        ["📸 Leitura de Etiqueta", "📊 Painel", "📋 Inventário"]
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

    arquivo = st.file_uploader("Selecione ou tire uma foto", type=["jpg","png","jpeg"])

    if arquivo:

        if not os.path.exists("imagens"):
            os.makedirs("imagens")

        caminho = os.path.join("imagens", arquivo.name)

        with open(caminho, "wb") as f:
            f.write(arquivo.getbuffer())

        st.image(caminho, width=300)

        texto = ler_imagem(caminho)

        dados = extrair_dados(texto)

        st.subheader("📊 Dados extraídos")
        st.write(dados)

        if dados and dados.get("codigo") and dados.get("peso"):

            dados["usuario"] = st.session_state.get("usuario")

            salvou = salvar_dado(dados)

            if salvou:
                st.success("✅ Registro salvo")
            else:
                st.error("⚠️ Registro duplicado!")

        else:
            st.error("Erro na leitura")

# =========================
# 📊 DASHBOARD
# =========================
def tela_dashboard():

    st.markdown("### 📊 Painel de Controle")

    df = carregar_dados()

    if not df.empty:

        total_registros = len(df)
        peso_total = df["peso"].sum()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class='card'>
                <h3>{total_registros}</h3>
                <p>Total de Registros</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='card'>
                <h3>{peso_total:.2f} kg</h3>
                <p>Peso Total</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 📊 Produção por Material")

        st.bar_chart(df.groupby("material")["peso"].sum())

    else:
        st.warning("Nenhum dado disponível")


# =========================
# 📋 INVENTÁRIO
# =========================
def tela_inventario():

    st.markdown("### 📋 Inventário")

    df = carregar_dados()

    if not df.empty:

        st.dataframe(df)

        # apagar tudo
        st.markdown("---")

        if st.button("🗑️ Apagar TODOS os registros"):
            limpar_banco()
            st.warning("Todos os registros apagados")
            st.rerun()

        # excluir individual
        st.markdown("### 🗑️ Remover registro")

        indice = st.number_input(
            "Número da linha",
            min_value=0,
            max_value=len(df)-1,
            step=1
        )

        if st.button("Excluir registro"):
            df = df.drop(indice)
            df.reset_index(drop=True, inplace=True)
            df.to_csv(ARQUIVO, index=False, sep=";")
            st.success("Registro removido")
            st.rerun()

        # download
        output = io.BytesIO()
        df.to_excel(output, index=False)

        st.download_button(
            "📥 Baixar Excel",
            data=output.getvalue(),
            file_name="relatorio.xlsx"
        )

    else:
        st.info("Sem registros")

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