from app import create_app
from flask import jsonify
import sqlalchemy
from sqlalchemy.sql import text

CONN = sqlalchemy.create_engine('sqlite:///data.db')
app = create_app("development")

@app.route('/')
def index():
    return 'Index Page'

@app.route('/status')
def hello_world():
    return 'Ok!'

#10116
@app.route('/player/<int:player_id>')
def get_player(player_id):
    fields = ["player_id","full_name","minutes","pull_up_field_goal_percentage"]
    return select_with_id(fields, player_id)

def select_with_id(fields, player_id):
    query = text('select '+", ".join(fields)+' from player_stats where player_id = :p')
    player = CONN.execute(query, p=player_id).fetchone()
    player_dict = { key:value for key, value in zip(fields, player) }
    return jsonify(player_dict)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port)