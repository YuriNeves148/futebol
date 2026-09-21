import streamlit as st
import pandas as pd
import url
from datetime import datetime
import datetime as dt
import acessa_datasets, analise_grafica
import matplotlib.pyplot as plt


def analise_por_time(competicao_df, time, escolhe_temporada):
    colunas = ['Partidas','Gols', 'Gols 1° Tempo por Partida', 'Gols por Partida', 'Aproveitamento (gols marcados)', 'Partidas Ganhas', 'Gols Sofridos', 'Gols Sofridos por Partida', 'Partidas Perdidas', 'Média de chutes', 
               'Média de Chutes ao Gol', 'Aproveitamento (gols marcados)','Cartão Amarelo (média)', 'Cartão Vermelho (média)', 
               'Faltas Cometidas (média)', 'Escanteios (média)'
               ]      
    dados = {
        'casa':{},
        'visitante':{}
    }
    for filtro in colunas:
        valor_casa, valor_visitante = gerenciamento_analise_time(competicao_df, filtro, time, escolhe_temporada)
        dados['casa'][filtro] = valor_casa
        dados['visitante'][filtro] = valor_visitante
    resumo = pd.DataFrame.from_dict(dados)
    st.dataframe(resumo.style.format({'Date':'{%d/%m/%Y}'}))

# filtros
def gerenciamento_analise_time(competicao_df, filtro, time, escolhe_temporada):
    # partidas
    if filtro == 'Partidas':
        partidas_casa = competicao_df.loc[competicao_df['HomeTeam'] == time].groupby('HomeTeam').size().get(time, 0)
        partidas_visitante =  competicao_df.loc[competicao_df['AwayTeam'] == time].groupby('AwayTeam').size().get(time, 0)
        return partidas_casa, partidas_visitante

    # gols
    if filtro == 'Gols':
        gols_casa = competicao_df.groupby('HomeTeam')['FTHG'].sum().get(time, 0)
        gols_visitante = competicao_df.groupby('AwayTeam')['FTAG'].sum().get(time, 0)
        return gols_casa, gols_visitante
    
    # gos primeiro tempo
    if filtro == 'Gols 1° Tempo por Partida':
        casa = competicao_df.groupby('HomeTeam')['HTHG'].mean().get(time, 0)
        fora = competicao_df.groupby('AwayTeam')['HTAG'].mean().get(time, 0)
        casa = f'{casa:.2f}'
        fora = f'{fora:.2f}'
        return casa, fora
    
    # gols por partida
    if filtro == 'Gols por Partida':
        gols_casa = competicao_df.groupby('HomeTeam')['FTHG'].mean().get(time, 0)
        gols_visitante = competicao_df.groupby('AwayTeam')['FTAG'].mean().get(time, 0)
        gols_casa = f'{gols_casa:.2f}'
        gols_visitante = f'{gols_visitante:.2f}'
        return gols_casa, gols_visitante
    
    # partidas ganhas
    if filtro == 'Partidas Ganhas':
        ganhas_casa = competicao_df.loc[competicao_df['FTR'] == 'H'].groupby('HomeTeam')['FTR'].size().get(time, 0)
        ganhas_fora = competicao_df.loc[competicao_df['FTR'] == 'A'].groupby('AwayTeam')['FTR'].size().get(time, 0)
        return ganhas_casa, ganhas_fora
    

    if filtro == 'Gols Sofridos':
        sofrido_casa = competicao_df.groupby('HomeTeam')['FTAG'].sum().get(time, 0)
        sofrido_fora = competicao_df.groupby('AwayTeam')['FTHG'].sum().get(time, 0)
        return sofrido_casa, sofrido_fora
    
    if filtro == 'Gols Sofridos por Partida':
        sofrido_casa = competicao_df.groupby('HomeTeam')['FTAG'].mean().get(time, 0)
        sofrido_casa = f'{sofrido_casa:.2f}'
        sofrido_fora = competicao_df.groupby('AwayTeam')['FTHG'].mean().get(time, 0)
        sofrido_fora = f'{sofrido_fora:.2f}'
        return sofrido_casa, sofrido_fora

    # partidas perdidas
    if filtro == 'Partidas Perdidas':
        perdida_casa = competicao_df.loc[competicao_df['FTR'] == 'A'].groupby('HomeTeam').size().get(time, 0)
        perdida_casa = f'{perdida_casa:.0f}'
        perdida_visit = competicao_df.loc[competicao_df['FTR'] == 'H'].groupby('AwayTeam').size().get(time, 0)
        perdida_visit = f'{perdida_visit:.0f}'
        return perdida_casa, perdida_visit
        
    # Chutes
    if filtro == 'Média de chutes':
        chute_casa = competicao_df.groupby('HomeTeam')['HS'].mean().get(time, 0)
        chute_fora = competicao_df.groupby('AwayTeam')['AS'].mean().get(time, 0)
        chute_casa = f'{chute_casa:.2f}'
        chute_fora = f'{chute_fora:.2f}'
        return chute_casa, chute_fora
    
    # chutes ao gol
    if filtro == 'Média de Chutes ao Gol':
        chute_casa = competicao_df.groupby('HomeTeam')['HST'].mean().get(time, 0)
        chute_fora = competicao_df.groupby('AwayTeam')['AST'].mean().get(time, 0)
        chute_casa = f'{chute_casa:.2f}'
        chute_fora = f'{chute_fora:.2f}'
        return chute_casa, chute_fora
    
    if filtro == 'Aproveitamento (gols marcados)':
        # quantidade de chutes dividido pela quantidade de gols marcados
        chutes_casa_ao_gol = competicao_df.groupby('HomeTeam')['HST'].sum().get(time, 0)
        gols_casa_ = competicao_df.groupby('HomeTeam')['FTHG'].sum().get(time, 0)
        apr_casa = (gols_casa_ / chutes_casa_ao_gol) * 100

        chutes_visitante_ao_gol = competicao_df.groupby('AwayTeam')['AST'].sum().get(time, 0)
        gols_visitante_ = competicao_df.groupby('AwayTeam')['FTAG'].sum().get(time, 0)
        apr_fora = (gols_visitante_ / chutes_visitante_ao_gol) * 100
        
        return f'{apr_casa:.2f}%', f'{apr_fora:.2f}%'

    # media de amarelo
    if filtro == 'Cartão Amarelo (média)':
        casa = competicao_df.groupby('HomeTeam')['HY'].mean().get(time, 0)
        fora = competicao_df.groupby('AwayTeam')['AY'].mean().get(time, 0)
        casa = f'{casa:.2f}'
        fora = f'{fora:.2f}'
        return casa, fora
    
    # media de vermelho
    if filtro == 'Cartão Vermelho (média)':
        casa = competicao_df.groupby('HomeTeam')['HR'].mean().get(time, 0)
        fora = competicao_df.groupby('AwayTeam')['AR'].mean().get(time, 0)
        casa = f'{casa:.2f}'
        fora = f'{fora:.2f}'
        return casa, fora
    
    # media de faltas
    if filtro == 'Faltas Cometidas (média)':
        casa = competicao_df.groupby('HomeTeam')['HF'].mean().get(time, 0)
        fora = competicao_df.groupby('AwayTeam')['AF'].mean().get(time, 0)
        casa = f'{casa:.2f}'
        fora = f'{fora:.2f}'
        return casa, fora

    # escanteios
    if filtro == 'Escanteios (média)':
        casa = competicao_df.groupby('HomeTeam')['HC'].mean().get(time, 0)
        fora = competicao_df.groupby('AwayTeam')['AC'].mean().get(time, 0)
        casa = f'{casa:.2f}'
        fora = f'{fora:.2f}'
        return casa, fora

