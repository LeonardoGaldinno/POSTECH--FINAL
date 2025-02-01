import streamlit as st 

col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.title("Introdução")
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
