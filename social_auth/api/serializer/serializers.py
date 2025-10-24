from rest_framework import serializers
from ...models import User, SocialAccount
from django.utils import timezone

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ('id', 'provider', 'uid', 'extra_data')


class UserProfileSerializer(serializers.ModelSerializer):
    social_accounts = SocialAccountSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'name',
            'phone', 'profile_image', 'gender',
            'description', 'date_joined', 'social_accounts'
        )
        read_only_fields = ('id', 'email', 'date_joined', 'social_accounts')
