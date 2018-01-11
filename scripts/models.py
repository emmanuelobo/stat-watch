from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db


class User(db.Model, UserMixin):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(30), nullable=False)
	email = Column(String(40), nullable=False)
	password = Column(String(130), nullable=False)
	players = relationship('PlayerProfile', backref='user', lazy=True)

	def __init__(self, username=None, email=None, password=None):
		self.username = username
		self.email = email
		self.password = password

	def __repr__(self):
		return f'<User: {self.username}>'

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def validate_password(self, password):
		return check_password_hash(self.password, password)


class PlayerProfile(db.Model):
	__tablename__ = 'playerprofile'
	id = Column(Integer, primary_key=True)
	full_name = Column(String(30), nullable=False)
	height = Column(String(10), nullable=False)
	weight = Column(String(10), nullable=False)
	prior = Column(String(15), nullable=False)
	team = Column(String(15), nullable=False)
	# position = Column(String(15), nullable=False)
	age = Column(Integer, nullable=False)
	experience = Column(Integer, nullable=False)
	picture = Column(String(40), nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	stats = relationship('PlayerStats', backref='playerprofile', lazy=True)

	def __repr__(self):
		return f'<Player: {self.full_name}>'


class PlayerStats(db.Model):
	__tablename__ = 'playerstats'
	id = Column(Integer, primary_key=True)
	ppg = Column(Float, nullable=False)
	rpg = Column(Float, nullable=False)
	apg = Column(Float, nullable=False)
	pie = Column(Float, nullable=False)
	per = Column(Float, nullable=False)
	bpg = Column(Float, nullable=True)
	spg = Column(Float, nullable=True)
	player_id = Column(Integer, ForeignKey('playerprofile.id'), nullable=False)
