import json
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from .models import User
from firebase_admin import auth
from phonenumber_field.serializerfields import PhoneNumberField
from ..user_profile.models import Profile
from ..auth_backend import PasswordlessAuthBackend
from decouple import config


class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='User with this Phone Number already exists.',
                            )],)

    class Meta:
        model = User
        fields = ['id', 'email', 'username',
                  'phone_number', 'date_of_birth', 'gender']

    def create(self, validated_data):
        return User.objects.createuser(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    email = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'token']
