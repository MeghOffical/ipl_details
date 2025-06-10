import numpy as np
import pandas as pd
from collections import OrderedDict


ipl=pd.read_csv("C:\\Users\\MEGH BAVARVA\\Desktop\\Data Scientist\\Project\\API_development\\IPL_Matches_2008_2022.csv")
# ipl_match.head(2)

def team_name():
    team1 = ipl['Team1'].unique()
    team2 = ipl['Team2'].unique()

    all_teams = pd.unique(np.concatenate((team1, team2)))
    
    team_dict={
        "teams":list(all_teams)
    }
    
    return team_dict
    
    
def team_vs_team(team1, team2):
    
    team1_ = ipl['Team1'].unique()
    team2_ = ipl['Team2'].unique()

    valid_team= pd.unique(np.concatenate((team1_, team2_)))
    
    if((team1 in valid_team) and (team2 in valid_team)):
        match=ipl[((ipl['Team1']==team1) & (ipl['Team2']==team2))
            |((ipl['Team1']==team2) & (ipl['Team2']==team1))]

        no_of_match=match.shape[0]

        team1_win=match[match['WinningTeam']==team1].shape[0]
        team2_win=match[match['WinningTeam']==team2].shape[0]
        draws=no_of_match-(team1_win+team2_win)

        team1_win_percentage=round((team1_win/no_of_match)*100,2)
        team2_win_percentage=round((team2_win/no_of_match)*100,2)


        team_vs_team_dict = {
        "team1": team1,
        "team2": team2,
        "matches_played": no_of_match,
        "team1_win": team1_win,
        "team1_win_percentage": round(team1_win_percentage, 2),
        "team2_win": team2_win,
        "team2_win_percentage": round(team2_win_percentage, 2),
        "draws": draws
        }

        return team_vs_team_dict
    
    
    else:
        return {
            "error": "Invalid team names provided. Please check the team names."
        }
     
url="https://docs.google.com/spreadsheets/d/e/2PACX-1vRy2DUdUbaKx_Co9F0FSnIlyS-8kp4aKv_I0-qzNeghiZHAI_hw94gKG22XTxNJHMFnFVKsO4xWOdIs/pub?gid=1655759976&single=true&output=csv"
ipl2=pd.read_csv(url)
change_team={
    'Delhi Daredevils':'Delhi Capitals',
    'Kings XI Punjab ':'Punjab Kings',
    'Rising Pune Supergiants ':'Rising Pune Supergiant'
}

ipl2.replace(change_team.keys(),change_team.values(),inplace=True) 


def winning_team():
    df = ipl2[~ipl2['WinningTeam'].isnull()]  # remove rows with null WinningTeam

    team_1 = df['Team1'].unique()
    team_2 = df['Team2'].unique()

    total_team = np.union1d(team_1, team_2)

    data_list = []

    for team in total_team:
        total_matches = df[(df['Team1'] == team) | (df['Team2'] == team)]
        total_wins = total_matches[total_matches['WinningTeam'] == team]

        # home and away
        home_wins = total_matches[(total_matches['WinningTeam'] == team) & (total_matches['Team1'] == team)]
        away_wins = total_matches[(total_matches['WinningTeam'] == team) & (total_matches['Team2'] == team)]

        # calculate percentages
        wins_perc = (total_wins.shape[0] / total_matches.shape[0]) * 100 if total_matches.shape[0] > 0 else 0
        home_wins_perc = (home_wins.shape[0] / total_wins.shape[0]) * 100 if total_wins.shape[0] > 0 else 0
        away_wins_perc = (away_wins.shape[0] / total_wins.shape[0]) * 100 if total_wins.shape[0] > 0 else 0

        # collect data
        data_list.append([team, total_matches.shape[0], round(wins_perc, 2),
                          round(home_wins_perc, 2), round(away_wins_perc, 2)])

    result_df = pd.DataFrame(data_list, columns=["Team", "Matches_Played", "Win_Percentage", "Home_Wins_Percentage", "Away_Wins_Percentage"])
    result_df = result_df.sort_values("Win_Percentage", ascending=False).set_index("Team")

    # Convert the DataFrame to a dictionary
    result_df = result_df.sort_values("Win_Percentage", ascending=False).reset_index()
    return result_df.to_dict(orient='records')

