import datetime
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
			player_stats = searched_player.headline_stats()[0]
			player_info = searched_player.info()[0]
			date = datetime.datetime.strptime(player_info['BIRTHDATE'], '%Y-%m-%dT00:00:00')
			dob = f'{date.month}/{date.day}/{date.year}'
			data = {
				'player_id': player_stats['PLAYER_ID'],
				'player_name': player_stats['PLAYER_NAME'],
				'player_height': player_info['HEIGHT'],
				'player_weight': player_info['WEIGHT'],
				'player_exp': player_info['SEASON_EXP'],
				'player_position': player_info['POSITION'],
				'player_team': player_info['TEAM_NAME'],
				'player_ppg': player_stats['PTS'],
				'player_rpg': player_stats['REB'],
				'player_apg': player_stats['AST'],
				'player_pie': player_stats['PIE'],
				'player_per': get_per(player_info),
				'profile_pic': get_profile_pic(player_info),
				'player_dob': dob,
			}

		except StopIteration:
			return 'Oops it appears that player doesn\'t exist. Please try again.'

		if player_info['SCHOOL'] is None:
			data['prior'] = player_info['COUNTRY']
		else:
			data['prior'] = player_info['SCHOOL']

		if get_per(player_info) is None:
			data['player_per'] = 0
		else:
			data['player_per'] = get_per(player_info)

		check_player = PlayerProfile.query.filter_by(pid=pid).first()
		has_player = True if check_player is not None else False

	return render_template('searched_player.html', **data, has_player=has_player)


@app.route('/player/<id>/added', methods=['POST', 'GET'])
def add_player(id):
	if request.method == 'POST':
		prior = request.form['prior']
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

		profile = PlayerProfile(full_name=name, pid=id, height=height, weight=weight, experience=exp, position=position,
								team=team, user_id=current_user.id, prior=prior, picture=profile_pic, dob=dob)
		stats = PlayerStats(ppg=ppg, apg=apg, rpg=rpg, pie=pie, per=per)

		current_user.players.append(profile)
		profile.stats = stats
		db.session.add(profile)
		db.session.add(stats)
		db.session.commit()

		flash('Player successfully added.')
		return redirect(url_for('home'))


@app.route('/player/<id>/removed', methods=['POST', 'GET'])
def remove_player(id):
	player = PlayerProfile.query.filter_by(pid=id).first()
	stats = player.stats
	db.session.delete(stats)
	db.session.delete(player)
	db.session.commit()

	flash('Player removed from your team')
	return redirect(url_for('home'))

if __name__ == '__main__':
	login_manager.init_app(app)
	app.run(debug=True)
