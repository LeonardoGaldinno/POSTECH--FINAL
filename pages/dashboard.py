import streamlit as st
import pandas as pd

st.subheader("Filtros Interativos")
year_range = st.slider("Selecione o período:", 2019, 2024,(2020,2022))

genres = ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"]
selected_genres = st.multiselect("Selecione os gêneros:", genres, default=["Action", "Comedy"])


st.write(f"Analisando de {year_range[0]} até {year_range[1]} para os gêneros: {', '.join(selected_genres)}.")
