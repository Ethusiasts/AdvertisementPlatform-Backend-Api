from rest_framework import serializers
from contract.models import Contract
from media_agency.serializers import MediaAgencySerializer
from proposal.serializers import ProposalSerializer
from user.serializers import UserSerializer


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class ContractDetailSerializer(serializers.ModelSerializer):
    proposal_id = ProposalSerializer()
    user_id = UserSerializer()
    media_agency_id = MediaAgencySerializer()

    class Meta:
        model = Contract
        fields = '__all__'
