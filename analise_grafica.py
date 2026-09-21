# https://chatgpt.com/c/6aad4c8a-aba0-83e9-9f5a-8bdbedd46736
# 1. evolucao dos pontos com o passar das temporadas (V)
# 2. Gols marcados e sofridos
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
    plt.title(f'Gols Marcados e Sofridos por Temporada - $\\bf{{{time_escolhido}}}$', fontsize='16')
    plt.xlabel('Temporadas', fontsize='11')
    plt.ylabel('Gols', fontsize='11')
    limite_y = int(np.ceil((max(gols_list_marc + gols_list_sof) +15 ) /10) *10)
    plt.yticks(range(0, limite_y+1, 10))
    plt.ylim(bottom=0, top=max(max(gols_list_marc), max(gols_list_sof)) + 15)
    plt.tight_layout()
    plt.legend()
    plt.grid(True, axis='y', alpha=0.5)
    plt.figtext(0.99, 0.01, 'Fonte: https://football-data.co.uk/', 
                ha='right', va='bottom',fontsize=7, color='gray')
    st.pyplot(plt.gcf())

    return

def barra_vit_derr(comppeticao_escolhida, time_escolhido):
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

    vitoria_2324 = int(df_2324.loc[df_2324['FTR'] == 'H'].groupby('HomeTeam').size().get(time_escolhido, 0) + df_2324.loc[df_2324['FTR'] == 'A'].groupby('AwayTeam').size().get(time_escolhido, 0))
    empate_2324 = int(df_2324.loc[df_2324['FTR'] == 'D'].groupby('HomeTeam').size().get(time_escolhido, 0) + df_2324.loc[df_2324['FTR'] == 'D'].groupby('AwayTeam').size().get(time_escolhido, 0))
    derrota_2324 = int(df_2324.loc[df_2324['FTR'] == 'A'].groupby('HomeTeam').size().get(time_escolhido, 0) + df_2324.loc[df_2324['FTR'] == 'H'].groupby('AwayTeam').size().get(time_escolhido, 0))
    
    vitoria_2425 = int(df_2425.loc[df_2425['FTR'] == 'H'].groupby('HomeTeam').size().get(time_escolhido, 0) + df_2425.loc[df_2425['FTR'] == 'A'].groupby('AwayTeam').size().get(time_escolhido, 0))
    empate_2425 = int(df_2425.loc[df_2425['FTR'] == 'D'].groupby('HomeTeam').size().get(time_escolhido, 0) + df_2425.loc[df_2425['FTR'] == 'D'].groupby('AwayTeam').size().get(time_escolhido, 0))
    derrota_2425 = int(df_2425.loc[df_2425['FTR'] == 'A'].groupby('HomeTeam').size().get(time_escolhido, 0) + df_2425.loc[df_2425['FTR'] == 'H'].groupby('AwayTeam').size().get(time_escolhido, 0))

    vitoria_2526 = int(df_2526.loc[df_2526['FTR'] == 'H'].groupby('HomeTeam').size().get(time_escolhido, 0) + df_2526.loc[df_2526['FTR'] == 'A'].groupby('AwayTeam').size().get(time_escolhido, 0))
    empate_2526 = int(df_2526.loc[df_2526['FTR'] == 'D'].groupby('HomeTeam').size().get(time_escolhido, 0) + df_2526.loc[df_2526['FTR'] == 'D'].groupby('AwayTeam').size().get(time_escolhido, 0))
    derrota_2526 = int(df_2526.loc[df_2526['FTR'] == 'A'].groupby('HomeTeam').size().get(time_escolhido, 0) + df_2526.loc[df_2526['FTR'] == 'H'].groupby('AwayTeam').size().get(time_escolhido, 0))
    
    vitoria_2627 = int(df_2627.loc[df_2627['FTR'] == 'H'].groupby('HomeTeam').size().get(time_escolhido, 0) + df_2627.loc[df_2627['FTR'] == 'A'].groupby('AwayTeam').size().get(time_escolhido, 0))    
    empate_2627 = int(df_2627.loc[df_2627['FTR'] == 'D'].groupby('HomeTeam').size().get(time_escolhido, 0) + df_2627.loc[df_2627['FTR'] == 'D'].groupby('AwayTeam').size().get(time_escolhido, 0))
    derrota_2627 = int(df_2627.loc[df_2627['FTR'] == 'A'].groupby('HomeTeam').size().get(time_escolhido, 0) + df_2627.loc[df_2627['FTR'] == 'H'].groupby('AwayTeam').size().get(time_escolhido, 0))
    
    total_vitorias = [vitoria_2324, vitoria_2425, vitoria_2526, vitoria_2627]
    total_empates = [empate_2324, empate_2425, empate_2526, empate_2627]
    total_derrotas = [derrota_2324, derrota_2425, derrota_2526, derrota_2627]
    
    fig, axis = plt.subplots()
    bar_vitoria = axis.bar(temporadas, total_vitorias, label='Vitórias', color='green')
    bar_empates = axis.bar(temporadas, total_empates, bottom=total_vitorias, label='Empates', color='yellow')
    bar_derrota = axis.bar(temporadas, total_derrotas, bottom=[v+e for v, e in zip(total_vitorias, total_empates)], label='Derrotas', color='darkred')

    axis.bar_label(bar_vitoria, label_type='center')
    axis.bar_label(bar_empates, label_type='center')

    axis.bar_label(bar_derrota, label_type='center', color='white')
    axis.set_title(f'Relação entre Resultados por Temporadas - $\\bf{{{time_escolhido}}}$', fontsize='16')
    axis.set_xlabel('Temporadas', fontsize='11')

    axis.set_ylabel('Jogos', fontsize='11')
    axis.set_ylim(bottom=0, top=48)
    axis.set_yticks([0, 10, 20, 30, 38])
    
    plt.tight_layout()
    plt.legend()
    plt.grid(True, axis='y', alpha=0.6)
    plt.figtext(0.99, 0.01, 'Fonte: https://football-data.co.uk/', 
                ha='right', va='bottom',fontsize=7, color='gray')

    st.pyplot(plt.gcf())

    return