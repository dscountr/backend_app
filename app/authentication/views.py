from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .serializers import (RegistrationSerializer,)
from . import models


class RegistrationViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    queryset = models.User.objects.all()
    http_method_names = ['post']


class UserViewSet(ModelViewSet):
    permission_classes = (IsAdminUser, IsAuthenticated)
    serializer_class = RegistrationSerializer
    queryset = models.User.objects.all()
    http_method_names = ['post', 'get', 'patch']
