from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(40), nullable=False)
	password = db.Column(db.String(50), nullable=False)

class PlayerProfile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(30), nullable=False)
	height = db.Column(db.String(10), nullable=False)
	weight = db.Column(db.String(10), nullable=False)
	prior = db.Column(db.String(15), nullable=False)
	age = db.Column(db.Integer, nullable=False)
	experience = db.Column(db.Integer, nullable=False)


class PlayerStats(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ppg = db.Column(db.Float, nullable=False)
	rpg = db.Column(db.Float, nullable=False)
	apg = db.Column(db.Float, nullable=False)
	pie = db.Column(db.Float, nullable=False)
	bpg = db.Column(db.Float, nullable=True)
	spg = db.Column(db.Float, nullable=True)