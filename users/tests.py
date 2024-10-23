from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status



class CustomUserModelTest(TestCase):
 
    # test aevc un email invalide
    def test_create_user_with_invalid_email(self):
        with self.assertRaises(ValidationError):
            user = CustomUser(
                email='userexample.com',  
                first_name='Thoma',
                last_name='Dupont',
            )
            user.full_clean()

    # test création d'un utilisateur avec succès avec un clé de sécurité générée
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email='test1@example.com',
            first_name='Jean',
            last_name='Dupont',
            password='thepassword123'
        )
        self.assertEqual(user.email, 'test1@example.com')
        self.assertTrue(user.check_password('thepassword123'))
        self.assertIsNotNone(user.security_key)

class RegisterUserViewTest(APITestCase):
    # test les données avec des mots de passe non identiques si l'API renvoi le bon statut
    def test_register_with_password_mismatch(self):
        data = {
            'email': 'user1@example.com',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'password': 'thepassword123',
            'password2': 'thepassword124'
        }
        response = self.client.post(reverse('register_user'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
class TokenObtainPairSerializerTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='user3@example.com',
            first_name='Paul',
            last_name='Dupont',
            password='testpassword123'
        )

    # Test connexion avec des identifiants valides
    def test_login_success(self):
        data = {
            'email': 'user3@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  

    # Test de la connexion avec un mot de passe incorrect
    def test_login_with_wrong_password(self):
        data = {
            'email': 'user3@example.com',
            'password': 'password'
        }
        response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data) 

    # Test de la connexion avec un email incorrect
    def test_login_with_invalid_email(self):
        data = {
            'email': 'user@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)  
