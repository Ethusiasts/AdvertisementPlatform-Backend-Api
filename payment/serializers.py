from rest_framework import serializers
from billboard.models import Billboard
from payment.models import Payment
from user.models import User


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False
    )
    billboard = serializers.PrimaryKeyRelatedField(
        queryset=Billboard.objects.all(),
        required=False
    )

    class Meta:
        model = Payment
        fields = ['first_name', 'last_name', 'email',
                  'amount', 'tx_ref', 'user', 'billboard']

    def create(self, validated_data):
        tx_ref = validated_data.get('tx_ref')
        user_id, billboard_id, date_time = tx_ref.split('/')
        validated_data['user_id'] = User.objects.get(pk=user_id)
        validated_data['billboard_id'] = Billboard.objects.get(pk=billboard_id)
        return super().create(validated_data)
