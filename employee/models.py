from django.db import models
from media_agency.models import MediaAgency

from user.models import User
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    media_agency_id = models.ForeignKey(
        MediaAgency, on_delete=models.CASCADE)
    task_metrics = models.IntegerField()
