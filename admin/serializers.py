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
