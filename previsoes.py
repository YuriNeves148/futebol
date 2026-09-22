import pandas as pd
from scipy.stats import poisson
import acessa_datasets as acds



def recebe(competicoa_df, casa, visitante):
    df = competicoa_df.copy()
    jogos_casa = df.loc[df['HomeTeam'] == casa]
    jogos_visi = df.loc[df['AwayTeam'] == visitante]
    qtd_jogos_casa = jogos_casa.loc[jogos_casa['HomeTeam'] == casa].shape[0]
    qtd_jogos_visi = jogos_visi.loc[jogos_visi['AwayTeam'] == visitante].shape[0]
    return gols(df, casa, visitante, jogos_casa, jogos_visi, qtd_jogos_casa, qtd_jogos_visi)

def gols(df, casa, visitante, jogos_casa, jogos_visi, qtd_jogos_casa, qtd_jogos_visi):
    # gols marcados e sofridos
    gols_marcados_casa = jogos_casa.loc[jogos_casa['HomeTeam'] == casa]['FTHG'].sum()
    gols_marcados_visi = jogos_visi.loc[jogos_visi['AwayTeam'] == visitante]['FTAG'].sum()
    gols_sof_casa = jogos_casa.loc[jogos_casa['HomeTeam'] == casa]['FTAG'].sum()
    gols_sof_visi = jogos_visi.loc[jogos_visi['AwayTeam'] == visitante]['FTHG'].sum()
    # media de marcados e sofridos
    media_marc_casa = gols_marcados_casa / qtd_jogos_casa
    media_sof_casa = gols_sof_casa / qtd_jogos_casa
    media_marc_visi = gols_marcados_visi / qtd_jogos_visi
    media_sof_visi = gols_sof_visi / qtd_jogos_visi

    # média da liga casa e fora
    liga_gols_marc_casa_media = df['FTHG'].mean()
    liga_gols_marc_visi_media = df['FTAG'].mean() 
    liga_gols_sof_casa_media = df['FTAG'].mean()
    liga_gols_sof_visi_media = df['FTHG'].mean() 
    
    # forca de ATAQUE em casa e fora
    forca_ataque_casa = round(media_marc_casa / liga_gols_marc_casa_media,2) 
    forca_ataque_visi = round(media_marc_visi / liga_gols_marc_visi_media, 2)
    # forca de DEFESA em casa e fora
    forca_defesa_casa = round(media_sof_casa / liga_gols_sof_casa_media, 2)
    forca_defesa_visi = round(media_sof_visi / liga_gols_sof_visi_media, 2)

    # (o quao bem o time A ataca em casa) vs (o quao mal o time B defende como visitante)
    lambda_casa = forca_ataque_casa * forca_defesa_visi * liga_gols_marc_casa_media
    lambda_fora = forca_ataque_visi * forca_defesa_casa * liga_gols_sof_casa_media

    # funcao que calcula a porcentagem dos gols
    return porcentagem_gols(lambda_casa, lambda_fora)
     

def porcentagem_gols(lambda_casa, lambda_fora):
    lambda_total = lambda_casa + lambda_fora
    dicio = {}
    dicio['Partida','Fixo'] = []
    dicio['Partida','Over'] = []
    dicio['Partida','Under'] = []
    dicio['Casa','Fixo'] = []
    dicio['Casa','Over'] = []
    dicio['Casa','Under'] = []
    dicio['Visitante','Fixo'] = []
    dicio['Visitante','Over'] = []
    dicio['Visitante','Under'] = []
    
    for i in range(0, 7):
        # encontrando a probabilidade de cada um e adicionando no dicionario
        casa_fixo = round(float(poisson.pmf(i, lambda_casa)*100),2)
        casa_over = round(float((1 - poisson.cdf(i, lambda_casa))*100),2)
        casa_under = round(float(poisson.cdf(i, lambda_casa)*100),2)

        fora_fixo = round(float(poisson.pmf(i, lambda_fora)*100),2)
        fora_over = round(float((1 - poisson.cdf(i, lambda_fora))*100),2)
        fora_under = round(float(poisson.cdf(i, lambda_fora)*100),2)
        
        partida_fixo = round(float(poisson.pmf(i, lambda_total)*100),2)
        partida_over = round(float((1 - poisson.cdf(i, lambda_total))*100),2)
        partida_under = round(float(poisson.cdf(i, lambda_total)*100),2)
        
        dicio['Partida', 'Fixo'].append(partida_fixo)
        dicio['Partida', 'Over'].append(partida_over)
        dicio['Partida', 'Under'].append(partida_under)
        dicio['Casa', 'Fixo'].append(casa_fixo)
        dicio['Casa', 'Over'].append(casa_over)
        dicio['Casa', 'Under'].append(casa_under)
        dicio['Visitante', 'Fixo'].append(fora_fixo)
        dicio['Visitante', 'Over'].append(fora_over)
        dicio['Visitante', 'Under'].append(fora_under)

    return dicio
