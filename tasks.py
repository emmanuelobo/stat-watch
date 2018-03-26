from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from nba_py.player import get_player
from nba_py import player as nba_player

from application import app, db
from scripts.models import PlayerProfile as profile


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(name="task.query_player_names")
def query_player_names():
	app.app_context().push()
	results = profile.query.all()
	for player in results:
		name = player.full_name.split()
		pid = get_player(name[0], name[1])
		player_last_game = nba_player.PlayerGameLogs(pid).info()[0]
		player.last_game_stats.matchup = player_last_game['MATCHUP']
		player.last_game_stats.points = player_last_game['PTS']
		player.last_game_stats.rebounds = player_last_game['REB']
		player.last_game_stats.assists = player_last_game['AST']
		player.last_game_stats.assists = player_last_game['AST']
		player.last_game_stats.steals = player_last_game['STL']
		player.last_game_stats.blocks = player_last_game['BLK']
		player.last_game_stats.turnovers = player_last_game['TOV']
		player.last_game_stats.plus_minus = player_last_game['PLUS_MINUS']
		player.last_game_stats.field_goal_percentage = player_last_game['FG_PCT']
		player.last_game_stats.field_goals_attempted = player_last_game['FGA']
		player.last_game_stats.field_goals_made = player_last_game['FGM']
		player.last_game_stats.free_throws_attempted = player_last_game['FTA']
		player.last_game_stats.free_throws_made = player_last_game['FTM']
		player.last_game_stats.offensive_rebounds = player_last_game['OREB']
		player.last_game_stats.result = player_last_game['WL']
		player.last_game_stats.defensive_rebounds = player_last_game['DREB']
		player.last_game_stats.three_point_field_goal_percentage = player_last_game['FG3_PCT']
		player.last_game_stats.three_pointers_attempted = player_last_game['FG3A']
		player.last_game_stats.three_pointers_made = player_last_game['FG3M']
		player.last_game_stats.fouls = player_last_game['PF']
		player.last_game_stats.minutes = player_last_game['MIN']

	db.session.commit()

@celery.task(name="app.booya")
def booya():
	print('BOOYA!')


@celery.task(name='player_name')
def get_player_name(name):
	return name