def getplayer(l):
    # Remove brackets and split by comma, then strip quotes/spaces
    return pd.Series([p.strip().strip("'") for p in l.strip("[]").split(",")])


def most_final_played():
    # Get only the final match
    final_match = ipl2[ipl2['MatchNumber'] == 'Final']

    # Collect players in a list
    players_list = []

    # Extract from Team1Players
    for player in final_match['Team1Players']:
        players_list.extend(getplayer(player))

    # Extract from Team2Players
    for player in final_match['Team2Players']:
        players_list.extend(getplayer(player))

    # Convert to final Series
    big_player = pd.Series(players_list)
    ans=big_player.value_counts().head(10)
    
    return ans.to_dict()




def matched_played(df, team):
    return df[(df['Team1'] == team) | (df['Team2'] == team)].shape[0]

def match_won(df, team):
    return df[df['WinningTeam'] == team].shape[0]

def no_result(df, team):
    return df[((df['Team1'] == team) | (df['Team2'] == team)) & (df['WinningTeam'].isnull())].shape[0]

def point_table(season):
    df = ipl2[ipl2['Season'].astype(str) == str(season)]
    teams = np.union1d(df['Team1'].unique(), df['Team2'].unique())

    new_dataframe = pd.DataFrame()
    new_dataframe['Team_name'] = teams

    new_dataframe['Match_played'] = new_dataframe['Team_name'].apply(lambda x: matched_played(df, x))
    new_dataframe['Wins'] = new_dataframe['Team_name'].apply(lambda x: match_won(df, x))
    new_dataframe['No_result'] = new_dataframe['Team_name'].apply(lambda x: no_result(df, x))
    new_dataframe['Losses'] = new_dataframe['Match_played'] - new_dataframe['Wins'] - new_dataframe['No_result']
    new_dataframe['Points'] = new_dataframe['Wins'] * 2 + new_dataframe['No_result']

    new_dataframe.sort_values('Points', ascending=False, inplace=True)
    new_dataframe.set_index('Team_name', inplace=True)

    return new_dataframe  # ✅ return DataFrame instead of dict


def point_table_extension(val):

    new_df = point_table(val)
    
    season_val = str(val)

    final = ipl[(ipl['Season'] == season_val) & (ipl['MatchNumber'] == 'Final')]
    if final['WinningTeam'].values[0] == final['Team1'].values[0]:
        new_df.loc[final['Team1'].values[0], 'SeasonPosition'] = 'Winner'
        new_df.loc[final['Team2'].values[0], 'SeasonPosition'] = 'Runner Up'
    else:
        new_df.loc[final['Team2'].values[0], 'SeasonPosition'] = 'Winner'
        new_df.loc[final['Team1'].values[0], 'SeasonPosition'] = 'Runner Up'

    qualifier = ipl[(ipl['Season'] == season_val) & (ipl['MatchNumber'] == 'Qualifier 2')]
    if qualifier['WinningTeam'].values[0] == qualifier['Team1'].values[0]:
        new_df.loc[qualifier['Team2'].values[0], 'SeasonPosition'] = '3rd Place'
    else:
        new_df.loc[qualifier['Team1'].values[0], 'SeasonPosition'] = '3rd Place'

    eliminator = ipl[(ipl['Season'] == season_val) & (ipl['MatchNumber'] == 'Eliminator')]
    if eliminator['WinningTeam'].values[0] == eliminator['Team1'].values[0]:
        new_df.loc[eliminator['Team2'].values[0], 'SeasonPosition'] = '4th Place'
    else:
        new_df.loc[eliminator['Team1'].values[0], 'SeasonPosition'] = '4th Place'


    start_rank = 5

    # Ensure 'SeasonPosition' column exists
    if 'SeasonPosition' not in new_df.columns:
        new_df['SeasonPosition'] = np.nan

    # Get indexes where SeasonPosition is NaN
    nan_indexes = new_df[new_df['SeasonPosition'].isna()].index

    # Assign "5th Place", "6th Place", ... to NaNs in order
    for i, idx in enumerate(nan_indexes, start=start_rank):
        new_df.at[idx, 'SeasonPosition'] = i

    return new_df.reset_index().to_dict(orient='records')





