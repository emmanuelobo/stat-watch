from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager, prompt_bool
import application
from application import db


manager = Manager(application)
migrate = Migrate(application, db)

manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
	"""
	Creates database
	:return:
	"""
	db.create_all()


@manager.command
def drop_db():
	"""
	Drops the database
	:return:
	"""
	if prompt_bool('Are you sure you want to drop this database?'):
		db.drop_all()
		print('Database dropped')


if __name__ == '__main__':
	manager.run()
