from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Advertisement


class AdvertisementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = '__all__'
