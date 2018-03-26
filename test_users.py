import os
import unittest
from decouple import config
from flask import url_for

from application import app, db
TEST_DB = 'test.db'


class UserTests(unittest.TestCase):
	"""
	User tests
	"""
	def setUp(self):
		app.config['TESTING'] = True
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(config('BASE_DIR'), TEST_DB)
		self.app = app.test_client()
		# db.drop_all()
		# db.create_all()

	def tearDown(self):
		# tear down testing suite
		pass

	def test_home_page(self):
		response = self.app.get(url_for('home'))
		print('Test running...')
		self.assertEqual(response.status_code, 200)


if __name__ == 'main':
	unittest.main()