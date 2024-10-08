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
        return Response(serializer.data, status=status.HTTP_201_CREATED)  
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 

