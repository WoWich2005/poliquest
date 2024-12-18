from django.urls import path, include

from . import views
from .views import StatCreateAPIView, StatUpdateDestroyAPIView

urlpatterns = [
    path('point-control/', views.point_control, name='point-control'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/points/<int:point_id>/stats/', StatCreateAPIView.as_view()),
    path('api/v1/points/<int:point_id>/stats/<int:stat_id>', StatUpdateDestroyAPIView.as_view())
]