def sequencia_vitorias_derrotas(competicao_df, time, escolhe_temporada):
    jogos = competicao_df.loc[(competicao_df['HomeTeam'] == time) | (competicao_df['AwayTeam'] == time)]
    maior_seq_vit = 0
    maior_seq_der = 0
    qtd_vitoria = 0
    qtd_derrota = 0
    # percorre cada jogo que o time jogou em formato de linha
    for _, linha in jogos.iterrows():
        # se ganhou dentro ou fora de casa
        if (linha['HomeTeam'] == time and linha['FTR'] == 'H') or (linha['AwayTeam'] == time and linha['FTR'] == 'A'):
            qtd_vitoria += 1
            if qtd_vitoria > maior_seq_vit:
                    maior_seq_vit = qtd_vitoria    
        else:
            qtd_vitoria = 0
        # se perdeu dentro ou fora de casa
        if (linha['HomeTeam'] == time and linha['FTR'] == 'A') or (linha['AwayTeam'] == time and linha['FTR'] == 'H'):
            qtd_derrota += 1
            if qtd_derrota > maior_seq_der:
                    maior_seq_der = qtd_derrota    
        else:
            qtd_derrota = 0
    st.write("Maior sequência de vitórias: ", maior_seq_vit)
    st.write("Maior sequência de derrotas: ", maior_seq_der)

    return 

def goleada(competicao_df, time, escolhe_temporada):
    maior_diferenca = 0
    armazena_diferenca = 0
    placar = [0,0]
    # quando o time jogou 
    jogos = competicao_df.loc[(competicao_df['HomeTeam'] == time) | (competicao_df['AwayTeam'] == time)]
    
    for _, linha in jogos.iterrows():
        # ganhou a partida?
        if (linha['HomeTeam'] == time and linha['FTR'] == 'H'):  
            # armazena diferenca
            armazena_diferenca = linha['FTHG'] - linha['FTAG']
            if armazena_diferenca > maior_diferenca:
                maior_diferenca = armazena_diferenca
                placar[0] = linha['FTHG']
                placar[1] = linha['FTAG']

        elif (linha['AwayTeam'] == time and linha['FTR'] == 'A'):
            # armazena diferenca
            armazena_diferenca = linha['FTAG'] - linha['FTHG']
            if armazena_diferenca > maior_diferenca:
                maior_diferenca = armazena_diferenca
                placar[0] = linha['FTHG']
                placar[1] = linha['FTAG']

    st.write(f"Maior goleada do {time}: {placar[0]} X {placar[1]}",)

    return