# point_table(2016)



balls=pd.read_csv("C:\\Users\\MEGH BAVARVA\\Desktop\\Data Scientist\\Pandas\\Task\\Task5\\IPL_Ball_by_Ball_2008_2022.csv")
matches=pd.read_csv("C:\\Users\\MEGH BAVARVA\\Desktop\\Data Scientist\\Pandas\\Task\\Task5\\IPL_Matches_2008_2022.csv")
season=balls.merge(matches[['ID','Season']],how='inner',on='ID')


def no_of_bowler(): 
    return season['bowler'].unique().tolist()

def no_of_batsman():
    return season['batter'].unique().tolist()



season['IsBowlerWicket']=season['kind'].apply(lambda x: 1 if x in ('caught', 'caught and bowled', 'bowled', 'stumped','lbw', 'hit wicket') else 0)

season['Bowler_run']=season['extra_type'].apply(lambda x: 0 if x in ('legbyes','byes') else 1) * season['total_run']

season['LegalDilevery']=season['extra_type'].apply(lambda x: 0 if x in ('wides','noballs') else 1)


def bowler_details(player_name):
    player = season[season['bowler'] == player_name]
    
    # Innings bowled
    innings_bowled = player.groupby(['Season'])['ID'].nunique()
    col1 = innings_bowled.reset_index(name="Innings")

    # Total wickets (exclude run-outs)
    total_wickets = player[player['IsBowlerWicket'] == 1].groupby(['Season'])['IsBowlerWicket'].sum()
    col2 = total_wickets.reset_index(name="Wickets")

    # Best spell (most wickets in a single match)
    best_spell = player[player['IsBowlerWicket'] == 1].groupby(['Season', 'ID'])['IsBowlerWicket'].sum().reset_index()
    best_spell = best_spell.sort_values(by=['Season', 'IsBowlerWicket'], ascending=[True, False])
    best_spell = best_spell.drop_duplicates(subset=['Season'], keep='first')
    col3 = best_spell[['Season', 'IsBowlerWicket']].rename(columns={'IsBowlerWicket': 'Best_spell'})

    # Total runs conceded
    runs_conceded = player.groupby(['Season'])['Bowler_run'].sum()
    col4 = runs_conceded.reset_index(name="Runs_conceded")

    # Legal deliveries
    legal_balls = player[player['LegalDilevery'] == 1].groupby(['Season'])['ballnumber'].count()
    col5 = legal_balls.reset_index(name="Balls_bowled")

    # Economy rate
    economy_rate = round((runs_conceded / legal_balls.replace(0, np.nan)) * 6,2)
    col6 = economy_rate.reset_index(name="Economy")


    # Merge all
    stats = col1.merge(col2, on='Season', how='left') \
                .merge(col3, on='Season', how='left') \
                .merge(col4, on='Season', how='left') \
                .merge(col5, on='Season', how='left') \
                .merge(col6, on='Season', how='left')

    stats.fillna(0, inplace=True)

    # Final result
    return stats[['Season', 'Innings', 'Wickets', 'Best_spell', 'Runs_conceded', 'Economy']].to_dict(orient='records')


