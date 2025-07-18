
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Prestação de Contas PNAB", layout="wide")

# Função para exibir os dados de cada projeto
def mostrar_dashboard(titulo, df):
    st.markdown(f"## {titulo}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Valor Total Recebido", f"R$ {df['Valor Recebido'].sum():,.2f}")
    col2.metric("👥 Beneficiários", df['Nome'].nunique())
    col3.metric("📤 IRPF Retido", f"R$ {df['IRPF Retido'].sum():,.2f}")
    col4.metric("🔴 Restos a Pagar", f"R$ {df['Restos a Pagar'].sum():,.2f}")

    st.markdown("### 📊 Distribuição dos Valores Recebidos")
    fig = px.bar(df, x="Nome", y="Valor Recebido", color="Nome", title="Valores por Beneficiário")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Tabela Detalhada")
    st.dataframe(df, use_container_width=True)

# Leitura dos dados
df_baixinho = pd.read_csv("dados_baixinho.csv")
df_pontoes = pd.read_csv("dados_pontoes.csv")

# Abas para navegação
aba1, aba2 = st.tabs(["Projeto 60.006/2024 - Baixinho", "Projeto 60.005/2024 - Pontões"])

with aba1:
    mostrar_dashboard("Projeto PNAB 60.006/2024 – Baixinho", df_baixinho)

with aba2:
    mostrar_dashboard("Projeto PNAB 60.005/2024 – Pontões de Cultura", df_pontoes)
