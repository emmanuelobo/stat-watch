from flask_restful import Resource


class Hola(Resource):
	def get(self):
		return {'hola': 'amigos'}


