import pandas as pd
from datetime import datetime 
import datetime as dt
import streamlit as st
import url
def mostra_dataframe_bra(dataframe):
    tabela = dataframe[['Date', 'Home', 'Away', 'Res', 'HG', 'AG']]
    tabela['Date'] = tabela['Date'].dt.strftime('%d/%m/%Y')
    
    # times
    times_casa = tabela['Home'].unique()
    times_visi = tabela['Away'].unique()
    times_total = pd.concat([tabela['Home'], tabela['Away']]).unique().tolist()

    jogos = (tabela.groupby('Home').size() + tabela.groupby('Away').size())

    vitorias = (tabela.loc[tabela['Res'] == 'H'].groupby('Home').size().reindex(times_casa, fill_value=0)
                + tabela.loc[tabela['Res'] == 'A'].groupby('Away').size().reindex(times_visi, fill_value=0))
    
    empates = (tabela.loc[tabela['Res'] == 'D'].groupby('Home').size().reindex(times_casa, fill_value=0) 
               + tabela.loc[tabela['Res'] == 'D'].groupby('Away').size().reindex(times_visi, fill_value=0))
    derrotas = (
        tabela.loc[tabela['Res'] == 'A'].groupby('Home').size().reindex(times_casa, fill_value=0) +
        tabela.loc[tabela['Res'] == 'H'].groupby('Away').size().reindex(times_visi, fill_value=0)
    )
    pontos = (
        # ganha 
        tabela.loc[tabela['Res'] == 'H'].groupby('Home').size().reindex(times_casa, fill_value=0) *3
        + tabela.loc[tabela['Res'] == 'A'].groupby('Away').size().reindex(times_visi, fill_value=0) *3
        # empata
        + tabela.loc[tabela['Res'] == 'D'].groupby('Home').size().reindex(times_casa, fill_value=0)
        + tabela.loc[tabela['Res'] == 'D'].groupby('Away').size().reindex(times_visi, fill_value=0) 
    )


    gols_feitos = (
        tabela.groupby('Home')['HG'].sum().reindex(times_total, fill_value=0)
        +tabela.groupby('Away')['AG'].sum().reindex(times_total, fill_value=0)
    )
    gols_sofridos = (
        tabela.groupby('Home')['AG'].sum().reindex(times_total, fill_value=0)
        +tabela.groupby('Away')['HG'].sum().reindex(times_total, fill_value=0)
    )
    saldo_gols = (gols_feitos - gols_sofridos)
    tabela_final = pontos.to_frame(name='Pontos')
    tabela_final = tabela_final.rename_axis('Times')
    
    tabela_final['Jogos'] = jogos
    tabela_final['Vitórias'] = vitorias
    tabela_final['Empates'] = empates
    tabela_final['Derrotas'] = derrotas
    tabela_final['GM'] = gols_feitos
    tabela_final['GC'] = gols_sofridos
    tabela_final['SG'] = saldo_gols
    
    st.dataframe(tabela_final.sort_values(by='Pontos', ascending=False))
    
    return


def mostra_dataframe(dataframe):
    tabela = dataframe[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']]
    times_casa = tabela['HomeTeam'] 
    times_fora = tabela['AwayTeam']
    times_unicos = pd.concat([times_casa, times_fora]).unique().tolist()

    jogos = (tabela.groupby(times_casa).size().reindex(times_unicos, fill_value=0) +
             tabela.groupby(times_fora).size().reindex(times_unicos, fill_value=0))
    
    vitorias = (
        tabela.loc[tabela['FTR'] == 'H'].groupby('HomeTeam')['FTR'].size().reindex(times_unicos, fill_value=0)
        + tabela.loc[tabela['FTR'] == 'A'].groupby('AwayTeam')['FTR'].size().reindex(times_unicos, fill_value=0)
    )
    derrotas = (
        tabela.loc[tabela['FTR'] == 'H'].groupby('AwayTeam')['FTR'].size().reindex(times_unicos, fill_value=0)
        + tabela.loc[tabela['FTR'] == 'A'].groupby('HomeTeam')['FTR'].size().reindex(times_unicos, fill_value=0)
    )
    empates = (
        tabela.loc[tabela['FTR'] == 'D'].groupby('AwayTeam')['FTR'].size().reindex(times_unicos, fill_value=0)
        + tabela.loc[tabela['FTR'] == 'D'].groupby('HomeTeam')['FTR'].size().reindex(times_unicos, fill_value=0)
    )
    pontos = vitorias*3 + empates
    
    gols_marcados = (
        tabela.groupby('HomeTeam')['FTHG'].sum().reindex(times_unicos, fill_value=0)
        + tabela.groupby('AwayTeam')['FTAG'].sum().reindex(times_unicos, fill_value=0)
    )

    gols_sofridos =  (
        tabela.groupby('HomeTeam')['FTAG'].sum().reindex(times_unicos, fill_value=0)
        + tabela.groupby('AwayTeam')['FTHG'].sum().reindex(times_unicos, fill_value=0)
    )

    saldo_gols = gols_marcados - gols_sofridos
    
    tabela_final = pontos.to_frame(name='Pontos') 
    tabela_final = tabela_final.rename_axis('Times')
    tabela_final['Jogos'] = jogos
    tabela_final['Vitórias'] = vitorias
    tabela_final['Empates'] = empates
    tabela_final['Derrotas'] = derrotas
    tabela_final['GM'] = gols_marcados
    tabela_final['GC'] = gols_sofridos
    tabela_final['SG'] = saldo_gols
    
    st.dataframe(tabela_final.sort_values(by='Pontos', ascending=False))
    
    # st.write(tabela)
    return

st.markdown(f"<h1 style='text-align: center; text-decoration: underline white solid 3px;'>Lista de Ligas Temporada 26/27</h1>", unsafe_allow_html=True)
st.write("### Brasil - Brasileirão")
brasileirao_df = pd.read_csv(url.brasileirao)
brasileirao_df['Date'] = pd.to_datetime(brasileirao_df['Date'], format="%d/%m/%Y")
brasileirao_2026_df = brasileirao_df.loc[(brasileirao_df['Date'] >= datetime(2026, 1, 28)) & (brasileirao_df['Date'] <= datetime(2026, 12, 2))]
mostra_dataframe_bra(brasileirao_2026_df)
st.write("### Inglaterra - Premier League")
df = pd.read_csv(url.inglaterra_1)
mostra_dataframe(df)
st.write("### França - Ligue 1")
df = pd.read_csv(url.franca_1)
mostra_dataframe(df)
st.write("### Itália - Serie A")
df = pd.read_csv(url.italia_1)
mostra_dataframe(df)
st.write("### Espanha - La Liga")
df = pd.read_csv(url.espanha_1)
mostra_dataframe(df)
st.write("### Holanda - Eredivisie")
df = pd.read_csv(url.holanda_1)
mostra_dataframe(df)
st.write("### Portugal - Primeira Liga")
df = pd.read_csv(url.portugla_1)
mostra_dataframe(df)
st.write("### Escocia - Scottish Premiership")
df = pd.read_csv(url.escocia_1)
mostra_dataframe(df)
st.write("### Argentina - Liga Profissional de Futebol")
argentina_df = pd.read_csv(url.argentina_1)
argentina_df['Date'] = pd.to_datetime(argentina_df['Date'], format='%d/%m/%Y')
argentina_df = argentina_df.loc[((argentina_df['Date'] >= datetime(2026, 1, 2)) & (argentina_df['Date'] <= datetime(2026, 12, 12)))]
mostra_dataframe_bra(argentina_df)



