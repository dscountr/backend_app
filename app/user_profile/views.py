from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.viewsets import ModelViewSet

from ..firebase_auth import FirebaseTokenAuthentication
from .models import Profile
from .serializers import UserProfileSerializer


class UserProfileViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()
    http_method_names = ["get", "patch"]