def batsman_details(player_name):     
    player=season[season['batter']==player_name]
    player

    innings_played=player.groupby(['Season'])['ID'].nunique()
    col1=innings_played.reset_index(name="innings_played")
    col1

    batsman_runs=player.groupby(['Season'])['total_run'].sum()
    col2=batsman_runs.reset_index(name="Total_runs")
    col2

    batsman_out = season[season['player_out'] == player_name] # nonstrike uper hoy and runout thaye to pun out ave ne 
    req= batsman_out.groupby('Season')['isWicketDelivery'].sum()
    col3= req.reset_index(name="total_no_out")

    Average=batsman_runs/req
    col4=Average.reset_index(name="average")

    highest_runs=player.groupby(['Season','ID'])['batsman_run'].sum().reset_index().sort_values(by=['batsman_run'],ascending=False).drop_duplicates(subset=['Season'],keep='first').set_index('Season').sort_index()
    col5=highest_runs.reset_index()[['Season','batsman_run']]

    balls_not_wide=player[~(player["extra_type"]=='wides')]
    balls_not_wide
    batsman_balls=balls_not_wide.groupby(['Season'])['ballnumber'].count()
    col6=batsman_balls.reset_index(name="Ball_played")

    strike_rate=round((batsman_runs/batsman_balls)*100,2)
    col7=strike_rate.reset_index(name='StrikeRate')
    col7
        
    stats=col1.merge(col2,on='Season').merge(col3,on='Season').merge(col4,on='Season').merge(col5,on='Season').merge(col6,on='Season').merge(col7,on='Season')

    stats.rename(columns={'innings_played':"Innings",
                        'average':'Average',
                        'batsman_run':'Highest_runs',
                        'StrikeRate':'Strike_rate'},inplace=True)
    final=stats[['Season','Innings','Total_runs','Average','Highest_runs','Strike_rate']].set_index('Season')
    
    return final.to_dict(orient='index')


def purple_cap():

    pcapdf=season.groupby(['Season','bowler']).agg({
        'IsBowlerWicket':'sum',
        'Bowler_run':'sum',
        'LegalDilevery':'sum',
    })


    pcapdf['Bowler_Economy']=round((pcapdf['Bowler_run']/pcapdf['LegalDilevery'])*6,2)

    final=pcapdf.reset_index().sort_values(by=['IsBowlerWicket','Bowler_Economy'],ascending=[False,True]).drop_duplicates(subset=['Season'],keep='first').sort_values('Season').set_index('Season')
    final=final[['bowler','IsBowlerWicket','Bowler_Economy']].rename(columns={'bowler':'Best_Bowler','IsBowlerWicket':'Wickets','Bowler_Economy':'Economy'})
    
    return final.to_dict(orient='index')


ipl3=pd.read_csv("C:\\Users\\MEGH BAVARVA\\Desktop\\Data Scientist\\Pandas\\Task\\Task4\\ipl_deliveries.csv")
def batting_pair():
    def func(x):
        #* This ensures batting pairs are always stored in a consistent order, no matter who was striker or non-striker.
        return "-".join(list(np.sort(x.values)))

    ipl3['batter_pair']=ipl3[['batter','non-striker']].apply(func,axis=1) #axis=1 means for row mate
    ipl3.groupby('batter_pair')['batsman_run'].sum().sort_values(ascending=False).head(10) 

    newdf=ipl3.groupby('batter_pair').agg({
        "isWicketDelivery": "sum",
        "batsman_run": "sum",
        "ballnumber": "sum",
    })

    newdf['Strike_rate']= (newdf['batsman_run']/newdf['ballnumber'])*100

    # If isWicketDelivery is 0, assign batsman_run; otherwise, compute average normally
    newdf['Average'] = np.where(newdf['isWicketDelivery'] == 0, newdf['batsman_run'], newdf['batsman_run'] / newdf['isWicketDelivery'])

    newdf.reset_index(inplace=True)

    newdf['Batsman1']=newdf['batter_pair'].apply(lambda x: x.split('-')[0])
    newdf['Batsman2']=newdf['batter_pair'].apply(lambda x: x.split('-')[1])

    # newdf.sort_values(by=['Average','Strike_rate'],ascending=[False,False],inplace=True)
    newdf.sort_values(by=['batsman_run'],ascending=[False],inplace=True)
    final=newdf[['Batsman1','Batsman2','batsman_run','Average']].head(10).rename(columns={'batsman_run':'Total Runs'})
    return final.to_dict(orient='records')



