import streamlit as st

st.header("Base de Dados")
st.write("""
            Para este projeto, utilizamos dados históricos de preços do petróleo brent, que são fornecidos pelo site do Instituto de Pesquisa 
            Econômica Aplicada (IPEA), como também dados de consumo mundial de petróleo de fontes como: Energy Information Administration (EIA), 
            International Energy Agency (IEA) e Organization of the Petroleum Exporting Countries (OPEC).
     
            Esses dados incluem informações sobre as datas, os preços e a média diária do consumo de petróleo ao longo do tempo. 
            Para garantir que os dados estejam bem organizados e facilmente acessíveis, armazenamos tudo no BigQuery, uma plataforma de 
            armazenamento de dados na nuvem. Isso não só facilita a estruturação dos dados, mas também permite que eles sejam integrados 
            automaticamente com o Streamlit, a ferramenta que usamos para criar nosso dashboard interativo e o modelo de previsão. 
            Dessa forma, conseguimos atualizar e visualizar os dados em tempo real, proporcionando uma experiência mais eficiente e dinâmica 
            para os usuários.
            """)