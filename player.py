import requests
from bs4 import BeautifulSoup

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
	profile_pic = f'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/{tid}/2017/260x190/{pid}.png'
	return profile_pic