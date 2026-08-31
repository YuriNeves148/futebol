import pandas as pd
import datetime as dt

premier_2526_df = pd.read_csv('datasets/premier_2526.csv') 
premier_2526_df['Date'] = pd.to_datetime(premier_2526_df['Date'], format='%Y-%m-%d')

premier_2425_df = pd.read_csv('datasets/premier_2425.csv')
premier_2425_df['Date'] = pd.to_datetime(premier_2425_df['Date'], format='%Y-%m-%d')
premier_2324_df = pd.read_csv('datasets/premier_2324.csv')
premier_2324_df['Date'] = pd.to_datetime(premier_2324_df['Date'], format='%Y-%m-%d')
premier_2425_df['Temporada'] = "24/25"
premier_2526_df['Temporada'] = "25/26"
premier_2324_df['Temporada'] = "23/24"

laliga_2526_df = pd.read_csv('datasets/laliga_2526.csv')
laliga_2526_df['Date'] = pd.to_datetime(laliga_2526_df['Date'], format='%Y-%m-%d') 
laliga_2425_df = pd.read_csv('datasets/laliga_2425.csv')
laliga_2425_df['Date'] = pd.to_datetime(laliga_2425_df['Date'], format='%Y-%m-%d')
laliga_2324_df = pd.read_csv('datasets/laliga_2324.csv')
laliga_2324_df['Date'] = pd.to_datetime(laliga_2324_df['Date'], format='%Y-%m-%d')
laliga_2425_df['Temporada'] = "24/25"
laliga_2526_df['Temporada'] = "25/26"
laliga_2324_df['Temporada'] = "23/24"

italia_2526_df = pd.read_csv('datasets/italia_2526.csv')
italia_2526_df['Date'] = pd.to_datetime(italia_2526_df['Date'], format='%Y-%m-%d')
italia_2425_df = pd.read_csv('datasets/italia_2425.csv')
italia_2425_df['Date'] = pd.to_datetime(italia_2425_df['Date'], format='%Y-%m-%d')
italia_2324_df = pd.read_csv('datasets/italia_2324.csv')
italia_2324_df['Date'] = pd.to_datetime(italia_2324_df['Date'], format='%Y-%m-%d')
italia_2425_df['Temporada'] = "24/25"
italia_2526_df['Temporada'] = "25/26"
italia_2324_df['Temporada'] = "23/24"

bundesliga_2526_df = pd.read_csv('datasets/bundesliga_2526.csv') 
bundesliga_2526_df['Date'] = pd.to_datetime(bundesliga_2526_df['Date'], format='%Y-%m-%d')
bundesliga_2425_df = pd.read_csv('datasets/bundesliga_2425.csv')
bundesliga_2425_df['Date'] = pd.to_datetime(bundesliga_2425_df['Date'], format='%Y-%m-%d')
bundesliga_2324_df = pd.read_csv('datasets/bundesliga_2324.csv')
bundesliga_2324_df['Date'] = pd.to_datetime(bundesliga_2324_df['Date'], format='%Y-%m-%d')
bundesliga_2425_df['Temporada'] = "24/25"
bundesliga_2526_df['Temporada'] = "25/26"
bundesliga_2324_df['Temporada'] = "23/24"

ligue1_2526_df = pd.read_csv('datasets/ligue1_2526.csv') 
ligue1_2526_df['Date'] = pd.to_datetime(ligue1_2526_df['Date'], format='%Y-%m-%d', dayfirst=True)
ligue1_2425_df = pd.read_csv('datasets/ligue1_2425.csv')
ligue1_2425_df['Date'] = pd.to_datetime(ligue1_2425_df['Date'], format='%Y-%m-%d', dayfirst=True)
ligue1_2324_df = pd.read_csv('datasets/ligue1_2324.csv')
ligue1_2324_df['Date'] = pd.to_datetime(ligue1_2324_df['Date'], format='%Y-%m-%d', dayfirst=True)
ligue1_2425_df['Temporada'] = "24/25"
ligue1_2526_df['Temporada'] = "25/26"
ligue1_2324_df['Temporada'] = "23/24"

holanda_2526_df = pd.read_csv('datasets/holanda_2526.csv') 
holanda_2526_df['Date'] = pd.to_datetime(holanda_2526_df['Date'], format='%d/%m/%Y', dayfirst=True)
holanda_2425_df = pd.read_csv('datasets/holanda_2425.csv') 
holanda_2425_df['Date'] = pd.to_datetime(holanda_2425_df['Date'], format='%d/%m/%Y', dayfirst=True)
holanda_2324_df = pd.read_csv('datasets/holanda_2324.csv') 
holanda_2324_df['Date'] = pd.to_datetime(holanda_2324_df['Date'], format='%d/%m/%Y', dayfirst=True)
holanda_2526_df['Temporada'] = '25/26'
holanda_2425_df['Temporada'] = '24/25'
holanda_2324_df['Temporada'] = '23/24'

