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


class MediaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    daily_rate_per_sq = serializers.DecimalField(
        max_digits=8, decimal_places=2)
    image = serializers.URLField(max_length=1000)
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    media_agency_id = serializers.IntegerField()
    approved = serializers.IntegerField()
    production = serializers.DecimalField(max_digits=11, decimal_places=2)
    paid = serializers.BooleanField()
    status = serializers.CharField(max_length=8)
    description = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    created_at = serializers.DateTimeField()
    file = serializers.BooleanField()
    average_rating = serializers.FloatField()
    count = serializers.IntegerField()


class AdditionalFieldsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    peak_hour = serializers.DecimalField(max_digits=10, decimal_places=2)
    normal = serializers.DecimalField(max_digits=10, decimal_places=2)
    production = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.URLField()
    channel_name = serializers.CharField()
    media_agency_id = serializers.IntegerField()


class MultipleProposalSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    user_id = serializers.IntegerField()
    advertisement_id = serializers.IntegerField()
    production = serializers.BooleanField()

    def get_medias_serializer(self, instance):
        if "peak_hour" in instance:
            return AdditionalFieldsSerializer(instance=instance, many=True)
        else:
            return MediaSerializer(instance=instance, many=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        medias = representation.pop("medias")
        medias_serializer = self.get_medias_serializer(medias)
        representation["medias"] = medias_serializer.data
        return representation

    def create(self, validated_data):
        return super().create(validated_data)
