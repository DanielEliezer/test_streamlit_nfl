import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt




def carrega_dados(caminho):
    dados = pd.read_csv(caminho, engine = 'python')
    return dados


def plota(dados):
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.barplot(data = dados, x='percentual_vitorias', y = 'time', palette = 'flare')
    ax.set_title("Times mais Vitoriosos (desde 1966)", fontsize = 30)
    ax.tick_params(axis='both', which='major', labelsize=19)
    ax.set_xlabel('Percentual Vitórias (%)',fontsize = 20) 
    ax.set_ylabel('Time',fontsize = 20) 
    return fig

def plota_reg(dados, eixoy, str_legenda):
    
    fig, ax = plt.subplots(figsize=(20, 10))
    ax = sns.regplot(data = dados, x='vitorias', y = eixoy)
    ax.set_title("Relação entre vitórias e Pontos {}".format(str_legenda), fontsize = 30)
    ax.tick_params(axis='both', which='major', labelsize=19)
    ax.set_xlabel('Vitórias',fontsize = 20) 
    ax.set_ylabel('Pontos {}'.format(str_legenda),fontsize = 20) 
    return fig



def main():
        
        
        #df = carrega_dados("C:\\Users\\55119\\Documents\\Carreira Daniel\\Estudos\\streamlit_nfl\\nfl_stlt\\dados\\spreadspoke_scores.csv")
        df = carrega_dados("dados/spreadspoke_scores.csv")
        
        st.title("Análise NLF")
        st.markdown("Este trabalho busca testar o streamlit, através da análise de dados da NFL")
        
        dic_teams = {'Denver Broncos': 'DEN','Arizona Cardinals':'ARI', 'Atlanta Falcons': 'ATL','Baltimore Ravens': 'BAL',
        'Dallas Cowboys': 'DAL', 'Houston Texans': 'HOU', 'Indianapolis Colts': 'IND', 'Jacksonville Jaguars': 'JAX', 
        'Kansas City Chiefs': 'KC', 'New Orleans Saints': 'NO', 'New York Jets': 'NYJ', 'Philadelphia Eagles': 'PHI', 
        'Seattle Seahawks': 'SEA', 'Tennessee Titans': 'TEN', 'San Francisco 49ers': 'SF', 'Washington Redskins': 'WAS', 
        'Buffalo Bills': 'BUF', 'Carolina Panthers': 'CAR', 'Cleveland Browns': 'CLE', 'Detroit Lions': 'DET',
        'Los Angeles Rams': 'LAR', 'Minnesota Vikings': 'MIN', 'New England Patriots': 'NE', 'New York Giants': 'NYG', 
        'Oakland Raiders': 'LVR', 'Pittsburgh Steelers': 'PIT','San Diego Chargers': 'LAC', 'Chicago Bears': 'CHI',
        'Cincinnati Bengals': 'CIN','Green Bay Packers': 'GB', 'Miami Dolphins': 'MIA','Tampa Bay Buccaneers': 'TB',
        'Los Angeles Chargers': 'LAC', 'Washington Football Team': 'WAS', 'Las Vegas Raiders': 'LVR', 'St. Louis Rams':'LAR',
        'Houston Oilers':"TEN", 'St. Louis Cardinals':"ARI", "Baltimore Colts":'IND', 'Boston Patriots':"NE",  
        'Phoenix Cardinals':"ARI", 'Tennessee Oilers':'TEN', 'Los Angeles Raiders':"LVR"}
        df['total_points'] = df['score_home']+df['score_away']
        df['team_home'] = df['team_home'].map(dic_teams) 
        df['team_away'] = df['team_away'].map(dic_teams)

        lista_vencedores = []
        lista_perdedores = []
        lista_dif = []
        for i in range(len(df['score_home'])):
            if df.loc[i, 'score_home'] > df.loc[i, 'score_away']:   
                lista_vencedores.append(df.loc[i, 'team_home'])
                lista_perdedores.append(df.loc[i, 'team_away'])
                lista_dif.append(df.loc[i, 'score_away']-df.loc[i, 'score_home'])
            elif df.loc[i, 'score_home'] < df.loc[i, 'score_away']:
                lista_vencedores.append(df.loc[i, 'team_away'])
                lista_dif.append(df.loc[i, 'score_home']-df.loc[i, 'score_away'])
                lista_perdedores.append(df.loc[i, 'team_home'])
            else:
                lista_vencedores.append("TIE")
                lista_perdedores.append("TIE")
                lista_dif.append(0)
        df['winner'] = lista_vencedores
        df['loser'] = lista_perdedores 
        df['dif'] = lista_dif
        aux = pd.DataFrame(df.groupby(["winner"]).count()['schedule_date'])
        aux.reset_index(inplace = True)
        aux.columns = ['time','vitorias']
        aux2 = pd.DataFrame(df.groupby(["loser"]).count()['schedule_date'])
        aux2.reset_index(inplace = True)
        aux2.columns = ['time','derrotas']
        aux3 = aux.merge(aux2, how = 'inner', on = 'time')
        aux3['total'] = aux3['vitorias'] + aux3['derrotas']
        aux3['percentual_vitorias'] = aux3['vitorias']/aux3['total']*100
        aux3.sort_values("percentual_vitorias", ascending = True, inplace = True)
        figura = plota(aux3)
        st.pyplot(figura)
        st.markdown("### Analisando agora a relação entre pontos realizados/levados vs Vitórias, tomando como base o período indicado no filtro")
        anos_disponiveis = df.query("schedule_season >= 2000")["schedule_season"].unique()
        anos_disponiveis = anos_disponiveis
        ano_min = st.sidebar.selectbox("Selecione o primeiro ano da análise",
                                   anos_disponiveis)
        recent_years = df[(df['schedule_season']>=ano_min) & (df['schedule_playoff']==False)]
        recent_years = recent_years[['schedule_season','schedule_week','team_home','score_home','score_away','team_away','team_favorite_id','spread_favorite','over_under_line','total_points','winner', 'loser','dif']]
        recent_years = recent_years.reset_index(drop=True)

        aux_teams = recent_years.groupby("team_home").sum()[['score_home','score_away']].reset_index()
        aux_teams.columns = ["time","pt_como_mandante","pt_adversario_visitante"]
        aux_teams2 = recent_years.groupby("team_away").sum()[['score_home','score_away']].reset_index()
        aux_teams2.columns = ["time","pt_como_visitante","pt_adversario_mandante"]
        aux_teams3 = aux_teams.merge(aux_teams2, on = 'time', how = 'inner')
        aux_teams3['pts_time'] = aux_teams3['pt_como_mandante'] +  aux_teams3['pt_como_visitante']
        aux_teams3['pts_adversario'] = aux_teams3['pt_adversario_visitante'] +  aux_teams3['pt_adversario_mandante']
        aux_teams4 = pd.DataFrame(recent_years['winner'].value_counts()).reset_index()
        aux_teams4.columns = ['time', 'vitorias']
        df_teams = (aux_teams3.sort_values("pts_time", ascending= False)).merge(aux_teams4, on = 'time', how = 'inner')

        figura2 = plota_reg(df_teams,'pts_time',"a favor")
        st.pyplot(figura2)
        figura3 = plota_reg(df_teams,'pts_adversario',"contra")
        st.pyplot(figura3)
        st.markdown("Curiosamente, nota-se uma correlação levamente positiva entre vitórias e pontos contra. Obviamente, isso não indica uma relação de causa e efeito, e é necessário entender melhor o por quê disso. Uma hipótese é que muitos desses pontos sejam levados no garbage time, após o time já ter garantido a vitória")

if __name__ == "__main__":
    main()

