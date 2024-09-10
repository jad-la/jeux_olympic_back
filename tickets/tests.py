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


#tester aucun type d'offre
class TicketModelTest(TestCase):
    def setUp(self):
        sport = Sport.objects.create(name='Athlétisme', description="Découvrez les épreuves d'athlétisme des Jeux Olympiques")
        event = Event.objects.create(
            sport=sport,
            name='100m homme',
            description='100 metre 1er tour',
            date='2024-08-01',
            time='10:00:00',
            location='Saint Denis',
            photo_url='http://example.com/photo.jpg'
        )
        self.booking = Booking.objects.create(user=CustomUser.objects.create_user(email='user@example.com', password='password'), total_price=100.00)
        self.ticket = Ticket.objects.create(booking=self.booking, event=event, offer='solo', security_key='so2567Ee678key', qr_code='unique_qr_code')
    def test_ticket_with_empty_offer(self):
        self.ticket.offer = ''
        with self.assertRaises(ValidationError):
                self.ticket.clean()  

#tester la quantité et le prix des item du panier
class CartItemModelTest(TestCase):
    def setUp(self):
        sport = Sport.objects.create(name='Athletisme', description="Découvrez les épreuves d'athlétisme des Jeux Olympiques")
        event = Event.objects.create(
            sport=sport,
            name='100m homme',
            description='100 metre 1er tour',
            date='2024-08-01',
            time='10:00:00',
            location='Saint Denis',
            photo_url='http://example.com/photo.jpg'
        )
        self.cart_item = CartItem.objects.create(
            cart=Cart.objects.create(user=CustomUser.objects.create_user(email='user@example.com', password='password')),
            event=event,
            offer='solo',
            quantity=1,
            total_price=100.00
        )

    def test_cart_item_with_negative_quantity(self):
        self.cart_item.quantity = -1  
        with self.assertRaises(ValidationError):
            self.cart_item.clean()  

    def test_cart_item_with_negative_total_price(self):
        self.cart_item.total_price = -100.00  
        with self.assertRaises(ValidationError):
            self.cart_item.clean()  