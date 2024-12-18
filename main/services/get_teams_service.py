from main.models import Team


class GetTeamsService:
	@staticmethod
	def execute():
		return list(Team.objects.all())
