from django.db import models
from django.conf import settings
from django.forms import ValidationError
from events.models import Event


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)

    # Gestion d'erreur s'assurer que le prix total n'est pas négatif
    def clean(self):
       
        if self.total_price < 0:
            raise ValidationError("Le prix total ne peut pas être négatif.")
        


class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    offer = models.CharField(max_length=100)  
    security_key = models.CharField(max_length=255)  
    qr_code = models.CharField(max_length=210, unique=True)  
    issued_at = models.DateTimeField(auto_now_add=True)

    # gestion d'erreur l'offre ne doit pas etre vide et la clé aussi 
    def clean(self):
        if not self.offer:
            raise ValidationError("L'offre ne peut pas être vide.")
       
        if not self.security_key:
            raise ValidationError("La clé de sécurité ne peut pas être vide.")



class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    offer = models.CharField(max_length=100)  
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # gestion d'erreur la quantité et le prix doivent etre positive
    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("La quantité doit être supérieure à zéro.")
        
        if self.total_price < 0:
            raise ValidationError("Le prix total ne peut pas être négatif.")