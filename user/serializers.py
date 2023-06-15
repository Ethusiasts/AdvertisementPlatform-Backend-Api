from rest_framework import serializers

from user.models import User, UserProfile


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'role', 'password']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password', None)
        return data


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role',
                  'is_verified', 'is_blocked', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = UserGetSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        return value


class UserStatsSerializer(serializers.Serializer):
    total_advertisements = serializers.IntegerField()
    total_contracts = serializers.IntegerField()
    total_proposals = serializers.IntegerField()

    def get_total_advertisements(self, obj):
        return obj.get('total_advertisements')

    def get_total_contracts(self, obj):
        return obj.get('total_contracts')

    def get_total_proposals(self, obj):
        return obj.get('total_proposals')