# --- Analysis Function ---
def orange_cap():
    season=balls.merge(matches[['ID','Season']],how='inner',on='ID')
    season['LegalDilevery']=season['extra_type'].apply(lambda x: 0 if x in ('wides','noballs') else 1)
    season['Player_out_hai'] = ((season['isWicketDelivery'] == 1) & (season['batter'] == season['player_out'])).astype(int)


    temp = season.groupby(['Season', 'batter']).agg({
        'batsman_run': 'sum',
        'LegalDilevery': 'sum',
        'Player_out_hai': 'sum'
    }).reset_index()

    # Compute average and strike rate
    temp['Average'] = temp['batsman_run'] / temp['Player_out_hai']
    temp['Strike_Rate'] = round((temp['batsman_run'] / temp['LegalDilevery']) * 100, 2)

    # Handle infinite or undefined average (when Player_out_hai == 0)
    temp['Average'] = temp.apply(
        lambda row: row['batsman_run'] if (row['Player_out_hai'] == 0) else round(row['Average'], 2),
        axis=1
    )


    temp.sort_values(by=['batsman_run','Strike_Rate','Average'], ascending=[False, False,False], inplace=True)
    temp.drop_duplicates(subset=['Season'], keep='first', inplace=True)
    final=temp.sort_values('Season').set_index('Season')[['batter','batsman_run','Strike_Rate','Average']].rename(columns={'batter':'Batsman','batsman_run':'Runs'})

    return final.to_dict(orient='index')  # clean list of dicts



def Player_Of_match_details():
    # Merge ball-level and match-level data
    merged_df = balls.merge(matches, how='inner', on='ID')

    # Get Player of the Match per match
    player_of_match_df = merged_df.groupby(['Season', 'ID'])['Player_of_Match'].first().reset_index()

    # Filter rows where the Player of the Match was the batter
    pom_batting = merged_df[merged_df['batter'] == merged_df['Player_of_Match']]

    # Batting runs and balls faced
    batting_runs = pom_batting.groupby(['Season', 'ID'])['batsman_run'].sum().reset_index()
    balls_faced = pom_batting.groupby(['Season', 'ID'])['ballnumber'].count().reset_index()

    # Calculate bowler-run (ignore legbyes and byes)
    merged_df['bowler_run'] = merged_df['extra_type'].apply(lambda x: 0 if x in ('legbyes', 'byes') else 1)

    # Identify wickets credited to bowler
    merged_df['is_bowler_wicket'] = merged_df['kind'].apply(
        lambda x: 1 if x in ('caught', 'caught and bowled', 'bowled', 'stumped', 'lbw', 'hit wicket') else 0)

    # Filter rows where Player of the Match was the bowler
    pom_bowling = merged_df[merged_df['bowler'] == merged_df['Player_of_Match']]

    # Wickets taken
    bowling_wickets = pom_bowling.groupby(['Season', 'ID'])['is_bowler_wicket'].sum().reset_index()

    # Runs conceded by bowler
    bowling_runs = pom_bowling[pom_bowling['bowler_run'] == 1]
    runs_conceded = bowling_runs.groupby(['Season', 'ID'])['total_run'].sum().reset_index()

    # Merge all data
    final_df = player_of_match_df \
        .merge(batting_runs, how='outer', on=['Season', 'ID']) \
        .merge(balls_faced, how='outer', on=['Season', 'ID']) \
        .merge(bowling_wickets, how='outer', on=['Season', 'ID']) \
        .merge(runs_conceded, how='outer', on=['Season', 'ID'])

    # Create Batting and Bowling Figure strings (e.g., 45/30 or 3/25)
    final_df["Batting_Figure"] = final_df['batsman_run'].astype('Int32').astype(str) + "/" + final_df['ballnumber'].astype('Int32').astype(str)
    final_df["Bowling_Figure"] = final_df['is_bowler_wicket'].astype('Int32').astype(str) + "/" + final_df['total_run'].astype('Int32').astype(str)

    # Final Display
    final=final_df[['Season','ID', 'Player_of_Match', 'Batting_Figure', 'Bowling_Figure']]
    
    return final.to_dict(orient='records')  # clean list of dicts

