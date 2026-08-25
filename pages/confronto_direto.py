import pandas as pd
import streamlit as st
import datetime as dt
st.write("## Análise por confronto")

# aproveitmaento de chutes: (chutes_ao_gol / total_chutes) ou (gols / total_chutes)
# ultimas 5 partidas dos times, assim tem um pequeno historico de cada um

def estatisticas(competicao_df, time1, time2):
    # media de gols:
    print('\n\n\naaaa')
    partidas_df = competicao_df.loc[(( (competicao_df['HomeTeam'] == time1) | (competicao_df['AwayTeam'] == time1) ) 
                             & ( (competicao_df['HomeTeam'] == time2) | (competicao_df['AwayTeam'] == time2) ) 
                             )]
    
    partidas_df['Date'] = pd.to_datetime(partidas_df['Date']).dt.strftime('%d/%m/%Y')

    partidas_gol = []
    primeiro_tempo = []
    cartao_a = []
    cartao_v = []
    conta_ambas = 0
    total_jogos = 0

    for _, linha in partidas_df.iterrows():
        partidas_gol.append(linha['FTHG']+linha['FTAG'])
        primeiro_tempo.append(linha['HTHG'] + linha['HTAG'])
        cartao_a.append(linha['HY'] + linha['AY'])
        cartao_v.append(linha['HR'] + linha['AR'])
        total_jogos += 1
        if (linha['FTHG'] > 0 and linha['FTAG'] > 0):
            conta_ambas += 1

    media = sum(partidas_gol) / len(partidas_gol)
    media_1tempo = sum(primeiro_tempo) / len(primeiro_tempo)
    media_cartao_a = sum(cartao_a) / len(cartao_a)
    media_cartao_v = sum(cartao_v) / len(cartao_v)
    st.markdown("#### Histórico do confronto")
    st.write(f'Media de gols por partida: {media:.2f}')
    st.write(f'Media de gols no 1° tempo: {media_1tempo:.2f}')
    st.write(f'Media de cartão amarelo por partida: {media_cartao_a:.2f}')
    st.write(f'Media de cartão vermelho por partida: {media_cartao_v:.2f}')
    st.write(f'Ambas marcam: {conta_ambas} / {total_jogos}')

    return

def historico(competicao_df, time1, time2):
    partidas_df = competicao_df.loc[(( (competicao_df['HomeTeam'] == time1) | (competicao_df['AwayTeam'] == time1) ) 
                             & ( (competicao_df['HomeTeam'] == time2) | (competicao_df['AwayTeam'] == time2) ) 
                             )].copy()
    partidas_df['Date'] = pd.to_datetime(partidas_df['Date'])
    
    # resumo ráido
    st.write("#### Visão geral")
    partidas_df = partidas_df.rename(columns={'Date':'Data', 'HomeTeam':'Casa', 'AwayTeam':'Visitante', 'FTHG':'Gols Casa', 'FTAG':'Gols Visitante'})
    partidas_df = partidas_df.sort_values('Data', ascending=False).head(8)
    partidas_df['Data'] = partidas_df['Data'].dt.strftime('%d/%m/%Y')
    st.dataframe(partidas_df[['Data', 'Casa', 'Gols Casa','Visitante', 'Gols Visitante']], hide_index=True)
    return

