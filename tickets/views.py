from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CartItem, Cart, Event, Ticket
from .serializers import CartItemSerializer, BookingSerializer, CartSerializer, TicketSerializer

class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    # Enregistre l'article en l'associant au panier de l'utilisateur
    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)

        serializer.save(cart=cart)

class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    #récupère le panier de l'utilisateur connecté
    def get_object(self):
        return Cart.objects.get(user=self.request.user)


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    # Crée une réservation et génère les billets
    def perform_create(self, serializer):
       serializer.save(user=self.request.user) 

class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    # Retourner les tickets de l'utilisateur connecté
    def get_queryset(self):
        return Ticket.objects.filter(booking__user=self.request.user)
