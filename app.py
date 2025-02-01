import streamlit as st
import pandas as pd
import altair as alt
from google.cloud import bigquery
import matplotlib.pyplot as plt
import seaborn as sns
from client.database import BigQuery

st.logo('img/Passos-magicos-icon-cor-removebg-preview.png', size='large')

page_introduction = st.Page('pages/introduction.py', title="Introdução", icon=":material/home:")
page_report = st.Page('pages/report.py', title="Relatório", icon=":material/description:")
page_dashboard = st.Page('pages/dashboard.py', title="Dashboard", icon=":material/analytics:")
page_ml = st.Page('pages/ml_model.py', title="Machine Learning", icon=":material/smart_toy:")

pg = st.navigation([page_introduction,page_report, page_dashboard, page_ml])
pg.run()


