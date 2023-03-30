from django.db import models
from landowner.models import Landowner

from user.models import User
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    landowners_id = models.ForeignKey(
        Landowner, on_delete=models.CASCADE)
    task_metrics = models.IntegerField()
