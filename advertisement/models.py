from django.db import models
from user.models import User
from django.utils import timezone
from user.models import User


# Create your models here.


def user_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'advertisement_user_{0}/{1}'.format(instance.user.id, filename)


class Advertisement(models.Model):
    advertisement_name = models.CharField(max_length=50)
    advertisement_type = models.CharField(max_length=50)
    duration_in_hour = models.DecimalField(
        decimal_places=2, default=0.0, max_digits=15,)
    width = models.DecimalField(decimal_places=2, default=0.0, max_digits=15,)
    height = models.DecimalField(decimal_places=2, default=0.0, max_digits=15,)
    quantity = models.IntegerField(default=0.0)
    advertisement_file = models.URLField(default=None, max_length=500)
    approved = models.BooleanField(default=False)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(default=timezone.now)


class ImageChecker(models.Model):
    image = models.ImageField()
