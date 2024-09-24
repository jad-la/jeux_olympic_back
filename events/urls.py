from django.urls import path
from . import views 
from .api_events_docs import original_list_sports,  original_sport_details


urlpatterns = [
    path('api/sports/', original_list_sports, name='list_sports'),
    path('api/sports/<int:sport_id>/events/', original_sport_details, name='sport_details'),

]

