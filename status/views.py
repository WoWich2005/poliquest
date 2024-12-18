import math

from django.shortcuts import render, redirect

from main.models import Point
from status.services.get_status_table_file_url_service import GetStatusTableFileUrlService
from status.services.get_team_places_service import GetTeamPlacesService, GetTeamTimeService
from main.services.get_teams_service import GetTeamsService
from status.services.get_team_points_service import GetTeamPointsService
from status.services.get_teams_on_point_service import GetTeamsOnPointService


def show_status_page(request):
    data = {
        'total_teams_time': GetTeamPlacesService.execute(GetTeamTimeService.TimeType.TOTAL_TIME),
        'total_teams_move_time': GetTeamPlacesService.execute(GetTeamTimeService.TimeType.MOVE_TIME),
        'total_teams_quest_time': GetTeamPlacesService.execute(GetTeamTimeService.TimeType.QUEST_TIME),
        'team_stats': [],
        'map_data': []
    }

    for team in GetTeamsService.execute():
        all_points_count = len(GetTeamPointsService.execute(team))
        points_passed = GetTeamPointsService.execute(team, GetTeamPointsService.PointType.PASSED)
        points_left = GetTeamPointsService.execute(team, GetTeamPointsService.PointType.LEFT)

        percentage_passed = str(math.trunc(len(points_passed) * 100 / all_points_count))

        team_stat = {
            "team_name": team.name,
            "points_passed": [],
            "points_left": [],
            "percentage_passed": percentage_passed
        }

        for point in points_passed:
            move_time = GetTeamTimeService.execute(team, GetTeamTimeService.TimeType.MOVE_TIME, point.point)
            quest_time = GetTeamTimeService.execute(team, GetTeamTimeService.TimeType.QUEST_TIME, point.point)

            team_stat["points_passed"].append(
                {
                    "number": point.number,
                    "name": point.point.name,
                    "move_time": move_time,
                    "quest_time": quest_time,
                    "total_time": move_time + quest_time
                }
            )

        for point in points_left:
            team_stat["points_left"].append(point.point.name)

        data['team_stats'].append(team_stat)

    for point in Point.objects.all():
        teams_on_point = GetTeamsOnPointService.execute(point)

        data['map_data'].append({
            'point_name': point.name,
            'point_id': point.id,
            'not_empty': "true" if len(teams_on_point) != 0 else "false",
            'teams_on_point': teams_on_point
        })

    return render(request, 'status/status.html', data)


def download_total_times_table(request):
    return redirect(GetStatusTableFileUrlService.execute(GetTeamTimeService.TimeType.TOTAL_TIME))


def download_move_times_table(request):
    return redirect(GetStatusTableFileUrlService.execute(GetTeamTimeService.TimeType.MOVE_TIME))


def download_quest_times_table(request):
    return redirect(GetStatusTableFileUrlService.execute(GetTeamTimeService.TimeType.QUEST_TIME))
