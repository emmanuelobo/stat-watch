import os
import unittest

import flask
from decouple import config
from flask import url_for
import tempfile

from application import app, db
from scripts.models import PlayerProfile

TEST_DB = 'test.db'


class UserTests(unittest.TestCase):
	"""
	User tests
	"""

	def setUp(self):
		app.config['TESTING'] = True
		app.config['DEBUG'] = True
		# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(config('BASE_DIR'), TEST_DB)
		app.config['DATABASE'] = tempfile.mkstemp()
		self.app = app
		self.app_context = self.app.app_context()
		self.app_context.push()
		self.client = self.app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	# def test_home_page(self):
	# 	response = self.client.get('/')
	# 	# import ipdb;ipdb.set_trace()
	# 	print('Test running...')
	# 	self.assertEqual(response.status_code, 200)

	def test_players(self):
		players = PlayerProfile.query.all()
		for player in players:
			print(player.full_name)

		self.assertTrue(len(players) > 0)

if __name__ == '__main__':
	unittest.main()
