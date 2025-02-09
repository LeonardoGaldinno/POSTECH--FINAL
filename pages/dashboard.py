import streamlit as st
import pandas as pd
from client.prepare_data from PrepareData

handler = PrepareData()


st.subheader("Filtros Interativos")
year_range = st.slider("Selecione o período:", 2019, 2024,(2020,2022))

genres = ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"]
selected_genres = st.multiselect("Selecione os gêneros:", genres, default=["Action", "Comedy"])

st.write(year_range)

col1, col2 = st.columns(2)

with col1:
    
    evolucao_classificacao_long = handler.evolucao_classificacao_long()
    st.write(evolucao_classificacao_long)
    chart = alt.Chart(evolucao_classificacao_long).mark_line(point=True).encode(
        x='SiglaPeriodo:O',
        y='NumeroDeAlunos:Q',
        color='ClassificacaoDescricao:N',
        tooltip=['SiglaPeriodo', 'ClassificacaoDescricao', 'NumeroDeAlunos']
    ).properties(
        title='Evolução das Classificações ao Longo dos Anos',
        width=600,
        height=400
    )


    st.altair_chart(chart, use_container_width=True)

    

