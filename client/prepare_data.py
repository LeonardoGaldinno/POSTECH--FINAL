from client.database import BigQuery
from client.classificador import Classificador
from client.utils import Utils

class PrepareData:

    def __init__(self):

        self.client = BigQuery()
        self.classificador = Classificador()
        self.utils = Utils()

    def df_pede_merged(self):
        df_pede_passos_tab2022 = client.load_table(tbPede2022)
        df_pede_passos_tab2023 = client.load_table(tbPede2023)
        df_pede_passos_tab2024 = client.load_table(tbPede2024)

        #Classificando instituicoes de ensino
        df_pede_passos_tab2022 = classificador.categorizar_escolas(df_pede_passos_tab2022,'Instituição de ensino')

        #Selecionando Colunas uteis
        df_pede_passos_tab2022 = df_pede_passos_tab2022[['CategoriaEscola_Instituição de ensino','RA','Ano ingresso','Fase','Fase ideal',
                                                        'Defas','Pedra 20','Pedra 21','Pedra 22','INDE 22','IEG','IDA','IPV','Destaque IEG']]

        #Renomeando indices
        df_pede_passos_tab2022 = df_pede_passos_tab2022.rename(columns={
            'IEG': 'IEG_22',
            'IDA': 'IDA_22',
            'IPV': 'IPV_22',
            'Fase': 'Fase_22',
            'Fase ideal': 'Fase_ideal_22',
            'Defas': 'Defas_22'
        })

        join_key = 'RA'
        columns_to_include = ['INDE 2023', 'Pedra 2023', 'IDA','IPV','IEG','Defasagem','Fase','Fase Ideal']
        df_final = pd.merge(df_pede_passos_tab2022, df_pede_passos_tab2023[[join_key] + columns_to_include], on=join_key, how='left')

        #Renomeando indices
        df_final = df_final.rename(columns={
            'IEG': 'IEG_23',
            'IDA': 'IDA_23',
            'IPV': 'IPV_23',
            'Fase': 'Fase_23',
            'Fase ideal': 'Fase_ideal_23',
            'Defasagem': 'Defasagem_23'
        })

        join_key = 'RA'
        columns_to_include = ['INDE 2024', 'Pedra 2024', 'IDA','IPV','IEG','Defasagem','Fase','Fase Ideal']
        df_final = pd.merge(df_final, df_pede_passos_tab2024[[join_key] + columns_to_include], on=join_key, how='left')

        #Renomeando indices
        df_final = df_final.rename(columns={
            'IEG': 'IEG_24',
            'IDA': 'IDA_24',
            'IPV': 'IPV_24',
            'Fase': 'Fase_24',
            'Fase ideal': 'Fase_ideal_24',
            'Defasagem': 'Defasagem_24'
        })

        # Numerando Pedras
        df_final['Pedra_20_num'] = df_final['Pedra 20'].apply(self.utils.numerando_pedra)
        df_final['Pedra_21_num'] = df_final['Pedra 21'].apply(self.utils.numerando_pedra)
        df_final['Pedra_22_num'] = df_final['Pedra 22'].apply(self.utils.numerando_pedra)
        df_final['Pedra_23_num'] = df_final['Pedra 2023'].apply(self.utils.numerando_pedra)
        df_final['Pedra_24_num'] = df_final['Pedra 2024'].apply(self.utils.numerando_pedra)

        #Categorizando Defasagem
        df_final['Defasagem_categoria_22'] = df_final['Defas_22'].apply(self.utils.categorize_defasagem)
        df_final['Defasagem_categoria_23'] = df_final['Defasagem_23'].apply(self.utils.categorize_defasagem)
        df_final['Defasagem_categoria_24'] = df_final['Defasagem_24'].apply(self.utils.categorize_defasagem)

        return df_final
    
    def df_escolas_perf_unpivoted(self):

        df_final = self.df_pede_merged()

        #Criando um DF para analise de performance dos indices INDE, IDA, IEG, IPV em escolas publicas vs particulartes
        df_escolas_perf = df_final.groupby(['CategoriaEscola_Instituição de ensino'])[['INDE 22','IDA_22','IEG_22','IPV_22','INDE 2023','IDA_23','IEG_23','IPV_23','INDE 2024','IDA_24','IEG_24','IPV_24']].median()
        df_escolas_perf = df_escolas_perf.reset_index()
        df_escolas_perf_unpivoted = df_escolas_perf.melt(id_vars='CategoriaEscola_Instituição de ensino',
                                                        var_name='Metrica',
                                                        value_name='Valor')
        df_escolas_perf_unpivoted['Ano'] = df_escolas_perf_unpivoted['Metrica'].apply(self.utils.get_year)
        df_escolas_perf_unpivoted['Metrica'] = df_escolas_perf_unpivoted['Metrica'].apply(self.utils.clean_metric)

        return df_escolas_perf_unpivoted

    def df_escolas_defas_unpivoted(self):
        
        df_final = self.df_pede_merged()

        df_escolas_defas = df_final.groupby(['CategoriaEscola_Instituição de ensino'])[['Defasagem_categoria_22']].value_counts().reset_index(name='count')
        df_escolas_defas['Ano'] = 2022
        df_escolas_defas2 = df_final.groupby(['CategoriaEscola_Instituição de ensino'])[['Defasagem_categoria_23']].value_counts().reset_index(name='count')
        df_escolas_defas2['Ano'] = 2023
        df_escolas_defas3 = df_final.groupby(['CategoriaEscola_Instituição de ensino'])[['Defasagem_categoria_24']].value_counts().reset_index(name='count')
        df_escolas_defas3['Ano'] = 2024

        df_escolas_defas = df_escolas_defas.rename(columns={
            'Defasagem_categoria_22': 'Defasagem_categoria',
        })
        df_escolas_defas2 = df_escolas_defas2.rename(columns={
            'Defasagem_categoria_23': 'Defasagem_categoria',
        })
        df_escolas_defas3 = df_escolas_defas3.rename(columns={
            'Defasagem_categoria_24': 'Defasagem_categoria',
        })

        df_escolas_defas = pd.concat([df_escolas_defas, df_escolas_defas2, df_escolas_defas3], ignore_index=True)
        df_escolas_defas_unpivoted = df_escolas_defas.melt(id_vars=['CategoriaEscola_Instituição de ensino', 'Defasagem_categoria', 'Ano'],
                                                        value_vars=['count'],
                                                        var_name='Metric',
                                                        value_name='Value')

        return df_escolas_defas_unpivoted

    def df_escolas_pedra_unpivoted(self):

        df_final = self.df_pede_merged

        df_escolas_pedra = df_final.groupby(['CategoriaEscola_Instituição de ensino'])[['Pedra_20_num','Pedra_21_num','Pedra_22_num','Pedra_23_num','Pedra_24_num']].quantile(0.80)
        df_escolas_pedra = df_escolas_pedra.reset_index()
        df_escolas_pedra_unpivoted = df_escolas_pedra.melt(id_vars='CategoriaEscola_Instituição de ensino',
                                                        var_name='Metrica',
                                                        value_name='Valor')
        df_escolas_pedra_unpivoted['Ano'] = df_escolas_pedra_unpivoted['Metrica'].apply(self.utils.get_year)
        df_escolas_pedra_unpivoted['Metrica'] = df_escolas_pedra_unpivoted['Metrica'].apply(self.utils.clean_metric)

        return df_escolas_pedra_unpivoted

                        