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

    import streamlit as st


    if predicao == 4:
        cor = "#1E90FF"  
        pedra = "Topázio"
    elif predicao == 1:
        cor = "#8A2BE2"  
        pedra = "Ametista"
    elif predicao == 0:
        cor = "#FFA500"  
        pedra = "Àgata"
    elif predicao == 3:
        cor = "#D3D3D3"  
        pedra = "Quartzo"

    # Exibindo a mensagem com a cor personalizada
    st.markdown(
        f'<div style="background-color: {cor}; padding: 10px; border-radius: 5px; font-size: 20px;">'
        f'Sua pedra é {pedra}. Excelente trabalho! Você está indo muito bem e sua dedicação está refletindo em seus resultados. Continue assim, você está no caminho certo!'
        '</div>',
        unsafe_allow_html=True
    )

    st.balloons()
    
    
    
