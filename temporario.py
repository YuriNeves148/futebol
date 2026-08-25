import pandas as pd
import streamlit as st
import datetime as dt
competicao_2526_df = pd.read_csv('datasets/premier_2526.csv') 
competicao_2425_df = pd.read_csv('datasets/premier_2425.csv')
competicao_2324_df = pd.read_csv('datasets/premier_2324.csv')

competicao_2425_df['Temporada'] = "24/25"
competicao_2526_df['Temporada'] = "25/26"
competicao_2324_df['Temporada'] = "23/24"



# quanto teve Arsenal x Liverpoo?
# Para cada partida (casa/visitante): data, placar, resultado, média de chutes, chutes ao gol, cartao A., cartao V., juizes

def media_gols(competicao_df, time1, time2):
    # encontra partida
    partidas_df = competicao_df.loc[(( (competicao_df['HomeTeam'] == time1) | (competicao_df['AwayTeam'] == time1) ) 
                             & ( (competicao_df['HomeTeam'] == time2) | (competicao_df['AwayTeam'] == time2) ) 
                             )]
    
    partidas_df['Date'] = pd.to_datetime(partidas_df['Date']).dt.strftime('%d/%m/%Y')
    resumo_df = partidas_df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
    print(resumo_df)

    # media de gols:
    partidas = []
    for _, linha in resumo_df.iterrows():
        partidas.append(linha['FTHG']+linha['FTAG'])
    media = sum(partidas) / len(partidas)
    print('Media de gols por partida: ', media)
    return


comp = pd.concat([competicao_2425_df, competicao_2526_df, competicao_2324_df])
time1 = "Arsenal"
time2 = "Liverpool"
media_gols(comp, time1, time2)

