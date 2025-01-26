import streamlit as st
import pandas as pd
import altair as alt
from google.cloud import bigquery
import matplotlib.pyplot as plt
import seaborn as sns
from database import BigQuery



st.set_page_config(layout="wide")
client = BigQuery()


st.logo("Passos-magicos-icon-cor-removebg-preview.png", size='large')

tabs = st.tabs(["Introdução", "Relatório", "Dashboard", "Modelo Machine Learning"])

# Tab: Introdução
with tabs[0]:
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.header("Introdução")
            st.write("""
            Bem-vindo(a) ao nosso projeto de análise e previsão de preços do petróleo Brent. 
            Este projeto foi desenvolvido para atender a uma demanda específica de um cliente, 
            que busca insights detalhados e previsões precisas para apoiar suas decisões estratégicas.
            """)

            st.write("""
            Nosso trabalho está dividido em três componentes principais:
            """)
            st.markdown("##### Análise de Dados Históricos")
            st.write("""Realizamos uma análise detalhada dos dados históricos de preços do petróleo Brent, 
            destacando as principais tendências e variações ao longo do tempo. Utilizamos gráficos para ilustrar essas informações 
            de forma clara e compreensível.""")

            st.markdown("##### Dashboard Interativo")
            st.write("""Desenvolvemos um dashboard dinâmico que oferece uma visualização interativa dos preços do petróleo. 
            Este dashboard considera fatores como eventos geopolíticos, crises econômicas e mudanças na demanda global por energia, 
            proporcionando uma compreensão aprofundada das flutuações do mercado.""")

            st.markdown("##### Modelo de Machine Learning")
            st.write("""Criamos um modelo de Machine Learning especializado em séries temporais para prever os preços do petróleo diariamente. 
            Incluímos uma análise de desempenho do modelo e as previsões geradas, demonstrando a eficácia e a aplicabilidade prática do nosso trabalho. O modelo que trouxe uma melhor previsao foi o prophet, usando uma base de dados de 5 anos.""")

            st.write("""O resultado deste projeto é uma combinação de visualizações interativas e previsões precisas que oferecem uma visão 
            abrangente do mercado de petróleo com insights adicionados em um relatório. As informações detalhadas sobre a análise de dados, o dashboard interativo e o 
            modelo de Machine Learning estão disponíveis em suas respectivas abas: Relatório, Dashboard e Modelo Machine Learning.""")


# # streamlit_app.py
# import streamlit as st

# pages = [
#     st.Page("page1.py", title="Page 1", icon="📊")
#     # st.Page("page2.py", title="Page 2", icon="🌀"),
#     # st.Page("page3.py", title="Page 3", icon="🧩"),
# ]

# # Makes pages available, but position="hidden" means it doesn't draw the nav
# # This is equivalent to setting config.toml: client.showSidebarNavigation = false
# page = st.navigation([pages], position="hidden")

# page.run()

# # page1.py
# st.write("Welcome to my app. Explore the sections below.")
# col1, col2, col3 = st.columns(3)
# col1.page_link("page1.py")
# # col2.page_link("page2.py")
# # col3.page_link("page3.py")

# # page2.py
# st.markdown('long_about_text')
# if st.button("Back"):
#     st.switch_page("page1.py")