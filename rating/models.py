from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from agency.models import Agency
from billboard.models import Billboard
from user.models import User

# Create your models here.


class Rating(models.Model):
    ENTITY_CHOICES = [
        ('Billboard', 'Billboard'),
        ('Agency', 'Agency')
    ]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    agency_id = models.ForeignKey(
        Agency, on_delete=models.CASCADE, default=None, null=True, blank=True)
    billboard_id = models.ForeignKey(
        Billboard, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='ratings')
    rating = models.DecimalField(decimal_places=2, max_digits=10,
                                 validators=[MinValueValidator(0), MaxValueValidator(5)], default=0.00)
    comment = models.CharField(max_length=128, default=None)
    entity_type = models.CharField(
        max_length=9, choices=ENTITY_CHOICES, default='Billboard')
