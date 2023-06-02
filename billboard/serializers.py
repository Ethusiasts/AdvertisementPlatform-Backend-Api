from rest_framework import serializers

from billboard.models import Billboard


class BillboardSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()

    class Meta:
        model = Billboard
        fields = ['id', 'daily_rate_per_sq', 'latitude', 'longitude', 'image', 'width', 'height',
                  'media_agency_id', 'approved', 'production', 'paid', 'status', 'description', 'average_rating']
