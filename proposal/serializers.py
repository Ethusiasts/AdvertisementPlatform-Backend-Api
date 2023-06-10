from rest_framework import serializers
from advertisement.serializers import AdvertisementGetSerializer
from billboard.serializers import BillboardGetSerializer
from media_agency.serializers import MediaAgencyGetSerializer
from proposal.models import Proposal
from user.serializers import UserSerializer


class ProposalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proposal
        fields = '__all__'


class ProposalDetailSerializer(serializers.ModelSerializer):
    billboard_id = BillboardGetSerializer()
    user_id = UserSerializer()
    media_agency_id = MediaAgencyGetSerializer()
    advertisement_id = AdvertisementGetSerializer()

    class Meta:
        model = Proposal
        fields = '__all__'
