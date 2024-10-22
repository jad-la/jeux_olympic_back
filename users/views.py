from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer  
from .serializers import LoginSerializer



# gérer l'inscription d'un utilisateur avec une requête POST
@api_view(['POST'])
def register_user(request):
    # Sérialise les données
    serializer = RegisterSerializer(data=request.data)  
    
    #vérification et sauvegarde des donnée de l'utilisateur
    if serializer.is_valid():  
        serializer.save() 
        return Response({
            "message": "Utilisateur créé avec succès",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    #si echec reponse erreur
    return Response({
        "message": "Échec de la validation des données",
        "erreurs": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
 

# gérer la connexion de l'utilisateur
@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    
    # Validation et récupération des données d'utlisateur
    if serializer.is_valid():
        user = serializer.get_user()    
        return Response({
            "message": "Connexion réussie",
            "user": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }, status=status.HTTP_200_OK)
    
     #si echec reponse erreur
    return Response({
        "message": "Échec de la connexion",
        "erreurs": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)