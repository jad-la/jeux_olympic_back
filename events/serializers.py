from rest_framework import serializers
from .models import Sport, Event

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ['id', 'name', 'description']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','sport', 'name', 'description', 'date', 'time', 'location', 'price_solo', 'price_duo', 'price_family', 'photo_url']


        