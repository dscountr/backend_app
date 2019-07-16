from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .serializers import (UserProfileSerializer,)
from .models import Profile
from ..firebase_auth import FirebaseTokenAuthentication


class UserProfileViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()
    http_method_names = ['get', 'patch']
