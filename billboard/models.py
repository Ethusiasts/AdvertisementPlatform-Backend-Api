from django.db import models

from landowner.models import Landowner


# Create your models here.


class Billboard(models.Model):
    rate = models.DecimalField(
        decimal_places=2, default=0.0, max_digits=15)
    location = models.CharField(max_length=128)
    image = models.ImageField()
    width = models.IntegerField()
    height = models.IntegerField()
    landowner_id = models.ForeignKey(
        Landowner, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    production = models.BooleanField(default=False)
