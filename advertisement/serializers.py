from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Advertisement, ImageChecker


class AdvertisementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = '__all__'


class ImageCheckerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageChecker
        fields = ['image']
