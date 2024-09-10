from django.test import TestCase
from events.models import Sport, Event
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

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
