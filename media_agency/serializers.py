from rest_framework import serializers

from media_agency.models import MediaAgency


class MediaAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAgency
        fields = '__all__'
