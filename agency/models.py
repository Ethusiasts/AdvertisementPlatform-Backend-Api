from django.db import models

from user.models import User

# Create your models here.


class Agency(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    peak_hour = models.DecimalField()
    normal = models.DecimalField()
    production = models.DecimalField()
    with_out_production = models.DecimalField()

    def __str__(self):
        return self.user_id
