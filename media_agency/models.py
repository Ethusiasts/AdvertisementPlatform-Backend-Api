from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from user.models import User

# Create your models here.


class MediaAgency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    company_name = models.CharField(max_length=50)
    tin_number = models.CharField(max_length=9)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name
