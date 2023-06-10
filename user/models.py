from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from user.manage import CustomUserManager
from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField


# User model.
class User(AbstractBaseUser, PermissionsMixin):

    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(
        default=False)  # verify user through email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# User profile mode.
class UserProfile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default=None)
    last_name = models.CharField(max_length=50, default=None)
    username = models.CharField(max_length=50, default=None)
    profile_picture = models.URLField(default=None)
    phone_number = PhoneNumberField(default=None)

    def __str__(self):
        return self.user.email


class TokenGenerator():
    def _create_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token


user_reset_password_token = TokenGenerator()
