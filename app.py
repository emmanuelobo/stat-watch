from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_migrate import Migrate

from nba_py.player import get_player
from nba_py import player
from scripts.forms import LoginForm, RegistrationForm
from scripts.models import User, PlayerStats, PlayerProfile
from scripts.player import get_profile_pic, get_per
from __init__ import generate_app, db

app = generate_app()
login_manager = LoginManager(app)


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
		first_name = request.form['first name'].strip()
		last_name = request.form['last name'].strip()
		try:
			pid = get_player(first_name, last_name)
			searched_player = player.PlayerSummary(pid)
			PLAYER_STATS = searched_player.headline_stats()[0]
			PLAYER_INFO = searched_player.info()[0]
			data = {
				'player_id': PLAYER_STATS['PLAYER_ID'],
				'player_name': PLAYER_STATS['PLAYER_NAME'],
				'player_height': PLAYER_INFO['HEIGHT'],
				'player_weight': PLAYER_INFO['WEIGHT'],
				'player_dob': PLAYER_INFO['BIRTHDATE'],
				'player_exp': PLAYER_INFO['SEASON_EXP'],
				'player_position': PLAYER_INFO['POSITION'],
				'player_team': PLAYER_INFO['TEAM_NAME'],
				'player_ppg': PLAYER_STATS['PTS'],
				'player_rpg': PLAYER_STATS['REB'],
				'player_apg': PLAYER_STATS['AST'],
				'player_pie': PLAYER_STATS['PIE'],
				'player_per': get_per(PLAYER_INFO),
				'profile_pic': get_profile_pic(PLAYER_INFO),
			}

		except StopIteration:
			return 'Oops it appears that player doesn\'t exist. Please try again.'

	return render_template('searched_player.html', **data)


@app.route('/player/<id>/added', methods=['POST', 'GET'])
def add_player(id):
	if request.method == 'POST':
		name = request.form['player_name']
		height = request.form['player_height']
		weight = request.form['player_weight']
		exp = request.form['player_exp']
		team = request.form['player_team']
		position = request.form['player_position']
		ppg = request.form['player_ppg']
		apg = request.form['player_apg']
		rpg = request.form['player_rpg']
		pie = request.form['player_pie']
		per = request.form['player_per']
		profile_pic = request.form['profile_pic']
		dob = request.form['player_dob']

		profile = PlayerProfile(full_name=name, height=height, weight=weight, experience=exp, position=position,
								team=team, user_id=current_user.id, prior='prior', picture=profile_pic, dob=dob)
		stats = PlayerStats(ppg=ppg, apg=apg, rpg=rpg, pie=pie, per=per)

		current_user.players.append(profile)
		profile.stats = stats
		db.session.add(profile)
		db.session.add(stats)
		db.session.commit()
		print('success!')

		flash('Player successfully added.')
		return redirect(url_for('home'))


if __name__ == '__main__':
	login_manager.init_app(app)
	app.run(debug=True)
