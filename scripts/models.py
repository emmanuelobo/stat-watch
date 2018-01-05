from sqlalchemy import Column, Integer, String, Float
from scripts.database import Base



class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(30), nullable=False)
	email = Column(String(40), nullable=False)
	password = Column(String(50), nullable=False)

	def __init__(self, username=None, email=None, password=None):
		self.username = username
		self.email = email
		self.password = password

	def __repr__(self):
		return '<User %r>' % self.username

class PlayerProfile(Base):
	__tablename__ = 'playerprofile'
	id = Column(Integer, primary_key=True)
	full_name = Column(String(30), nullable=False)
	height = Column(String(10), nullable=False)
	weight = Column(String(10), nullable=False)
	prior = Column(String(15), nullable=False)
	age = Column(Integer, nullable=False)
	experience = Column(Integer, nullable=False)


class PlayerStats(Base):
	__tablename__ = 'playerstats'
	id = Column(Integer, primary_key=True)
	ppg = Column(Float, nullable=False)
	rpg = Column(Float, nullable=False)
	apg = Column(Float, nullable=False)
	pie = Column(Float, nullable=False)
	bpg = Column(Float, nullable=True)
	spg = Column(Float, nullable=True)