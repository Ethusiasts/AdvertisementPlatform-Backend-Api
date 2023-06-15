from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Advertisement


class AdvertisementPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = ['advertisement_name', 'advertisement_type', 'duration_in_hour',
                  'width', 'height', 'quantity', 'advertisement_file', 'user_id']


class AdvertisementGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = '__all__'


class ImageCheckerSerializer(serializers.Serializer):
    image = serializers.CharField(max_length=100000)
