import json

from flask_restful import Resource, Api, reqparse
from flask import Flask
from nba_py import player
from nba_py.player import get_player

from application import app, db
from scripts.playerutil import PlayerUtility

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('firstname')
parser.add_argument('lastname')


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


class SearchedPlayer(Resource):
	def get(self):
		args = parser.parse_args()
		first_name = args['firstname']
		last_name = args['lastname']
		try:
			pid = get_player(first_name, last_name)
			current_player = player.PlayerSummary(pid)
			stats = current_player.headline_stats()[0]
			info = current_player.info()[0]
			profile_pic = PlayerUtility.get_profile_pic(info)
		except StopIteration:
			try:
				pid = get_player(last_name, first_name)
				current_player = player.PlayerSummary(pid)
				stats = current_player.headline_stats()[0]
				info = current_player.info()[0]
				profile_pic = PlayerUtility.get_profile_pic(info)

			except StopIteration:
				return {'error_message': 'Oops it appears that player doesn\'t exist. Please try again.'}
		return {'player': info,
				'stats': stats,
				'profile_pic': profile_pic}


class PlayerLastGames(Resource):
	def get(self):
		pass


if __name__ == '__main__':
	api.add_resource(PlayerProfileResource, '/players/<int:player_id>/profile')
	api.add_resource(SearchedPlayer, '/players/search')
	app.run(host='0.0.0.0', port=8080, debug=True)
