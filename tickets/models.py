from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin')
    ]
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='user')
    security_key = models.CharField(max_length=255)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups', 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions', 
        blank=True
    )


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)


class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    offer = models.CharField(max_length=100)  
    security_key = models.CharField(max_length=255)  
    qr_code = models.CharField(max_length=210, unique=True)  
    issued_at = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    sport = models.ForeignKey('Sport', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    photo_url = models.URLField()


class Sport(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    offer = models.CharField(max_length=100)  
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    