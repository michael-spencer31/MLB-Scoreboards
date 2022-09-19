from datetime import datetime, timedelta
import requests
import json

# function to determine the status of a game if no team is selected
# here we just print the matchup data and not full box score
def game_info():
   
    if (game['status']['status'] == "Final" or game['status']['status'] == "Game Over"):
        return '%s (%s) vs %s (%s) @ %s %s' % (
                game['away_team_name'],
                game['linescore']['r']['away'],
                game['home_team_name'],
                game['linescore']['r']['home'],
                game['venue'],
                game['status']['status']
            )
# function to determine the status of a game, if a team is selected
def team_score():
    if game['status']['status'] == "In Progress":
        return \
        '-------------------------------\n' \
        '%s (%s) vs. %s (%s) @ %s\n' \
        '%s: %s of the %s\n' \
        'Pitching: %s || Batting: %s || S: %s B: %s O: %s\n' \
        '-------------------------------' % (
                game['away_team_name'],
                game['linescore']['r']['away'],
                game['home_team_name'],
                game['linescore']['r']['home'],
                game['venue'],
                game['status']['status'],
                game['status']['inning_state'],
                game['status']['inning'],
                game['pitcher']['last'],
                game['batter']['last'],
                game['status']['s'],
                game['status']['b'],
                game['status']['o']
            )
    elif (game['status']['status'] == "Final" or game['status']['status'] == "Game Over"):
        return \
        '-------------------------------\n' \
        '%s (%s) vs. %s (%s) @ %s\n' \
        'W: %s || L: %s || SV: %s\n' \
        '-------------------------------' % (
                game['away_team_name'],
                game['linescore']['r']['away'],
                game['home_team_name'],
                game['linescore']['r']['home'],
                game['venue'],
                game['winning_pitcher']['name_display_roster'],
                game['losing_pitcher']['name_display_roster'],
                game['save_pitcher']['name_display_roster']
            )

# this function takes in a date and creates the URL link to return
def date_url(date):

        baseball_url = "http://gd2.mlb.com/components/game/mlb/year_%d/month_%s/day_%s/master_scoreboard.json" \
        % (now.year, now.strftime("%m"), yesterday.strftime("%d"))

        return baseball_url

# get the current time
now = datetime.now()
yesterday = datetime.now() - timedelta(days=1)
date = "yesterday"

# build the link and then use the request to call the api
data = requests.get(date_url(date))

# once we have the data back we jsonify it to make it easier to read
game_data = data.json()
game_array = game_data['data']['games']['game']

# get a team name from the user
team = input('What team do you want to see? To see all games for today, press enter ').upper()

# list of all MLB teams
teams = ["LA", "NY", "STL", "ATL", "SD", "PHI", "MIL", "SF", "ARI", "COL",
			"CHI", "MIA", "CIN", "PIT", "WSH", "HOU", "NY", "CLE", "TOR", "TB",
			"SEA", "BAL", "CHI", "MIN", "BOS", "LA", "TEX", "KC", "DET", "OAK", ""]

# check if the user enters a valid team name, and loop until they do
while team not in teams:
	print("Invalid team name - please try again")
	team = input('What team do you want to see? To see all games for today, press enter ').upper()

for game in game_array:
    if team == "":
        display = game_info()
        if display:
            print(display)
    else:
    	# if the user specified a team, check if the game contains that team
        if (game['home_name_abbrev']) == team or (game['away_name_abbrev']) == team:
            display = team_score()
            if display:
                print(display)

