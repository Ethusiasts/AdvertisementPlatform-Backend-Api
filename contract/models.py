from django.db import models
from media_agency.models import MediaAgency
from django.utils import timezone
from proposal.models import Proposal
from user.models import User

# Create your models here.


class Contract(models.Model):
    proposal_id = models.ForeignKey(
        Proposal, on_delete=models.CASCADE, default=None)
    media_agency_id = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, related_name='media')
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    customer_signature = models.CharField(max_length=100000, null=True)
    agency_signature = models.CharField(max_length=100000)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)
    gross_total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    net_free = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.proposal_id
