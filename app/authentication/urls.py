from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from ..user_profile.views import UserProfileViewSet
from .views import LoginViewSet, RegistrationViewSet, UpdateUserViewSet

app_name = "authentication"


class OptionalTrailingSlashRouter(SimpleRouter):
    def __init_(self, trailing_slash="/?"):
        self.trailing_slash = trailing_slash
        super().__init__()


router = OptionalTrailingSlashRouter()

# users
router.register("users", RegistrationViewSet, "users")
router.register("profiles", UserProfileViewSet, "profile")
router.register("login", LoginViewSet, "login")
router.register("user", UpdateUserViewSet, "user")


urlpatterns = [
    # path("login/", LoginViewSet.as_view({'post': 'post'}), name="login"),
]

urlpatterns += router.urls
