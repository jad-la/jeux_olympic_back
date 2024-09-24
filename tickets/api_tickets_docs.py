from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from .serializers import CartItemSerializer, BookingSerializer, CartSerializer, TicketSerializer
from .views import BookingCreateView,CartDetailView, TicketListView, CartItemCreateView, CartItemDeleteView

#Ajout des info pour l'endpoint /api/cart/items
@extend_schema(
    summary="Ajoute un article au panier",
    description="Permet aux utilisateurs authentifiés d'ajouter un article au panier en spécifiant l'ID de l'événement, l'offre et la quantité.",
    request=CartItemSerializer,
    responses={
        201: CartItemSerializer,
        401: OpenApiResponse(description="Utilisateur non authentifié"),
    }
)
class CustomCartItemCreateView(CartItemCreateView):
    pass


#Ajout des info pour l'endpoint /api/cart/
@extend_schema(
    summary="Récupère le panier de l'utilisateur authentifié",
    description="Permet aux utilisateurs authentifiés de voir les articles dans leur panier.",
    responses={
        200: CartSerializer,
        401: OpenApiResponse(description="Utilisateur non authentifié"),
        404: OpenApiResponse(description="Panier non trouvé"),
    }
)
class CustomCartDetailView(CartDetailView):
    pass


#Ajout des info pour l'endpoint /api/cart/items/{id}
@extend_schema(
    summary="Supprime un article du panier",
    description="Permet à l'utilisateur connecté de supprimer un article spécifique de son panier en fournissant l'ID de l'article.",
    responses={
        200: OpenApiResponse(description="Article supprimé."),
        404: OpenApiResponse(description="Article non trouvé."),
        401: OpenApiResponse(description="Utilisateur non authentifié."),
    },
    examples=[
        OpenApiExample(
            name="Suppression réussie",
            value={"detail": "Article supprimé."},
            response_only=True,
            status_codes=["200"],
        ),
        OpenApiExample(
            name="Article non trouvé",
            value={"detail": "Article non trouvé."},
            response_only=True,
            status_codes=["404"],
        )
    ]
)
class CustomCartItemDeleteView(CartItemDeleteView):
    pass


#Ajout des info pour l'endpoint /api/bookings/
@extend_schema(
    summary="Crée une réservation",
    description="Permet à un utilisateur connecté de finaliser une réservation en payant, et la réservation va génèrer des billets en fonction des articles du panier.",
    request=BookingSerializer,
    responses={
        201: BookingSerializer,
        400: BookingSerializer,
        401: BookingSerializer,
    },
    examples=[
        OpenApiExample(
            "Réponse succès",
            value={
                "id": 10,
                "user": 5,
                "total_price": "250.00",
                "booking_date": "2024-09-22T14:00:00Z"
            },
            response_only=True,
            status_codes=["201"],
        ),
        OpenApiExample(
            "Echec",
            value={"Detail":"Votre panier est vide. Vous ne pouvez pas faire de réservation sans articles."},
            response_only=True,
            status_codes=["400"],
        ),
         OpenApiExample(
            "Echec",
            value={"Detail": "Informations d'authentification non fournies."},
            response_only=True,
            status_codes=["401"],
        ),
    ]
)
class CustomBookingCreateView(BookingCreateView):
    pass


#Ajout des info pour l'endpoint /api/tickets/
@extend_schema(
    summary="Récupère les billets de l'utilisateur",
    description="Permet à l'utilisateur connecté de récupérer la liste des billets validés et leur QRcode",
    responses={
        201: TicketSerializer,
        401: TicketSerializer
    },
    examples=[
        OpenApiExample(
            "Echec",
            value={"Informations d'authentification non fournies."},
            response_only=True,
            status_codes=["401"],
        ),
    ]
)
class CustomTicketListView(TicketListView):
    pass