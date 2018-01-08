import decouple


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
	pass
