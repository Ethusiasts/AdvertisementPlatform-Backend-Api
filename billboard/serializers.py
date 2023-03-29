from rest_framework import serializers

from billboard.models import Billboard


class BillboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billboard
        fields = '__all__'
