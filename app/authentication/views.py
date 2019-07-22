from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from ..filters import UserFilter
from . import models
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer


class RegistrationViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    queryset = models.User.objects.all()
    http_method_names = ["post", "get"]


class LoginViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    queryset = models.User.objects.all()
    filterset_class = UserFilter
    http_method_names = ["get"]

    DEFAULT_LOGIN_DATA = dict([(field, "") for field in LoginSerializer.Meta.fields])

    def list(self, request, *args, **kwargs):
        phone_number = request.query_params.get("phone_number", "")
        if not phone_number:
            data = self.DEFAULT_LOGIN_DATA
        else:
            user = models.User.objects.get_by_natural_key(phone_number)
            data = LoginSerializer(user).data

        return Response(data)


class UpdateUserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = models.User.objects.all()
    http_method_names = ["patch", "get"]
