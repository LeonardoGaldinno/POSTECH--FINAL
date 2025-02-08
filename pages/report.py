import streamlit as st
from client.database import BigQuery
from client.prepare_data import PrepareData
import altair as alt 
import matplotlib.pyplot as plt
import seaborn as sns


handler = PrepareData()
client = BigQuery()
periododf = client.load_table('tbDados')

st.header("Base de Dados")
st.write("""
            Para este projeto, utilizamos um conjunto de dados fornecido pela ONG Passos Mágicos, contendo informações educacionais dos estudantes  entre os anos de 2020 e 2024, essenciais para compreender o impacto das ações da ONG no desenvolvimento dos alunos e identificar padrões que possam orientar futuras estratégias.
            """)

st.divider()

### --------------- DF PERÍODO ------------------------------------###
st.markdown("""#### Análise de distribuição da classificação dos alunos.""")

df_distribuicao = periododf.copy()

df_distribuicao['ClassificacaoDescricao'] = df_distribuicao['ClassificacaoDescricao'].map({1: '1 - Bom', 2: '2 - Regular', 3: '3 - Ruim'})


chart = alt.Chart(df_distribuicao).mark_bar().encode(
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



alunos_classificacao_3_2021 = periododf[(periododf['ClassificacaoDescricao'] == 3) & (periododf['SiglaPeriodo'] == 2021)]

# Obter os IDs dos aluno
alunos_ids = alunos_classificacao_3_2021['IdAluno'].unique()

# Filtrar os dados para esses alunos nos anos subsequentes
evolucao_alunos = periododf[periododf['IdAluno'].isin(alunos_ids)]

# Agrupar os dados por ano e classificação
evolucao_classificacao = evolucao_alunos.groupby(['SiglaPeriodo', 'ClassificacaoDescricao']).size().unstack(fill_value=0)

# Resetando o índice para transformar os dados em formato longo
evolucao_classificacao_long = evolucao_classificacao.reset_index().melt(id_vars=['SiglaPeriodo'], var_name='ClassificacaoDescricao', value_name='NumeroDeAlunos')


# Criar o gráfico com Altair
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

# Exibir o gráfico no Streamlit
st.altair_chart(chart, use_container_width=True)


### --------------- DF EVOLUÇÃO -----------------------------------###

st.divider()

### --------------- MÉTRICAS POR ANO E ESCOLA--------------------- ###

df_escolas_perf_unpivoted = handler.df_escolas_perf_unpivoted()

st.markdown("""### Mediana das Métricas por Ano e Categoria de Escola""")
st.write("""Ao analisar os dados dos indicadores educacionais de 2022 a 2024, podemos perceber algumas tendências importantes tanto nas escolas particulares quanto nas públicas.""")
st.write("""Nas escolas particulares, o Índice de Desenvolvimento Educacional (INDE) teve uma queda de 2022 para 2023, mas apresentou uma recuperação significativa em 2024, indicando uma recuperação e um desempenho robusto. Os outros indicadores também mostram um desempenho consistente, com o Desempenho Acadêmico (IDA), o Engajamento (IEG) e o Ponto de Virada (IPV) mantendo níveis elevados ao longo dos três anos. Embora tenha havido uma leve oscilação em alguns desses índices, as escolas particulares continuam com um desempenho superior.""")

st.write("""Por outro lado, as escolas públicas mostraram um crescimento em alguns indicadores até 2023, mas enfrentaram desafios em 2024. O INDE, que havia aumentado em 2023, apresentou uma leve redução em 2024, refletindo uma desaceleração no avanço. O IDA e o IEG, que também cresceram até 2023, sofreram uma queda em 2024, o que pode indicar dificuldades em manter os progressos alcançados. O IPV teve um aumento até 2023, mas também caiu ligeiramente em 2024.""")

st.write("""Essas observações indicam que, embora as escolas públicas tenham feito progressos notáveis até 2023, o desempenho não se manteve de forma consistente, com uma leve queda em 2024. Já as escolas particulares mostraram estabilidade e continuidade no alto desempenho, o que aponta para a necessidade da Passos Mágicos de reforçar as estratégias nas escolas públicas, a fim de consolidar os avanços e evitar retrocessos.""")

# # Criar a figura
# fig, ax = plt.subplots(figsize=(12, 6))

# sns.lineplot(
#     x='Ano', y='Valor', hue='CategoriaEscola_Instituição de ensino', style='Metrica',
#     data=df_escolas_perf_unpivoted, markers=True, markersize=8, ax=ax
# )

# ax.set_title('Mediana das Métricas por Ano e Categoria de Escola')
# ax.set_xlabel('Ano')
# ax.set_ylabel('Mediana')
# ax.set_xticks(df_escolas_perf_unpivoted['Ano'].unique())
# ax.legend(title='Categoria / Métrica', bbox_to_anchor=(1.05, 1), loc='upper left')
# ax.grid(True, linestyle='--', alpha=0.5)

# # Exibir no Streamlit
# st.pyplot(fig)

# Criar o gráfico em Altair
df = df_escolas_perf_unpivoted.copy()

# Criar o gráfico em Altair
grafico = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x=alt.X("Ano:O", title="Ano", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Valor:Q", title="Mediana"),
        color=alt.Color("CategoriaEscola_Instituição de ensino:N", title="Categoria"),
        strokeDash=alt.StrokeDash("Metrica:N", title="Métrica")
    )
)

