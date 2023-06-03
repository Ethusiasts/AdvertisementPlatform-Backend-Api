from rest_framework import serializers

from billboard.models import Billboard
from django.db.models import Avg

from rating.models import Rating


class BillboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Billboard
        fields = '__all__'


class BillboardRatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Billboard
        fields = ['id', 'daily_rate_per_sq', 'image', 'width', 'height', 'media_agency_id', 'approved',
                  'production', 'paid', 'status', 'description', 'latitude', 'longitude', 'created_at', 'average_rating']

    def get_average_rating(self, obj):
        return obj.ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']


class BillboardSearchSerializer(serializers.ModelSerializer):
    average_rating = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Billboard
        fields = '__all__'
