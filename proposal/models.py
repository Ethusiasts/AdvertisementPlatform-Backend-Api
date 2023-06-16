from django.db import models
from advertisement.models import Advertisement
from agency.models import Agency
from billboard.models import Billboard
from media_agency.models import MediaAgency
from user.models import User
from billboard.models import Billboard
from django.utils import timezone
# Create your models here.


class Proposal(models.Model):
    APPROVAL_CHOICES = [
        (0, 0),
        (1, 1),
        (2, 2),
    ]
    ENTITY_CHOICES = [
        ('Billboard', 'Billboard'),
        ('Agency', 'Agency')
    ]

    name = models.CharField(max_length=128)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='proposal_user')
    agency_id = models.ForeignKey(
        Agency, on_delete=models.CASCADE, default=None, null=True, blank=True)
    billboard_id = models.ForeignKey(
        Billboard, on_delete=models.CASCADE, default=None, null=True, blank=True)
    media_agency_id = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, related_name='media_proposal')
    advertisement_id = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE)
    description = models.TextField()
    total_price = models.DecimalField(
        decimal_places=2, default=0.0, max_digits=15,)
    approved = models.PositiveIntegerField(choices=APPROVAL_CHOICES, default=1)
    production = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
