from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Sport, Event
from .serializers import SportSerializer, EventSerializer

@api_view(['GET'])
def list_sports(request):
    #recuperation des sports
    sports = Sport.objects.all() 
    #serialise la liste de sports
    serializer = SportSerializer(sports, many=True)  
    if sports.exists():
        return Response(serializer.data, status=status.HTTP_200_OK)  
    return Response({"message": "Aucun sport trouvé."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def sport_details(request, sport_id):
   #recuperation du sport ou information s'il n'est pas trouver
    sport = get_object_or_404(Sport, id=sport_id)  
    #filtre les épreuves du sport selectionner et serialise la liste
    events = Event.objects.filter(sport=sport)  
    event_serializer = EventSerializer(events, many=True)
    if events.exists():
        return Response(event_serializer.data, status=status.HTTP_200_OK)  
    return Response({"message": "Aucun événement trouvé."}, status=status.HTTP_404_NOT_FOUND)  
    


    