from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .serializers import (RegistrationSerializer, LoginSerializer)
from . import models
from ..filters import UserFilter


class RegistrationViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    queryset = models.User.objects.all()
    http_method_names = ['post']


class LoginViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    queryset = models.User.objects.all()
    filterset_class = UserFilter
    http_method_names = ['get', ]

    # def get_object(self):
    #     print(self.kwargs)
    #     user = self.request.user
    #     pn = models.User.objects.filter(email=user)
    #     print(pn)
    #     queryset = models.User.objects.filter(
    #         id=2999, phone_number__startswith='+')
    #     print('<><><><>', queryset)
    #     obj = get_object_or_404(queryset, id=self.kwargs["pk"])
    #     return obj


class UserViewSet(ModelViewSet):
    permission_classes = (IsAdminUser, IsAuthenticated)
    serializer_class = RegistrationSerializer
    queryset = models.User.objects.all()
    http_method_names = ['post', 'get', 'patch']
