from rest_framework import serializers
from billboard.serializers import BillboardSerializer
from proposal.models import Proposal


class ProposalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proposal
        fields = '__all__'


class ProposalDetailSerializer(serializers.ModelSerializer):
    billboard_id = BillboardSerializer()

    class Meta:
        model = Proposal
        fields = '__all__'
