from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Sport, Event
from .serializers import SportSerializer, EventSerializer


@api_view(['GET'])
def list_sports(request):
    sports = Sport.objects.all() 
    serializer = SportSerializer(sports, many=True)  
    return Response(serializer.data) 

@api_view(['GET'])
def sport_details(request, sport_id):
    sport = get_object_or_404(Sport, id=sport_id)  
    events = Event.objects.filter(sport=sport)  
    event_serializer = EventSerializer(events, many=True)
    return Response(event_serializer.data)
    