import streamlit as st
from client.database import BigQuery
import altair as alt 
import matplotlib.pyplot as plt
import seaborn as sns


client = BigQuery()


st.header("Base de Dados")
st.write("""
            Para este projeto, utilizamos um conjunto de dados fornecido pela ONG Passos Mágicos, contendo informações educacionais dos estudantes  entre os anos de 2020 e 2024, essenciais para compreender o impacto das ações da ONG no desenvolvimento dos alunos e identificar padrões que possam orientar futuras estratégias.
            """)

st.divider()


### --------------- MÉTRICAS POR ANO E ESCOLA--------------------- ###

df_escolas_perf_unpivoted = client.load_table("df_escolas_perf_unpivoted")

st.markdown("""### Mediana das Métricas por Ano e Categoria de Escola""")
st.write("""Ao analisar os dados dos indicadores educacionais de 2022 a 2024, podemos perceber algumas tendências importantes tanto nas escolas particulares quanto nas públicas.""")
st.write("""Nas escolas particulares, o Índice de Desenvolvimento Educacional (INDE) teve uma queda de 2022 para 2023, mas apresentou uma recuperação significativa em 2024, indicando uma recuperação e um desempenho robusto. Os outros indicadores também mostram um desempenho consistente, com o Desempenho Acadêmico (IDA), o Engajamento (IEG) e o Ponto de Virada (IPV) mantendo níveis elevados ao longo dos três anos. Embora tenha havido uma leve oscilação em alguns desses índices, as escolas particulares continuam com um desempenho superior.""")

st.write("""Por outro lado, as escolas públicas mostraram um crescimento em alguns indicadores até 2023, mas enfrentaram desafios em 2024. O INDE, que havia aumentado em 2023, apresentou uma leve redução em 2024, refletindo uma desaceleração no avanço. O IDA e o IEG, que também cresceram até 2023, sofreram uma queda em 2024, o que pode indicar dificuldades em manter os progressos alcançados. O IPV teve um aumento até 2023, mas também caiu ligeiramente em 2024.""")

st.write("""Essas observações indicam que, embora as escolas públicas tenham feito progressos notáveis até 2023, o desempenho não se manteve de forma consistente, com uma leve queda em 2024. Já as escolas particulares mostraram estabilidade e continuidade no alto desempenho, o que aponta para a necessidade da Passos Mágicos de reforçar as estratégias nas escolas públicas, a fim de consolidar os avanços e evitar retrocessos.""")


grafico = (
    alt.Chart(df_escolas_perf_unpivoted)
    .mark_line()
    .encode(
        x=alt.X("Ano:O", title="Ano", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Valor:Q", title="Mediana"),
        color=alt.Color("CategoriaEscola_Instituição de ensino:N", title="Categoria"),
        strokeDash=alt.StrokeDash("Metrica:N", title="Métrica")
    )
)

pontos = (
    alt.Chart(df_escolas_perf_unpivoted)
    .mark_point()
    .encode(
        x="Ano:O",
        y="Valor:Q",
        color="CategoriaEscola_Instituição de ensino:N",
        shape="Metrica:N"
    )
)

grafico_final = (grafico + pontos).properties(title="Mediana das Métricas por Ano e Categoria de Escola", width=700, height=400)

st.altair_chart(grafico_final, use_container_width=True)



### --------------- MÉTRICAS POR ANO E ESCOLA --------------------- ###

st.divider()


### --------------- DEFASAGEM DE ALUNOS POR ESCOLA E ANO --------------------- ###

df_escolas_defas_unpivoted = client.load_table("df_escolas_defas_unpivoted")

st.markdown("""### Defasagem de alunos por categoria de escola e ano""")

st.write("""Focando exclusivamente na defasagem escolar, observamos uma melhora significativa entre 2022 e 2024, tanto nas escolas particulares quanto nas públicas. Nas escolas particulares, a defasagem severa foi completamente eliminada, o que reflete a eficácia das estratégias adotadas, como programas de recuperação e apoio pedagógico. Isso sugere um esforço bem-sucedido para atender aos alunos que estavam em situação de defasagem.""")

st.write("""Nas escolas públicas, a defasagem severa também diminuiu consideravelmente ao longo dos anos, com uma redução notável entre 2022 e 2024. Embora o progresso seja evidente, ainda existem alunos em situação de defasagem severa, o que indica que, embora as estratégias de recuperação tenham sido parcialmente eficazes, mais esforços são necessários para eliminar completamente essa lacuna.""")

st.write("""Enquanto as escolas particulares conseguiram erradicar a defasagem severa, as escolas públicas ainda enfrentam desafios em superar completamente essa questão, exigindo atenção contínua e ações mais direcionadas da Passos Mágicos.""")

st.write("""Por fim, Verificamos também a diminuição da defasagem moderada e aumento dos Alunos em Fase tanto nas escolas particulares quanto nas públicas, indicando um bom progresso.
""")


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
            .properties(title=f"{school_type} - {year}", width=100, height=100)
        )
        
        charts.append(chart)


charts_1 = charts[:3]
charts_2 = charts[3:]

st.altair_chart(alt.hconcat(*charts_1), use_container_width=True)
st.altair_chart(alt.hconcat(*charts_2), use_container_width=True)

### --------------- DEFASAGEM DE ALUNOS POR ESCOLA E ANO --------------------- ###

st.divider()

### --------------- MÉTRICA PEDRA POR ANO E ESCOLA --------------------- ###

df_escolas_pedra_unpivoted = client.load_table("df_escolas_pedra_unpivoted")


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

### --------------- MÉTRICA PEDRA POR ANO E ESCOLA --------------------- ###

