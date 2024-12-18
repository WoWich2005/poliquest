from main.models import TeamPoints, Stat


class GetTeamPointsService:
    class PointType:
        PASSED = 1
        LEFT = 2

    @staticmethod
    def execute(team, point_type=None):
        if point_type is None:
            return list(TeamPoints.objects.filter(team=team))
        elif point_type == GetTeamPointsService.PointType.PASSED:
            result = []

            finished_stats = list(Stat.objects.filter(
                team=team,
                type=Stat.FINISH_QUEST_TYPE
            ))
            for finished_stat in finished_stats:
                result.extend(
                    list(TeamPoints.objects.filter(
                        team=team,
                        point=finished_stat.point)
                    )
                )

            return result
        elif point_type == GetTeamPointsService.PointType.LEFT:
            all_points = GetTeamPointsService.execute(team)
            passed_points = set(GetTeamPointsService.execute(team, GetTeamPointsService.PointType.PASSED))

            return [point for point in all_points if point not in passed_points]
