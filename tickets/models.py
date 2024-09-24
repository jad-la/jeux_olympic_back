import json
from django.db import models
from django.conf import settings
from django.forms import ValidationError
import qrcode
import io
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from events.models import Event
import logging

logger = logging.getLogger(__name__)

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
        
    
    # Génère une clé de sécurité unique
    def generate_security_key(self):
        import uuid
        return str(uuid.uuid4())

    # Génére le QR code à partir des clés de sécurité
    def generate_qr_code(self):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f'{self.booking.user.security_key}-{self.security_key}')
        qr.make(fit=True)
        qr_code_img = qr.make_image(fill='black', back_color='white')
        return qr_code_img

    # Création l'image du billet en y ajoutant le QR code
    def create_ticket_image(self, qr_code_img):
        qr_img_pil = qr_code_img.convert("RGB")
        qr_img_pil = qr_img_pil.resize((200, 200))

        ticket_image = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(ticket_image)
        font = ImageFont.load_default()

        # Ajout des info sur l'image du billet
        text = f"Événement: {self.event.name}\nDate: {self.event.date}\n"
        text += f"Lieu: {self.event.location}\nNom: {self.booking.user.first_name} {self.booking.user.last_name}"
        draw.text((10, 10), text, font=font, fill="black")

        ticket_image.paste(qr_img_pil, (10, 250))
        return ticket_image

    # Sauvegarde l'image dans un fichier temporaire
    def save_ticket_image(self, ticket_image):
        buffer = io.BytesIO()
        ticket_image.save(buffer, format="PNG")
        filename = f"ticket_{self.id}.png"
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

    # sauvegarde
    def save(self, *args, **kwargs):
        if not self.security_key:
            self.security_key = self.generate_security_key()
        
        qr_code_img = self.generate_qr_code()
        ticket_image = self.create_ticket_image(qr_code_img)
        self.save_ticket_image(ticket_image)

        super().save(*args, **kwargs)

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
    
    