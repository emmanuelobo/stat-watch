import json

from flask_restful import Resource, Api, reqparse
from flask import Flask
from nba_py import player

from application import app, db
from scripts.playerutil import PlayerUtility

api = Api(app)


class PlayerProfileResource(Resource):
	def get(self, player_id):
		current_player = player.PlayerSummary(player_id)
		stats = current_player.headline_stats()[0]
		info = current_player.info()[0]
		profile_pic = PlayerUtility.get_profile_pic(info)
		return {'player': info,
				'stats': stats,
				'profile_pic': profile_pic}

	def post(self):
		pass


class PlayerLastGames(Resource):
	def get(self):
		pass




if __name__ == '__main__':
	api.add_resource(PlayerProfileResource, '/players/<int:player_id>/profile')

	app.run(host='0.0.0.0', port=8080, debug=True)
