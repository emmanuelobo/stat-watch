from flask_restful import Resource


class PlayerProfileResource(Resource):
	def get(self):
		self.name = 'Lebron James'
		return {'name': self.name}