# Adicionar marcadores diferentes por Métrica
pontos = (
    alt.Chart(df)
    .mark_point()
    .encode(
        x="Ano:O",
        y="Valor:Q",
        color="CategoriaEscola_Instituição de ensino:N",
        shape="Metrica:N"
    )
)

# Combinar os gráficos
grafico_final = (grafico + pontos).properties(title="Mediana das Métricas por Ano e Categoria de Escola", width=700, height=400)

# Exibir no Streamlit
st.altair_chart(grafico_final, use_container_width=True)
st.write(df_escolas_perf_unpivoted)


### --------------- MÉTRICAS POR ANO E ESCOLA --------------------- ###

st.divider()


### --------------- DEFASAGEM DE ALUNOS POR ESCOLA E ANO --------------------- ###

df_escolas_defas_unpivoted = handler.df_escolas_defas_unpivoted()

st.markdown("""### Defasagem de alunos por categoria de escola e ano""")

st.write("""Focando exclusivamente na defasagem escolar, observamos uma melhora significativa entre 2022 e 2024, tanto nas escolas particulares quanto nas públicas. Nas escolas particulares, a defasagem severa foi completamente eliminada, o que reflete a eficácia das estratégias adotadas, como programas de recuperação e apoio pedagógico. Isso sugere um esforço bem-sucedido para atender aos alunos que estavam em situação de defasagem.""")

st.write("""Nas escolas públicas, a defasagem severa também diminuiu consideravelmente ao longo dos anos, com uma redução notável entre 2022 e 2024. Embora o progresso seja evidente, ainda existem alunos em situação de defasagem severa, o que indica que, embora as estratégias de recuperação tenham sido parcialmente eficazes, mais esforços são necessários para eliminar completamente essa lacuna.""")

st.write("""Enquanto as escolas particulares conseguiram erradicar a defasagem severa, as escolas públicas ainda enfrentam desafios em superar completamente essa questão, exigindo atenção contínua e ações mais direcionadas da Passos Mágicos.""")

st.write("""Por fim, Verificamos também a diminuição da defasagem moderada e aumento dos Alunos em Fase tanto nas escolas particulares quanto nas públicas, indicando um bom progresso.
""")

# sns.set_theme(style="whitegrid")

# fig, axes = plt.subplots(3, 2, figsize=(10, 8))

