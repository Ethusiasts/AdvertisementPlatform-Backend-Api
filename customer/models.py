from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from user.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_sector = models.CharField(max_length=50)
