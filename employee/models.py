from django.db import models
from billboard.models import Billboard
from django.utils import timezone
from user.models import User
# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    billboard_id = models.ForeignKey(
        Billboard, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(default=timezone.now)
