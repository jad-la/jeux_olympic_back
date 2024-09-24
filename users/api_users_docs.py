from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import register_user as original_register_user
from .serializers import RegisterSerializer


#Ajout des info pour l'endpoint /api/users/register dans la doc Swagger
register_user_decorator = extend_schema(
    summary="Enregistrement d'un utilisateur",
    description="Permet de créer un compte utilisateur avec email, nom, prénom et mot de passe.",
    request=RegisterSerializer,  
    responses={
        200: RegisterSerializer,  
        400: OpenApiResponse(description='Bad Request') 
    },
    examples=[
        OpenApiExample(
            'Exemple de requête',
            request_only=True,  
            value={
                "email": "test@example.com",
                "first_name": "Nom",
                "last_name": "Prenom",
                "password": "Password123",
                "password2": "Password123"
            }
        )
    ]
)(original_register_user)


#Ajout des info pour l'endpoint /api/users/login
@extend_schema(
    summary="Connexion de l'utilisateur",
    description="Permet à un utilisateur de se connecter en fournissant un email et un mot de passe.",
    request=TokenObtainPairSerializer,
    responses={
        200: TokenObtainPairSerializer,
        400: OpenApiResponse(description="Ce champ ne peut être vide."),
        401: OpenApiResponse(description='Unauthorized - Aucun compte actif n\'a été trouvé ')
    }
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


