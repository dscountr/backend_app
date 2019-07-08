from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.core.exceptions import ValidationError
from decouple import config
from phonenumber_field.modelfields import PhoneNumberField
from firebase_admin import auth
from .choices import GENDER_CHOICES


class UserManager(BaseUserManager):
    use_in_migrations = True

    def createuser(self, **fields):
        email = fields.pop('email')
        password = fields.get('password')

        if not email:
            raise ValueError("Email address is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **fields):
        """
        Create and return a `User` with superuser (admin) permissions.
        """

        user = self.createuser(**fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    phone_number = PhoneNumberField(db_index=True, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # The `USERNAME_FIELD` property specifies the log in field.
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email', 'date_of_birth', ]

    # the UserManager class should manage objects of this type.
    objects = UserManager()

    class Meta:
        verbose_name_plural = "All Users"

    def __str__(self):
        """
        Returns a string representation of this `User`.
        used when a `User` is printed in the console.
        """
        return self.email

    @property
    def token(self):
        """
        method allows us to get a user's token
        """
        return self._generate_firebase_token()

    def _generate_firebase_token(self):
        """
        Generates a firebase token
        """
        uid = 'some-uid'
        token = auth.create_custom_token(uid)

        return token.decode('utf-8')
