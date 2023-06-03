from rest_framework import serializers
from advertisement.serializers import AdvertisementSerializer
from billboard.serializers import BillboardSerializer
from media_agency.serializers import MediaAgencySerializer
from proposal.models import Proposal
from user.serializers import UserSerializer


class ProposalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proposal
        fields = '__all__'


class ProposalDetailSerializer(serializers.ModelSerializer):
    billboard_id = BillboardSerializer()
    user_id = UserSerializer()
    media_agency_id = MediaAgencySerializer()
    advertisement_id = AdvertisementSerializer()

    class Meta:
        model = Proposal
        fields = '__all__'
