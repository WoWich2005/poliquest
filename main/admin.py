from django.contrib import admin
from .models import Point, Team, Stat, TeamPoints

admin.site.register(Point)
admin.site.register(Team)
admin.site.register(Stat)
admin.site.register(TeamPoints)
