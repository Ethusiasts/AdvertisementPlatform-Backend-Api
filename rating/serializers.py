from rest_framework import serializers

from rating.models import Rating


class RatingPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rating', 'comment', 'entity_type',
                  'user_id', 'agency_id', 'billboard_id']


class RatingGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
