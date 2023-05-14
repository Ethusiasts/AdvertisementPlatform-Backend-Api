from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from media_agency.models import MediaAgency


# Create your models here.


class Billboard(models.Model):
    rate = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    location = models.CharField(max_length=128)
    image = models.ImageField()
    width = models.IntegerField()
    height = models.IntegerField()
    media_agency_id = models.ForeignKey(
        MediaAgency, on_delete=models.CASCADE, default=None)
    approved = models.BooleanField(default=False)
    production = models.BooleanField(default=False)

    def __str__(self):
        return self.location
