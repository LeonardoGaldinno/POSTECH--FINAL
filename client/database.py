import pandas as pd
from google.cloud import bigquery
import streamlit as st
import json


class BigQuery:

    def __init__(self, dataset : str = 'fase_5'):
        self.dataset = dataset
        self.client = self._create_credentials()
    
    def _create_credentials(self):

         # Carrega secrets do Streamlit
        project_id = st.secrets["project_id"]
        private_key = st.secrets["private_key"].replace("\\n", "\n") 
        client_email = st.secrets["client_email"]
        
    # Prepara o Credentials Dictionary
        credentials = {
            "type": "service_account",
            "project_id": project_id,
            "private_key_id": st.secrets["private_key_id"],
            "private_key": private_key,
            "client_email": client_email,
            "client_id": st.secrets["client_id"],
            "auth_uri": st.secrets["auth_uri"],
            "token_uri": st.secrets["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["client_x509_cert_url"],
        }

        client = bigquery.Client.from_service_account_info(credentials)

        return client
    
    def _create_query(self, table_name, *args, **kwargs):

        query = f"SELECT * FROM `tc-fiap.{self.dataset}.{table_name}`"
        

        if args:
            query += " " + " ".join(args)

        if kwargs:
            conditions = " AND ".join(f"{key} = '{value}'" for key, value in kwargs.items())
            if "WHERE" not in query.upper():
                query += f" WHERE {conditions}"
            else:
                query += f" AND {conditions}"
        
        return query


    def load_table(self, tablename, *args, **kwargs):

        query = self._create_query(tablename, *args, **kwargs)


        df = self.client.query(query).to_dataframe()
        
        return df
    


    


