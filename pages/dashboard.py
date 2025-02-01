import streamlit as st
import pandas as pd

   
# col_dash, col_filters = st.columns([5, 1])
# with col_filters:
#             st.subheader("Filtros Interativos")
#             min_date = pd.to_datetime('2024-02-01')
#             max_date = pd.to_datetime('2025-02-01')
            
            
#             start_date = st.date_input("Data de Início", value=min_date, min_value=min_date, max_value=max_date)
#             end_date = st.date_input("Data de Fim", value=max_date, min_value=min_date, max_value=max_date)

st.subheader("Filtros Interativos")
year_range = st.slider("Selecione o período:", 2019, 2024,(2020,2022))

genres = ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"]
selected_genres = st.multiselect("Selecione os gêneros:", genres, default=["Action", "Comedy"])


st.write(f"Analisando de {year_range[0]} até {year_range[1]} para os gêneros: {', '.join(selected_genres)}.")
