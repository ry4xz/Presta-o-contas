
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Prestação de Contas PNAB", layout="wide", page_icon="📊")

# Estilo personalizado com CSS para um visual mais moderno
st.markdown("""
    <style>
        .main {
            background-color: #F7F9FB;
        }
        .stButton>button {
            border-radius: 0.75rem;
            background-color: #0066CC;
            color: white;
            font-weight: 600;
            padding: 0.5rem 1rem;
        }
        .stButton>button:hover {
            background-color: #004C99;
        }
        .stMetric {
            background-color: #FFFFFF;
            padding: 1rem;
            border-radius: 1rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    arquivo = "dados/PRESTAÇÃO DE CONTAS PNAB.xlsx"
    planilhas = pd.read_excel(arquivo, sheet_name=None)
    for aba in planilhas:
        planilhas[aba] = planilhas[aba].dropna(how="all", axis=0)
        planilhas[aba] = planilhas[aba].loc[:, ~planilhas[aba].columns.str.contains("^Unnamed")]
    return planilhas

dados = carregar_dados()
abas = list(dados.keys())

# Capa
if "pagina" not in st.session_state:
    st.session_state.pagina = "capa"

if st.session_state.pagina == "capa":
    st.title("📊 Prestação de Contas - PNAB")
    st.markdown("#### Bem-vindo ao painel de prestação de contas. Escolha um projeto para visualizar os detalhes:")

    colunas = st.columns(2)
    for i, aba in enumerate(abas):
        with colunas[i % 2]:
            if st.button(f"📁 {aba}"):
                st.session_state.pagina = aba

# Conteúdo da aba selecionada
else:
    aba_selecionada = st.session_state.pagina
    df = dados[aba_selecionada]

    st.markdown(f"## 📁 Projeto: {aba_selecionada}")
    st.button("🔙 Voltar à capa", on_click=lambda: st.session_state.update({"pagina": "capa"}))
    st.markdown("---")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if "VALOR RECEBIDO" in df.columns:
            st.metric("Valor Recebido", f"R$ {df['VALOR RECEBIDO'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col2:
        if "VALOR PAGO" in df.columns:
            st.metric("Valor Pago", f"R$ {df['VALOR PAGO'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col3:
        if "RETENÇÃO IRPF" in df.columns:
            st.metric("Retenção IRPF", f"R$ {df['RETENÇÃO IRPF'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col4:
        if "RESTANTE A PAGAR" in df.columns:
            st.metric("Restos a Pagar", f"R$ {df['RESTANTE A PAGAR'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col5:
        if "CREDOR" in df.columns:
            st.metric("Contemplados", df['CREDOR'].nunique())

    st.markdown("---")
    st.subheader("📋 Tabela Detalhada")
    st.dataframe(df, use_container_width=True)
