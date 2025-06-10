from flask import Flask,jsonify,request,Response
import ipl
from collections import OrderedDict
import json

app=Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/teams')
def teams():
    team=ipl.team_name()
    return jsonify(team) # as we required the json format data in API


@app.route('/api/teamVteam')
def teamVteam():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    
    data = ipl.team_vs_team(team1, team2)

    ordered_data = OrderedDict([
        ("Team1", data["team1"]),
        ("Team2", data["team2"]),
        ("Matches_played", data["matches_played"]),
        ("Team1_win", data["team1_win"]),
        ("Team1_win_percentage", data["team1_win_percentage"]),
        ("Team2_win", data["team2_win"]),
        ("Team2_win_percentage", data["team2_win_percentage"]),
        ("Draws", data["draws"])
    ])

    return Response(json.dumps(ordered_data, indent=4), mimetype='application/json')


@app.route('/api/team_winning_record')
def team_winning_record():
    data = ipl.winning_team()
    return jsonify(data)


@app.route('/api/most_final_played')
def most_final_played():
    data = ipl.most_final_played()
    return jsonify(data)


@app.route('/api/point_table')
def point_table():
    season = request.args.get('season')
    if not season:
        return jsonify({'error': 'Season parameter is missing'}), 400
    try:
        data = ipl.point_table_extension(season)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/purple_cap')
def purple_cap():
    data = ipl.purple_cap()
    return jsonify(data)   

@app.route('/api/orange_cap')
def orange_cap():
    data = ipl.orange_cap()
    return jsonify(data)   


@app.route('/api/batting_pair')
def batting_pair():
    data = ipl.batting_pair()
    return jsonify(data)
    
    
@app.route('/api/Player_Of_Match')
def player_of_match():
    data=ipl.Player_Of_match_details()
    return jsonify(data)


@app.route('/api/bowler_details')
def bowler_details_api():
    bowler = request.args.get('bowler')
    data = ipl.bowler_details(bowler)
    return jsonify(data)

        
@app.route('/api/batsman_details')
def batsman_details_api():
    batsman = request.args.get('batsman')
    data = ipl.batsman_details(batsman)
    return jsonify(data) 



@app.route('/api/name_of_bowlers')
def bowlers():
    return jsonify({"bowler": ipl.no_of_bowler()})

@app.route('/api/name_of_batsmens')
def batsman():
    return jsonify({"batsmen": ipl.no_of_batsman()})

    
if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)


