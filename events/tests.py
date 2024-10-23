from django.test import TestCase
from events.models import Sport, Event
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from datetime import date, time
from .serializers import SportSerializer, EventSerializer

class EventModelTest(TestCase):
    def setUp(self):
        self.sport = Sport.objects.create(name='Athlétisme', description="Découvrez les épreuves d'athlétisme des Jeux Olympiques")

    # créer un événement avec une date dans le passé
    def test_event_with_past_date(self):
        past_date = timezone.now().date() - timedelta(days=1)
        event = Event(
            sport=self.sport,
            name='100m hommes',
            description='100 meter 1er tour',
            date=past_date,
            time='10:00:00',
            location='Saint Denis',
            photo_url='http://example.com/photo.jpg'
        )

        with self.assertRaises(ValidationError) as context:
            event.clean()


    # créer un événement avec une date dans le futur
    def test_event_with_future_date(self):
        future_date = timezone.now().date() + timedelta(days=10)
        event = Event(
            sport=self.sport,
            name='100m Men',
            description='100 meter sprint',
            date=future_date,
            time='10:00:00',
            location='Stadium',
            photo_url='http://example.com/photo.jpg'
        )

        try:
            event.clean()  
        except ValidationError:
            self.fail('La validation de la date a échoué pour une date future.')


class ListSportsViewTest(APITestCase):

    def setUp(self):
        # Création de quelques catégorie de sport pour les tests
        self.sport1 = Sport.objects.create(name='Althétisme')
        self.sport2 = Sport.objects.create(name='Natation')

    # Test de la récupération des ctégories existantes
    def test_get_list_of_sports(self):
        response = self.client.get(reverse('list_sports'))  
        sports = Sport.objects.all()
        serializer = SportSerializer(sports, many=True)  

        # Vérification du statut de la réponse et du message d'erreur
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data) 

    # Test lorsque aucun catégorie n'est trouvé
    def test_get_no_sports(self):
        # Suppression des sports créés dans setUp
        Sport.objects.all().delete()

        response = self.client.get(reverse('list_sports')) 

        # Vérification du statut de la réponse et du message d'erreur
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "Aucun sport trouvé.")


class SportDetailsViewTest(APITestCase):

    def setUp(self):
        # Création d'un sport et épreuve pour les tests
        self.sport = Sport.objects.create(name='Athlétisme')
        
        # Création d'épreuve associés à l'athlétisme
        self.event1 = Event.objects.create(
            sport=self.sport,
            name='100m homme',
            description='100 m homme',
            date=date(2024, 11, 24),
            time='10:00:00', 
            location='Stade de France, Paris',
            photo_url='https://example.com/match_ouverture.jpg',
            price_solo=50.00,
            price_duo=90.00,
            price_family=150.00
        )
    
    # Test pour un sport avec des événements
    def test_get_sport_with_events(self):
        response = self.client.get(reverse('sport_details', args=[self.sport.id]))  
        events = Event.objects.filter(sport=self.sport)
        event_serializer = EventSerializer(events, many=True) 

        # Vérifier que le statut est 200 OK et que les événements sont correctement renvoyés
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, event_serializer.data)

    # Test pour un sport non existant
    def test_get_non_existent_sport(self):
        invalid_sport_id = 9999  # Un ID de sport qui n'existe pas
        response = self.client.get(reverse('sport_details', args=[invalid_sport_id]))  # Appel de la vue avec un ID invalide

        # Vérifier que le statut est 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)