
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Gestão à Vista - PNAB", layout="wide")

# Estilização
st.markdown("""
    <style>
    .main {
        background-color: #f7f9fa;
    }
    .css-1v0mbdj, .css-ffhzg2 {
        background-color: #f7f9fa !important;
    }
    .stMetric {
        font-size: 28px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Leitura dos dados
df_baixinho = pd.read_csv("dados_baixinho.csv")
df_pontoes = pd.read_csv("dados_pontoes.csv")
df = pd.concat([df_baixinho, df_pontoes], ignore_index=True)

# Título
st.title("📊 Gestão à Vista - Prestação de Contas PNAB")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Recebido", f"R$ {df['Valor Recebido'].sum():,.2f}")
col2.metric("👥 Beneficiários", df['Nome'].nunique())
col3.metric("📤 IRPF Retido", f"R$ {df['IRPF Retido'].sum():,.2f}")
col4.metric("🔴 Restos a Pagar", f"R$ {df['Restos a Pagar'].sum():,.2f}")

# Gráfico de barras
st.markdown("### 🔹 Distribuição dos Valores Recebidos")
fig_bar = px.bar(df, x="Nome", y="Valor Recebido", color="Nome", title="Valores Recebidos por Beneficiário")
st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico de pizza IRPF vs Líquido
st.markdown("### 🔹 IRPF Retido vs Valor Líquido")
valor_irpf = df['IRPF Retido'].sum()
valor_liquido = df['Valor Recebido'].sum() - valor_irpf
fig_pie = px.pie(
    names=["IRPF Retido", "Valor Líquido"],
    values=[valor_irpf, valor_liquido],
    title="Proporção entre IRPF e Valor Líquido"
)
st.plotly_chart(fig_pie, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("<center><sub>Atualizado automaticamente com base nos dados consolidados dos projetos PNAB</sub></center>", unsafe_allow_html=True)
