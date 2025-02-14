import streamlit as st 
import joblib
import numpy as np


modelo = joblib.load('model.pkl')


st.title("Modelo de Classificação")

st.write("Insira os valores dos indicadores abaixo e descubro sua próxima pedra:")

ieg = st.number_input("Indicador de Engajamento", value=0.0)
ipv = st.number_input("Indicador de ponto de virada", value=0.0)
ida = st.number_input("Indicador de desenvolvimento acadêmico", value=0.0)



if st.button("Prever pedra"):
    
    valores = np.array([[ieg, ipv, ida]])
    predicao = modelo.predict(valores)

    if predicao == 4:
        cor = "#1E90FF"  
        pedra = "Topázio"

        st.markdown(
        f'<div style="background-color: {cor}; padding: 10px; border-radius: 5px; font-size: 20px;">'
        f'Sua pedra é {pedra}. Você está fazendo um trabalho incrível! Continue explorando suas habilidades e aproveitando as oportunidades que surgem.'
        '</div>',
        unsafe_allow_html=True
    )

    elif predicao == 1:
        cor = "#8A2BE2"  
        pedra = "Ametista"

        st.markdown(
        f'<div style="background-color: {cor}; padding: 10px; border-radius: 5px; font-size: 20px;">'
        f'Sua pedra é {pedra}. Há um bom progresso aqui! Com pequenas mudanças, você pode continuar avançando e atingindo novos patamares.'
        '</div>',
        unsafe_allow_html=True
    )

    elif predicao == 0:
        cor = "#FFA500"  
        pedra = "Àgata"

        st.markdown(
        f'<div style="background-color: {cor}; padding: 10px; border-radius: 5px; font-size: 20px;">'
        f'Sua pedra é {pedra}. Às vezes, enfrentamos obstáculos, mas isso faz parte do processo. O importante é saber que há sempre oportunidades para aprender e melhorar.'
        '</div>',
        unsafe_allow_html=True
    )
        
    elif predicao == 3:
        cor = "#D3D3D3"  
        pedra = "Quartzo"

        st.markdown(
        f'<div style="background-color: {cor}; padding: 10px; border-radius: 5px; font-size: 20px;">'
        f'Sua pedra é {pedra}. Esta fase pode trazer algumas dificuldades, mas é uma chance para refletir e entender melhor suas necessidades e caminhos. Com paciência, você pode transformar essa experiência em aprendizado valioso.'
        '</div>',
        unsafe_allow_html=True
    )
        st.balloons()

 

    
    
    
    
