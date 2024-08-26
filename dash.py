import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Configuração da página
st.set_page_config(layout="wide")

# Título do dashboard
st.markdown("""
    <style>
    .custom-title {
        font-size: 48px;
        font-family: 'Helvetica Neue', sans-serif;
        color: #ffffff;
        text-align: center;
        margin-top: -50px;
    }
    .custom-title img {
        width: 50px;
        vertical-align: middle;
        margin-left: 15px;
    }
    </style>
    <h1 class="custom-title">
        Controle de combustível
        <img src="https://i.postimg.cc/GpNg5TqD/combustivel-1.png" alt="Ícone">
    </h1>
    """, unsafe_allow_html=True)

# Carregar os dados
df = pd.read_csv("consumo.csv", sep=",")
if 'Data' in df.columns:
    df["Data"] = pd.to_datetime(df["Data"], format="%d-%m-%Y", errors='coerce')
    df["Data"] = df["Data"].dt.strftime('%d-%m-%Y')  # Formatar para dia-mês-ano
    df = df.sort_values("Data")
    df["Month"] = df["Data"].apply(lambda x: f"{pd.to_datetime(x, format='%d-%m-%Y').year}-{pd.to_datetime(x, format='%d-%m-%Y').month:02d}")
else:
    st.error("A coluna 'Data' não foi encontrada no arquivo CSV.")

# Remover a coluna 'Selecionado' do DataFrame
if 'Selecionado' in df.columns:
    df.drop(columns=['Selecionado'], inplace=True)

# Função para estilizar a sidebar
def style_sidebar():
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            color: #333333;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .sidebar .sidebar-content h2 {
            color: #4CAF50;
            font-size: 22px;
            text-align: center;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .sidebar .sidebar-content label {
            color: #333333;
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 8px;
            display: block;
        }
        .sidebar .sidebar-content .stSelectbox, .sidebar .sidebar-content .stRadio, .sidebar .sidebar-content .stSlider {
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        </style>
        <div class="sidebar-content">
        <h2>Filtros</h2>
        """, unsafe_allow_html=True)

# Adicionar filtros na sidebar
with st.sidebar:
    style_sidebar()

    month = st.selectbox("Mês", ["Todos"] + list(df["Month"].unique()))
    if month == "Todos":
        df_filtred = df
    else:
        df_filtred = df[df["Month"] == month]

    modelos = ["Todos"] + list(df["Modelo"].unique())
    modelo = st.selectbox("Modelo", modelos)
    if modelo != "Todos":
        df_filtred = df_filtred[df_filtred["Modelo"] == modelo]

    placas = ["Todos"] + list(df["Placa"].unique())
    placa = st.selectbox("Placa", placas)
    if placa != "Todos":
        df_filtred = df_filtred[df_filtred["Placa"] == placa]

    formas_pagamento = ["Todos"] + list(df["Forma de pagamento"].unique())
    forma_pagamento = st.selectbox("Forma de pagamento", formas_pagamento)
    if forma_pagamento != "Todos":
        df_filtred = df_filtred[df_filtred["Forma de pagamento"] == forma_pagamento]

    st.markdown("</div>", unsafe_allow_html=True)

# Layout principal
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Gráficos
with col1:
    fig_date = px.bar(df_filtred, x="Data", y="Valor", color="Modelo", title="Valor abastecido por veículo")
    fig_date.update_layout(
        title_text='Valor abastecido por veículo',
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_date, use_container_width=True)

with col2:
    fig_combustivel = px.bar(df_filtred, x="Data", y="Tipo combustivel", color="Modelo", title="Tipo de combustível", orientation="h")
    fig_combustivel.update_layout(
        title_text='Tipo de combustível',
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_combustivel, use_container_width=True)

with col3:
    valor_total = df_filtred.groupby("Modelo")[["Valor"]].sum().reset_index()
    fig_total = px.bar(valor_total, x="Modelo", y="Valor", title="Valor total por veículo")
    fig_total.update_layout(
        title_text='Valor total por veículo',
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_total, use_container_width=True)

with col4:
    fig_form_pg = px.pie(df_filtred, values="Valor", names="Forma de pagamento", title="Ranking forma de pagamento")
    fig_form_pg.update_layout(
        title_text='Ranking forma de pagamento',
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_form_pg, use_container_width=True)

# Exibir a tabela centralizada e ocupando toda a largura disponível
st.markdown("""
    <style>
    .dataframe-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        width: 100%;
    }
    .dataframe-container .stDataFrame {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Exibir a tabela
select_colums = ["Placa", "Modelo", "Data", "Tipo combustivel", "Valor", "Forma de pagamento"]
df_selected = df_filtred[select_colums]
st.dataframe(df_selected, height=420, use_container_width=True)











