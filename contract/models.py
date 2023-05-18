from django.db import models
from agency.models import Agency

from proposal.models import Proposal

# Create your models here.


class Contract(models.Model):
    proposal_id = models.ForeignKey(
        Proposal, on_delete=models.CASCADE, default=None)
    agency_id = models.ForeignKey(
        Agency, on_delete=models.CASCADE, default=None)
    customer_signature = models.ImageField()
    agency_signature = models.ImageField()
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)
    gross_total_tax = models.DecimalField(max_digits=10, decimal_places=2)
    net_free = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.proposal_id
