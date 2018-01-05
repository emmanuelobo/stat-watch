from flask import Flask, render_template, request
from nba_py.player import get_player
from nba_py import player
from decouple import config
from scripts.player import get_profile_pic


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config('SQLALCHEMY_TRACK_MODIFICATIONS', True)


@app.route('/')
def home():
	return render_template('homepage.html')

@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/register')
def register():
	return render_template('signup.html')

@app.route('/search', methods = ['POST', 'GET'])
def search():
	if request.method == 'POST':
		first_name = request.form['first name'].strip()
		last_name = request.form['last name'].strip()
		try:
			pid = get_player(first_name,last_name)
			searched_player = player.PlayerSummary(pid)
			player_name = searched_player.headline_stats()[0]['PLAYER_NAME']
			player_ppg = searched_player.headline_stats()[0]['PTS']
			player_apg = searched_player.headline_stats()[0]['AST']
			player_rpg = searched_player.headline_stats()[0]['REB']
			player_pie = searched_player.headline_stats()[0]['PIE']

			data = {
				'player_name': player_name,
				'player_ppg': player_ppg,
				'player_rpg': player_rpg,
				'player_apg': player_apg,
				'player_pie': player_pie,
				'profile_pic': get_profile_pic(searched_player.info()[0])
			}

		except StopIteration:
			return 'Oops it appears that player doesn\'t exist. Please try again.'

	return render_template('searched_player.html', **data)


if __name__ == '__main__':
	app.run(debug=True)



# TODO: Wireframing for pages
# TODO: Create error pages
# TODO: Create user login/signup
# TODO: Create add/remove player functionality
