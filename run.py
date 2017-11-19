from app import create_app
from flask import jsonify, request
import sqlalchemy
import os
from sqlalchemy.sql import text
from exceptions import InvalidUsage
import math
import operator
import zones

CONN = sqlalchemy.create_engine('sqlite:///data.db')
app = create_app("development")

#Constants
possible_zones = ['Above the Break 3', 'Backcourt','In The Paint (Non-RA)','Left Corner 3','Mid-Range','Restricted Area','Right Corner 3']
averages = {'Above the Break 3': 0.34,
                'Backcourt': 0.026,
                'In The Paint (Non-RA)': 0.40375,
                'Left Corner 3': 0.38,
                'Mid-Range': 0.39912499999999995,
                'Restricted Area': 0.601,
                'Right Corner 3': 0.392}

database_fields = {
    "player_stats":['player_id',
                 'full_name',
                 'first_name',
                 'last_name',
                 'team',
                 'games_played',
                 'minutes',
                 'pull_up_shots_points_per_game',
                 'pull_up_field_goals_made_per_game',
                 'pull_up_field_goals_attempted_per_game',
                 'pull_up_field_goal_percentage',
                 'pull_up_3_point_field_goals_made_per_game',
                 'pull_up_3_point_field_goals_attempted_per_game',
                 'pull_up_3_point_percentage',
                 'pull_up_3_point_effective_field_goal_percentage',
                 'pull_up_points_total',
                 'drives_per_game',
                 'points_per_game_off_drives',
                 'field_goal_percentage_on_drives',
                 'points_per_48_minutes_on_drives',
                 'total_points_on_drives',
                 'total_drives',
                 'blocks_per_game',
                 'steals_per_game',
                 'field_goals_made_against_when_defending_rim',
                 'field_goals_attempted_against_when_defending_rim',
                 'field_goal_percentage_against_when_defending_rim',
                 'total_blocks',
                 'passes_per_game',
                 'assists_per_game',
                 'free_throws_assisted_per_game',
                 'second_pass_hockey_assist',
                 'assist_opportunities_per_game',
                 'points_created_off_assists_per_game',
                 'total_assists',
                 'touches_per_game',
                 'front_court_touches_per_game',
                 'time_of_possession',
                 'close_range_touches_per_game',
                 'elbow_touches_per_game',
                 'points_per_game',
                 'points_per_touch',
                 'points_per_half_court_touch',
                 'total_touches',
                 'average_speed',
                 'average_speed_offense',
                 'average_speed_defense',
                 'rebounds_per_game',
                 'rebound_chances',
                 'rebound_percentage',
                 'contested_rebounds_per_game',
                 'uncontested_rebounds_per_game',
                 'percentage_of_rebounds_uncontested',
                 'total_rebounds',
                 'offensive_rebounds_per_game',
                 'offensive_rebound_chances',
                 'offensive_rebounds_collected_percentage',
                 'offensive_rebounds_contested',
                 'offensive_rebounds_uncontested',
                 'offensive_rebounds_uncontested_percentage',
                 'defensive_rebounds',
                 'defensive_rebound_chances',
                 'defensive_rebounds_collected_percentage',
                 'defensive_rebounds_contested',
                 'defensive_rebounds_uncontested',
                 'defensive_rebounds_uncontested_percentage',
                 'catch_and_shoot_points_per_game',
                 'catch_and_shoot_field_goal_made_per_game',
                 'catch_and_shoot_field_goal_attempted_per_game',
                 'catch_and_shoot_field_goal_percentage',
                 'catch_and_shoot_3_point_made_per_game',
                 'catch_and_shoot_3_point_attempts_per_game',
                 'catch_and_shoot_3_point_field_goal_percentage',
                 'catch_and_shoot_effective_field_goal_percentage',
                 'catch_and_shoot_points_total',
                 'points_per_game_drive',
                 'field_goal_percentage_drive',
                 'points_per_game_close_range',
                 'field_goal_percentage_close_range',
                 'points_per_game_catch_and_shoot',
                 'field_goal_percentage_catch_and_shoot',
                 'points_per_game_pull_up',
                 'field_goal_percentage_pull_up',
                 'field_goal_attempted_drive',
                 'field_goal_attempted_close_range',
                 'field_goal_attempted_catch_and_shoot',
                 'field_goal_attempted_pull_up',
                 'effective_field_goal_percentage',
                 'position',
                 'number']}