# years = df_escolas_defas_unpivoted['Ano'].unique()
# school_types = df_escolas_defas_unpivoted['CategoriaEscola_Instituição de ensino'].unique()

# for i, year in enumerate(years):
#     for j, school_type in enumerate(school_types):
#         year_school_data = df_escolas_defas_unpivoted[(df_escolas_defas_unpivoted['Ano'] == year) &
#                                                       (df_escolas_defas_unpivoted['CategoriaEscola_Instituição de ensino'] == school_type)]
#         defasagem_totals = year_school_data.groupby('Defasagem_categoria')['Value'].sum()

#         ax = axes[i, j]
#         defasagem_totals.plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2", len(defasagem_totals)), ax=ax)

#         ax.set_title(f'{school_type} - {year}')
#         ax.set_ylabel('')

# plt.suptitle('Defasagem de alunos por categoria de escola e ano', fontsize=16)
# plt.tight_layout()

# st.pyplot(fig)


# Criar uma lista para armazenar os gráficos
charts = []

years = df_escolas_defas_unpivoted['Ano'].unique()
school_types = df_escolas_defas_unpivoted['CategoriaEscola_Instituição de ensino'].unique()

for year in years:
    for school_type in school_types:
        year_school_data = df_escolas_defas_unpivoted[(df_escolas_defas_unpivoted['Ano'] == year) & (df_escolas_defas_unpivoted['CategoriaEscola_Instituição de ensino'] == school_type)]
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
            .properties(title=f"{school_type} - {year}", width=200, height=200)
        )
        
        charts.append(chart)

# Organizar os gráficos em um layout empilhado
st.write("# Defasagem de alunos por categoria de escola e ano")
st.altair_chart(alt.vconcat(*charts), use_container_width=True)

### --------------- DEFASAGEM DE ALUNOS POR ESCOLA E ANO --------------------- ###

st.divider()

### --------------- MÉTRICA PEDRA POR ANO E ESCOLA --------------------- ###

df_escolas_pedra_unpivoted = handler.df_escolas_pedra_unpivoted()


st.title('Percentil 80 da Métrica Pedra por Ano e Categoria de Escola')

st.write("""O gráfico acima, categorizado por tipo de escola, ilustra a evolução das pedras dos alunos, considerando o percentil 80, ao longo de 5 anos, durante os quais fizeram parte da Passos Mágicos.""")

st.markdown("""Legenda das Pedras:

*   Quartzo = 1
*   Ágata = 2
*   Ametista = 3
*   Topázio = 4""")

st.write("""Podemos observar que, nas escolas públicas, de 2020 a 2022, 80% dos alunos atingiram no máximo a pedra Ametista, com uma mudança apenas a partir de 2023. Já nas escolas particulares, a mesma proporção de alunos alcançou consistentemente o nível Topázio.""")

st.write("""Isso mostra que o setor público enfrentou mais dificuldades ao longo dos anos de ter um número considerável de alunos atingindo níveis máximos das pedras.
""")
fig, ax = plt.subplots(figsize=(10, 3))
ax = sns.barplot(x='Ano', y='Valor', hue='CategoriaEscola_Instituição de ensino', data=df_escolas_pedra_unpivoted, palette="tab10")
ax.set_title('Percentil 80 da Métrica Pedra por Ano e Categoria de Escola')
ax.set_xlabel('Ano')
ax.set_ylabel('Valor do Percentil 80')
ax.legend(title='Categoria de Escola', bbox_to_anchor=(1.02, 1), loc='upper left')

for p in ax.patches:
    if p.get_height() != 0.0:
        ax.annotate(format(p.get_height(), '.2f'),
                    (p.get_x() + p.get_width() / 2., p.get_height() / 2),
                    ha='center', va='center',
                    xytext=(0, 0),
                    textcoords='offset points')

plt.tight_layout()
st.pyplot(fig)

### --------------- MÉTRICA PEDRA POR ANO E ESCOLA --------------------- ###

st.divider()





