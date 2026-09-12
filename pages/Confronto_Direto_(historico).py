import pandas as pd
import streamlit as st
import datetime as dt
import acessa_datasets
st.write("## Análise por confronto")

# aproveitmaento de chutes: (chutes_ao_gol / total_chutes) ou (gols / total_chutes)
# ultimas 5 partidas dos times, assim tem um pequeno historico de cada um ***

def estatisticas(competicao_df, time1, time2):
    # media de gols:
    partidas_df = competicao_df.loc[(( (competicao_df['HomeTeam'] == time1) | (competicao_df['AwayTeam'] == time1) ) 
                             & ( (competicao_df['HomeTeam'] == time2) | (competicao_df['AwayTeam'] == time2) ) 
                             )]
    
    partidas_df['Date'] = pd.to_datetime(partidas_df['Date'], dayfirst=True).dt.strftime('%d/%m/%Y')

    partidas_gol = []
    primeiro_tempo = []
    cartao_a = []
    cartao_v = []
    conta_ambas = 0
    total_jogos = 0
    cantos_time1 = []
    cantos_time2 = []

    for _, linha in partidas_df.iterrows():
        partidas_gol.append(linha['FTHG']+linha['FTAG'])
        primeiro_tempo.append(linha['HTHG'] + linha['HTAG'])
        cartao_a.append(linha['HY'] + linha['AY'])
        cartao_v.append(linha['HR'] + linha['AR'])
        
        total_jogos += 1
        if (linha['FTHG'] > 0 and linha['FTAG'] > 0):
            conta_ambas += 1
        
        if (linha['HomeTeam'] == time1):
            cantos_time1.append(linha['HC'])
        if (linha['AwayTeam'] == time1):
            cantos_time1.append(linha['AC'])
        if (linha['HomeTeam'] == time2):
            cantos_time2.append(linha['HC'])
        if (linha['AwayTeam'] == time2):
            cantos_time2.append(linha['AC'])

    media = sum(partidas_gol) / len(partidas_gol)
    media_1tempo = sum(primeiro_tempo) / len(primeiro_tempo)
    media_cartao_a = sum(cartao_a) / len(cartao_a)
    media_cartao_v = sum(cartao_v) / len(cartao_v)
    media_cantos_time1 = sum(cantos_time1) / len(cantos_time1)
    media_cantos_time2 = sum(cantos_time2) / len(cantos_time2) 
    

    st.markdown("#### Histórico do confronto")
    st.write('Media de gols por partida: ', round(media, 2))
    st.write('Media de gols no 1° tempo: ', round(media_1tempo, 2))
    st.write(f'Media de cartão amarelo por partida: ', round(media_cartao_a, 2))
    st.write(f'Media de cartão vermelho por partida: ', round(media_cartao_v , 2))
    st.write(f'Ambas marcam: {conta_ambas} / {total_jogos}')
    st.write(f'Média de escanteios - {time1}: ', round(media_cantos_time1, 2))
    st.write(f'Média de escanteios - {time2}: ', round(media_cantos_time2, 2))

    return

def historico(competicao_df, time1, time2):
    # convertendo tabela para o formato que será melhor trabalhado
    padrao_df = competicao_df.copy()
    padrao_df['Date'] = pd.to_datetime(competicao_df['Date'], dayfirst=True)
    padrao_df = padrao_df.rename(columns={'Date':'Data', 'HomeTeam':'Casa', 
                                          'AwayTeam':'Visitante', 'FTHG':'Gols Casa', 
                                          'FTAG':'Gols Visitante'})
    
    partidas_df = padrao_df.loc[(( (padrao_df['Casa'] == time1) | (padrao_df['Visitante'] == time1) ) 
                             & ( (padrao_df['Casa'] == time2) | (padrao_df['Visitante'] == time2) ) 
                             )]
    
    partidas_df = partidas_df.sort_values('Data', ascending=False).head(6)    
    partidas_df['Data'] = partidas_df['Data'].dt.strftime('%d/%m/%Y')
    partidas_df = partidas_df.copy()

    st.write("#### Visão geral")
    st.dataframe(partidas_df[['Data', 'Casa', 'Gols Casa','Visitante', 'Gols Visitante']], hide_index=True)

    return

