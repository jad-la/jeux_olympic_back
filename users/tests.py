from django.test import TestCase
from users.models import CustomUser
from django.core.exceptions import ValidationError



class CustomUserModelTest(TestCase):
    #test avec un email valide
    def test_create_user_with_valid_email(self):
        user = CustomUser(
            email='user@example.com',
            first_name='Thoma',
            last_name='Dupont',
            role='user',
            security_key='so2567Ee678key'
        )
        try:
            user.clean()  
        except ValidationError:
            self.fail('La validation de l\'email a échoué pour un email valide.')


    # test aevc un email invalide
    def test_create_user_with_invalid_email(self):
        user = CustomUser(
            email='userexample.com',  
            first_name='Thoma',
            last_name='Dupont',
            role='user',
            security_key='so2567Ee678key'
        )
        with self.assertRaises(ValidationError):
            user.clean()  

    def test_create_user_with_invalid_role(self):
        user = CustomUser(
            email='user@example.com',
            first_name='thoma',
            last_name='Dupont',
            role='testeur', 
            security_key='so2567Ee678key'
        )
        with self.assertRaises(ValidationError):
            user.clean()  