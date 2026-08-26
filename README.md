# Análise de Ligas e Times de Futebol
Um projeto perfeito para as pessoas que buscam saber um pouco mais sobre estatísticas de times e ligas europeias concentradas em apenas uma aplicação.

## Sobre
E se uma pessoa pretende saber um pouco mais sobre times de ligas de futebol como estatísticas ou histórico de confronto? 
Essa pessoa conseguiria essas informações na internet, mas para isso ela deve acessar vários sites diferentes (sites duvidosos, diga-se de passagem).
Este projeto visa concentrar essas informações em um só lugar com uma interface amigável e rica em detalhes.
**Link para acessar a página:** [futebol-estatisticas.streamlit.app](https://futebol-estatisticas.streamlit.app/)

## Demonstração
 - Histórico do confronto entre Arsenal x Chelsea (a imagem não mostra todas as informações):
    <img width="1919" height="910" alt="Captura de tela de 2026-08-26 12-55-57" src="https://github.com/user-attachments/assets/9872b730-51b7-4171-99c6-5a54f36285f9" />
 
 - Histórico do Barcelona na temporada de 25/26:
    <img width="1919" height="910" alt="Captura de tela de 2026-08-26 12-55-05" src="https://github.com/user-attachments/assets/b8a7fc63-c859-4118-ab44-08ea38076abd" />

## Funcionalidades
 - É possível verificar as ligas da primeira divisão dos seguintes países: Alemanha, França, Itália, Inglaterra e Espanha.
 - Tabela final da classificação acordo com a liga.
 - Histórico de confronto direto entre times de mesma liga, como: últimas 8 partidas entre os dois times, média de gols, média de cartão amarelo e muito mais.
 - Detalhes de um determinado time como: total de gols em casa e como visitante, maior sequência de vitórias, maior goleada e outras estatísticas.
 - Análise por juízes como: nome, média de faltas e cartões (disponibilizada apenas para a Premier League, Inglaterra).

## Tecnologias
 - Python (Pandas e Streamlit)

## Como Utilizar e Instalação
  - Para utilizar a aplicação: entre no link disponibilizado na seção Sobre.
  - Para rodar na máquina:
      1. Clone o repositório;
      2. Acesse o requirements.txt e baixe as dependências especificadas;
      3. Na raiz do projeto, rode: streamlit run app.py 

## Próximos Passos
 - Acesso a dados de temporadas atuais e também informações sobre o campeonato brasileiro que se atualizam sozinhas conforme as rodadas avançam.
 - Acesso aos arquivos utilizando URL e não arquivos .csv baixados e que abarque mais temporadas.
 - Informações mais específicas sobre times ou sobre a temporada mantendo a boa visualização dos dados.
 - Sempre poder escolher a temporada (pelo menos de 2010 até 2026) para cada uma das análises de time ou liga.

 ## Créditos
  Esse projeto só foi possível ser desenvolvido por conta da comunidade do GitHub que disponibilizou um repositório com arquivos .csv com os dados perfeitamente organizados.
  Repositório em questão: [datasets/football-datasets](https://github.com/datasets/football-datasets)

## Autor
 Yuri de Souza Neves
