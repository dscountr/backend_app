from rest_framework import serializers


from .models import Profile
from ..authentication.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for getting user profile
    """
    email = serializers.ReadOnlyField(source='user.email')
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'first_name',
                  'last_name', 'full_name', 'email']

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
