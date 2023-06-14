from rest_framework import serializers

from rating.models import Rating


class RatingPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class RatingGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
