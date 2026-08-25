import streamlit as st
import pandas as pd

#futebol_df = pd.read_csv("datasets/premier_2526.csv")

def tabela_inicial(competicao):
    # quantidade total de jogos para cada time
    jogos = (competicao.groupby("HomeTeam").size() + competicao.groupby("AwayTeam").size())

    tabela = jogos.to_frame(name='Jogos')

    # garante que todos times aparecerão nas listas
    times_casa = competicao['HomeTeam'].unique()
    times_fora = competicao['AwayTeam'].unique()

    # quantidade de partidas ganhas
    vitorias = (
        competicao.loc[(competicao['FTR'] == 'H')].groupby('HomeTeam').size().reindex(times_casa, fill_value=0) 
        + competicao.loc[(competicao['FTR'] == 'A')].groupby('AwayTeam').size().reindex(times_fora, fill_value=0)
                )
    
    # empate total por time
    empate = (
        competicao.loc[competicao['FTR'] == 'D'].groupby('AwayTeam').size().reindex(times_casa, fill_value=0)
        + competicao.loc[competicao['FTR'] == 'D'].groupby('HomeTeam').size().reindex(times_casa, fill_value=0)
    )
    
    # derrota total por time
    derrota = (
        competicao.loc[competicao['FTR'] == 'A'].groupby('HomeTeam').size().reindex(times_casa, fill_value=0)
        + competicao.loc[competicao['FTR'] == 'H'].groupby('AwayTeam').size().reindex(times_fora, fill_value=0)
    )

    # total de gols
    gols_marcados = (competicao.groupby('HomeTeam')['FTHG'].sum().reindex(fill_value=0)
            + competicao.groupby('AwayTeam')['FTAG'].sum().reindex(fill_value=0))

    # Gols Sofridos
    gols_sofridos = (
        competicao.groupby('HomeTeam')['FTAG'].sum().reindex(fill_value=0)
        + competicao.groupby('AwayTeam')['FTHG'].sum().reindex(fill_value=0)
    ) 

    # Pontos
    pontos = (competicao.loc[competicao['FTR'] == 'H'].groupby('HomeTeam').size().reindex(times_casa, fill_value=0) * 3
          + competicao.loc[competicao['FTR'] == 'A'].groupby('AwayTeam').size().reindex(times_casa, fill_value=0) * 3
          + competicao.loc[competicao['FTR'] == 'D'].groupby('HomeTeam').size().reindex(times_casa, fill_value=0)
          + competicao.loc[competicao['FTR'] == 'D'].groupby('AwayTeam').size().reindex(times_casa, fill_value=0))

    # HomeTeam é o indice, aqui troca o nome dele
    tabela = tabela.rename_axis('Times')
    tabela['Vitória'] = vitorias
    tabela['Empates'] = empate
    tabela['Derrotas'] = derrota
    tabela['Gols Marcados'] = gols_marcados
    tabela['Gols Sofridos'] = gols_sofridos
    tabela['Pontos Totais'] = pontos
    
    st.dataframe(tabela.sort_values(by='Pontos Totais', ascending=False))

st.write("## Tabela de resultados")
st.write("### Escolha a liga e a temporada: ")
competicoes = ['Premier League', 'La Liga', 'Italian', 'Bundesliga', 'Ligue 1']
escolhe_liga = st.selectbox(" ", competicoes)
escolhe_temp = st.selectbox(" ", ['Temporada 23/24', 'Temporada 24/25', 'Temporada 25/26'])

def escolhe_temporada(liga):
    # se for premier
    if liga == 'Premier League':
        if escolhe_temp == 'Temporada 23/24':
            premier = pd.read_csv('datasets/premier_2324.csv')
            tabela_inicial(premier)
        elif escolhe_temp == 'Temporada 24/25':
            premier = pd.read_csv('datasets/premier_2425.csv')
            tabela_inicial(premier)
        else:
            premier = pd.read_csv('datasets/premier_2526.csv')
            tabela_inicial(premier)
    # se la liga
    if liga == 'La Liga':
        if escolhe_temp == 'Temporada 23/24':
            laliga = pd.read_csv('datasets/laliga_2324.csv')
            tabela_inicial(laliga)
        elif escolhe_temp == 'Temporada 24/25':
            laliga = pd.read_csv('datasets/laliga_2425.csv')
            tabela_inicial(laliga)
        else:
            laliga = pd.read_csv('datasets/laliga_2526.csv')
            tabela_inicial(laliga)
    # se Ligue 1
    if liga == 'Ligue 1':
        if escolhe_temp == 'Temporada 23/24':
            ligue1 = pd.read_csv('datasets/ligue1_2324.csv')
            tabela_inicial(ligue1)
        elif escolhe_temp == 'Temporada 24/25':
            ligue1 = pd.read_csv('datasets/ligue1_2425.csv')
            tabela_inicial(ligue1)
        else:
            ligue1 = pd.read_csv('datasets/ligue1_2526.csv')
            tabela_inicial(ligue1)
    # se Italia
    if liga == 'Italian':
        if escolhe_temp == 'Temporada 23/24':
            Italian = pd.read_csv('datasets/italia_2324.csv')
            tabela_inicial(Italian)
        elif escolhe_temp == 'Temporada 24/25':
            Italian = pd.read_csv('datasets/italia_2425.csv')
            tabela_inicial(Italian)
        else:
            Italian = pd.read_csv('datasets/italia_2526.csv')
            tabela_inicial(Italian)
    # se Alemanha
    if liga == 'Bundesliga':
        if escolhe_temp == 'Temporada 23/24':
            bundesliga = pd.read_csv('datasets/bundesliga_2324.csv')
            tabela_inicial(bundesliga)
        elif escolhe_temp == 'Temporada 24/25':
            bundesliga = pd.read_csv('datasets/bundesliga_2425.csv')
            tabela_inicial(bundesliga)
        else:
            bundesliga = pd.read_csv('datasets/bundesliga_2526.csv')
            tabela_inicial(bundesliga)
    
    return

def escolha_liga(liga_escolhida):
    escolhe_temporada(liga_escolhida)



escolha_liga(escolhe_liga)
