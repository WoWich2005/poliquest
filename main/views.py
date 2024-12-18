from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView

from main.models import Stat
from main.permissions import IsUserHasPointPermissionsOrReadOnly
from main.serializers import StatUpdateSerializer, StatCreateSerializer
from main.services.get_point_stats_service import GetPointStatsService
from main.services.get_user_points_service import GetUserPointsService
from main.services.get_teams_service import GetTeamsService


@login_required
def point_control(request):
    data = {
        'points': [],
        'teams': GetTeamsService.execute(),
        'team_actions': Stat.STAT_TYPE_CHOICES
    }

    points = GetUserPointsService.execute(request.user)
    for point in points:
        data['points'].append({
            'id': point.id,
            'name': point.name,
            'stats': GetPointStatsService.execute(point)
        })

    return render(request, 'main/point-control.html', data)


class StatCreateAPIView(CreateAPIView):
    serializer_class = StatCreateSerializer
    permission_classes = [IsUserHasPointPermissionsOrReadOnly]

    def get_queryset(self):
        queryset = Stat.objects.filter(point=self.kwargs.get('point_id'))
        return queryset


class StatUpdateDestroyAPIView(UpdateAPIView,
                               DestroyAPIView):
    serializer_class = StatUpdateSerializer
    lookup_url_kwarg = 'stat_id'
    permission_classes = [IsUserHasPointPermissionsOrReadOnly]

    def get_queryset(self):
        queryset = Stat.objects.filter(point=self.kwargs.get('point_id'))
        return queryset
