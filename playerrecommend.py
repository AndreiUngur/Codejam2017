'''
Module to recommend players who fit in the same cluster as an input player (through K-Means unsupervised learning)
'''
import pandas as pd
import sqlalchemy
import pickle
from sklearn.cluster import KMeans

CONN = sqlalchemy.create_engine('sqlite:///data.db')
season_stats_df = pd.read_sql('select * from season_stats',CONN)

season_stats_fields = ['Year', 'Age', 'Games Played',
       'Games Started', 'Minutes Per Game', 'Player Efficiency Rating ',
       'True Shooting Percentage', '3 Point Attempted Rate', 'Free Throw Rate',
       'Offensive Rebound Percentage', 'Defensive Rebound Percentage',
       'True Rebounding Percentage', 'Assist Percentage', 'Steal Percentage',
       'Block Percentage', 'Turn Over Percentage', 'Usage Rate', 'Unnamed: 21',
       'Offensive Win Shares', 'Defensive Win Shares', 'Win Shares',
       'Win Shares Per 48 Minutes', 'Unnamed: 26',
       'Offensive Basketball Plus Minus', 'Defensive Basketball Plus Minus',
       'Basketball Plus Minus', 'Value Over Replacement Player',
       'Field Goals Made', 'Field Goals Attempted', 'Field Goal Percentage',
       'Three Point Field Goals Made', 'Three Point Field Goals Attempted',
       'Three Point Field Goal Percentage', 'Two Point Field Goals Made',
       'Two Point Field Goals Attempted', 'Two Point Field Goal Percentage',
       'Effective Field Goal Percentage', 'Free Throws Made',
       'Free Throws Attempted', 'Free Throw Percentage', 'Offensive Rebounds',
       'Defensive Rebounds', 'Total Rebounds', 'Total Assists', 'Total Steals',
       'Total Blocks', 'Total Turnovers', 'Total Personal Fouls',
       'Total Points']

def get_seasonstats_means():
    seasonstats_means = season_stats_df[season_stats_fields]
    season_stats_means = seasonstats_means.fillna(value=0.0)
    return season_stats_means

def load_KMeans():
    try:
        season_clusters = pickle.load(open('season_clusters.dump','rb'))
    except Exception as e:
        print(e)
        seasonstats_means = get_seasonstats_means()
        #TODO: Configure n clusters to elbow point
        season_clusters = KMeans(n_clusters=5).fit(seasonstats_means)
        pickle.dump(season_clusters,open('season_clusters.dump','wb'))
    return season_clusters

season_clusters = load_KMeans()

def get_cluster(player):
    '''
    Will classify the shot using a decision tree. Pass the X and Y
    value here.
    '''
    return season_clusters.fit_predict([player])