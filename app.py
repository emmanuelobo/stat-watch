import datetime
from flask import render_template, request, url_for, redirect, flash, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user
from nba_py import player
from nba_py.player import get_player

from scripts.forms import LoginForm, RegistrationForm
from scripts.models import User, PlayerStats, PlayerProfile, LastGameStats
from scripts.playerutil import PlayerUtility
from application import app, db

login_manager = LoginManager(app)


def has_player(id):
	check_player = PlayerProfile.query.filter_by(pid=id).first()
	user_has_player = True if check_player is not None else False
	return user_has_player


@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.route('/')
def home():
	return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username_or_email.data).first()
		if user is None or not user.validate_password(form.password.data):
			user = User.query.filter_by(email=form.username_or_email.data).first()
			if user is None or not user.validate_password(form.password.data):
				flash('Invalid credentials. Please try again')
				return redirect(url_for('login'))

		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('home'))
	return render_template('login.html', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you\'re ready to go!')
		return redirect(url_for('login'))
	return render_template('signup.html', form=form)


@app.route('/search', methods=['POST', 'GET'])
def search():
	if request.method == 'POST':
		first_name, last_name = request.form['full name'].lstrip().rstrip().split()
		try:
			pid = get_player(first_name, last_name)
		except StopIteration:
			try:
				pid = get_player(last_name, first_name)
			except StopIteration:
				return 'Oops it appears that player doesn\'t exist. Please try again.'

	return redirect(url_for('player_page', id=pid))


@app.route('/players/<id>', methods=['POST', 'GET'])
def player_page(id):
	current_player = player.PlayerSummary(id)
	stats = current_player.headline_stats()[0]
	info = current_player.info()[0]
	profile_pic = PlayerUtility.get_profile_pic(info)
	return render_template('/player/profile.html', stats=stats, info=info, profile_pic=profile_pic,
						   has_player=has_player(id), per=PlayerUtility.get_per(info))


@app.route('/players/<id>/careerstats', methods=['POST', 'GET'])
def career_stats(id):
	current_player = player.PlayerSummary(id)
	stats = current_player.headline_stats()[0]
	profile_pic = PlayerUtility.get_profile_pic(current_player.info()[0])
	return render_template('/player/career_stats.html', stats=stats, profile_pic=profile_pic, has_player=has_player(id))


@app.route('/players/<id>/lastgames', methods=['POST', 'GET'])
def last_games(id):
	current_player = player.PlayerSummary(id)
	last_game = player.PlayerGameLogs(id).info()[0]
	stats = current_player.headline_stats()[0]
	profile_pic = PlayerUtility.get_profile_pic(current_player.info()[0])
	return render_template('/player/last_games.html', last_game=last_game, stats=stats, profile_pic=profile_pic,
						   has_player=has_player(id))


@app.route('/players/<id>/analytics', methods=['POST', 'GET'])
def analytics(id):
	current_player = player.PlayerSummary(id)
	stats = current_player.headline_stats()[0]
	profile_pic = PlayerUtility.get_profile_pic(current_player.info()[0])
	return render_template('/player/analytics.html', stats=stats, profile_pic=profile_pic, has_player=has_player(id))


@app.route('/players/<id>/news', methods=['POST', 'GET'])
def news(id):
	current_player = player.PlayerSummary(id)
	stats = current_player.headline_stats()[0]
	profile_pic = PlayerUtility.get_profile_pic(current_player.info()[0])
	return render_template('/player/news.html', stats=stats, profile_pic=profile_pic, has_player=has_player(id))


@app.route('/players/<id>/compare', methods=['POST', 'GET'])
def compare(id):
	current_player = player.PlayerSummary(id)
	stats = current_player.headline_stats()[0]
	profile_pic = PlayerUtility.get_profile_pic(current_player.info()[0])
	return render_template('/player/compare.html', stats=stats, profile_pic=profile_pic, has_player=has_player(id))


@app.route('/players/<id>/added', methods=['POST', 'GET'])
def add_player(id):
	if request.method == 'POST':
		searched_player = player.PlayerSummary(id)
		player_last_game = player.PlayerGameLogs(id).info()[0]
		player_stats = searched_player.headline_stats()[0]
		player_info = searched_player.info()[0]
		date = datetime.datetime.strptime(player_info['BIRTHDATE'], '%Y-%m-%dT00:00:00')
		dob = f'{date.month}/{date.day}/{date.year}'

		if player_info['SCHOOL'] is None:
			prior = player_info['COUNTRY']
		else:
			prior = player_info['SCHOOL']

		if PlayerUtility.get_per(player_info) is None:
			player_per = 0
		else:
			player_per = PlayerUtility.get_per(player_info)

		player_profile = {
			'full_name': player_stats['PLAYER_NAME'],
			'height': player_info['HEIGHT'],
			'weight': player_info['WEIGHT'],
			'experience': player_info['SEASON_EXP'],
			'position': player_info['POSITION'],
			'team': player_info['TEAM_NAME'],
			'user_id': current_user.id,
			'pid': id,
			'picture': PlayerUtility.get_profile_pic(player_info),
			'dob': dob,
			'prior': prior,
		}

		player_stats = {
			'ppg': player_stats['PTS'],
			'rpg': player_stats['REB'],
			'apg': player_stats['AST'],
			'pie': player_stats['PIE'],
			'per': player_per,
		}

		last_game = {
			'date': player_last_game['GAME_DATE'],
			'result': player_last_game['WL'],
			'matchup': player_last_game['MATCHUP'],
			'minutes': player_last_game['MIN'],
			'field_goal_percentage': player_last_game['FG_PCT'],
			'field_goals_made': player_last_game['FGM'],
			'field_goals_attempted': player_last_game['FGA'],
			'three_point_field_goal_percentage': player_last_game['FG3_PCT'],
			'three_pointers_made': player_last_game['FG3M'],
			'three_pointers_attempted': player_last_game['FG3A'],
			'free_throw_percentage': player_last_game['FT_PCT'],
			'free_throws_made': player_last_game['FTM'],
			'free_throws_attempted': player_last_game['FTA'],
			'points': player_last_game['PTS'],
			'rebounds': player_last_game['REB'],
			'offensive_rebounds': player_last_game['OREB'],
			'defensive_rebounds': player_last_game['DREB'],
			'assists': player_last_game['AST'],
			'steals': player_last_game['STL'],
			'blocks': player_last_game['BLK'],
			'turnovers': player_last_game['TOV'],
			'plus_minus': player_last_game['PLUS_MINUS'],
			'fouls': player_last_game['PF']
		}

		profile = PlayerProfile(**player_profile)
		stats = PlayerStats(**player_stats)
		last_game_stats = LastGameStats(**last_game)

		profile.stats = stats
		profile.last_game_stats = last_game_stats
		current_user.players.append(profile)
		db.session.add(profile)
		db.session.add(stats)
		db.session.add(last_game_stats)
		db.session.commit()

		return jsonify({'message': 'player created successfully!'})


@app.route('/players/<id>/removed', methods=['POST', 'GET'])
def remove_player(id):
	player = PlayerProfile.query.filter_by(pid=id).first()
	stats = player.stats
	last_game_stats = player.last_game_stats
	db.session.delete(last_game_stats)
	db.session.delete(stats)
	db.session.delete(player)
	db.session.commit()
	return jsonify({'message': 'player deleted successfully!'})


if __name__ == '__main__':
	login_manager.init_app(app)
	app.run(debug=True)