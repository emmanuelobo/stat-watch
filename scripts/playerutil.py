import decouple
import requests
from bs4 import BeautifulSoup


class PlayerUtility:
	@staticmethod
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

	@staticmethod
	def get_team_colors(team):
		"""
		Returns the primary and secondary colors of the player's team
		:param team:
		:return:
		"""
		pass

	@staticmethod
	def get_per(player):
		"""
		Retrieve the player's PER
		:param player:
		:return:
		"""
		last_name = player['LAST_NAME']
		first_name = player['FIRST_NAME']
		initial = last_name[:1].lower()

		last_name = last_name.lower() if len(last_name) <= 5 else last_name[:5].lower()
		first_name = first_name.lower() if len(first_name) <= 2 else first_name[:2].lower()

		one = '01.html'
		two = '02.html'

		url = decouple.config('PLAYER_PER').replace('last_name_initial', initial) + last_name + first_name
		source = requests.get(url + one)

		if source.status_code == 404:
			source = requests.get(url + two)

		soup = BeautifulSoup(source.content, 'html.parser')
		player_full_name = soup.find_all(name='span', attrs={'itemprop': 'name'})[2].contents[0]

		if player_full_name != (player['FIRST_NAME'] + ' ' + player['LAST_NAME']):
			source = requests.get(url + two)
			soup = BeautifulSoup(source.content, 'html.parser')

		return list(soup.find_all(class_='p3')[0].descendants)[5].string

	@staticmethod
	def update_player_last_game(player, player_last_game):
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
		player.last_game_stats.date = player_last_game['GAME_DATE']
		return player

	def update_player_stats(self, player, player_stats, player_info):
		player.stats.ppg = player_stats['PTS'],
		player.stats.rpg = player_stats['REB'],
		player.stats.apg = player_stats['AST'],
		player.stats.pie = player_stats['PIE']
		player.stats.per = self.get_per(player_info)
		return player


class Notifier:
	"""
	Send user player notifications
	"""

	def double_double_notification(self):
		"""
		Notify user when a player records a double double
		:return:
		"""
		pass

	def triple_double_notification(self):
		"""
		Notify user when a player records a triple double
		:return:
		"""
		pass

	def career_high_notification(self):
		"""
		Notify user when a player has a career high game
		:return:
		"""


class StatAnalyzer:
	"""
	Deep analysis of players' stats
	"""
