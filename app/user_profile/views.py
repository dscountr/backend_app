from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from .serializers import (UserProfileSerializer,)
from . import models
from ..firebase_auth import FirebaseTokenAuthentication


class UserProfileViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserProfileSerializer
    authentication_classes = (FirebaseTokenAuthentication,)
    queryset = models.Profile.objects.all()
    http_method_names = ['get', 'patch']