def historico_casa_visitante(competicao_df, time, casa=False, visitante=False):
    padrao_df = competicao_df.copy()
    padrao_df['Date'] = pd.to_datetime(competicao_df['Date'], dayfirst=True)
    padrao_df = padrao_df.rename(columns={'Date':'Data', 'HomeTeam':'Casa', 'AwayTeam':'Visitante', 'FTHG':'Gols Casa', 'FTAG':'Gols Visitante'})

    # se selecionada CASA
    if casa:
        partidas_casa = padrao_df.loc[padrao_df['Casa'] == time].sort_values('Data', ascending=False).head(5).copy()
        partidas_casa['Data'] = partidas_casa['Data'].dt.strftime('%d/%m/%Y')
        st.dataframe(partidas_casa[['Data', 'Casa', 'Gols Casa','Visitante', 'Gols Visitante']], hide_index=True)
    # se selecionada VISITANTE
    elif visitante:
        partidas_visitante = padrao_df.loc[padrao_df['Visitante'] == time].sort_values('Data', ascending=False).head(5).copy()
        partidas_visitante['Data'] = partidas_visitante['Data'].dt.strftime('%d/%m/%Y')
        st.dataframe(partidas_visitante[['Data', 'Casa', 'Gols Casa','Visitante', 'Gols Visitante']], hide_index=True)
    return



def historico_por_time(competicao_df, time1, time2):
    # ultimas 5 partidas de cada time
    hist_time1 = competicao_df.loc[(competicao_df['HomeTeam'] == time1) | (competicao_df['AwayTeam'] == time1)]
    hist_time2 = competicao_df.loc[(competicao_df['HomeTeam'] == time2) | (competicao_df['AwayTeam'] == time2)]
    tabela_time1 = hist_time1[['Date', 'HomeTeam', 'FTHG',  'AwayTeam', 'FTAG']].copy()
    tabela_time2 = hist_time2[['Date', 'HomeTeam', 'FTHG',  'AwayTeam', 'FTAG']].copy()

    tabela_time1['Date'] = pd.to_datetime(tabela_time1['Date'], dayfirst=True)
    tabela_time2['Date'] = pd.to_datetime(tabela_time2['Date'], dayfirst=True)

    # ORDENA por data (mais recente primeiro)
    tabela_time1 = tabela_time1.sort_values('Date', ascending=False)
    tabela_time2 = tabela_time2.sort_values('Date', ascending=False)

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

    tabela_time1['Data'] = tabela_time1['Data'].dt.strftime('%d/%m/%Y')
    tabela_time2['Data'] = tabela_time2['Data'].dt.strftime('%d/%m/%Y')

    st.write(f"#### Últimas 5 partidas do {time1}:")
    coluna1, coluna2 = st.columns([1,1])
    with coluna1:
        casa = st.checkbox('Casa', key='casa_time1')
        if casa:
            historico_casa_visitante(competicao_df, time1, casa=True)
    with coluna2:
        visitante = st.checkbox('Visitante', key='visitante_time1')
        if visitante:
            historico_casa_visitante(competicao_df, time1, visitante=True)
    st.dataframe(tabela_time1.head(), hide_index=True)
    
    st.write(f"#### Últimas 5 partidas do {time2}:")
    coluna1, coluna2 = st.columns([1,1])
    with coluna1:
        casa = st.checkbox('Casa', key='casa_time2')
        if casa:
            historico_casa_visitante(competicao_df, time2, casa=True)
    with coluna2:
        visitante = st.checkbox('Visitante', key='visitante_time2')
        if visitante:
            historico_casa_visitante(competicao_df, time2, visitante=True)
    st.dataframe(tabela_time2.head(), hide_index=True)


    return

