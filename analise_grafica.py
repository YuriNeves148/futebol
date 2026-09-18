# https://chatgpt.com/c/6aad4c8a-aba0-83e9-9f5a-8bdbedd46736
# 1. evolucao dos pontos com o passar das temporadas
# 2. Gols marcados e sofricos
# 3. Desempenho dentro e fora de casa

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import acessa_datasets as ads
import numpy as np


def normalizar_temporada(valor):
    """Converte anos-calendario, como 2023, para o rotulo 23/24."""
    valor = str(valor)

    if '/' in valor:
        return valor

    ano = int(valor)
    return f'{ano % 100:02d}/{(ano + 1) % 100:02d}'


# grafico de barra entre gols marcados e sofridos ao longo das temporadas
def barra_marc_sof(comppeticao_escolhida, time_escolhido):
    if comppeticao_escolhida == 'Inglaterra':
        df = ads.premier_df
    if comppeticao_escolhida == 'Espanha':
        df = ads.laliga_df
    if comppeticao_escolhida == 'Alemanha':
        df = ads.bundesliga_df
    if comppeticao_escolhida == 'Italia':
        df = ads.italia_df
    if comppeticao_escolhida == 'França':
        df = ads.ligue1_df
    if comppeticao_escolhida == 'Holanda':
        df = ads.holanda_df
    if comppeticao_escolhida == 'Portugal':
        df = ads.portugal_df
    if comppeticao_escolhida == 'Escocia':
        df = ads.escocia_df
    if comppeticao_escolhida == 'Brasil':
        df = ads.brasil_df
    if comppeticao_escolhida == 'Argentina':
        df = ads.argentina_df

    temporadas = ['23/24', '24/25', '25/26', '26/27']
    df_grafico = df.copy()
    df_grafico['TemporadaGrafico'] = df_grafico['Temporada'].apply(normalizar_temporada)

    df_2324 = df_grafico[df_grafico['TemporadaGrafico'] == '23/24']
    df_2425 = df_grafico[df_grafico['TemporadaGrafico'] == '24/25']
    df_2526 = df_grafico[df_grafico['TemporadaGrafico'] == '25/26']
    df_2627 = df_grafico[df_grafico['TemporadaGrafico'] == '26/27']

    gols_marc_2324 = df_2324.loc[df_2324['HomeTeam'] == time_escolhido, 'FTHG'].sum() + df_2324.loc[df_2324['AwayTeam'] == time_escolhido, 'FTHG'].sum()
    gols_sof_2324 = df_2324.loc[df_2324['HomeTeam'] == time_escolhido, 'FTAG'].sum() + df_2324.loc[df_2324['AwayTeam'] == time_escolhido, 'FTAG'].sum()

    gols_marc_2425 = df_2425.loc[df_2425['HomeTeam'] == time_escolhido, 'FTHG'].sum() + df_2425.loc[df_2425['AwayTeam'] == time_escolhido, 'FTHG'].sum()
    gols_sof_2425 = df_2425.loc[df_2425['HomeTeam'] == time_escolhido, 'FTAG'].sum() + df_2425.loc[df_2425['AwayTeam'] == time_escolhido, 'FTAG'].sum()
    
    gols_marc_2526 = df_2526.loc[df_2526['HomeTeam'] == time_escolhido, 'FTHG'].sum() + df_2526.loc[df_2526['AwayTeam'] == time_escolhido, 'FTHG'].sum()
    gols_sof_2526 = df_2526.loc[df_2526['HomeTeam'] == time_escolhido, 'FTAG'].sum() + df_2526.loc[df_2526['AwayTeam'] == time_escolhido, 'FTAG'].sum()
    
    gols_marc_2627 = df_2627.loc[df_2627['HomeTeam'] == time_escolhido, 'FTHG'].sum() + df_2627.loc[df_2627['AwayTeam'] == time_escolhido, 'FTHG'].sum()
    gols_sof_2627 = df_2627.loc[df_2627['HomeTeam'] == time_escolhido, 'FTAG'].sum() + df_2627.loc[df_2627['AwayTeam'] == time_escolhido, 'FTAG'].sum()
    
    gols_list_marc = [gols_marc_2324, gols_marc_2425, gols_marc_2526, gols_marc_2627]
    gols_list_sof = [gols_sof_2324, gols_sof_2425, gols_sof_2526, gols_sof_2627]
    
    x = np.arange(len(temporadas))
    width = 0.35
    
    plt_marc = plt.bar(x - width/2, gols_list_marc, width, label='Gols marcados', color='green')
    plt_sof = plt.bar(x + width/2, gols_list_sof, width, label='Gols sofridos', color='red')
    
    plt.bar_label(plt_marc)
    plt.bar_label(plt_sof)
    plt.xticks(x, temporadas)
    plt.title('Gols marcados e Sofridos por Temporada', fontsize='16')
    plt.xlabel('Temporadas', fontsize='11')
    plt.ylabel('Gols', fontsize='11')
    limite_y = int(np.ceil((max(gols_list_marc + gols_list_sof) +15 ) /10) *10)
    plt.yticks(range(0, limite_y+1, 10))
    plt.ylim(bottom=0, top=max(max(gols_list_marc), max(gols_list_sof)) + 15)
    plt.tight_layout()
    plt.legend()
    plt.grid(True, axis='y', alpha=0.2)
    plt.figtext(0.99, 0.01, 'Fonte: https://football-data.co.uk/', 
                ha='right', va='bottom',fontsize=7, color='gray')
    st.pyplot(plt.gcf())

    return