def ultimas_partidas(compericao_df, time, escolhe_temporada):
    # historico jogando dentro de casa
    partidas_casa = compericao_df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']].loc[compericao_df['HomeTeam'] == time]
    partidas_casa= partidas_casa.rename(columns={'Date': 'Data', 'HomeTeam':'Casa', 'AwayTeam':'Visitante', 'FTHG':'Gols Casa', 'FTAG':'Gols Visitante'})
    partidas_casa['RESULTADO'] = "EMPATE"
    partidas_casa.loc[partidas_casa['Gols Casa'] > partidas_casa['Gols Visitante'], 'RESULTADO'] = 'VITÓRIA'
    partidas_casa.loc[partidas_casa['Gols Casa'] < partidas_casa['Gols Visitante'], 'RESULTADO'] = 'DERROTA'    
    partidas_casa = partidas_casa.sort_values('Data', ascending=False).head()
    # historico jogando fora de casa
    partidas_fora = compericao_df[['Date' ,'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']].loc[compericao_df['AwayTeam'] == time]
    partidas_fora= partidas_fora.rename(columns={'Date': 'Data', 'HomeTeam':'Casa', 'AwayTeam':'Visitante', 'FTHG':'Gols Casa', 'FTAG':'Gols Visitante'})
    partidas_fora['RESULTADO'] = "EMPATE"
    partidas_fora.loc[partidas_fora['Gols Casa'] > partidas_fora['Gols Visitante'], 'RESULTADO'] = 'DERROTA'
    partidas_fora.loc[partidas_fora['Gols Casa'] < partidas_fora['Gols Visitante'], 'RESULTADO'] = 'VITÓRIA'
    
    partidas_fora = partidas_fora.sort_values('Data', ascending=False).head()
    # historico das 5 utimas partidas
    ultimas_partidas = compericao_df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']].loc[(compericao_df['HomeTeam'] == time) | (compericao_df['AwayTeam'] == time)]
    ultimas_partidas = ultimas_partidas.rename(columns={'Date': 'Data', 'HomeTeam':'Casa', 'AwayTeam':'Visitante', 'FTHG':'Gols Casa', 'FTAG':'Gols Visitante'})
    ultimas_partidas['RESULTADO'] = "EMPATE"
    ultimas_partidas.loc[ultimas_partidas['Gols Casa'] > ultimas_partidas['Gols Visitante'], 'RESULTADO'] = 'VITÓRIA'
    ultimas_partidas.loc[ultimas_partidas['Gols Casa'] < ultimas_partidas['Gols Visitante'], 'RESULTADO'] = 'DERROTA'
    ultimas_partidas = ultimas_partidas.sort_values('Data', ascending=False).head()

    # CONTINUAR FORMATANDO DATAS ***
    st.write("#### Últimas 5 partidas:")
    st.dataframe(ultimas_partidas.style.format({'Data': '{:%d/%m/%Y}'}), hide_index=True )    
    st.write("#### Últimas 5 - CASA:")
    st.dataframe(partidas_casa.style.format({'Data': '{:%d/%m/%Y}'}), hide_index=True)
    st.write("#### Últimas 5 - VISITANTE:")
    st.dataframe(partidas_fora.style.format({'Data': '{:%d/%m/%Y}'}), hide_index=True)

    return

# APENAS Brasil e Argentina
def br_arg_sequencia_vit_der(competicao_df, time, temporada_escolhida):
        jogos = competicao_df.loc[(competicao_df['HomeTeam'] == time) | (competicao_df['AwayTeam'] == time)]
        maior_seq_vit = 0
        maior_seq_der = 0
        qtd_vitoria = 0
        qtd_derrota = 0
        # percorre cada jogo que o time jogou em formato de linha
        for _, linha in jogos.iterrows():
            # se ganhou dentro ou fora de casa
            if (linha['HomeTeam'] == time and linha['FTR'] == 'H') or (linha['AwayTeam'] == time and linha['FTR'] == 'A'):
                qtd_vitoria += 1
                if qtd_vitoria > maior_seq_vit:
                        maior_seq_vit = qtd_vitoria    
            else:
                qtd_vitoria = 0
            # se perdeu dentro ou fora de casa
            if (linha['HomeTeam'] == time and linha['FTR'] == 'A') or (linha['AwayTeam'] == time and linha['FTR'] == 'H'):
                qtd_derrota += 1
                if qtd_derrota > maior_seq_der:
                        maior_seq_der = qtd_derrota    
            else:
                qtd_derrota = 0
        st.write("Maior sequência de vitórias: ", maior_seq_vit)
        st.write("Maior sequência de derrotas: ", maior_seq_der)

