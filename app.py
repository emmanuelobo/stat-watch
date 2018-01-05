from flask import Flask, render_template, request
from nba_py.player import get_player
from nba_py import player
from decouple import config
from scripts.player import get_profile_pic

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')


@app.route('/')
def home():
	my_player = None
	try:
		curr_player = get_player('Anthony', 'Davis')
		my_player = player.PlayerSummary(curr_player)
		print(player.PlayerSummary(curr_player).headline_stats())
		print(player.PlayerSummary(curr_player).info())
	except StopIteration:
		print('Oops that player doesn\'t exist')
	return render_template('homepage.html', player=my_player)

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
			print(f'Player ID: {pid}')
			searched_player = player.PlayerSummary(pid)
			print(searched_player.headline_stats()[0])
			player_name = searched_player.headline_stats()[0]['PLAYER_NAME']
			player_ppg = searched_player.headline_stats()[0]['PTS']
			player_apg = searched_player.headline_stats()[0]['AST']
			player_rpg = searched_player.headline_stats()[0]['REB']
			player_pie = searched_player.headline_stats()[0]['PIE']

			data = {}
			data['player_name'] = player_name
			data['player_ppg'] = player_ppg
			data['player_rpg'] = player_rpg
			data['player_apg'] = player_apg
			data['player_pie'] = player_pie
			data['profile_pic'] = get_profile_pic(searched_player.info()[0])

		except StopIteration:
			return 'Oops it appears that player doesn\'t exist. Please try again.'

	return render_template('searched_player.html', **data)


if __name__ == '__main__':
	app.run(debug=True)


# TODO: Wireframing for pages
# TODO: Create error page
# TODO: Fix DB creation issue
# TODO: Create user login/signup
# TODO: Create add/remove player functionality