def historico_por_time(competicao_df, time1, time2):
    # ultimas 5 partidas de cada time
    hist_time1 = competicao_df.loc[(competicao_df['HomeTeam'] == time1) | (competicao_df['AwayTeam'] == time1)]
    hist_time2 = competicao_df.loc[(competicao_df['HomeTeam'] == time2) | (competicao_df['AwayTeam'] == time2)]
    tabela_time1 = hist_time1[['Date', 'HomeTeam', 'FTHG',  'AwayTeam', 'FTAG']]
    tabela_time2 = hist_time2[['Date', 'HomeTeam', 'FTHG',  'AwayTeam', 'FTAG']]
    tabela_time1['Date'] = pd.to_datetime(tabela_time1['Date'])
    tabela_time2['Date'] = pd.to_datetime(tabela_time2['Date'])
    tabela_time1['Resultado'] = ""
    tabela_time2['Resultado'] = ""

    for indice, linha in tabela_time1.iterrows():
        if linha['HomeTeam'] == time1:
            if linha['FTHG'] > linha['FTAG']:
                tabela_time1.loc[indice, 'Resultado'] = 'Vitória'
            elif linha['FTHG'] < linha['FTAG']:
                tabela_time1.loc[indice, 'Resultado'] = 'Derrota'
            else:
                tabela_time1.loc[indice, 'Resultado'] = 'Empate'
        elif linha['AwayTeam'] == time1:
            if linha['FTAG'] > linha['FTHG']:
                tabela_time1.loc[indice, 'Resultado'] = 'Vitória'
            elif linha['FTAG'] < linha['FTHG']:
                tabela_time1.loc[indice, 'Resultado'] = 'Derrota'
            else:
                tabela_time1.loc[indice, 'Resultado'] = 'Empate'
    for indice, linha in tabela_time2.iterrows():
        if linha['HomeTeam'] == time2:
            if linha['FTHG'] > linha['FTAG']:
                tabela_time2.loc[indice, 'Resultado'] = 'Vitória'
            elif linha['FTHG'] < linha['FTAG']:
                tabela_time2.loc[indice, 'Resultado'] = 'Derrota'
            else:
                tabela_time2.loc[indice, 'Resultado'] = 'Empate'
        elif linha['AwayTeam'] == time2:
            if linha['FTAG'] > linha['FTHG']:
                tabela_time2.loc[indice, 'Resultado'] = 'Vitória'
            elif linha['FTAG'] < linha['FTHG']:
                tabela_time2.loc[indice, 'Resultado'] = 'Derrota'
            else:
                tabela_time2.loc[indice, 'Resultado'] = 'Empate'
    tabela_time1 = tabela_time1.rename(columns={'Date': 'Data', 'HomeTeam':'Casa', 'AwayTeam':'Visitante', 'FTHG': 'Gols Casa', 'FTAG': 'Gols Visitante'})
    tabela_time2 = tabela_time2.rename(columns={'Date': 'Data', 'HomeTeam':'Casa', 'AwayTeam':'Visitante', 'FTHG': 'Gols Casa', 'FTAG': 'Gols Visitante'})

    tabela_time1 = tabela_time1.sort_values('Data', ascending=False).head()
    tabela_time2= tabela_time2.sort_values('Data', ascending=False).head()

    tabela_time1['Data'] = tabela_time1['Data'].dt.strftime('%d/%m/%Y')
    tabela_time2['Data'] = tabela_time2['Data'].dt.strftime('%d/%m/%Y')

    st.write(f"#### Últimas 5 partidas do {time1}:")
    st.dataframe(tabela_time1, hide_index=True)
    st.write(f"#### Últimas 5 partidas do {time2}:")
    st.dataframe(tabela_time2, hide_index=True)
    return

