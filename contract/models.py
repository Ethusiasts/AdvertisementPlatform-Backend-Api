from django.db import models
from media_agency.models import MediaAgency

from proposal.models import Proposal
from user.models import User

# Create your models here.


class Contract(models.Model):
    proposal_id = models.ForeignKey(
        Proposal, on_delete=models.CASCADE, default=None)
    media_agency_id = models.ForeignKey(
        MediaAgency, on_delete=models.CASCADE, default=None)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_signature = models.ImageField()
    agency_signature = models.ImageField()
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)
    gross_total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    net_free = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.proposal_id
