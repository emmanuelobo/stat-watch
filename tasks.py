from celery import Celery
from nba_py import player as nba_player
from nba_py.player import get_player

from application import app, db
from scripts.models import PlayerProfile as profile
from scripts.playerutil import update_player_last_game, update_player_stats

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(name="task.update_player")
def update_player():
	app.app_context().push()
	results = profile.query.all()
	for player in results:
		name = player.full_name.split()
		pid = get_player(name[0], name[1])
		player_last_game = nba_player.PlayerGameLogs(pid).info()[0]
		player_stats = nba_player.PlayerSummary(pid).headline_stats()[0]
		player_info = nba_player.PlayerSummary(pid).info()[0]
		player = update_player_last_game(player, player_last_game)
		player = update_player_stats(player, player_stats, player_info)

	db.session.commit()

