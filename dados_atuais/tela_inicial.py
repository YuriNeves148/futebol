import requests
import re
import pandas as pd
from datetime import datetime
import streamlit as st

def cria_dataframe(url):
    resposta = requests.get(url)

    texto = resposta.json()
    partidas_json = texto['matches']

    colunas = ['Rodada', 'Data', 'Casa', 'Visitante', 'Placar 1T', 'Placar Final']
    linhas = []

    for i in partidas_json:
        if 'score' in i.keys():
            score = i['score']
            if isinstance(score, dict):
                linhas.append({
                    'Rodada': i['round'][-1],
                    'Data': i['date'],
                    'Casa': i['team1'],
                    'Visitante': i['team2'],
                    'Placar 1T': i['score']['ht'],
                    'Placar Final': i['score']['ft']
                })
        else:
            break

    data_frame = pd.DataFrame(linhas, columns=colunas)
    data_frame['Data'] = pd.to_datetime(data_frame['Data'], format='%Y-%m-%d')
    data_frame['Data'] = data_frame['Data'].dt.strftime('%d/%m/%Y')
    calcula_pontos(data_frame)
    return 

def calcula_pontos(dataframe):
    # calculo dos pontos por time
    return

url_premier1 = "https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2026-27/en.1.json"
url_premier2 = "https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2026-27/en.2.json"
url_brasileirao = "https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2026/br.1.json"
url_laliga = "https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2026-27/es.1.json"
url_ligue1 = "https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2026-27/fr.1.json"
url_italia = "https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2026-27/it.1.json"
url_portugal = "https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2026-27/pt.1.json"
url_holanda = "https://raw.githubusercontent.com/openfootball/football.json/refs/heads/master/2026-27/nl.1.json"

st.write('# Tabelas de classificao (26/27)')
st.write('### Premier League')
cria_dataframe(url_premier1)

#cria_dataframe(url_brasileirao)
#cria_dataframe(url_laliga)
#cria_dataframe(url_italia)
#cria_dataframe(url_ligue1)
#cria_dataframe(url_portugal)
#cria_dataframe(url_holanda)
# ligas = ['Brasileirão', 'Inglaterra 1D', 'Inglaterra 2D', 'Espanha', 'França', 'Itália', 'Portugal', 'Holanda']