import json
from django.db import models
from django.conf import settings
from django.forms import ValidationError
import qrcode
import io
from django.core.files.base import ContentFile
from events.models import Event


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)

    #s'assurer que le prix total n'est pas négatif
    def clean(self):
       
        if self.total_price < 0:
            raise ValidationError("Le prix total ne peut pas être négatif.")
        


class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    offer = models.CharField(max_length=100)  
    security_key = models.CharField(max_length=255)  
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True) 
    issued_at = models.DateTimeField(auto_now_add=True)

    #l'offre ne doit pas etre vide et la clé aussi 
    def clean(self):
        if not self.offer:
            raise ValidationError("L'offre ne peut pas être vide.")
       
        if not self.security_key:
            raise ValidationError("La clé de sécurité ne peut pas être vide.")
        
    # Génération de la clé de sécurité et du QR code
    def save(self, *args, **kwargs):
        if not self.security_key:
            self.security_key = self.generate_security_key()

        # Concaténer les clés ici
        final_key = f'{self.booking.user.security_key}-{self.security_key}'
        # info à inclure dans le QR code
        data = {
            "identifiant_unique": final_key,
            "buyer_name": f'{self.booking.user.first_name} {self.booking.user.last_name}',
            "event_name": self.event.name,
            "event_date": self.event.date.strftime('%Y-%m-%d'),
            "event_time": self.event.date.strftime('%H:%M'),
            "event_location": self.event.location,
            "offer": self.offer
        }
        qr_data = json.dumps(data)
        
        # Génération du QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        file_name = f'qrcode_{self.booking.id}.png'
        self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

    # Génère une clé de sécurité unique
    def generate_security_key(self):
        import uuid
        return str(uuid.uuid4())

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    offer = models.CharField(max_length=100)  
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    #la quantité et le prix doivent etre positive
    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("La quantité doit être supérieure à zéro.")
        
        if self.total_price < 0:
            raise ValidationError("Le prix total ne peut pas être négatif.")
    
    