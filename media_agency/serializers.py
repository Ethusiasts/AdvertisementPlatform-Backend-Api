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


class MediaAgencyStatsSerializer(serializers.Serializer):
    total_billboards = serializers.IntegerField()
    total_contracts = serializers.IntegerField()
    total_proposals = serializers.IntegerField()

    def get_total_billboards(self, obj):
        return obj.get('total_billboards')

    def get_total_contracts(self, obj):
        return obj.get('total_contracts')

    def get_total_proposals(self, obj):
        return obj.get('total_proposals')
