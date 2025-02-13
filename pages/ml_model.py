import streamlit as st 
import joblib
import numpy as np

st.markdown('long_about_text')

modelo = joblib.load('model.pkl')


st.title("Modelo de Classificação")

st.write("Insira os valores dos indicadores abaixo e descubro sua próxima pedra:")

ieg = st.number_input("Indicador de Engajamento", value=0.0)
ipv = st.number_input("Indicador de ponto de virada", value=0.0)
ida = st.number_input("Indicador de desenvolvimento acadêmico", value=0.0)



if st.button("Prever pedra"):
    
    valores = np.array([[ieg, ipv, ida]])
    predicao = modelo.predict(valores)

    if predicao == 3:
        st.info("Sua pedra é Quartzo. Esta fase pode trazer algumas dificuldades, mas é uma chance para refletir e entender melhor suas necessidades e caminhos. Com paciência, você pode transformar essa experiência em aprendizado valioso.")
    if predicao == 0:
        st.info("Sua pedra é Ágata. Às vezes, enfrentamos obstáculos, mas isso faz parte do processo. O importante é saber que há sempre oportunidades para aprender e melhorar.")

    if predicao == 1:
        st.info("Sua pedra é Ametista. Há um bom progresso aqui! Com pequenas mudanças, você pode continuar avançando e atingindo novos patamares")

    if predicao == 4:
        st.info("Sua pedra é Topázio. Você está fazendo um trabalho incrível! Continue explorando suas habilidades e aproveitando as oportunidades que surgem.")
        st.balloons()
    
    
    
