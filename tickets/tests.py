from datetime import date
from django.test import TestCase
from tickets.models import Booking, Ticket, CartItem, Cart
from events.models import Event, Sport
from users.models import CustomUser
from django.core.exceptions import ValidationError


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='user@example.com', password='password')
        self.booking = Booking.objects.create(user=self.user, total_price=100.00)
    #test avec un prix negatif
    def test_booking_with_negative_price(self):
        self.booking.total_price = -10.00  
        with self.assertRaises(ValidationError):
            self.booking.clean()  
    
    # Test de création d'une réservation avec un prix total correct
    def test_booking_total_price_calculation(self):
        cart = Cart.objects.create(user=self.user)
        event = Event.objects.create(
            sport=Sport.objects.create(name='Athlétisme'),
            name='100m homme',
            description='1er tour 100m',
            date='2024-08-01',
            time='10:00:00',
            location='Saint Denis',
            photo_url='http://example.com/photo.jpg',
            price_solo=50.00,  
            price_duo=80.00,
            price_family=120.00
        )
        CartItem.objects.create(cart=cart, event=event, offer='solo', quantity=1, total_price=50.00)
        total_price = sum(item.total_price for item in cart.items.all())
        booking = Booking.objects.create(user=self.user, total_price=total_price)
        self.assertEqual(booking.total_price, 50.00) 


class TicketModelTest(TestCase):
    def setUp(self):
        sport = Sport.objects.create(name='Athlétisme', description="Découvrez les épreuves d'athlétisme des Jeux Olympiques")
        event = Event.objects.create(
            sport=sport,
            name='100m homme',
            description='100 metre 1er tour',
            date=date(2024, 8, 1), 
            time='10:00:00',
            location='Saint Denis',
            photo_url='http://example.com/photo.jpg',
            price_solo=50.00,  
            price_duo=80.00,
            price_family=120.00
        )
        self.booking = Booking.objects.create(user=CustomUser.objects.create_user(email='user@example.com', password='password'), total_price=100.00)
        self.ticket = Ticket.objects.create(booking=self.booking, event=event, offer='solo', security_key='so2567Ee678key', qr_code='unique_qr_code')
    
    # Test de la validation d'une offre vide
    def test_ticket_with_empty_offer(self):
        self.ticket.offer = ''
        with self.assertRaises(ValidationError):
                self.ticket.clean()  
    

    # Test de la génération du QR code
    def test_ticket_qr_code_generation(self):
        self.ticket.qr_code = None
        self.ticket.save()
        self.assertTrue(self.ticket.qr_code)


class CartItemModelTest(TestCase):
    def setUp(self):
        sport = Sport.objects.create(name='Athletisme', description="Découvrez les épreuves d'athlétisme des Jeux Olympiques")
        event = Event.objects.create(
            sport=sport,
            name='100m homme',
            description='100 metre 1er tour',
            date=date(2024, 8, 1), 
            time='10:00:00',
            location='Saint Denis',
            photo_url='http://example.com/photo.jpg',
            price_solo=50.00,  
            price_duo=80.00,   
            price_family=120.00
        )
        self.cart_item = CartItem.objects.create(
            cart=Cart.objects.create(user=CustomUser.objects.create_user(email='user@example.com', password='password')),
            event=event,
            offer='solo',
            quantity=1,
            total_price=100.00
        )

    # Test de validation de la quantité négative
    def test_cart_item_with_negative_quantity(self):
        self.cart_item.quantity = -1  
        with self.assertRaises(ValidationError):
            self.cart_item.clean()  

    # Test de validation d'un prix total négatif
    def test_cart_item_with_negative_total_price(self):
        self.cart_item.total_price = -100.00  
        with self.assertRaises(ValidationError):
            self.cart_item.clean()  