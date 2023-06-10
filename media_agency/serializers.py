from rest_framework import serializers

from media_agency.models import MediaAgency


class MediaAgencyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAgency
        fields = ['company_name', 'tin_number', 'user']


class MediaAgencyGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAgency
        fields = '__all__'
