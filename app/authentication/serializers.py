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
from .backends import JWTAuthentication


class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='User with this Phone Number already exists.',
                            )],)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email',
                  'phone_number', 'date_of_birth', 'gender']

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def create(self, validated_data):
        return User.objects.createuser(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    email = serializers.CharField(max_length=255, read_only=True)
    token = serializers.SerializerMethodField()
    first_name = serializers.CharField(max_length=50, read_only=True)
    last_name = serializers.CharField(max_length=50, read_only=True)

    def get_token(self, obj):
        token = JWTAuthentication.generate_token(self, obj.pk)
        return token

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'token']


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    class Meta:
        model = User
        fields = ['id', 'email']

        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop('password')

        for (key, value) in validated_data.items():

            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
