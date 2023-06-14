from rest_framework import serializers

from agency.models import Agency
from django.db.models import Avg


class AgencyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['peak_hour', 'normal', 'production',
                  'image', 'channel_name', 'media_agency_id']


class AgencyRatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Agency
        fields = ['id', 'peak_hour', 'image', 'normal', 'production',
                  'media_agency_id', 'channel_name', 'created_at', 'average_rating']

    def get_average_rating(self, obj):
        average = obj.ratings.filter(entity_type="Agency").aggregate(
            avg_rating=Avg('rating'))['avg_rating']
        return average if average is not None else 0


class AgencySearchSerializer(serializers.ModelSerializer):
    average_rating = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Agency
        fields = '__all__'
