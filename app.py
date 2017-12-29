from flask import Flask, render_template
from nba_py.player import get_player
from nba_py import player
from flask_sqlalchemy import SQLAlchemy
from decouple import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)


@app.route('/')
def home():
	my_player = None
	try:
		curr_player = get_player('Anthony', 'Davis')
		my_player = player.PlayerSummary(curr_player)
		print(player.PlayerSummary(curr_player).headline_stats())
	except StopIteration:
		print('Oops that player doesn\'t exist')
	return render_template('homepage.html', player=my_player)

@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/register')
def register():
	return render_template('signup.html')


if __name__ == '__main__':
	app.run(debug=True)
