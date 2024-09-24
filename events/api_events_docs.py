from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.views import SpectacularAPIView
from events.serializers import SportSerializer, EventSerializer
from .views import sport_details as original_sport_details, list_sports as original_list_sports


#Ajout des info pour l'endpoint /api/sports
sport_details_decorator = extend_schema(
    summary="Récuperation des catégories de sport",
        description="Permet de récuperer la liste des sports disponible.",
        request=SportSerializer,
        responses={
        200: SportSerializer,  
        400: OpenApiResponse(description='Bad Request') 
    }
)(original_list_sports)

#Ajout des info pour l'endpoint /api/sports/id/events
sport_details = extend_schema(
    summary="Récupération des événements d'un sport choisi",
    description="Permet de récupérer la liste des événements associés à un sport en fonction de l'ID du sport.",
    responses={
        200: EventSerializer(many=True),  
        404: OpenApiResponse(description="Aucun sport trouvé")
    }
)(original_sport_details)

@extend_schema(exclude=True)
class CustomSpectacularAPIView(SpectacularAPIView):
    pass