st.divider()


### --------------- DF PERÍODO ------------------------------------###

df_distribuicao = client.load_table("df_distribuicao")

df_distribuicao = df_distribuicao.dropna(subset=['ClassificacaoDescricao'])

st.markdown("""#### Análise de distribuição da classificação dos alunos.""")

st.write("""O gráfico apresentado ilustra a distribuição das classificações dos alunos em três categorias distintas: "1 - Bom", "2 - Regular" e "3 - Ruim". Essa visualização permite uma análise que facilita a identificação de áreas que podem necessitar de atenção e intervenção.""")

st.write("""Na categoria "1 - Bom", observamos que um número considerável de alunos se destaca positivamente. Embora essa barra represente uma quantidade significativa, ela não é a mais alta entre as três classificações. Isso indica que, embora haja alunos que estão se saindo bem, ainda existe uma maior proporção de alunos em outras categorias, sugerindo que o desempenho acadêmico pode ser aprimorado em geral.
""")

st.write("""A classificação "2 - Regular" é a que apresenta o maior número de alunos, superando as demais categorias. Essa predominância sugere que a maioria dos alunos está em um nível de desempenho considerado regular. Essa situação pode ser interpretada como um sinal de que muitos alunos estão se saindo adequadamente, mas também aponta para a necessidade de estratégias de melhoria, uma vez que um desempenho regular pode não ser suficiente para garantir o sucesso acadêmico a longo prazo.""")

st.write("""Por fim, a categoria "3 - Ruim" apresenta o menor número de alunos, o que é um aspecto positivo, pois indica que a maioria dos alunos não está em um nível de desempenho baixo. No entanto, essa faixa ainda precisa de atenção, pois os alunos classificados como "ruim" podem necessitar de suporte adicional para melhorar seu desempenho. Em suma, o gráfico sugere que, enquanto a maioria dos alunos está em um nível regular, há uma quantidade significativa que se destaca como bons, e a presença de alunos com desempenho ruim deve ser abordada para garantir que todos tenham a oportunidade de progredir academicamente.""")


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

evolucao_classificacao_long = client.load_table('evolucao_classificacao_long')

st.markdown("""#### Análise da evolução das Classificações ao Longo dos Anos""")

st.write("""O gráfico ilustra a evolução do número de alunos em três classificações diferentes ao longo dos anos de 2021 a 2024. Essa análise permite ter clareza das tendências de desempenho acadêmico dos alunos ao longo do tempo, facilitando a identificação de padrões e mudanças significativas nas classificações. A visualização dos dados é fundamental para entender como os alunos estão se saindo em diferentes categorias e para identificar áreas que podem necessitar de intervenções.""")

st.write("""A Classificação 1, representada pela linha azul, começou com aproximadamente 4.000 alunos em 2021. Ao longo de 2022, houve um aumento gradual no número de alunos, mas a partir de 2023, a classificação apresentou uma leve queda, estabilizando-se em torno de 4.000 alunos. Essa estabilidade sugere que, embora haja um número considerável de alunos nessa categoria, não houve um crescimento significativo nos anos seguintes, o que pode indicar uma saturação ou um equilíbrio no desempenho. Essa falta de crescimento pode levar os alunos a não perceberem melhorias em seu desempenho.""")

st.write("""A Classificação 2, indicada pela linha laranja, teve um início relativamente baixo em 2021, mas experimentou um crescimento notável até 2022, atingindo mais de 10.000 alunos. No entanto, a partir de 2022, essa classificação sofreu uma queda acentuada, continuando a diminuir até 2024. Essa tendência de redução pode sugerir uma mudança nas preferências dos alunos, uma possível diminuição na qualidade percebida do ensino ou alterações na oferta de cursos que não atenderam às expectativas dos alunos. Essa situação pode gerar insegurança nos alunos, que podem não ter uma noção clara de seu desempenho.""")

st.write("""A Classificação 3, representada pela linha verde, começou com um número de alunos semelhante ao da Classificação 1, em torno de 2.000, e apresentou um leve aumento em 2022. Contudo, a partir de então, a classificação mostrou uma leve queda, mantendo-se entre 2.000 e 3.000 alunos nos anos seguintes. Essa dinâmica sugere que, enquanto as Classificações 1 e 3 mantêm uma estabilidade relativa, a Classificação 2 apresenta uma mudança drástica que merece atenção. A análise das causas dessas variações pode ser crucial para entender melhor o desempenho acadêmico e as necessidades dos alunos. Logo, a falta de clareza sobre o desempenho pode levar os alunos a não perceberem se estão indo bem, dificultando sua capacidade de identificar áreas de melhoria e progresso.""")



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


### --------------- DF EVOLUÇÃO -----------------------------------###

st.divider()

st.title("Ferramentas Estratégicas para Aprimorar Seu Caminho Acadêmico")

st.write(""" Estamos disponibilizando ferramentas que auxiliam os alunos a compreenderem melhor as pedras futuras, com base nos índices IPV, IEG e IDA. Esses indicadores permitem uma análise mais clara do progresso individual, ajudando na identificação de desafios e oportunidades de melhoria. Nosso objetivo é trazer mais transparência ao desenvolvimento acadêmico, fornecendo insights valiosos para cada aluno. Com isso, buscamos incentivar a evolução contínua, permitindo ajustes estratégicos ao longo do tempo. Ao entenderem melhor seu desempenho, os alunos podem tomar decisões mais assertivas. Dessa forma, promovemos um acompanhamento mais eficaz e orientado ao crescimento.""")

st.page_link("pages/ml_model.py", label="Acessar ferramenta")



