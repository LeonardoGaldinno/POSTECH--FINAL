import re


class Utils:

    def __init__(self):
        pass

    def categorize_defasagem(self, defasagem):
        if defasagem >= 0:
            return 'Em Fase'
        elif defasagem >= -2 and defasagem < 0:
            return 'Moderada'
        elif defasagem < -2:
            return 'Severa'


    def get_year2(self, metrica):
        if '20' in metrica:
            return 2020
        elif '21' in metrica:
            return 2021
        elif '22' in metrica:
            return 2022
        elif '23' in metrica:
            return 2023
        elif '24' in metrica:
            return 2024
        return None

    def get_year(self,metrica):
        if '22' in metrica:
            return 2022
        elif '23' in metrica:
            return 2023
        elif '24' in metrica:
            return 2024
        return None

    def clean_metric(self, metric):
        cleaned_metric = re.sub(r'[\d_]', '', metric).strip()
        return cleaned_metric

    def numerando_pedra(self, pedra):
        if pedra == 'Quartzo':
            return 1
        elif pedra == 'Ágata':
            return 2
        elif pedra == 'Ametista':
            return 3
        elif pedra == 'Topázio':
            return 4