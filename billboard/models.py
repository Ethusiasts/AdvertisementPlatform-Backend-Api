from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from media_agency.models import MediaAgency


# Create your models here.


class Billboard(models.Model):
    STATUS_CHOICES = [
        ('Free', 'Free'),
        ('Occupied', 'Occupied'),
    ]

    rate = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    monthly_rate_per_sq = models.DecimalField(
        max_digits=8, decimal_places=2, default=0)
    location = models.CharField(max_length=128)
    image = models.URLField()
    width = models.IntegerField()
    height = models.IntegerField()
    media_agency_id = models.ForeignKey(
        MediaAgency, on_delete=models.CASCADE, default=None)
    approved = models.BooleanField(default=False)
    production = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default=None)

    def __str__(self):
        return self.location
