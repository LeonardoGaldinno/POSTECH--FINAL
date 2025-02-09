import streamlit as st
import pandas as pd
from client.prepare_data import PrepareData
import altair as alt

handler = PrepareData()


st.subheader("Filtros Interativos")
year_range = st.slider("Selecione o período:", 2021, 2024,(2021,2022))

genres = ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"]
selected_genres = st.multiselect("Selecione os gêneros:", genres, default=["Action", "Comedy"])

st.write(year_range)

col1, col2 = st.columns(2)

# ------------------ DF EVOLUÇÃO ----------------------------------#
    
evolucao_classificacao_long = handler.evolucao_classificacao_long()

evolucao_classificacao_long = evolucao_classificacao_long[
        (evolucao_classificacao_long["SiglaPeriodo"] >= year_range[0]) &
        (evolucao_classificacao_long["SiglaPeriodo"] <= year_range[1])
    ]

chart = alt.Chart(evolucao_classificacao_long).mark_bar(point=True).encode(
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

# ------------------ DF EVOLUÇÃO ----------------------------------#

df_escolas_pedra_unpivoted = handler.df_escolas_pedra_unpivoted()

st.write(df_escolas_pedra_unpivoted)

chart = alt.Chart(df_escolas_pedra_unpivoted).mark_bar().encode(
    x='Ano:N',
    y='Valor:Q',
    color='CategoriaEscola_Instituição de ensino:N',
    tooltip=['Ano', 'CategoriaEscola_Instituição de ensino', 'Valor']
).properties(
    width=200,
    height=300
)

text = alt.Chart(df_escolas_pedra_unpivoted).mark_text(dy=-10, color='black').encode(
    x='Ano:N',
    y='Valor:Q',
    text='Valor:Q',
    color='CategoriaEscola_Instituição de ensino:N'
)

final_chart = chart + text


st.altair_chart(final_chart, use_container_width=True)

