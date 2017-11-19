'''
Module to recommend players who fit in the same cluster as an input player (through K-Means unsupervised learning)
'''
import pandas as pd
import sqlalchemy
import pickle
from sklearn.cluster import KMeans

CONN = sqlalchemy.create_engine('sqlite:///data.db')
season_stats_df = pd.read_sql('select * from season_stats',CONN)

season_stats_fields = ['year', 'age', 'games_played',
       'games_started', 'minutes_per_game', 'player_efficiency_rating',
       'true_shooting_percentage', 'free_throw_rate',
       'offensive_rebound_percentage', 'defensive_rebound_percentage',
       'true_rebounding_percentage', 'assist_percentage', 'steal_percentage',
       'block_percentage', 'turn_over_percentage', 'usage_rate',
       'offensive_win_shares', 'defensive_win_shares', 'win_shares',
       'offensive_basketball_plus_minus', 'defensive_basketball_plus_minus',
       'basketball_plus_minus', 'value_over_replacement_player',
       'field_goals_made', 'field_goals_attempted', 'field_goal_percentage',
       'three_point_field_goals_made', 'three_point_field_goals_attempted',
       'three_point_field_goal_percentage', 'two_point_field_goals_made',
       'two_point_field_goals_attempted', 'two_point_field_goal_percentage',
       'effective_field_goal_percentage', 'free_throws_made',
       'free_throws_attempted', 'free_throw_percentage', 'offensive_rebounds',
       'defensive_rebounds', 'total_rebounds', 'total_assists', 'total_steals',
       'total_blocks', 'total_turnovers', 'total_personal_fouls',
       'total_points']

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
    return season_clusters.fit_predict([player,player,player,player,player,player])