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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserProfile(AbstractBaseUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    profile_picture = models.ImageField()
    phone_number = PhoneNumberField()


class CustomerProfile(AbstractBaseUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_sector = models.CharField(max_length=50)


class LandownerProfile(AbstractBaseUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    company_name = models.CharField(max_length=50)
    tin_number = models.CharField(max_length=9)
    is_verified = models.BooleanField(default=False)


class EmployeeProfile(AbstractBaseUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    landowners_id = models.ForeignKey(
        LandownerProfile, on_delete=models.CASCADE)
    task_metrics = models.IntegerField()


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