@app.route('/')
def index():
    return 'Index Page'

@app.route('/status')
def hello_world():
    return 'Ok!'

@app.route('/player/<int:player_id>')
def get_player(player_id):
    fields = ["player_id","full_name","minutes","pull_up_field_goal_percentage","position"]
    return select_with_id(fields, player_id)

def get_zone_stats(player_id, shot_zone):
    query = text('select count from player_stats_by_zone where player_id = :p and zone = :shot_zone and event=:made_shot')
    shots = {}
    shots['made_shots'] = CONN.execute(query, p=player_id, shot_zone=shot_zone,made_shot='Made Shot').fetchone()
    shots['missed_shots'] = CONN.execute(query, p=player_id, shot_zone=shot_zone, made_shot='Missed Shot').fetchone()
    
    if not shots['made_shots'] or not shots['missed_shots']:
        raise InvalidUsage('Could not find this player', status_code = 402)

    made_shots = int(shots['made_shots'].count)
    missed_shots = int(shots['missed_shots'].count)
    
    try:
        zone_stats['percentage_success'] = made_shots / (made_shots + missed_shots)
    except ZeroDivisionError:
        zone_stats['percentage_success'] = 0.0

    zone_stats['percent_difference_average'] = zone_stats['percentage_success'] - averages[shot_zone]
    return zone_stats

def findmax(pref_zones):
    max = -1
    max_zone = ""
    for zone in possible_zones:
        if (pref_zones[zone] > max):
            max_zone = zone
            max = pref_zones[zone]
    return max_zone

@app.route('/player/<int:player_id>/zone',methods=['POST'])
def get_player_percentage_from_zone(player_id):
    if "x" not in request.form or "y" not in request.form:
        raise InvalidUsage('Missing x or y parameter in post request', status_code = 422)

    x = request.form['x']
    y = request.form['y']

    try:
        x = float(x) * 10
        y = float(y) * 10
    except ValueError:
        raise InvalidUsage('Must pass x and y as valid float values', status_code= 402)

    shot_zone = zones.classify_shot(x,y)[0]
    euclidean_distance = math.sqrt(math.pow(x,2) + math.pow(y,2))
    zone_stats = {}
    try:
        zone_stats = get_zone_stats(player_id, shot_zone)
    except:
        zone_stats['percentage_difference_average'] = -1
        zone_stats['percentage_success'] = -1

    per_zone_stats = {}
    for zone in possible_zones:
        try:
            per_zone_stats[zone] = get_zone_stats(player_id,zone)
        except:
            print("No data!")
            per_zone_stats[zone] = 0

    preferred_zone = findmax(per_zone_stats)

    return jsonify({"player_id": player_id,
                    "percentage_success":zone_stats['percentage_success'],
                    "percent_difference_average":zone_stats['percentage_difference_average'],
                    "zone":shot_zone,
                    "preferred_zone":preferred_zone})

@app.route('/teams/<team>')
def get_team_players(team):
    fields = database_fields['player_stats']
    query = text("select " + ','.join(fields) + " from player_stats where player_stats.team = :t")
    players = CONN.execute(query,t=team).fetchall()
    return jsonify([map_keys_to_values(fields, player) for player in players])


def map_keys_to_values(keys, values):
    return {key : value for key, value in zip(keys, values)}


def select_with_id(fields, player_id):
    query = text('select distinct '+", ".join(fields)+' from player_stats ps inner join season_stats ss on ss.name = ps.full_name where ps.player_id = :p ')
    player = CONN.execute(query, p=player_id).fetchone()
    player_dict = { key:value for key, value in zip(fields, player) }
    return jsonify(player_dict)



@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8886))
    app.run(host='0.0.0.0', port=port)