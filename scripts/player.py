import decouple
import requests


def get_profile_pic(player):
	"""
	Retrieve the player's profile picture
	:param player:
	:return:
	"""
	pid = str(player['PERSON_ID'])
	year = str(player['TO_YEAR'])
	tid = str(player['TEAM_ID'])
	profile_pic = decouple.config('PLAYER_PROFILE_IMG').replace('team_id', tid).replace('player_id', pid).replace(
		'current_year', year)
	return profile_pic


def get_team_colors(team):
	"""
	Returns the primary and secondary colors of the player's team
	:param team:
	:return:
	"""
	pass


def get_per(player):
	"""
	Retrieve the player's PER
	:param player:
	:return:
	"""

	last_name = player['LAST_NAME']
	first_name = player['FIRST_NAME']
	initial = last_name[:1].lower()

	last_name = last_name if len(last_name) <= 5 else last_name[:5]
	first_name = first_name if len(first_name) <= 2 else first_name[:2]

	one = '01.html'
	two = '02.html'

	url = decouple.config('PLAYER_PER').replace('last_name_initial', initial) + last_name + first_name

	source = requests.get(url + one)

	if source.status_code == 404:
		source = requests.get(url + two)