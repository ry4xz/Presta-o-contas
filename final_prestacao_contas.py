
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestão à Vista - Prestação de Contas", layout="wide")

@st.cache_data
def carregar_dados():
    return pd.read_excel("PRESTAÇÃO DE CONTAS PNAB.xlsx", sheet_name=None)

dados = carregar_dados()

st.title("📊 Gestão à Vista - Prestação de Contas PNAB")

abas_disponiveis = list(dados.keys()) + ["Cadastro de Beneficiários"]

col1, col2, col3 = st.columns(3)
for i, aba in enumerate(abas_disponiveis):
    if i % 3 == 0:
        col = col1
    elif i % 3 == 1:
        col = col2
    else:
        col = col3
    if col.button(f"🔎 {aba}"):
        st.session_state["aba_atual"] = aba

if "aba_atual" not in st.session_state:
    st.session_state["aba_atual"] = abas_disponiveis[0]

aba = st.session_state["aba_atual"]
st.markdown("---")

def formatar_moeda(valor):
    try:
        valor = float(valor)
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

if aba != "Cadastro de Beneficiários":
    df = dados[aba].copy()

    df.replace("None", pd.NA, inplace=True)
    df.dropna(how="all", inplace=True)
    df.fillna("R$ 0,00", inplace=True)

    st.subheader(f"📁 {aba}")
    st.dataframe(df, use_container_width=True)

    # Tentativa de identificar colunas numéricas
    colunas_valores = [col for col in df.columns if df[col].astype(str).str.contains("R\$|\d", regex=True).any()]
    df_numerico = df[colunas_valores].apply(lambda x: pd.to_numeric(x.astype(str).str.replace("R\$", "", regex=True)
                                                                    .str.replace(".", "", regex=False)
                                                                    .str.replace(",", ".", regex=False),
                                                                    errors='coerce'))

    total_recebido = df_numerico.sum().sum()
    valor_pago = df_numerico.iloc[:, 0].sum() if df_numerico.shape[1] > 0 else 0
    retencao = df_numerico.iloc[:, 1].sum() if df_numerico.shape[1] > 1 else 0
    restos = df_numerico.iloc[:, 2].sum() if df_numerico.shape[1] > 2 else 0
    num_pessoas = df.shape[0]

    st.markdown("### 📌 Indicadores do Projeto")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📥 Valor Total Recebido", formatar_moeda(total_recebido))
    c2.metric("📤 Valor Pago", formatar_moeda(valor_pago))
    c3.metric("💰 Retenção IRPF", formatar_moeda(retencao))
    c4.metric("🧾 Restos a Pagar", formatar_moeda(restos))
    c5.metric("👥 Contemplados", f"{num_pessoas} pessoa(s)")

else:
    st.subheader("📇 Cadastro de Beneficiários")
    dados_benef = [
        {"Projeto": "PONTÕES DE CULTURA", "Nome": "2024NE000130", "CPF/CNPJ": "22.222.222/2222-22"},
        {"Projeto": "REDE DE PONTOS", "Nome": "2024NE000123", "CPF/CNPJ": "000.000.000-00"},
        {"Projeto": "PONTÕES DE CULTURA", "Nome": "2024NE000001", "CPF/CNPJ": "111.111.111-11"},
        {"Projeto": "REDE DE PONTOS", "Nome": "2024NE000002", "CPF/CNPJ": "33.333.333/3333-33"},
        {"Projeto": "REDE DE PONTOS", "Nome": "2024NE000321", "CPF/CNPJ": "123.456.789-00"},
    ]
    df_benef = pd.DataFrame(dados_benef)
    st.dataframe(df_benef, use_container_width=True)
