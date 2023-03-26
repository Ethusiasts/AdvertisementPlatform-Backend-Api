from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Advertisement


class AdvertisementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = [
            'id',
            'advertisement_type',
            'billBoard_id_or_agency_name',
            'duration_in_hour',
            'width',
            'height',
            'quantity',
            'advertisement_file'
        ]
