from django.db import models
from media_agency.models import MediaAgency
# Create your models here.


class Agency(models.Model):
    media_agency_id = models.ForeignKey(
        MediaAgency, on_delete=models.CASCADE, default=None)
    peak_hour = models.DecimalField(max_digits=10, decimal_places=2)
    normal = models.DecimalField(max_digits=10, decimal_places=2)
    production = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=1000)
    latitude = models.FloatField()
    longitude = models.FloatField()
    channel_name = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.user_id
