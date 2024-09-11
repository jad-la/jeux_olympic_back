import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.forms import ValidationError
from django.core.validators import validate_email


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    security_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    # gestion d'erreur pour l'email
    def clean(self):
        try:
            validate_email(self.email)
        except ValidationError:
            raise ValidationError("L'adresse email n'est pas valide.")

    def save(self, *args, **kwargs):
        if not self.security_key:
            self.security_key = str(uuid.uuid4())
        super().save(*args, **kwargs)


    def has_perm(self, perm, obj=None):
      return self.is_superuser  

    def has_module_perms(self, app_label):
      return self.is_superuser