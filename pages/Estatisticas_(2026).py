import streamlit as st
import pandas as pd
import url
from datetime import datetime

st.write("## Análise por Times ")
st.write("### Escolha a competição e o time pertencente: ")

def analise_por_time(competicao_df, time):
    colunas = ['Partidas','Gols', 'Gols por Partida', 'Partidas Ganhas', 'Partidas Perdidas', 'Média de chutes', 
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


# APENAS Brasil e Argentina
def br_arg_sequencia_vit_der(competicao_df, time):
        jogos = competicao_df.loc[(competicao_df['Home'] == time) | (competicao_df['Away'] == time)]
        maior_seq_vit = 0
        maior_seq_der = 0
        qtd_vitoria = 0
        qtd_derrota = 0
        # percorre cada jogo que o time jogou em formato de linha
        for _, linha in jogos.iterrows():
            # se ganhou dentro ou fora de casa
            if (linha['Home'] == time and linha['Res'] == 'H') or (linha['Away'] == time and linha['Res'] == 'A'):
                qtd_vitoria += 1
                if qtd_vitoria > maior_seq_vit:
                        maior_seq_vit = qtd_vitoria    
            else:
                qtd_vitoria = 0
            # se perdeu dentro ou fora de casa
            if (linha['Home'] == time and linha['Res'] == 'A') or (linha['Away'] == time and linha['Res'] == 'H'):
                qtd_derrota += 1
                if qtd_derrota > maior_seq_der:
                        maior_seq_der = qtd_derrota    
            else:
                qtd_derrota = 0
        st.write("Maior sequência de vitórias: ", maior_seq_vit)
        st.write("Maior sequência de derrotas: ", maior_seq_der)

def br_arg_gerenciamento_por_time(competicao_df, filtro, time):
    # gols
    if filtro == 'Gols':
        gols_casa = competicao_df.groupby('Home')['HG'].sum().get(time, 0)
        gols_visitante = competicao_df.groupby('Away')['AG'].sum().get(time, 0)
        return gols_casa, gols_visitante
    
    # gols por partida
    if filtro == 'Gols por Partida':
        gols_casa = competicao_df.groupby('Home')['HG'].mean().get(time, 0)
        gols_visitante = competicao_df.groupby('Away')['AG'].mean().get(time, 0)
        gols_casa = f'{gols_casa:.2f}'
        gols_visitante = f'{gols_visitante:.2f}'
        return gols_casa, gols_visitante
    
    # partidas ganhas
    if filtro == 'Partidas Ganhas':
        ganhas_casa = competicao_df.loc[competicao_df['Res'] == 'H'].groupby('Home')['Res'].size().get(time, 0)
        ganhas_fora = competicao_df.loc[competicao_df['Res'] == 'A'].groupby('Away')['Res'].size().get(time, 0)
        return ganhas_casa, ganhas_fora

    # partidas perdidas
    if filtro == 'Partidas Perdidas':
        perdida_casa = competicao_df.loc[competicao_df['Res'] == 'A'].groupby('Home').size().get(time, 0)
        perdida_visit = competicao_df.loc[competicao_df['Res'] == 'H'].groupby('Away').size().get(time, 0)

        return perdida_casa, perdida_visit
    # partidas
    if filtro == 'Partidas':
        partidas_casa = competicao_df.loc[competicao_df['Home'] == time].groupby('Home').size().get(time, 0)
        partidas_visitante =  competicao_df.loc[competicao_df['Away'] == time].groupby('Away').size().get(time, 0)
        return partidas_casa, partidas_visitante
    
def br_arg_goleada(competicao_df, time):
    maior_diferenca = 0
    armazena_diferenca = 0
    placar = [0,0]
    # quando o time jogou 
    jogos = competicao_df.loc[(competicao_df['Home'] == time) | (competicao_df['Away'] == time)]
    
    for _, linha in jogos.iterrows():
        # ganhou a partida?
        if (linha['Home'] == time and linha['Res'] == 'H'):  
            # armazena diferenca
            armazena_diferenca = linha['HG'] - linha['AG']
            if armazena_diferenca > maior_diferenca:
                maior_diferenca = armazena_diferenca
                placar[0] = linha['HG']
                placar[1] = linha['AG']

        elif (linha['Away'] == time and linha['Res'] == 'A'):
            # armazena diferenca
            armazena_diferenca = linha['AG'] - linha['HG']
            if armazena_diferenca > maior_diferenca:
                maior_diferenca = armazena_diferenca
                placar[0] = linha['HG']
                placar[1] = linha['AG']

    st.write(f"Maior goleada do {time}: {placar[0]} X {placar[1]}",)

    return

# resultado ultimas 5 partidas do time
# resultado ultimas 5 partidas do time jogando em casa
# resultado ultimas 5 partidas do time jogando fora

def bra_arg_analie(competicao_df, competicao_escolhida, time):
    # maior sequencia de vitorias
    colunas = ['Partidas', 'Gols', 'Gols por Partida', 'Partidas Ganhas', 'Partidas Perdidas']
    dados = {
        'casa':{},
        'visitante':{}
    }
    for filtro in colunas:
        valor_casa, valor_visitante = br_arg_gerenciamento_por_time(competicao_df, filtro, time)
        dados['casa'][filtro] = valor_casa
        dados['visitante'][filtro] = valor_visitante
    resumo = pd.DataFrame.from_dict(dados)
    st.dataframe(resumo)
    br_arg_sequencia_vit_der(competicao_df, time)
    br_arg_goleada(competicao_df, time)

    return

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

def time_por_competicao(competicao_escolhida):    
    if competicao_escolhida == 'Premier League':
        inglaterra_1 = pd.read_csv(url.inglaterra_1)
        escolhe_time = st.selectbox('Escolha um time da Premier League', inglaterra_1['HomeTeam'].sort_values().unique())
        analise_por_time(inglaterra_1, escolhe_time)
        sequencia_vitorias_derrotas(inglaterra_1, escolhe_time)
        goleada(inglaterra_1, escolhe_time)
        st.write("## Análise por Juiz")
        analise_por_juiz(inglaterra_1)
    elif competicao_escolhida == 'Brasileirão':
        brasileirao = pd.read_csv(url.brasileirao)
        brasileirao['Date'] = pd.to_datetime(brasileirao['Date'], format="%d/%m/%Y")
        brasileirao = brasileirao.loc[(brasileirao['Date'] >= datetime(2026, 1, 28)) & (brasileirao['Date'] <= datetime(2026, 12, 2))]
        escolhe_time = st.selectbox('Escolha um time do Brasileirão:', brasileirao['Home'].sort_values().unique())
        bra_arg_analie(brasileirao, competicao_escolhida, escolhe_time)
    elif competicao_escolhida == 'La Liga':
        espanha_1 = pd.read_csv(url.espanha_1)
        escolhe_time = st.selectbox('Escolha um time da competição da La Liga', espanha_1['HomeTeam'].sort_values().unique())
        analise_por_time(espanha_1 ,escolhe_time)
        sequencia_vitorias_derrotas(espanha_1, escolhe_time)
        goleada(espanha_1, escolhe_time)
    elif competicao_escolhida == 'Italia':
        italia_1 = pd.read_csv(url.italia_1)
        escolhe_time = st.selectbox('Escolha um time da liga Italiana', italia_1['HomeTeam'].sort_values().unique())
        analise_por_time(italia_1, escolhe_time)
        sequencia_vitorias_derrotas(italia_1, escolhe_time)
        goleada(italia_1, escolhe_time)
    elif competicao_escolhida == 'Ligue 1':
        franca_1 = pd.read_csv(url.franca_1)
        escolhe_time = st.selectbox('Escolha um time da Ligue 1:', franca_1['HomeTeam'].sort_values().unique())
        analise_por_time(franca_1, escolhe_time)
        sequencia_vitorias_derrotas(franca_1, escolhe_time)
        goleada(franca_1, escolhe_time)
    elif competicao_escolhida == 'Holanda':
        holanda_1 = pd.read_csv(url.holanda_1)
        escolhe_time = st.selectbox('Escolha um time da Holanda:', holanda_1['HomeTeam'].sort_values().unique())
        analise_por_time(holanda_1, escolhe_time)
        sequencia_vitorias_derrotas(holanda_1, escolhe_time)
        goleada(holanda_1, escolhe_time)
    elif competicao_escolhida == 'Portugal':
        portugla_1 = pd.read_csv(url.portugla_1)
        escolhe_time = st.selectbox('Escolha um time de Portugal:', portugla_1['HomeTeam'].sort_values().unique())
        analise_por_time(portugla_1, escolhe_time)
        sequencia_vitorias_derrotas(portugla_1, escolhe_time)
        goleada(portugla_1, escolhe_time)
    elif competicao_escolhida == 'Escocia':
        escocia_1 = pd.read_csv(url.escocia_1)
        escolhe_time = st.selectbox('Escolha um time da Esócia:', escocia_1['HomeTeam'].sort_values().unique())
        analise_por_time(escocia_1, escolhe_time)
        sequencia_vitorias_derrotas(escocia_1, escolhe_time)
        goleada(escocia_1, escolhe_time)
    elif competicao_escolhida == 'Argentina':
        argentina_1 = pd.read_csv(url.argentina_1)
        argentina_1['Date'] = pd.to_datetime(argentina_1['Date'], format="%d/%m/%Y")
        argentina_1 = argentina_1.loc[(argentina_1['Date'] >= datetime(2026, 1, 22)) & (argentina_1['Date'] <= datetime(2026, 12, 12))]
        escolhe_time = st.selectbox('Escolha um time da Argentina:', argentina_1['Home'].sort_values().unique())
        bra_arg_analie(argentina_1, competicao_escolhida, escolhe_time)  
       
# selecionar competicao e seus respectivos times
competicoes_ = ['Premier League', 'Brasileirão', 'La Liga', 'Italia', 'Ligue 1', 'Holanda', 'Portugal', 'Escocia', 'Argentina']
escolhe_comp = st.selectbox("Escolha a competição: ",competicoes_)
time_por_competicao(escolhe_comp)




