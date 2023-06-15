from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from media_agency.models import MediaAgency
from django.utils import timezone


# Create your models here.


class Billboard(models.Model):
    STATUS_CHOICES = [
        ('Free', 'Free'),
        ('Occupied', 'Occupied'),
    ]

    APPROVAL_CHOICES = [
        (0, 0),
        (1, 1),
        (2, 2),
    ]

    daily_rate_per_sq = models.DecimalField(
        max_digits=8, decimal_places=2, default=0)
    image = models.URLField(max_length=1000)
    width = models.IntegerField()
    height = models.IntegerField()
    media_agency_id = models.ForeignKey(
        MediaAgency, on_delete=models.CASCADE, default=None)
    approved = models.PositiveIntegerField(choices=APPROVAL_CHOICES, default=1)
    production = models.DecimalField(
        max_digits=11, decimal_places=2, default=None)
    paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default=None)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    file = models.URLField(default='')
    adult_content = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description
