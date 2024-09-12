from django.urls import path
from .views import (
    CartItemCreateView,
    CartDetailView,
    BookingCreateView,
    TicketListView
)

urlpatterns = [
    # Ajouter un article au panier
    path('cart/items/', CartItemCreateView.as_view(), name='cart-item-create'),

    # Voir le contenu du panier
    path('cart/', CartDetailView.as_view(), name='cart-detail'),

    # Valider le panier et créer une réservation
    path('bookings/', BookingCreateView.as_view(), name='booking-create'),

    # Récupérer les tickets générés
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
]