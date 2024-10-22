from rest_framework import serializers
from .models import CustomUser  
from django.contrib.auth.password_validation import validate_password 
from django.core.validators import validate_email
from django.core.exceptions import ValidationError 
from django.contrib.auth import authenticate

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
    
    # Validation de l'email, vérifier si l'email est valide
    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("L'adresse email n'est pas valide.")
        
        # Vérifier si l'email est déjà utilisé
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("cet email existe déjà.")       
        return value
    
    # Validation du prénom etvdu nom 
    def validate_first_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Le prénom doit contenir au moins 2 caractères.")
        return value
    
    def validate_last_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Le nom doit contenir au moins 2 caractères.")
        return value

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
    

# validation et connexion d'utilisateur 
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        # Vérifier si l'email et le mot de passe sont corrects
        user = authenticate(email=data['email'], password=data['password'])
        
        if not user:
            raise serializers.ValidationError("Les informations de connexion sont incorrectes.")
          
        # sinon retourne les données validées 
        return data

    # pour obtenir l'utilisateur authentifié
    def get_user(self):
        email = self.validated_data['email']
        return CustomUser.objects.get(email=email)