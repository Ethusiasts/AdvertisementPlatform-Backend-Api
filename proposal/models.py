from django.db import models
from advertisement.models import Advertisement
from customer.models import Customer

# Create your models here.


class Proposal(models.Model):
    name = models.CharField(max_length=128)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    asvertisement_id = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE)
    description = models.TextField()
