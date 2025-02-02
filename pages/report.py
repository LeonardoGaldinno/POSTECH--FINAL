import streamlit as st
from client.database import BigQuery
import altair as alt 
import matplotlib as plt
client = BigQuery()

periododf = client.load_table('tbDados')

st.header("Base de Dados")
st.write("""
            Para este projeto, utilizamos um conjunto de dados fornecido pela ONG Passos Mágicos, contendo informações educacionais dos estudantes  entre os anos de 2020 e 2024, essenciais para compreender o impacto das ações da ONG no desenvolvimento dos alunos e identificar padrões que possam orientar futuras estratégias.
            """)

st.divider()

### --------------- DF PERÍODO ------------------------------------###
st.markdown("""#### Análise de distribuição da classificação dos alunos.""")

periododf['ClassificacaoDescricao'] = periododf['ClassificacaoDescricao'].map({1: '1 - Bom', 2: '2 - Regular', 3: '3 - Ruim'})


chart = alt.Chart(periododf).mark_bar().encode(
    x=alt.X('ClassificacaoDescricao:N', title='Classificação'),
    y=alt.Y('count()', title='Número de Alunos'),
    color=alt.Color('ClassificacaoDescricao:N', scale=alt.Scale(scheme='viridis'))
).properties(
    width=600,
    height=400
)

st.altair_chart(chart, use_container_width=True)



### --------------- DF PERÍODO ------------------------------------###


st.divider()

### --------------- DF EVOLUÇÃO -----------------------------------###

st.markdown("""#### Análise da evolução das Classificações ao Longo dos Anos""")

alunos_classificacao_3_2021 = periododf[(perjiododf['ClassificacaoDescricao'] == 3) & (periododf['SiglaPeriodo'] == 2021)]
alunos_ids = alunos_classificacao_3_2021['IdAluno'].unique()
evolucao_alunos = periododf[periododf['IdAluno'].isin(alunos_ids)]
evolucao_classificacao = evolucao_alunos.groupby(['SiglaPeriodo', 'ClassificacaoDescricao']).size().unstack(fill_value=0)


fig, ax = plt.subplots(figsize=(10, 6))
for classificacao in evolucao_classificacao.columns:
    ax.plot(evolucao_classificacao.index, evolucao_classificacao[classificacao], marker='o', label=f'Classificação {classificacao}')


ax.set_title('Evolução das Classificações ao Longo dos Anos')
ax.set_xlabel('Ano')
ax.set_ylabel('Número de Alunos')
ax.set_xticks(evolucao_classificacao.index)
ax.legend(title='Classificação')
ax.grid()

st.pyplot(fig)








### --------------- DF EVOLUÇÃO -----------------------------------###





