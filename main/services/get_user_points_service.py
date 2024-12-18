class GetUserPointsService:
	@staticmethod
	def execute(user):
		return list(user.points.all())
