class Classificador:
    def __init__(self):

        self.categorias = {
            'Escolas Públicas': ['Escola Pública', 'Escolas Públicas','Escola Pública','Escola Publica','Escola Pública','Pública','Concluiu o 3º EM','Nenhuma das opções acima'],
            'Escolas Particulares': ['Escolas Particulares', 'Einstein', 'Escola João Paulo II',
                                     'Rede Decisão/União','Rede Decisão','Escola JP II','V202','Rede Decisão/União','Privada',
                                     'Privada - Programa de Apadrinhamento','Privada *Parcerias com Bolsa 100%','Privada - Pagamento por *Empresa Parceira',
                                     'Privada - Programa de apadrinhamento'],
            'Universidades': ['Estácio', 'FIAP', 'UNISA']
        }

    def categorizar_escolas(self, df, coluna):
        
        df[f'CategoriaEscola_{coluna}'] = df[coluna].apply(self.classificar)

        return df

    def classificar(self, escola):
            for categoria, escolas in self.categorias.items():
                if escola in escolas:
                    return categoria