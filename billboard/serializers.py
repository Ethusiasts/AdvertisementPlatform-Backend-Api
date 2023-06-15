from rest_framework import serializers

from billboard.models import Billboard
from django.db.models import Avg

from rating.models import Rating


class BillboardPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Billboard
        fields = ['daily_rate_per_sq', 'image', 'width', 'height', 'production', 'status',
                  'description', 'latitude', 'longitude', 'media_agency_id', 'file']


class BillboardGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Billboard
        fields = '__all__'


class BillboardRatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Billboard
        fields = ['id', 'daily_rate_per_sq', 'image', 'width', 'height', 'media_agency_id', 'approved',
                  'production', 'paid', 'status', 'description', 'latitude', 'longitude', 'created_at', 'file', 'average_rating']

    def get_average_rating(self, obj):
        average = obj.ratings.filter(entity_type='Billboard').aggregate(
            avg_rating=Avg('rating'))['avg_rating']
        return average if average is not None else 0


class BillboardSearchSerializer(serializers.ModelSerializer):
    average_rating = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Billboard
        fields = '__all__'
