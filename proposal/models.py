from django.db import models
from advertisement.models import Advertisement
from user.models import User

# Create your models here.


class Proposal(models.Model):
    name = models.CharField(max_length=128)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    advertisement_id = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE)
    description = models.TextField()
