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

    DEFAULT_LOGIN_DATA = \
            dict([(field, "") for field in LoginSerializer.Meta.fields])

    def list(self, request, *args, **kwargs):
        print(dir(request))
        print(args, kwargs, request.content_type, request.data, request.query_params)
        phone_number = request.query_params.get("phone_number", "")
        print(phone_number)
        if not phone_number:
            data = self.DEFAULT_LOGIN_DATA
        else:
            user = models.User.objects.get_by_natural_key(phone_number)
            data = LoginSerializer(user).data

        return Response(data)


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
