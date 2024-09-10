from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Sport(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Event(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    photo_url = models.URLField()

    # validation de donné vérification que la date est dans le futur
    def clean(self):
        if self.date < timezone.now().date():
            raise ValidationError("La date de l'événement ne peut pas être dans le passé.")
