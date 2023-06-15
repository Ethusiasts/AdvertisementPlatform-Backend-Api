from rest_framework import serializers
from advertisement.serializers import AdvertisementGetSerializer
from agency.serializers import AgencyRatingSerializer
from billboard.serializers import BillboardGetSerializer
from media_agency.serializers import MediaAgencyGetSerializer
from proposal.models import Proposal
from user.serializers import UserGetSerializer


class AdminBlockUserSerializer(serializers.Serializer):
    is_blocked = serializers.BooleanField(default=False)

    def get_user(self, obj):
        return obj.get('is_blocked')


class AdminStatsSerializer(serializers.Serializer):
    total_user = serializers.IntegerField()
    total_landowner = serializers.IntegerField()
    total_tv = serializers.IntegerField()
    total_radio = serializers.IntegerField()
    total_employee = serializers.IntegerField()

    def get_total_user(self, obj):
        return obj.get('total_user')

    def get_total_landowner(self, obj):
        return obj.get('total_landowner')

    def get_total_tv(self, obj):
        return obj.get('total_tv')

    def get_total_radio(self, obj):
        return obj.get('total_radio')

    def get_total_employee(self, obj):
        return obj.get('total_employee')
