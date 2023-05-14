from django.db import models

from user.models import User

# Create your models here.


class Agency(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    peak_hour = models.DecimalField(max_digits=10, decimal_places=2)
    normal = models.DecimalField(max_digits=10, decimal_places=2)
    production = models.DecimalField(max_digits=10, decimal_places=2)
    with_out_production = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user_id
