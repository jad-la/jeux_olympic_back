from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import CartItem, Cart, Ticket
from .serializers import CartItemSerializer, BookingSerializer, CartSerializer, TicketSerializer


class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    # Enregistre l'article en l'associant au panier de l'utilisateur
    def get_serializer_context(self):
        context = super().get_serializer_context()
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        return context

    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    #récupère le panier de l'utilisateur connecté
    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    # Crée une réservation et génère les billets
    def perform_create(self, serializer):
       serializer.save(user=self.request.user) 
       return Response(serializer.data, status=status.HTTP_201_CREATED)


class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    # Retourner les tickets de l'utilisateur connecté
    def get_queryset(self):
        return Ticket.objects.filter(booking__user=self.request.user)


class CartItemDeleteView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    # On ne supprime que les articles du panier appartenant à l'utilisateur connecté
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'detail': 'Article supprimé.'}, status=status.HTTP_200_OK)
        except Http404:
            return Response({'detail': 'Article non trouvé.'}, status=status.HTTP_404_NOT_FOUND)