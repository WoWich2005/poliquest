from main.models import Stat
from main.services.get_teams_service import GetTeamsService


class GetTeamsOnPointService:
    @staticmethod
    def execute(point):
        arrival_stats = Stat.objects.filter(point=point, type=Stat.ARRIVAL_TYPE)
        finish_stats = Stat.objects.filter(point=point, type=Stat.FINISH_QUEST_TYPE)

        teams = set()
        for stat in arrival_stats:
            teams.add(stat.team)

        for stat in finish_stats:
            if stat.team in teams:
                teams.remove(stat.team)

        return list(teams)