escocia_2526_df = pd.read_csv('datasets/escocia_2526.csv')
escocia_2526_df = escocia_2526_df[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','Referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
escocia_2526_df['Date'] = pd.to_datetime(escocia_2526_df['Date'], format='%d/%m/%Y')
escocia_2425_df = pd.read_csv('datasets/escocia_2425.csv')
escocia_2425_df = escocia_2425_df[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','Referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
escocia_2425_df['Date'] = pd.to_datetime(escocia_2425_df['Date'], format='%d/%m/%Y')
escocia_2324_df = pd.read_csv('datasets/escocia_2324.csv')
escocia_2324_df = escocia_2324_df[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','Referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
escocia_2324_df['Date'] = pd.to_datetime(escocia_2324_df['Date'], format='%d/%m/%Y')
escocia_2526_df['Temporada'] = "25/26"
escocia_2425_df['Temporada'] = "24/25"
escocia_2324_df['Temporada'] = "23/24"

noruega_2526_df = pd.read_csv('datasets/noruega_2526.csv')
noruega_2526_df = noruega_2526_df[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
noruega_2526_df['Date'] = pd.to_datetime(noruega_2526_df['Date'], format='%d/%m/%Y')
noruega_2425_df = pd.read_csv('datasets/noruega_2425.csv')
noruega_2425_df = noruega_2425_df[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
noruega_2425_df['Date'] = pd.to_datetime(noruega_2425_df['Date'], format='%d/%m/%Y')
noruega_2423_df = pd.read_csv('datasets/noruega_2324.csv')
noruega_2423_df = noruega_2423_df[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
noruega_2423_df['Date'] = pd.to_datetime(noruega_2423_df['Date'], format='%d/%m/%Y')
noruega_2526_df['Temporada'] = "25/26"
noruega_2425_df['Temporada'] = "24/25"
noruega_2423_df['Temporada'] = "23/24"

portugal_2526_df = pd.read_csv('datasets/noruega_2526.csv')
portugal_2526_df = portugal_2526_df[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
portugal_2526_df['Date'] = pd.to_datetime(portugal_2526_df['Date'], format='%d/%m/%Y')
portugal_2425_df = pd.read_csv('datasets/noruega_2425.csv')
portugal_2425_df = portugal_2425_df[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
portugal_2425_df['Date'] = pd.to_datetime(portugal_2425_df['Date'], format='%d/%m/%Y')
portugal_2324_df = pd.read_csv('datasets/noruega_2324.csv')
portugal_2324_df = portugal_2324_df[['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
portugal_2324_df['Date'] = pd.to_datetime(portugal_2324_df['Date'], format='%d/%m/%Y')
portugal_2526_df['Temporada'] = "25/26"
portugal_2425_df['Temporada'] = "24/25"
portugal_2324_df['Temporada'] = "23/24"

argentina_tudo = pd.read_csv('datasets/argentina.csv')
argentina_tudo['Date'] = pd.to_datetime(argentina_tudo['Date'], format='%d/%m/%Y')
argentina_tudo = argentina_tudo[['Date','Home', 'Season','Away','HG','AG','Res']]
argentina_23_df = argentina_tudo.loc[argentina_tudo['Season'] == '2023']
argentina_24_df = argentina_tudo.loc[argentina_tudo['Season'] == '2024']
argentina_25_df = argentina_tudo.loc[argentina_tudo['Season'] == '2025']
argentina_26_df = argentina_tudo.loc[argentina_tudo['Season'] == '2026']

brasil_tudo = pd.read_csv('datasets/brasileirao.csv')
brasil_tudo['Date'] = pd.to_datetime(brasil_tudo['Date'], format='%d/%m/%Y')
brasil_tudo = brasil_tudo[['Date','Home', 'Season','Away','HG','AG','Res']]

brasil_23_df = brasil_tudo.loc[brasil_tudo['Season'] == 2023]
brasil_24_df = brasil_tudo.loc[brasil_tudo['Season'] == 2024]
brasil_25_df = brasil_tudo.loc[brasil_tudo['Season'] == 2025]
brasil_26_df = brasil_tudo.loc[brasil_tudo['Season'] == 2026]

premier_df = pd.concat([premier_2425_df, premier_2526_df, premier_2324_df])
laliga_df = pd.concat([laliga_2425_df, laliga_2526_df, laliga_2324_df])
italia_df = pd.concat([italia_2425_df, italia_2526_df, italia_2324_df])
bundesliga_df = pd.concat([bundesliga_2425_df, bundesliga_2526_df, bundesliga_2324_df])
ligue1_df = pd.concat([ligue1_2425_df, ligue1_2526_df, ligue1_2324_df])
escocia_df = pd.concat([escocia_2526_df, escocia_2425_df, escocia_2324_df])
noruega_df = pd.concat([noruega_2526_df, noruega_2425_df, noruega_2423_df])
portugal_df = pd.concat([portugal_2526_df, portugal_2425_df, portugal_2324_df])
argentina_df = pd.concat([argentina_23_df, argentina_24_df, argentina_25_df, argentina_26_df])
brasil_df = pd.concat([brasil_23_df, brasil_24_df, brasil_25_df, brasil_26_df])
