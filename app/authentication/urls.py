from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import RegistrationViewSet, LoginViewSet
from ..user_profile.views import UserProfileViewSet

app_name = 'authentication'


class OptionalTrailingSlashRouter(SimpleRouter):
    def __init_(self, trailing_slash='/?'):
        self.trailing_slash = trailing_slash
        super().__init__()


router = OptionalTrailingSlashRouter()

# users
router.register('users', RegistrationViewSet, 'user')
router.register('profiles', UserProfileViewSet, 'profile')
router.register('login', LoginViewSet, 'login')


urlpatterns = [
    # path("login/", LoginViewSet.as_view({'post': 'post'}), name="login"),
]

urlpatterns += router.urls
