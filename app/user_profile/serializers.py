from rest_framework import serializers

from ..authentication.models import User
from .models import Profile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for getting user profile
    """

    email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Profile
        fields = ["id", "email"]
