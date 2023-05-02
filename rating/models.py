from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from agency.models import Agency
from billboard.models import Billboard
from user.models import User

# Create your models here.


class Rating(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, defaul=None)
    agency_id = models.ForeignKey(
        Agency, on_delete=models.CASCADE, defaul=None)
    billboard_id = models.ForeignKey(
        Billboard, on_delete=models.CASCADE, default=None)
    rating = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
