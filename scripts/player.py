import decouple
import requests
from bs4 import BeautifulSoup


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
