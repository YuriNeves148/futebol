import streamlit as st
import pandas as pd

st.write("## Análise por Times")
st.write("### Escolha a competição e o time pertencente: ")

def analise_por_time(competicao_df, time):
    colunas = ['Gols', 'Gols por Partida', 'Partidas Ganhas', 'Partidas Perdidas', 'Média de chutes', 
               'Média de Chutes ao Gol', 'Cartão Amarelo (média)', 'Cartão Vermelho (média)', 
               'Faltas Cometidas (média)', 'Escanteios (média)', 'Gols 1° Tempo'
               ]
        

    dados = {
        'casa':{},
        'visitante':{}
    }

    for filtro in colunas:
        valor_casa, valor_visitante = gerenciamento_analise_time(competicao_df, filtro, time)
        dados['casa'][filtro] = valor_casa
        dados['visitante'][filtro] = valor_visitante
    
    resumo = pd.DataFrame.from_dict(dados)
    st.dataframe(resumo)

# filtros
def gerenciamento_analise_time(competicao_df, filtro, time):
    # gols
    if filtro == 'Gols':
        gols_casa = competicao_df.groupby('HomeTeam')['FTHG'].sum().get(time, 0)
        gols_visitante = competicao_df.groupby('AwayTeam')['FTAG'].sum().get(time, 0)
        return gols_casa, gols_visitante
    
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

    # partidas perdidas
    if filtro == 'Partidas Perdidas':
        perdida_casa = competicao_df.loc[competicao_df['FTR'] == 'A'].groupby('HomeTeam').size().get(time, 0)
        perdida_visit = competicao_df.loc[competicao_df['FTR'] == 'H'].groupby('AwayTeam').size().get(time, 0)

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
    
    # gos primeiro tempo
    if filtro == 'Gols 1° Tempo':
        casa = competicao_df.groupby('HomeTeam')['HTHG'].mean().get(time, 0)
        fora = competicao_df.groupby('AwayTeam')['HTAG'].mean().get(time, 0)
        casa = f'{casa:.2f}'
        fora = f'{fora:.2f}'
        return casa, fora
    
    # gos segundo tempo
    if filtro == 'Gols 1° Tempo':
        casa = competicao_df.groupby('HomeTeam')['HTHG'].mean().get(time, 0)
        fora = competicao_df.groupby('AwayTeam')['HTAG'].mean().get(time, 0)
        casa = f'{casa:.2f}'
        fora = f'{fora:.2f}'
        return casa, fora

def sequencia_vitorias_derrotas(competicao_df, time):
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

def goleada(competicao_df, time):
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

def time_por_competicao(competicao_escolhida):
    premier_df = pd.read_csv('datasets/premier_2526.csv') 
    laliga_df = pd.read_csv('datasets/laliga_2526.csv')
    italia_df = pd.read_csv('datasets/italia_2526.csv')
    bundesliga_df = pd.read_csv('datasets/bundesliga_2526.csv')
    ligue1_df = pd.read_csv('datasets/ligue1_2526.csv')
    
    if competicao_escolhida == 'Premier League':
        escolhe_time = st.selectbox('Escolha um time da Premier League', premier_df['HomeTeam'].sort_values().unique())
        analise_por_time(premier_df, escolhe_time)
        sequencia_vitorias_derrotas(premier_df, escolhe_time)
        goleada(premier_df, escolhe_time)
    elif competicao_escolhida == 'La Liga':
        escolhe_time = st.selectbox('Escolha um time da competição da La Liga', laliga_df['HomeTeam'].sort_values().unique())
        analise_por_time(laliga_df ,escolhe_time)
        sequencia_vitorias_derrotas(laliga_df, escolhe_time)
        goleada(laliga_df, escolhe_time)
    elif competicao_escolhida == 'Italian':
        escolhe_time = st.selectbox('Escolha um time da liga Italiana', italia_df['HomeTeam'].sort_values().unique())
        analise_por_time(italia_df, escolhe_time)
        sequencia_vitorias_derrotas(italia_df, escolhe_time)
        goleada(italia_df, escolhe_time)
    elif competicao_escolhida == 'Bundesliga':
        escolhe_time = st.selectbox('Escolha um time da Bundesliga', bundesliga_df['HomeTeam'].sort_values().unique())
        analise_por_time(bundesliga_df, escolhe_time)
        sequencia_vitorias_derrotas(bundesliga_df, escolhe_time)
        goleada(bundesliga_df, escolhe_time)
    elif competicao_escolhida == 'Ligue 1':
        escolhe_time = st.selectbox('Escolha um time da Ligue 1:', ligue1_df['HomeTeam'].sort_values().unique())
        analise_por_time(ligue1_df, escolhe_time)
        sequencia_vitorias_derrotas(ligue1_df, escolhe_time)
        goleada(ligue1_df, escolhe_time)

# selecionar competicao e seus respectivos times
competicoes_ = ['Premier League', 'La Liga', 'Italian', 'Bundesliga', 'Ligue 1']
escolhe_comp = st.selectbox("Escolha a competição: ",competicoes_)
time_por_competicao(escolhe_comp)


# ÁREA DE JUIZES

def analise_por_juiz(competicao_df):
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

def escolher_competicao(competicao_escolhida):
    premier_df = pd.read_csv('datasets/premier_2526.csv') 
    laliga_df = pd.read_csv('datasets/laliga_2526.csv')
    italia_df = pd.read_csv('datasets/italia_2526.csv')
    bundesliga_df = pd.read_csv('datasets/bundesliga_2526.csv')
    ligue1_df = pd.read_csv('datasets/ligue1_2526.csv')
    
    if competicao_escolhida == 'Premier League ':
        # tabela com nomes dos juizes (vertical) e atributos de juiz (horizontal)
        analise_por_juiz(premier_df)
    elif competicao_escolhida == 'La Liga':
        analise_por_juiz(laliga_df)
    elif competicao_escolhida == 'Italian':
        analise_por_juiz(italia_df)
    elif competicao_escolhida == 'Bundesliga':
        analise_por_juiz(bundesliga_df)
    elif competicao_escolhida == 'Ligue 1':
        analise_por_juiz(ligue1_df)


st.write("## Análise por Juiz")
competicoes_j = ['Premier League ', 'La Liga', 'Italian', 'Bundesliga', 'Ligue 1']
juiz_escolhe_comp = st.selectbox("Selecione a competição: ", competicoes_j)
escolher_competicao(juiz_escolhe_comp)
