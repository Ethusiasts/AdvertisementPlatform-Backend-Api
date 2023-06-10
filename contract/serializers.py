from rest_framework import serializers
from contract.models import Contract
from media_agency.serializers import MediaAgencyGetSerializer
from proposal.serializers import ProposalGetSerializer
from user.serializers import UserGetSerializer


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class ContractDetailSerializer(serializers.ModelSerializer):
    proposal_id = ProposalGetSerializer()
    user_id = UserGetSerializer()
    media_agency_id = MediaAgencyGetSerializer()

    class Meta:
        model = Contract
        fields = '__all__'