def br_arg_gerenciamento_por_time(competicao_df, filtro, time, temporada_escolhida):
    competicao_df = competicao_df.loc[(competicao_df['HomeTeam'] == time) | (competicao_df['AwayTeam'] == time)].copy()
    
    # gols
    if filtro == 'Gols':
        gols_casa = competicao_df.groupby('HomeTeam')['FTHG'].sum().get(time, 0)
        gols_visitante = competicao_df.groupby('AwayTeam')['FTAG'].sum().get(time, 0)
        return int(gols_casa), int(gols_visitante)
    
    # gols por partida
    if filtro == 'Gols por Partida':
        gols_casa = competicao_df.groupby('HomeTeam')['FTHG'].mean().get(time, 0)
        gols_visitante = competicao_df.groupby('AwayTeam')['FTAG'].mean().get(time, 0)
        gols_casa = f'{gols_casa:.2f}'
        gols_visitante = f'{gols_visitante:.2f}'
        return gols_casa, gols_visitante
    if filtro == 'Gols Sofridos':
        gols_sofridos_casa = competicao_df.groupby('HomeTeam')['FTAG'].sum().get(time, 0)
        gols_sofridos_visi = competicao_df.groupby('AwayTeam')['FTHG'].sum().get(time, 0)

        return f'{gols_sofridos_casa:.0f}', f'{gols_sofridos_visi:.0f}'
    if filtro == 'Gols Sofridos por Partida':
        partidas_casa = competicao_df.loc[competicao_df['HomeTeam'] == time].groupby('HomeTeam').size().get(time, 0)
        partidas_visitante =  competicao_df.loc[competicao_df['AwayTeam'] == time].groupby('AwayTeam').size().get(time, 0)
        
        gols_sofridos_casa = competicao_df.groupby('HomeTeam')['FTAG'].sum().get(time, 0)
        gols_sofridos_visi = competicao_df.groupby('AwayTeam')['FTHG'].sum().get(time, 0)
        if partidas_casa != 0:
            casa = gols_sofridos_casa / partidas_casa
        else:
            casa = 0
        if partidas_visitante != 0:
            visi = gols_sofridos_visi / partidas_visitante
        else:
            visi = 0
        return f'{casa:.2f}', f'{visi:.2f}'
    
    if filtro == 'Partidas Ganhas':
        ganhas_casa = competicao_df.loc[competicao_df['FTR'] == 'H'].groupby('HomeTeam').size().get(time, 0)
        ganhas_fora = competicao_df.loc[competicao_df['FTR'] == 'A'].groupby('AwayTeam').size().get(time, 0)
        return ganhas_casa, ganhas_fora

    # partidas perdidas
    if filtro == 'Partidas Perdidas':
        perdida_casa = competicao_df.loc[competicao_df['FTR'] == 'A'].groupby('HomeTeam').size().get(time, 0)
        perdida_visit = competicao_df.loc[competicao_df['FTR'] == 'H'].groupby('AwayTeam').size().get(time, 0)

        return perdida_casa, perdida_visit
    # partidas
    if filtro == 'Partidas':
        partidas_casa = competicao_df.loc[competicao_df['HomeTeam'] == time].groupby('HomeTeam').size().get(time, 0)
        partidas_visitante =  competicao_df.loc[competicao_df['AwayTeam'] == time].groupby('AwayTeam').size().get(time, 0)
        return partidas_casa, partidas_visitante
    
    if filtro == 'Aproveitamento (vitória)':
        # quantidade de chutes dividido pela quantidade de gols marcados
        jogos_casa = competicao_df.loc[competicao_df['HomeTeam'] == time].groupby('HomeTeam').size().get(time, 0)
        vitoria_casa = competicao_df.loc[(competicao_df['HomeTeam'] == time) & (competicao_df['FTR'] == 'H')].groupby('HomeTeam').size().get(time, 0)
        if jogos_casa != 0:
            apr_casa = (vitoria_casa / jogos_casa) * 100
        else:
            apr_casa = 0
        jogos_visi = competicao_df.loc[competicao_df['AwayTeam'] == time].groupby('AwayTeam').size().get(time, 0)
        vitoria_visi = competicao_df.loc[(competicao_df['AwayTeam'] == time) & (competicao_df['FTR'] == 'A')].groupby('AwayTeam').size().get(time, 0)
        if jogos_visi != 0:
            apr_visi = (vitoria_visi / jogos_visi) * 100
        else:
            apr_visi = 0

        return f'{apr_casa:.2f}%', f'{apr_visi:.2f}%'

def br_arg_goleada(competicao_df, time):
    maior_diferenca = 0
    armazena_diferenca = 0
    placar = [0,0]
    # quando o time jogou 
    jogos = competicao_df.loc[(competicao_df['HomeTeam'] == time) | (competicao_df['AwayTeam'] == time)]
    gols_sofridos = 0
    gols_feitos = 0
    for _, linha in jogos.iterrows():
        # ganhou a partida?
        if (linha['HomeTeam'] == time and linha['FTR'] == 'H'):  
            # armazena diferenca
            armazena_diferenca = linha['FTHG'] - linha['FTAG']
            if armazena_diferenca > maior_diferenca:
                maior_diferenca = armazena_diferenca
                placar[0] = linha['FTHG']
                placar[1] = linha['FTAG']

        elif (linha['AwayTeam'] == time and linha['FTR'] == 'A'):
            # armazena diferenca
            armazena_diferenca = linha['FTAG'] - linha['FTHG']
            if armazena_diferenca > maior_diferenca:
                maior_diferenca = armazena_diferenca
                placar[0] = linha['FTHG']
                placar[1] = linha['FTAG']

        # SALDO DE GOLS
        if (linha['HomeTeam'] == time):
            gols_sofridos += linha['FTAG'] 
        elif (linha['AwayTeam'] == time):
            gols_sofridos += linha['FTHG']
        if (linha['HomeTeam'] == time):
            gols_feitos += linha['FTHG'] 
        elif (linha['AwayTeam'] == time):
            gols_feitos += linha['FTAG']
        saldo = int(gols_feitos - gols_sofridos)
        
    st.write(f"Maior goleada do {time}: {placar[0]:.0f} X {placar[1]:.0f}")
    st.write(f"Saldo de gols do {time}: ", saldo) # eu sei, está mal organizado, vamos ter mais paciencia com o coleguinha?

    return

