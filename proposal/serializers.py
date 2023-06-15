from rest_framework import serializers
from advertisement.serializers import AdvertisementGetSerializer
from agency.serializers import AgencyRatingSerializer
from billboard.serializers import BillboardGetSerializer
from media_agency.serializers import MediaAgencyGetSerializer
from proposal.models import Proposal
from user.serializers import UserGetSerializer


class ProposalPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proposal
        fields = ['name', 'description', 'total_price', 'user_id',
                  'billboard_id', 'agency_id', 'media_agency_id', 'advertisement_id', 'production']


class ProposalGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proposal
        fields = '__all__'


class ProposalDetailSerializer(serializers.ModelSerializer):
    billboard_id = BillboardGetSerializer()
    user_id = UserGetSerializer()
    media_agency_id = MediaAgencyGetSerializer()
    advertisement_id = AdvertisementGetSerializer()
    agency_id = AgencyRatingSerializer()

    class Meta:
        model = Proposal
        fields = '__all__'
