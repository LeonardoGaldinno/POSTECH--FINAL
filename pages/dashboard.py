import streamlit as st
import pandas as pd
from client.prepare_data import PrepareData
import altair as alt

handler = PrepareData()


st.set_page_config(layout="centered")

st.subheader("Filtros Interativos")
year_range = st.slider("Selecione o período:", 2021, 2024,(2021,2022))

col1, col2 = st.columns(2)

with col1:
    schools = []
    st.markdown("""### Selecione a Instituição de Ensino""")
    private_school = st.checkbox("Escolas Particulares")
    public_school = st.checkbox("Escolas Públicas")

    if private_school:
        schools.append("Escolas Particulares")

    if public_school:
        schools.append("Escolas Públicas")

with col2:
    selected_classification = []
    st.markdown("""### Selecione a classificação do aluno""")
    good = st.checkbox("1 - Desempenho Bom ")
    regular = st.checkbox("2 - Desempenho Regular")
    bad = st.checkbox("3 - Desempenho Inferior")

    if good:
        schools.append(1)

    if regular:
        schools.append(2)

    if bad:
        schools.append(3)




# ---------------------------------------------------------------#
        
evolucao_classificacao_long = handler.evolucao_classificacao_long()

evolucao_classificacao_long = evolucao_classificacao_long[
        (evolucao_classificacao_long["SiglaPeriodo"] >= year_range[0]) &
        (evolucao_classificacao_long["SiglaPeriodo"] <= year_range[1])
    ]

evolucao_classificacao_long = evolucao_classificacao_long[
    evolucao_classificacao_long["ClassificacaoDescricao"].isin(selected_classification)
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

# ---------------------------------------------------------------#

df_escolas_pedra_unpivoted = handler.df_escolas_pedra_unpivoted()


df_escolas_pedra_unpivoted = df_escolas_pedra_unpivoted[
        (df_escolas_pedra_unpivoted["Ano"] >= year_range[0]) &
        (df_escolas_pedra_unpivoted["Ano"] <= year_range[1])
    ]

df_escolas_pedra_unpivoted = df_escolas_pedra_unpivoted[
    df_escolas_pedra_unpivoted["CategoriaEscola_Instituição de ensino"].isin(schools)
]


chart = alt.Chart(df_escolas_pedra_unpivoted).mark_bar().encode(
    x='Ano:N',
    y='Valor:Q',
    color='CategoriaEscola_Instituição de ensino:N',
    tooltip=['Ano', 'CategoriaEscola_Instituição de ensino', 'Valor']
).properties(
    width=200,
    height=300,
    title= 'Percentil 80 da Métrica Pedra por Ano e Categoria de Escola'
    )

text = alt.Chart(df_escolas_pedra_unpivoted).mark_text(dy=-10, color='black').encode(
    x='Ano:N',
    y='Valor:Q',
    text='Valor:Q',
    color='CategoriaEscola_Instituição de ensino:N'
)

final_chart = chart + text


st.altair_chart(final_chart, use_container_width=True)


# ---------------------------------------------------------------#

df_escolas_defas_unpivoted = handler.df_escolas_defas_unpivoted()


year_school_data = df_escolas_defas_unpivoted[(df_escolas_defas_unpivoted['Ano'] == year_range[0]) & (df_escolas_defas_unpivoted['Ano'] == year_range[1])]
year_school_data = df_escolas_defas_unpivoted[df_escolas_defas_unpivoted['CategoriaEscola_Instituição de ensino'].isin(schools)]


defasagem_totals = year_school_data.groupby('Defasagem_categoria')['Value'].sum().reset_index()
defasagem_totals["Percentage"] = (defasagem_totals["Value"] / defasagem_totals["Value"].sum()) * 100
        
chart = (
    alt.Chart(defasagem_totals)
    .mark_arc()
    .encode(
        theta=alt.Theta(field="Value", type="quantitative"),
        color=alt.Color(field="Defasagem_categoria", type="nominal", legend=alt.Legend(title="Defasagem Categoria")),
        tooltip=["Defasagem_categoria", "Value", alt.Tooltip("Percentage:Q", format=".1f", title="%")]
    )
    .properties(title=f"Defasagem de alunos no anos {year_range} e {schools}", width=300, height=300)
)
        


st.altair_chart(chart, use_container_width=True)


