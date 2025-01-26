import pandas as pd
from google.cloud import bigquery
import streamlit as st


class BigQuery:

    def __init__(self, dataset : str = 'fase-5'):

        self.dataset = dataset
        self.client = self.create_credentials()
    
    def create_credentials(self):

        credential = {
            "type": "service_account",
            "project_id": "tc-fiap",
            "private_key_id": "b51c8428bc5051efce0dcc095e3c7a82556530ab",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDYIqTdOrvgjDT2\nUhttdIQuJkhPhKFKspprkDMhJ9ECRTmhXJRNh6ey5Fs6Z5k/E/4GFGdaNA7FLf04\n+53eikxvRUowXNq8er3orVu1E1id006rDBoBMQHmF/5NOweQgw1rUqkyc74sDHCZ\nDvQmUPqbUvLETFz1pSAHZo4YJfgji5vjZbgl1MeOSWqNlm0xLRai024kOtJR2Wzr\nDoGk8QApzWo0AN73CSTQFpZ1yq92GrwO5Fwe5kr7oZTCOC1lEH4DNY3Nu12ESmeE\ngsv3wdI9L3dkTORolcPhyxCIqVieb7VCXrXV2Zj1fh7MquEmZCLIEmiA4MtawlDg\nYHsWvgNDAgMBAAECggEAZ5nDmN+saugKAwA8cWzmZxCmnKcggSO3bVPDjmL9hq8T\n/srXs4oQ0mkvaYF7LYcxvkxNdil54v42YPgLJj74gGWgOCpqFupm2X8vdE5/rbc6\nADdex69sD5T0qqRe7eBDsGwA+lQMliSoXFWUpkEuvwE1qO5JqN2ryqBYAC9DEBXb\n8bF1pfRvM1EYT4sIU0L6Bh1ahsLGcwp2kRN6+/CRL/4cPBy0fwQcy3bBCSJ/fNIi\n8Fg6rVocgQAJkCLNdlDkY51x6+B/Erx5jY8D43mM+bjoroB7wYJBAOsrlsKtTJGP\nS3xtSuuMDqcQ49wUFOaLNK1XjWze/iqiN+6T/lkDIQKBgQDtXQWsMqVk7snyNJPk\nXnJv2fRFZLrK2dXSIlgQS/nc0uQznfoVZDqLuRMXTkEzTq8KUbB5zU8Z23r6ZMvN\n5q4/dh1wTLzHc0mk/63E1r2g4DFYGsAhjHHnH5oKIWqFbu+oRg/6qTAsMsaETIFW\nbmRo0Yv74Fl6NTDfBN1Y7uTaWwKBgQDpGvDITL6XJ699CVUBenItlJMz/jjouzzh\ncQ8jdj23rv5d5WifQ9HXyyXh5DY+Xz75J6/0uRytcPREy+yH+E9IkhELpXNjugm8\n6XRI33wc/wAXTkysasBnqSwEalszOOW860L5Poz53wCPJjxZzI//48cDZd3wnmhz\nczppB7c/OQKBgFSNK0UgsVvX16XoZroVjqwbNnE1pXg2ynzU8Qu1FKc9lD5yyq+u\nCVDWN1+4527QW3fQi42HveKXFSJ2n0aUIoPGnkvveduOTLByx0JzwA67bbhVpxUM\nQ1KyJhvvtVMcplAJzQ1cESXdXGuqGPRh1HCmHDg3vYfTxLncsMBKMMk7AoGADqS/\nnYWcr3gxwQQWD/q2M4DS4oBE6PHiODNXBR5HcEOQ/SsNMHwdMZY0cgVZFv/6v8Ir\nfo8mawrefXfmCwChUmjCo12oawpj1DdCM9W+QUAPrGchz+8A2UI6XqijxAr9+6k3\n0tqIFqZYraV0Qxvjq+qONPtwPs5kt2P0tmZir5kCgYEAyWLOLhp1f4A9S+pbx1YZ\nueYVJQvJ3BSk6Ny/wO8NLRNyixZ/94nC69QDa9l6YzC0XxyXclJHWBpI72wYWA3B\n33faHN/qFdFySit5zQr3igqUthxCcL8SlTL0r5QLzb/TO0B2SF5vOIL9Pm4Omp5v\ncoGMnjM65mgETjirFDq7ep0=\n-----END PRIVATE KEY-----\n",
            "client_email": "tc-fiap@tc-fiap.iam.gserviceaccount.com",
            "client_id": "107786924408647433538",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/tc-fiap%40tc-fiap.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }

        client = bigquery.Client.from_service_account_info(credential)

        return client
    
    def create_query(self, table_name, *args, **kwargs):

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

        df = self.client.query(tablename, *args, **kwargs).to_dataframe()
        
        return df
    


    


