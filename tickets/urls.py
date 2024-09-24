from django.urls import path
from .api_tickets_docs import (
    CustomCartItemCreateView, 
    CustomCartDetailView, 
    CustomTicketListView, 
    CustomBookingCreateView, 
    CustomCartItemDeleteView  
)

urlpatterns = [
    # Ajouter un article au panier
    path('cart/items/', CustomCartItemCreateView.as_view(), name='cart-item-create'),

    # Voir le contenu du panier
    path('cart/', CustomCartDetailView.as_view(), name='cart-detail'),

    #Supprimer un article du panier
    path('cart/items/<int:pk>/', CustomCartItemDeleteView.as_view(), name='cart-item-delete'),

    # Valider le panier et créer une réservation
    path('bookings/', CustomBookingCreateView.as_view(), name='booking-create'),

    # Récupérer les tickets générés
    path('tickets/', CustomTicketListView.as_view(), name='ticket-list'),
]