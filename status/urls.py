from django.urls import path
from . import views

urlpatterns = [
	path('', views.show_status_page, name='show-status-page'),
	path('download/total-time-table', views.download_total_times_table, name='download-total-time-table'),
	path('download/move-time-table', views.download_move_times_table, name='download-move-time-table'),
	path('download/quest-time-table', views.download_quest_times_table, name='download-quest-time-table'),
]
