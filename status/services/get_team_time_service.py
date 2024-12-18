from datetime import timedelta
from main.models import Stat
from status.services.get_team_points_service import GetTeamPointsService


class GetTeamTimeService:
    class TimeType:
        TOTAL_TIME = 1
        MOVE_TIME = 2
        QUEST_TIME = 3

    @staticmethod
    def _get_team_times(team, stat_type, point=None):
        if point is None:
            return [
                stat.time.replace(microsecond=0) for stat in Stat.objects.filter(
                    team=team.id,
                    type=stat_type
                ).order_by('time')
            ]
        else:
            return [
                stat.time.replace(microsecond=0) for stat in Stat.objects.filter(
                    team=team.id,
                    type=stat_type,
                    point=point
                ).order_by('time')
            ]

    @staticmethod
    def _get_move_time(team, point=None):
        result = timedelta()

        arrival_times = GetTeamTimeService._get_team_times(team, Stat.ARRIVAL_TYPE, point)[1:]
        finish_quest_times = GetTeamTimeService._get_team_times(team, Stat.FINISH_QUEST_TYPE, point)

        if point is None:
            for data in list(zip(arrival_times, finish_quest_times)):
                result += data[0] - data[1]
        else:
            points_passed = GetTeamPointsService.execute(team, GetTeamPointsService.PointType.PASSED)
            point_idx = 0
            for i in range(len(points_passed)):
                point_passed = points_passed[i]
                if point_passed.point == point:
                    point_idx = i
                    break

            if point_idx != 0:
                cur_point_arrival_time = Stat.objects.filter(
                    point=point,
                    team=team,
                    type=Stat.ARRIVAL_TYPE
                )[0].time.replace(microsecond=0)

                prev_point_finish_time = Stat.objects.filter(
                    point=points_passed[point_idx - 1].point,
                    team=team,
                    type=Stat.FINISH_QUEST_TYPE
                )[0].time.replace(microsecond=0)

                result += cur_point_arrival_time - prev_point_finish_time

        return result

    @staticmethod
    def _get_quest_time(team, point=None):
        result = timedelta()

        start_quest_times = GetTeamTimeService._get_team_times(team, Stat.START_QUEST_TYPE, point)
        finish_quest_times = GetTeamTimeService._get_team_times(team, Stat.FINISH_QUEST_TYPE, point)

        for data in list(zip(start_quest_times, finish_quest_times)):
            result += data[1] - data[0]

        return result

    @staticmethod
    def execute(team, time_type, point=None):
        result = timedelta()

        if time_type == GetTeamTimeService.TimeType.TOTAL_TIME:
            result += GetTeamTimeService._get_move_time(team, point)
            result += GetTeamTimeService._get_quest_time(team, point)
        elif time_type == GetTeamTimeService.TimeType.MOVE_TIME:
            result += GetTeamTimeService._get_move_time(team, point)
        elif time_type == GetTeamTimeService.TimeType.QUEST_TIME:
            result += GetTeamTimeService._get_quest_time(team, point)

        return result
