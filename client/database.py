import pandas as pd
from google.cloud import bigquery
import streamlit as st
import json


class BigQuery:

    def __init__(self,  credential: str, dataset : str = 'fase_5'):
        self.dataset = dataset
        self.client = self._create_credentials(credential)
    
    def _create_credentials(self, credential):

        with open(credential, 'r') as file:
            credential = json.load(file)

        client = bigquery.Client.from_service_account_info(credential)

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
    


    


