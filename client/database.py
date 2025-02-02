import pandas as pd
from google.cloud import bigquery
import streamlit as st
import json


class BigQuery:

    def __init__(self, dataset : str = 'fase_5'):
        self.dataset = dataset
        self.client = self._create_credentials()
    
    def _create_credentials(self):

        credentials = {
            "type": "service_account",
            "project_id": st.secrets["google_cloud"]["project_id"],
            "private_key_id": st.secrets["google_cloud"]["private_key_id"],
            "private_key": st.secrets["google_cloud"]["private_key"].replace("\\n", "\n"),
            "client_email": st.secrets["google_cloud"]["client_email"],
            "client_id": st.secrets["google_cloud"]["client_id"],
            "auth_uri": st.secrets["google_cloud"]["auth_uri"],
            "token_uri": st.secrets["google_cloud"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["google_cloud"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["google_cloud"]["client_x509_cert_url"],
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
    


    