def time_por_competicao(comp_escolhida):    
    if comp_escolhida == 'Premier League':
        escolhe_time1 = st.selectbox('Escolha um time', premier_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', premier_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Os times devem ser diferentes para esse tipo de análise.")
            return
        historico(premier_df, escolhe_time1, escolhe_time2)
        estatisticas(premier_df, escolhe_time1, escolhe_time2)
        historico_por_time(premier_df, escolhe_time1, escolhe_time2)

    elif comp_escolhida == 'La Liga':
        escolhe_time1 = st.selectbox('Escolha um time', laliga_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', laliga_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        historico(laliga_df, escolhe_time1, escolhe_time2)
        estatisticas(laliga_df, escolhe_time1, escolhe_time2)
        historico_por_time(laliga_df, escolhe_time1, escolhe_time2)

    elif comp_escolhida == 'Italian':
        escolhe_time1 = st.selectbox('Escolha um time', italia_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', italia_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        historico(italia_df, escolhe_time1, escolhe_time2)    
        estatisticas(italia_df, escolhe_time1, escolhe_time2)
        historico_por_time(italia_df, escolhe_time1, escolhe_time2)

    elif comp_escolhida == 'Bundesliga':
        escolhe_time1 = st.selectbox('Escolha um time', bundesliga_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', bundesliga_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        historico(bundesliga_df, escolhe_time1, escolhe_time2)
        estatisticas(bundesliga_df, escolhe_time1, escolhe_time2)
        historico_por_time(bundesliga_df, escolhe_time1, escolhe_time2)

    elif comp_escolhida == 'Ligue 1':
        escolhe_time1 = st.selectbox('Escolha um time', ligue1_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', ligue1_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        historico(ligue1_df, escolhe_time1, escolhe_time2)
        estatisticas(ligue1_df, escolhe_time1, escolhe_time2)
        historico_por_time(ligue1_df, escolhe_time1, escolhe_time2)

premier_2526_df = pd.read_csv('datasets/premier_2526.csv') 
premier_2425_df = pd.read_csv('datasets/premier_2425.csv')
premier_2324_df = pd.read_csv('datasets/premier_2324.csv')
premier_2425_df['Temporada'] = "24/25"
premier_2526_df['Temporada'] = "25/26"
premier_2324_df['Temporada'] = "23/24"

laliga_2526_df = pd.read_csv('datasets/laliga_2526.csv') 
laliga_2425_df = pd.read_csv('datasets/laliga_2425.csv')
laliga_2324_df = pd.read_csv('datasets/laliga_2324.csv')
laliga_2425_df['Temporada'] = "24/25"
laliga_2526_df['Temporada'] = "25/26"
laliga_2324_df['Temporada'] = "23/24"

italia_2526_df = pd.read_csv('datasets/italia_2526.csv') 
italia_2425_df = pd.read_csv('datasets/italia_2425.csv')
italia_2324_df = pd.read_csv('datasets/italia_2324.csv')
italia_2425_df['Temporada'] = "24/25"
italia_2526_df['Temporada'] = "25/26"
italia_2324_df['Temporada'] = "23/24"

bundesliga_2526_df = pd.read_csv('datasets/bundesliga_2526.csv') 
bundesliga_2425_df = pd.read_csv('datasets/bundesliga_2425.csv')
bundesliga_2324_df = pd.read_csv('datasets/bundesliga_2324.csv')
bundesliga_2425_df['Temporada'] = "24/25"
bundesliga_2526_df['Temporada'] = "25/26"
bundesliga_2324_df['Temporada'] = "23/24"

ligue1_2526_df = pd.read_csv('datasets/ligue1_2526.csv') 
ligue1_2425_df = pd.read_csv('datasets/ligue1_2425.csv')
ligue1_2324_df = pd.read_csv('datasets/ligue1_2324.csv')
ligue1_2425_df['Temporada'] = "24/25"
ligue1_2526_df['Temporada'] = "25/26"
ligue1_2324_df['Temporada'] = "23/24"

premier_df = pd.concat([premier_2425_df, premier_2526_df, premier_2324_df])
laliga_df = pd.concat([laliga_2425_df, laliga_2526_df, laliga_2324_df])
italia_df = pd.concat([italia_2425_df, italia_2526_df, italia_2324_df])
bundesliga_df = pd.concat([bundesliga_2425_df, bundesliga_2526_df, bundesliga_2324_df])
ligue1_df = pd.concat([ligue1_2425_df, ligue1_2526_df, ligue1_2324_df])

lista_competicoes = ['Premier League', 'La Liga', 'Italian', 'Bundesliga', 'Ligue 1']
comp_escolhida = st.selectbox("Escolha a competicao", lista_competicoes)
time_por_competicao(comp_escolhida)



