from .get_team_time_service import GetTeamTimeService
from main.services.get_teams_service import GetTeamsService


class GetTeamPlacesService:
	@staticmethod
	def _get_team_times(time_type):
		result = {}
		for team in GetTeamsService.execute():
			result[team.name] = GetTeamTimeService.execute(team, time_type)

		result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}
		return result

	@staticmethod
	def execute(time_type):
		places = []

		times = GetTeamPlacesService._get_team_times(time_type)
		teams = list(times.keys())
		for i in range(len(times)):
			places.append({
				'place': i + 1,
				'name': teams[i],
				'time': times[teams[i]]
			})

		return places
