from rest_framework import serializers

from user.models import User, UserProfile


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'role', 'password']


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_verified']


class UserProfileSerializer(serializers.ModelSerializer):
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
