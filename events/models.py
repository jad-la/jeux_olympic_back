from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Event(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    photo_url = models.URLField()

