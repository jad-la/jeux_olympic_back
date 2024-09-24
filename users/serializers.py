from rest_framework import serializers
from .models import CustomUser  
from django.contrib.auth.password_validation import validate_password  

# validation et la création d'un nouvel utilisateur lors de l'inscription
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password]) 
    password2 = serializers.CharField(write_only=True, required=True) 

    class Meta:
        model = CustomUser  
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')  

    # vérifier si les deux mots de passe correspondent
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."}) 
        return attrs  

    # création d'un nouvel utilisateur dans la base de données après validation des données
    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])  
        user.save() 
        return user 
    
