from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from app.manage import CustomUserManager
from rest_framework.authtoken.models import Token
# User model.


class User(AbstractBaseUser, PermissionsMixin):

    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class TokenGenerator():
    def _create_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token


user_reset_password_token = TokenGenerator()


'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField()
    image = models.ImageField(null=True, blank=True)
'''
