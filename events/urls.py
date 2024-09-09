from django.urls import path
from . import views 

urlpatterns = [
    path('api/sports/', views.list_sports, name='list_sports'),
    path('api/sports/<int:sport_id>/events/', views.sport_details, name='sport_details'),
]