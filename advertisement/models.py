from django.db import models
from django.db.models import Q


# Create your models here.


def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'advertisement_user_{0}/{1}'.format(instance.user.id, filename)


class Advertisement(models.Model):

    advertisement_type = models.CharField(max_length=50)
    billBoard_id_or_agency_name = models.CharField(max_length=50)
    duration_in_hour = models.DecimalField(
        decimal_places=2, default=0.0, max_digits=15,)
    width = models.DecimalField(decimal_places=2, default=0.0, max_digits=15,)
    height = models.DecimalField(decimal_places=2, default=0.0, max_digits=15,)
    quantity = models.IntegerField(default=0.0)
    advertisement_file = models.FileField(blank=True, null=True)
    total_price = models.DecimalField(
        decimal_places=2, default=0.0, max_digits=15,)
    approved = models.BooleanField(default=False)
    # customer = models.ForeignKey(
    #     User, default=1, null=True, on_delete=models.SET_NULL)
