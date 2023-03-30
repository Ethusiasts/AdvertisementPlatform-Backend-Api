from rest_framework import serializers

from landowner.models import Landowner


class LandownerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landowner
        fields = '__all__'
