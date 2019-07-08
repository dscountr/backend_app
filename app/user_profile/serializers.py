from rest_framework import serializers

from .models import Profile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for getting user profile
    """
    username = serializers.ReadOnlyField(source='fetch_username')
    first_name = serializers.CharField(
        allow_blank=True, required=False, min_length=1, max_length=50)
    last_name = serializers.CharField(
        allow_blank=True, required=False, min_length=1, max_length=50)

    class Meta:
        model = Profile
        fields = ['username', 'id', 'first_name', 'last_name']
