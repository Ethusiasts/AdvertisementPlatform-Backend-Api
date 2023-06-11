from django.db import models

from billboard.models import Billboard
from user.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class Payment(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    billboard_id = models.ForeignKey(
        Billboard, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=50, default=None)
    last_name = models.CharField(max_length=50, default=None)
    email = models.EmailField()
    amount = models.DecimalField(
        max_digits=11, decimal_places=2, default=None)
    tx_ref = models.CharField(max_length=500, unique=True)
