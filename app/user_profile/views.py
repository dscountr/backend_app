from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from .serializers import (UserProfileSerializer,)
from . import models
from ..firebase_auth import FirebaseTokenAuthentication


class UserProfileViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserProfileSerializer
    authentication_classes = (FirebaseTokenAuthentication,)
    queryset = models.Profile.objects.all()
    http_method_names = ['get', 'patch']
