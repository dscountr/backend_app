from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from .models import User
from firebase_admin import auth
from phonenumber_field.serializerfields import PhoneNumberField
from ..user_profile.models import Profile


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)
    phone_number = PhoneNumberField(
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='User with this Phone Number already exists.',
                            )],)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'token',
                  'phone_number', 'date_of_birth', 'gender']

    def create(self, validated_data):
        return User.objects.createuser(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(
        max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, data):
        email = data.get('email')
        password = data.get('password')

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }
