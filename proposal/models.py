from django.db import models
from advertisement.models import Advertisement
from billboard.models import Billboard
from user.models import User
from billboard.models import Billboard

# Create your models here.


class Proposal(models.Model):
    name = models.CharField(max_length=128)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    billBoard_id = models.ForeignKey(
        Billboard, on_delete=models.CASCADE, default=None)
    advertisement_id = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE)
    description = models.TextField()
    total_price = models.DecimalField(
        decimal_places=2, default=0.0, max_digits=15,)
    approved = models.BooleanField(default=False)
