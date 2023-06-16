from rest_framework import serializers
from contract.models import Contract
from media_agency.serializers import MediaAgencyGetSerializer
from proposal.serializers import ProposalGetSerializer
from user.serializers import UserGetSerializer


class ContractPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['proposal_id', 'media_agency_id', 'user_id', 'customer_signature',
                  'agency_signature', 'total_tax', 'gross_total_fee', 'net_free']


class ContractGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class ContractDetailSerializer(serializers.ModelSerializer):
    proposal_id = ProposalGetSerializer()
    user_id = UserGetSerializer()
    media_agency_id = UserGetSerializer()

    class Meta:
        model = Contract
        fields = '__all__'