def time_por_competicao(comp_escolhida):    
    if comp_escolhida == 'Premier League':
        escolhe_time1 = st.selectbox('Escolha um time', acessa_datasets.premier_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', acessa_datasets.premier_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Os times devem ser diferentes para esse tipo de análise.")
            return
        historico(acessa_datasets.premier_df, escolhe_time1, escolhe_time2)
        estatisticas(acessa_datasets.premier_df, escolhe_time1, escolhe_time2)
        historico_por_time(acessa_datasets.premier_df, escolhe_time1, escolhe_time2)

    elif comp_escolhida == 'La Liga':
        escolhe_time1 = st.selectbox('Escolha um time', acessa_datasets.laliga_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', acessa_datasets.laliga_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        historico(acessa_datasets.laliga_df, escolhe_time1, escolhe_time2)
        estatisticas(acessa_datasets.laliga_df, escolhe_time1, escolhe_time2)
        historico_por_time(acessa_datasets.laliga_df, escolhe_time1, escolhe_time2)

    elif comp_escolhida == 'Italian':
        escolhe_time1 = st.selectbox('Escolha um time', acessa_datasets.italia_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', acessa_datasets.italia_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        historico(acessa_datasets.italia_df, escolhe_time1, escolhe_time2)    
        estatisticas(acessa_datasets.italia_df, escolhe_time1, escolhe_time2)
        historico_por_time(acessa_datasets.italia_df, escolhe_time1, escolhe_time2)

    elif comp_escolhida == 'Bundesliga':
        escolhe_time1 = st.selectbox('Escolha um time', acessa_datasets.bundesliga_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', acessa_datasets.bundesliga_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        historico(acessa_datasets.bundesliga_df, escolhe_time1, escolhe_time2)
        estatisticas(acessa_datasets.bundesliga_df, escolhe_time1, escolhe_time2)
        historico_por_time(acessa_datasets.bundesliga_df, escolhe_time1, escolhe_time2)

    elif comp_escolhida == 'Ligue 1':
        escolhe_time1 = st.selectbox('Escolha um time', acessa_datasets.ligue1_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', acessa_datasets.ligue1_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        historico(acessa_datasets.ligue1_df, escolhe_time1, escolhe_time2)
        estatisticas(acessa_datasets.ligue1_df, escolhe_time1, escolhe_time2)
        historico_por_time(acessa_datasets.ligue1_df, escolhe_time1, escolhe_time2)
    elif comp_escolhida == 'Holanda':
        escolhe_time1 = st.selectbox('Escolha um time', acessa_datasets.holanda_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', acessa_datasets.holanda_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        historico(acessa_datasets.holanda_df, escolhe_time1, escolhe_time2)
        estatisticas(acessa_datasets.holanda_df, escolhe_time1, escolhe_time2)
        historico_por_time(acessa_datasets.holanda_df, escolhe_time1, escolhe_time2)

    elif comp_escolhida == 'Escocia':
        escolhe_time1 = st.selectbox('Escolha um time', acessa_datasets.escocia_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', acessa_datasets.escocia_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        historico(acessa_datasets.escocia_df, escolhe_time1, escolhe_time2)
        estatisticas(acessa_datasets.escocia_df, escolhe_time1, escolhe_time2)
        historico_por_time(acessa_datasets.escocia_df, escolhe_time1, escolhe_time2)
    elif comp_escolhida == 'Portugal':
        escolhe_time1 = st.selectbox('Escolha um time', acessa_datasets.portugal_df['HomeTeam'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', acessa_datasets.portugal_df['HomeTeam'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        historico(acessa_datasets.portugal_df, escolhe_time1, escolhe_time2)
        estatisticas(acessa_datasets.portugal_df, escolhe_time1, escolhe_time2)
        historico_por_time(acessa_datasets.portugal_df, escolhe_time1, escolhe_time2)
    elif comp_escolhida == 'Brasil':
        escolhe_time1 = st.selectbox('Escolha um time', acessa_datasets.brasil_df['Home'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', acessa_datasets.brasil_df['Home'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        bra_arg_historico(acessa_datasets.brasil_df, escolhe_time1, escolhe_time2)
        bra_arg_estatistica(acessa_datasets.brasil_df, escolhe_time1, escolhe_time2)
        bra_arg_historico_por_time(acessa_datasets.brasil_df, escolhe_time1, escolhe_time2)

    elif comp_escolhida == 'Argentina':
        escolhe_time1 = st.selectbox('Escolha um time', acessa_datasets.argentina_df['Home'].sort_values().unique())
        escolhe_time2 = st.selectbox('Escolha OUTRO time', acessa_datasets.argentina_df['Home'].sort_values().unique())
        if escolhe_time1 == escolhe_time2:
            st.error("Não é possível escolher o mesmo time para esta análise")
            return
        bra_arg_historico(acessa_datasets.argentina_df, escolhe_time1, escolhe_time2)
        bra_arg_estatistica(acessa_datasets.argentina_df, escolhe_time1, escolhe_time2)
        bra_arg_historico_por_time(acessa_datasets.argentina_df, escolhe_time1, escolhe_time2)



# BRASIL e ARGENTINA
def bra_arg_estatistica(competicao_df, time1, time2):
    # media de gols:
    partidas_df = competicao_df.loc[(( (competicao_df['Home'] == time1) | (competicao_df['Away'] == time1) ) 
                             & ( (competicao_df['Home'] == time2) | (competicao_df['Away'] == time2) ) 
                             )]
    
    partidas_df['Date'] = pd.to_datetime(partidas_df['Date'], dayfirst=True).dt.strftime('%d/%m/%Y')

    partidas_gol = []
    conta_ambas = 0
    total_jogos = 0

    for _, linha in partidas_df.iterrows():
        partidas_gol.append(linha['HG']+linha['AG'])
        total_jogos += 1
        if (linha['HG'] > 0 and linha['AG'] > 0):
            conta_ambas += 1

    if len(partidas_gol) != 0:
        media = sum(partidas_gol) / len(partidas_gol)
    else:
        media = 0
        
    st.markdown("#### Histórico do confronto")
    st.write('Media de gols por partida: ', round(media, 2))
    st.write(f'Ambas marcam: {conta_ambas} / {total_jogos}')

    return

def bra_arg_historico(competicao_df, time1, time2):
    print("comp:\n\n", competicao_df)
    partidas_df = competicao_df.loc[(( (competicao_df['Home'] == time1) | (competicao_df['Away'] == time1) ) 
                             & ( (competicao_df['Home'] == time2) | (competicao_df['Away'] == time2) ) 
                             )].copy()
    partidas_df['Date'] = pd.to_datetime(partidas_df['Date'], dayfirst=True)
    
    
    # resumo ráido
    st.markdown(f"<h3 style='text-align: center;'>{time1}  x  {time2}</h3>", unsafe_allow_html=True)
    st.write("#### Últimos 5 jogos entre eles")
    partidas_df = partidas_df.rename(columns={'Date':'Data', 'Home':'Casa', 'Away':'Visitante', 'HG':'Gols Casa', 'AG':'Gols Visitante'})
    partidas_df = partidas_df.sort_values('Data', ascending=False).head(5)
    partidas_df['Data'] = partidas_df['Data'].dt.strftime('%d/%m/%Y')
    st.dataframe(partidas_df[['Data', 'Casa', 'Gols Casa','Visitante', 'Gols Visitante']], hide_index=True)
    return

def bra_arg_historico_casa_visi(competicao_df, time, casa=False, visitante=False):
    padrao_df = competicao_df.copy()
    padrao_df['Date'] = pd.to_datetime(competicao_df['Date'], dayfirst=True)
    padrao_df = padrao_df.rename(columns={'Date':'Data', 'Home':'Casa', 'Away':'Visitante', 'HG':'Gols Casa', 'AG':'Gols Visitante'})

    # se selecionada CASA
    if casa:
        partidas_casa = padrao_df.loc[padrao_df['Casa'] == time].sort_values('Data', ascending=False).head(5).copy()
        partidas_casa['Data'] = partidas_casa['Data'].dt.strftime('%d/%m/%Y')
        st.dataframe(partidas_casa[['Data', 'Casa', 'Gols Casa','Visitante', 'Gols Visitante']], hide_index=True)
    # se selecionada VISITANTE
    elif visitante:
        partidas_visitante = padrao_df.loc[padrao_df['Visitante'] == time].sort_values('Data', ascending=False).head(5).copy()
        partidas_visitante['Data'] = partidas_visitante['Data'].dt.strftime('%d/%m/%Y')
        st.dataframe(partidas_visitante[['Data', 'Casa', 'Gols Casa','Visitante', 'Gols Visitante']], hide_index=True)
    return

def bra_arg_historico_por_time(competicao_df, time1, time2):
    # ultimas 5 partidas de cada time
    hist_time1 = competicao_df.loc[(competicao_df['Home'] == time1) | (competicao_df['Away'] == time1)]
    hist_time2 = competicao_df.loc[(competicao_df['Home'] == time2) | (competicao_df['Away'] == time2)]
    tabela_time1 = hist_time1[['Date', 'Home', 'HG',  'Away', 'AG']]
    tabela_time2 = hist_time2[['Date', 'Home', 'HG',  'Away', 'AG']]


    tabela_time1['Date'] = pd.to_datetime(tabela_time1['Date'], dayfirst=True)
    tabela_time2['Date'] = pd.to_datetime(tabela_time2['Date'], dayfirst=True)
    tabela_time1['Resultado'] = ""
    tabela_time2['Resultado'] = ""

    for indice, linha in tabela_time1.iterrows():
        if linha['Home'] == time1:
            if linha['HG'] > linha['AG']:
                tabela_time1.loc[indice, 'Resultado'] = 'Vitória'
            elif linha['HG'] < linha['AG']:
                tabela_time1.loc[indice, 'Resultado'] = 'Derrota'
            else:
                tabela_time1.loc[indice, 'Resultado'] = 'Empate'
        elif linha['Away'] == time1:
            if linha['AG'] > linha['HG']:
                tabela_time1.loc[indice, 'Resultado'] = 'Vitória'
            elif linha['AG'] < linha['HG']:
                tabela_time1.loc[indice, 'Resultado'] = 'Derrota'
            else:
                tabela_time1.loc[indice, 'Resultado'] = 'Empate'
    for indice, linha in tabela_time2.iterrows():
        if linha['Home'] == time2:
            if linha['HG'] > linha['AG']:
                tabela_time2.loc[indice, 'Resultado'] = 'Vitória'
            elif linha['HG'] < linha['AG']:
                tabela_time2.loc[indice, 'Resultado'] = 'Derrota'
            else:
                tabela_time2.loc[indice, 'Resultado'] = 'Empate'
        elif linha['Away'] == time2:
            if linha['AG'] > linha['HG']:
                tabela_time2.loc[indice, 'Resultado'] = 'Vitória'
            elif linha['AG'] < linha['HG']:
                tabela_time2.loc[indice, 'Resultado'] = 'Derrota'
            else:
                tabela_time2.loc[indice, 'Resultado'] = 'Empate'
    tabela_time1 = tabela_time1.rename(columns={'Date': 'Data', 'Home':'Casa', 'Away':'Visitante', 'HG': 'Gols Casa', 'AG': 'Gols Visitante'})
    tabela_time2 = tabela_time2.rename(columns={'Date': 'Data', 'Home':'Casa', 'Away':'Visitante', 'HG': 'Gols Casa', 'AG': 'Gols Visitante'})

    tabela_time1 = tabela_time1.sort_values('Data', ascending=False).head()
    tabela_time2= tabela_time2.sort_values('Data', ascending=False).head()

    tabela_time1['Data'] = tabela_time1['Data'].dt.strftime('%d/%m/%Y')
    tabela_time2['Data'] = tabela_time2['Data'].dt.strftime('%d/%m/%Y')

    st.write(f"#### Últimas 5 partidas do {time1}:")
    coluna1, coluna2 = st.columns([1,1])
    with coluna1:
        casa = st.checkbox('Casa', key='casa_time1')
        if casa:
            bra_arg_historico_casa_visi(competicao_df, time1, casa=True)
    with coluna2:
        visitante = st.checkbox('Visitante', key='visitante_time1')
        if visitante:
            bra_arg_historico_casa_visi(competicao_df, time1, visitante=True)
    st.dataframe(tabela_time1, hide_index=True)
    
    st.write(f"#### Últimas 5 partidas do {time2}:")
    coluna1, coluna2 = st.columns([1,1])
    with coluna1:
        casa = st.checkbox('Casa', key='casa_time2')
        if casa:
            bra_arg_historico_casa_visi(competicao_df, time2, casa=True)
    with coluna2:
        visitante = st.checkbox('Visitante', key='visitante_time2')
        if visitante:
            bra_arg_historico_casa_visi(competicao_df, time2, visitante=True)
    st.dataframe(tabela_time2, hide_index=True)



lista_competicoes = ['Brasil', 'Argentina', 'Premier League', 'La Liga', 'Italian', 'Bundesliga', 'Ligue 1', 'Escocia', 'Portugal', 'Holanda']
comp_escolhida = st.selectbox("Escolha a competicao", lista_competicoes)
time_por_competicao(comp_escolhida)