def br_arg_ultimas_partidas(compericao_df, time, temporada_escolhida):
    # TRABALHAR COM A DATA RETORNADA
    # historico jogando dentro de casa
    compericao_df= compericao_df.rename(columns={'Date': 'Data', 'HomeTeam':'Casa', 'AwayTeam':'Visitante', 'FTHG':'Gols Casa', 'FTAG':'Gols Visitante'})
    partidas_casa = compericao_df[['Data', 'Casa', 'Visitante', 'Gols Casa', 'Gols Visitante']].loc[compericao_df['Casa'] == time]
    partidas_casa['RESULTADO'] = "EMPATE"
    partidas_casa.loc[partidas_casa['Gols Casa'] > partidas_casa['Gols Visitante'], 'RESULTADO'] = 'VITÓRIA'
    partidas_casa.loc[partidas_casa['Gols Casa'] < partidas_casa['Gols Visitante'], 'RESULTADO'] = 'DERROTA'    
    partidas_casa = partidas_casa.tail()
    # historico jogando fora de casa
    partidas_fora = compericao_df[['Data' ,'Casa', 'Visitante', 'Gols Casa', 'Gols Visitante']].loc[compericao_df['Visitante'] == time]
    partidas_fora['RESULTADO'] = "EMPATE"
    partidas_fora.loc[partidas_fora['Gols Casa'] > partidas_fora['Gols Visitante'], 'RESULTADO'] = 'VITÓRIA'
    partidas_fora.loc[partidas_fora['Gols Casa'] < partidas_fora['Gols Visitante'], 'RESULTADO'] = 'DERROTA'
    partidas_fora = partidas_fora.tail()
    # historico das 5 utimas partidas
    ultimas_partidas = compericao_df[['Data', 'Casa', 'Visitante', 'Gols Casa', 'Gols Visitante']].loc[(compericao_df['Casa'] == time) | (compericao_df['Visitante'] == time)]
    ultimas_partidas['RESULTADO'] = "EMPATE"
    ultimas_partidas.loc[ultimas_partidas['Gols Casa'] > ultimas_partidas['Gols Visitante'], 'RESULTADO'] = 'VITÓRIA'
    ultimas_partidas.loc[ultimas_partidas['Gols Casa'] < ultimas_partidas['Gols Visitante'], 'RESULTADO'] = 'DERROTA'
    ultimas_partidas = ultimas_partidas.tail()

    partidas_casa['Gols Casa'] = partidas_casa['Gols Casa'].astype(int)
    partidas_casa['Gols Visitante'] = partidas_casa['Gols Visitante'].astype(int)
    partidas_fora['Gols Casa'] = partidas_fora['Gols Casa'].astype(int)
    partidas_fora['Gols Visitante'] = partidas_fora['Gols Visitante'].astype(int)
    ultimas_partidas['Gols Casa'] = ultimas_partidas['Gols Casa'].astype(int)
    ultimas_partidas['Gols Visitante'] = ultimas_partidas['Gols Visitante'].astype(int)
    
    st.write("#### Últimas 5 partidas:")
    st.dataframe(ultimas_partidas.style.format({'Data':'{:%d/%m/%Y}'}), hide_index=True)    
    st.write("#### Últimas 5 - CASA:")
    st.dataframe(partidas_casa.style.format({'Data':'{:%d/%m/%Y}'}), hide_index=True)
    st.write("#### Últimas 5 - VISITANTE:")
    st.dataframe(partidas_fora.style.format({'Data':'{:%d/%m/%Y}'}), hide_index=True)

    return

def bra_arg_analie(competicao_df, competicao_escolhida, time, temporada_escolhida):
    # maior sequencia de vitorias
    colunas = ['Partidas', 'Partidas Ganhas', 'Gols', 'Gols por Partida', 'Aproveitamento (vitória)', 'Partidas Perdidas', 'Gols Sofridos', 'Gols Sofridos por Partida']
    dados = {
        'casa':{},
        'visitante':{}
    }
    for filtro in colunas:
        valor_casa, valor_visitante = br_arg_gerenciamento_por_time(competicao_df, filtro, time, temporada_escolhida)
        dados['casa'][filtro] = valor_casa
        dados['visitante'][filtro] = valor_visitante
    resumo = pd.DataFrame.from_dict(dados)
    st.dataframe(resumo)
    br_arg_sequencia_vit_der(competicao_df, time, temporada_escolhida)
    br_arg_goleada(competicao_df, time)

    return


def analise_por_juiz(competicao_df, escolhe_temporada):
    jogos = competicao_df.groupby('Referee').size()
    # media de cartoes e faltas por jogo
    amarelo = round(((competicao_df.groupby('Referee')['HY'].sum()
               + competicao_df.groupby('Referee')['AY'].sum()) 
               / competicao_df.groupby('Referee').size()), 2)
    vermelho = round(((competicao_df.groupby('Referee')['HR'].sum()
               + competicao_df.groupby('Referee')['AR'].sum()) 
               / competicao_df.groupby('Referee').size()), 2)
    falta = round(((competicao_df.groupby('Referee')['HF'].sum()
               + competicao_df.groupby('Referee')['AF'].sum()) 
               / competicao_df.groupby('Referee').size()), 1)
    
    tabela = pd.DataFrame({
        'Jogos Apitados': jogos, 
        'Faltas (média)':falta,
        'Cartão A. (média)':amarelo,
        'Cartão V. (média)':vermelho
                           })
    tabela = tabela.rename_axis('Nome')
    st.dataframe(tabela.sort_values(by='Jogos Apitados', ascending=False))

