from django.utils.timezone import localtime
from main.models import Stat


class GetPointStatsService:
	@staticmethod
	def execute(point):
		point_stats = list(Stat.objects.filter(point=point.id))

		for point_stat in point_stats:
			point_stat.formatted_time = localtime(point_stat.time).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%S')
			point_stat.time = localtime(point_stat.time).strftime('%d.%m.%Y %H:%M:%S')

		return point_stats
