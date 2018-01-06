from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_migrate import Migrate

from nba_py.player import get_player
from nba_py import player
from scripts.forms import LoginForm
from scripts.models import User
from scripts.player import get_profile_pic
from __init__ import generate_app, db

app = generate_app()

migrate = Migrate(app, db)

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
		user = User.query.filter_by(username=form.username.data).first()
		print(user)
		if user is None or not user.validate_password(form.password.data):
			flash('Invalid credentials. Please try again')
			print('Invalid credentials. Please try again')
			return redirect(url_for('login'))

		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('home'))
	return render_template('login.html', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/register')
def register():
	return render_template('signup.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
	if request.method == 'POST':
		first_name = request.form['first name'].strip()
		last_name = request.form['last name'].strip()
		try:
			pid = get_player(first_name, last_name)
			searched_player = player.PlayerSummary(pid)
			data = {
				'player_name': searched_player.headline_stats()[0]['PLAYER_NAME'],
				'player_ppg': searched_player.headline_stats()[0]['PTS'],
				'player_rpg': searched_player.headline_stats()[0]['REB'],
				'player_apg': searched_player.headline_stats()[0]['AST'],
				'player_pie': searched_player.headline_stats()[0]['PIE'],
				'profile_pic': get_profile_pic(searched_player.info()[0])
			}

		except StopIteration:
			return 'Oops it appears that player doesn\'t exist. Please try again.'

	return render_template('searched_player.html', **data)


if __name__ == '__main__':
	login_manager.init_app(app)
	app.run(debug=True)

# TODO: Wireframing for pages
# TODO: Create error pages
# TODO: Create user login/signup
# TODO: Create add/remove player functionality
