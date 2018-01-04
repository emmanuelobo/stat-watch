import requests
from bs4 import BeautifulSoup
import decouple

def get_profile_pic(pid):
	"""
	Retrieve the player's profile picture
	:param pid:
	:return:
	"""
	pid = str(pid)
	html = requests.get(f'https://stats.nba.com/player/{pid}/')
	source = BeautifulSoup(html.content, 'html.parser')
	tid = source.find(attrs={'player-id': f'{pid}'})['team-id']
	profile_pic = decouple.config('PLAYER_PROFILE_IMG').replace('team_id', tid).replace('player_id', pid)
	return profile_pic