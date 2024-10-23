from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer  




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
 

