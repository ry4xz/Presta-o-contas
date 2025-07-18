
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Prestação de Contas PNAB", layout="wide")

# Função para exibir os dados de cada projeto
def mostrar_dashboard(titulo, df):
    # Título fixo na aba
    st.markdown(f"## {titulo}")

    # Estilo de fundo e cabeçalho
    st.markdown("""
    <style>
    .main {
        background-color: #f0f4f8;
    }
    .stButton>button {
        background-color: #4F81BD;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # Adicionando métricas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Valor Total Recebido", f"R$ {df['Valor Recebido'].sum():,.2f}")
    col2.metric("👥 Beneficiários", df['Nome'].nunique())
    col3.metric("📤 IRPF Retido", f"R$ {df['IRPF Retido'].sum():,.2f}")
    col4.metric("🔴 Restos a Pagar", f"R$ {df['Restos a Pagar'].sum():,.2f}")

    # Gráfico de distribuição de valores recebidos
    st.markdown("### 📊 Distribuição dos Valores Recebidos")
    fig = px.bar(df, x="Nome", y="Valor Recebido", color="Nome", title="Valores por Beneficiário")
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de Pizza de IRPF vs Valor Líquido
    st.markdown("### 📈 Distribuição de IRPF Retido vs Valor Líquido")
    pie_data = pd.DataFrame({
        'Categoria': ['IRPF Retido', 'Valor Líquido'],
        'Valor': [df['IRPF Retido'].sum(), df['Valor Recebido'].sum() - df['IRPF Retido'].sum()]
    })
    fig_pie = px.pie(pie_data, names='Categoria', values='Valor', title="IRPF Retido vs Valor Líquido")
    st.plotly_chart(fig_pie, use_container_width=True)

    # Tabela detalhada
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

# Rodapé com data automática
st.markdown(f"### Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
