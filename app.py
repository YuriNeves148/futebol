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

st.write("## Tabela de resultados (25/26)")
st.write("### Escolha a competição: ")
competicoes = ['Premier League', 'La Liga', 'Italian', 'Bundesliga', 'Ligue 1']
escolheu = st.selectbox(" ", competicoes)

def escolha(escolheu):
    if escolheu == "Premier League":
        premier = pd.read_csv("datasets/premier_2526.csv")
        tabela_inicial(premier)
    elif escolheu == "La Liga":
        laliga = pd.read_csv("datasets/laliga_2526.csv")
        tabela_inicial(laliga)
    elif escolheu == "Italian":
        italia = pd.read_csv("datasets/italia_2526.csv")
        tabela_inicial(italia)
    elif escolheu == "Ligue 1":
        ligue1 = pd.read_csv("datasets/ligue1_2526.csv")
        tabela_inicial(ligue1)
    elif escolheu == "Bundesliga":
        bundesliga = pd.read_csv("datasets/bundesliga_2526.csv")
        tabela_inicial(bundesliga)
escolha(escolheu)
