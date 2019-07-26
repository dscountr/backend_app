import json

from decouple import config
from django.contrib.auth import authenticate
from firebase_admin import auth
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..auth_backend import PasswordlessAuthBackend
from ..user_profile.models import Profile
from .backends import JWTAuthentication
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="User with this Phone Number already exists.",
            )
        ]
    )
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "date_of_birth",
            "gender",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def create(self, validated_data):
        return User.objects.createuser(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    email = serializers.CharField(max_length=255, read_only=True)
    token = serializers.SerializerMethodField()
    first_name = serializers.CharField(max_length=50, read_only=True)
    last_name = serializers.CharField(max_length=50, read_only=True)
    gender = serializers.CharField(max_length=50, read_only=True)
    date_of_birth = serializers.CharField(max_length=50, read_only=True)

    def get_token(self, obj):
        token = JWTAuthentication.generate_token(self, obj.pk)
        return token

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name",
                  "phone_number", "token", "gender", "date_of_birth"]


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "date_of_birth",
            "gender",
        ]

        read_only_fields = ("token",)

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        email = validated_data.pop("email")
        phone_number = validated_data.pop("phone_number")

        for (key, value) in validated_data.items():

            setattr(instance, key, value)

        instance.save()

        return instance