def time_por_competicao(competicao_escolhida, temporada_escolhida):    
    if competicao_escolhida == 'Inglaterra':
        if temporada_escolhida == '26/27':
            inglaterra_1 = pd.read_csv(url.inglaterra_1)
            inglaterra_1['Date'] = pd.to_datetime(inglaterra_1['Date'], format='%d/%m/%Y')
        elif temporada_escolhida == '25/26':
            inglaterra_1 = acessa_datasets.premier_2526_df
        elif temporada_escolhida == '24/25':
            inglaterra_1 = acessa_datasets.premier_2425_df
        elif temporada_escolhida == '23/24':
            inglaterra_1 = acessa_datasets.premier_2324_df
        elif temporada_escolhida == '23/24 até 26/27':
            inglaterra_1 = acessa_datasets.premier_df

            
        escolhe_time = st.selectbox('Escolha um time da Premier League', inglaterra_1['HomeTeam'].sort_values().unique())
        st.markdown(f"<h3 style='text-align: center;'>Análise do {escolhe_time}</h3>", unsafe_allow_html=True)
        grafico = st.checkbox('Análise Gráfica', False)
        if grafico:
            analise_grafica.barra_marc_sof(competicao_escolhida, escolhe_time)
            analise_grafica.barra_vit_derr(competicao_escolhida, escolhe_time)
            analise_grafica.aproveitamento(competicao_escolhida, escolhe_time)
        analise_por_time(inglaterra_1, escolhe_time, escolhe_temporada)
        sequencia_vitorias_derrotas(inglaterra_1, escolhe_time, escolhe_temporada)
        goleada(inglaterra_1, escolhe_time, escolhe_temporada)
        ultimas_partidas(inglaterra_1, escolhe_time, escolhe_temporada)
        st.write("## Análise por Juiz")
        analise_por_juiz(inglaterra_1, escolhe_temporada)

    elif competicao_escolhida == 'Brasil':
        if temporada_escolhida == '26/27':
            brasileirao = acessa_datasets.brasil_26_df
        elif temporada_escolhida == '25/26':
            brasileirao = acessa_datasets.brasil_25_df
        elif temporada_escolhida == '24/25':
            brasileirao = acessa_datasets.brasil_24_df
        elif temporada_escolhida == '23/24':
            brasileirao = acessa_datasets.brasil_23_df
        elif temporada_escolhida == '23/24 até 26/27':
            brasileirao = acessa_datasets.brasil_df

        escolhe_time = st.selectbox('Escolha um time do Brasileirão:', brasileirao['HomeTeam'].sort_values().unique())
        st.markdown(f"<h3 style='text-align: center;'>Análise do {escolhe_time}</h3>", unsafe_allow_html=True)
        grafico = st.checkbox('Análise Gráfica', False)
        if grafico:
            analise_grafica.barra_marc_sof(competicao_escolhida, escolhe_time)
            analise_grafica.barra_vit_derr(competicao_escolhida, escolhe_time)
            analise_grafica.aproveitamento(competicao_escolhida, escolhe_time)
        bra_arg_analie(brasileirao, competicao_escolhida, escolhe_time, temporada_escolhida)
        br_arg_ultimas_partidas(brasileirao, escolhe_time, temporada_escolhida)
        
    elif competicao_escolhida == 'Espanha':
        if temporada_escolhida == '26/27':
            espanha_1 = pd.read_csv(url.espanha_1)  
            espanha_1['Date'] = pd.to_datetime(espanha_1['Date'], format='%d/%m/%Y')  
        elif temporada_escolhida == '25/26':
            espanha_1 = acessa_datasets.laliga_2526_df
        elif temporada_escolhida == '24/25':
            espanha_1 = acessa_datasets.laliga_2425_df
        elif temporada_escolhida == '23/24':
            espanha_1 = acessa_datasets.laliga_2324_df
        elif temporada_escolhida == '23/24 até 26/27':
            espanha_1 = acessa_datasets.laliga_df

        escolhe_time = st.selectbox('Escolha um time da competição da La Liga', espanha_1['HomeTeam'].sort_values().unique())
        st.markdown(f"<h3 style='text-align: center;'>Análise do {escolhe_time}</h3>", unsafe_allow_html=True)
        grafico = st.checkbox('Análise Gráfica', False)
        if grafico:
            analise_grafica.barra_marc_sof(competicao_escolhida, escolhe_time)
            analise_grafica.barra_vit_derr(competicao_escolhida, escolhe_time)
            analise_grafica.aproveitamento(competicao_escolhida, escolhe_time)
        analise_por_time(espanha_1 ,escolhe_time, temporada_escolhida)
        sequencia_vitorias_derrotas(espanha_1, escolhe_time, temporada_escolhida)
        goleada(espanha_1, escolhe_time, temporada_escolhida)
        ultimas_partidas(espanha_1, escolhe_time, temporada_escolhida)
    elif competicao_escolhida == 'Alemanha':
        if temporada_escolhida == '26/27':
            bundesliga = pd.read_csv(url.bundesliga)
            bundesliga['Date'] = pd.to_datetime(bundesliga['Date'],  format='%d/%m/%Y')
        elif temporada_escolhida == '25/26':
            bundesliga = acessa_datasets.bundesliga_2526_df
        elif temporada_escolhida == '24/25':
            bundesliga = acessa_datasets.bundesliga_2425_df
        elif temporada_escolhida == '23/24':
            bundesliga = acessa_datasets.bundesliga_2324_df
        elif temporada_escolhida == '23/24 até 26/27':
            bundesliga = acessa_datasets.bundesliga_df

        escolhe_time = st.selectbox('Escolha um time da Bundeliga', bundesliga['HomeTeam'].sort_values().unique())
        st.markdown(f"<h3 style='text-align: center;'>Análise do {escolhe_time}</h3>", unsafe_allow_html=True)
        grafico = st.checkbox('Análise Gráfica', False)
        if grafico:
            analise_grafica.barra_marc_sof(competicao_escolhida, escolhe_time)
            analise_grafica.barra_vit_derr(competicao_escolhida, escolhe_time)
            analise_grafica.aproveitamento(competicao_escolhida, escolhe_time)
        
        analise_por_time(bundesliga, escolhe_time, escolhe_temporada)
        sequencia_vitorias_derrotas(bundesliga, escolhe_time, escolhe_temporada)
        goleada(bundesliga, escolhe_time, escolhe_temporada)
        ultimas_partidas(bundesliga, escolhe_time, escolhe_temporada)
    elif competicao_escolhida == 'Italia':
        if temporada_escolhida == '26/27':
            italia_1 = pd.read_csv(url.italia_1)
            italia_1['Date'] = pd.to_datetime(italia_1['Date'],  format='%d/%m/%Y')
        elif temporada_escolhida == '25/26':
            italia_1 = acessa_datasets.italia_2526_df
        elif temporada_escolhida == '24/25':
            italia_1 = acessa_datasets.italia_2425_df
        elif temporada_escolhida == '23/24':
            italia_1 = acessa_datasets.italia_2324_df
        elif temporada_escolhida == '23/24 até 26/27':
            italia_1 = acessa_datasets.italia_df

        escolhe_time = st.selectbox('Escolha um time da liga Italiana', italia_1['HomeTeam'].sort_values().unique())
        st.markdown(f"<h3 style='text-align: center;'>Análise do {escolhe_time}</h3>", unsafe_allow_html=True)
        grafico = st.checkbox('Análise Gráfica', False)
        if grafico:
            analise_grafica.barra_marc_sof(competicao_escolhida, escolhe_time)
            analise_grafica.barra_vit_derr(competicao_escolhida, escolhe_time)
            analise_grafica.aproveitamento(competicao_escolhida, escolhe_time)
        analise_por_time(italia_1, escolhe_time, escolhe_temporada)
        sequencia_vitorias_derrotas(italia_1, escolhe_time, escolhe_temporada)
        goleada(italia_1, escolhe_time, escolhe_temporada)
        ultimas_partidas(italia_1, escolhe_time, escolhe_temporada)
    elif competicao_escolhida == 'França':
        if temporada_escolhida == '26/27':
            df = pd.read_csv(url.franca_1)
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        elif temporada_escolhida == '25/26':
            df = acessa_datasets.ligue1_2526_df
        elif temporada_escolhida == '24/25':
            df = acessa_datasets.ligue1_2425_df
        elif temporada_escolhida == '23/24':
            df = acessa_datasets.italia_2324_df
        elif temporada_escolhida == '23/24 até 26/27':
            df = acessa_datasets.ligue1_df
                
        escolhe_time = st.selectbox('Escolha um time da Ligue 1:', df['HomeTeam'].sort_values().unique())
        st.markdown(f"<h3 style='text-align: center;'>Análise do {escolhe_time}</h3>", unsafe_allow_html=True)
        grafico = st.checkbox('Análise Gráfica', False)
        if grafico:
            analise_grafica.barra_marc_sof(competicao_escolhida, escolhe_time)
            analise_grafica.barra_vit_derr(competicao_escolhida, escolhe_time)
            analise_grafica.aproveitamento(competicao_escolhida, escolhe_time)
        
        analise_por_time(df, escolhe_time, escolhe_temporada)
        sequencia_vitorias_derrotas(df, escolhe_time, escolhe_temporada)
        goleada(df, escolhe_time, escolhe_temporada)
        ultimas_partidas(df, escolhe_time, escolhe_temporada)
    elif competicao_escolhida == 'Holanda':
        if temporada_escolhida == '26/27':
            df = pd.read_csv(url.holanda_1)
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        elif temporada_escolhida == '25/26':
            df = acessa_datasets.holanda_2526_df
        elif temporada_escolhida == '24/25':
            df = acessa_datasets.holanda_2425_df
        elif temporada_escolhida == '23/24':
            df = acessa_datasets.holanda_2324_df
        elif temporada_escolhida == '23/24 até 26/27':
            df = acessa_datasets.holanda_df
        escolhe_time = st.selectbox('Escolha um time da Holanda:', df['HomeTeam'].sort_values().unique())
        st.markdown(f"<h3 style='text-align: center;'>Análise do {escolhe_time}</h3>", unsafe_allow_html=True)
        grafico = st.checkbox('Análise Gráfica', False)
        if grafico:
            analise_grafica.barra_marc_sof(competicao_escolhida, escolhe_time)
            analise_grafica.barra_vit_derr(competicao_escolhida, escolhe_time)
            analise_grafica.aproveitamento(competicao_escolhida, escolhe_time)
        
        analise_por_time(df, escolhe_time, temporada_escolhida)
        sequencia_vitorias_derrotas(df, escolhe_time, temporada_escolhida)
        goleada(df, escolhe_time, temporada_escolhida)
        ultimas_partidas(df, escolhe_time, temporada_escolhida)
    elif competicao_escolhida == 'Portugal':
        if temporada_escolhida == '26/27':
            portugla_1 = pd.read_csv(url.portugla_1)
            portugla_1['Date'] = pd.to_datetime(portugla_1['Date'], format='%d/%m/%Y')
        elif temporada_escolhida == '25/26':
            portugla_1 = acessa_datasets.portugal_2526_df
        elif temporada_escolhida == '24/25':
            portugla_1 = acessa_datasets.portugal_2425_df
        elif temporada_escolhida == '23/24':
            portugla_1 = acessa_datasets.portugal_2324_df
        elif temporada_escolhida == '23/24 até 26/27':
            portugla_1 = acessa_datasets.portugal_df

        escolhe_time = st.selectbox('Escolha um time de Portugal:', portugla_1['HomeTeam'].sort_values().unique())
        st.markdown(f"<h3 style='text-align: center;'>Análise do {escolhe_time}</h3>", unsafe_allow_html=True)
        grafico = st.checkbox('Análise Gráfica', False)
        if grafico:
            analise_grafica.barra_marc_sof(competicao_escolhida, escolhe_time)
            analise_grafica.barra_vit_derr(competicao_escolhida, escolhe_time)
            analise_grafica.aproveitamento(competicao_escolhida, escolhe_time)
        
        analise_por_time(portugla_1, escolhe_time, temporada_escolhida)
        sequencia_vitorias_derrotas(portugla_1, escolhe_time, temporada_escolhida)
        goleada(portugla_1, escolhe_time, temporada_escolhida)
        ultimas_partidas(portugla_1, escolhe_time, temporada_escolhida)
    elif competicao_escolhida == 'Escocia':
        if temporada_escolhida == '26/27':
            escocia_1 = pd.read_csv(url.escocia_1)
            escocia_1['Date'] = pd.to_datetime(escocia_1['Date'], format='%d/%m/%Y')
        elif temporada_escolhida == '25/26':
            escocia_1 = acessa_datasets.escocia_2526_df
        elif temporada_escolhida == '24/25':
            escocia_1 = acessa_datasets.escocia_2425_df
        elif temporada_escolhida == '23/24':
            escocia_1 = acessa_datasets.escocia_2324_df
        elif temporada_escolhida == '23/24 até 26/27':
            escocia_1 = acessa_datasets.escocia_df

        escolhe_time = st.selectbox('Escolha um time da Esócia:', escocia_1['HomeTeam'].sort_values().unique())
        st.markdown(f"<h3 style='text-align: center;'>Análise do {escolhe_time}</h3>", unsafe_allow_html=True)
        grafico = st.checkbox('Análise Gráfica', False)
        if grafico:
            analise_grafica.barra_marc_sof(competicao_escolhida, escolhe_time)
            analise_grafica.barra_vit_derr(competicao_escolhida, escolhe_time)
            analise_grafica.aproveitamento(competicao_escolhida, escolhe_time)
        
        analise_por_time(escocia_1, escolhe_time, temporada_escolhida)
        sequencia_vitorias_derrotas(escocia_1, escolhe_time, temporada_escolhida)
        goleada(escocia_1, escolhe_time, temporada_escolhida)
        ultimas_partidas(escocia_1, escolhe_time, temporada_escolhida)
    elif competicao_escolhida == 'Argentina':
        if temporada_escolhida == '26/27':
            argentina_1 = acessa_datasets.argentina_26_df
            argentina_1['Date'] = pd.to_datetime(argentina_1['Date'], format="%d/%m/%Y")    
        elif temporada_escolhida == '25/26':
            argentina_1 = acessa_datasets.argentina_25_df
        elif temporada_escolhida == '24/25':
            argentina_1 = acessa_datasets.argentina_24_df
        elif temporada_escolhida == '23/24':
            argentina_1 = acessa_datasets.argentina_23_df
        elif temporada_escolhida == '23/24 até 26/27':
            argentina_1 = acessa_datasets.argentina_df

        escolhe_time = st.selectbox('Escolha um time da Argentina:', argentina_1['HomeTeam'].sort_values().unique())
        st.markdown(f"<h3 style='text-align: center;'>Análise do {escolhe_time}</h3>", unsafe_allow_html=True)
        grafico = st.checkbox('Análise Gráfica', False)
        if grafico:
            analise_grafica.barra_marc_sof(competicao_escolhida, escolhe_time)
            analise_grafica.barra_vit_derr(competicao_escolhida, escolhe_time)
            analise_grafica.aproveitamento(competicao_escolhida, escolhe_time)
        bra_arg_analie(argentina_1, competicao_escolhida, escolhe_time, temporada_escolhida)  
        br_arg_ultimas_partidas(argentina_1, escolhe_time, temporada_escolhida)


st.write("<h1 style='text-align:center;'> Análise do Time por Temporada </h1>", unsafe_allow_html=True)
st.write("### Escolha a competição e o time pertencente: ")

# selecionar competicao e seus respectivos times
escolhe_temporada = st.selectbox("Escolha a temporada: ", ["26/27", "25/26", "24/25", "23/24", "23/24 até 26/27"])
competicoes_ = ['Inglaterra', 'Brasil', 'Espanha', 'Alemanha', 'Italia', 'França', 'Holanda', 'Portugal', 'Escocia', 'Argentina']
escolhe_comp = st.selectbox("Escolha a competição: ",competicoes_)
time_por_competicao(escolhe_comp, escolhe_temporada)





