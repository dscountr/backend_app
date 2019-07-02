from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import RegistrationViewSet

app_name = 'authentication'


class OptionalTrailingSlashRouter(SimpleRouter):
    def __init_(self, trailing_slash='/?'):
        self.trailing_slash = trailing_slash
        super().__init__()


router = OptionalTrailingSlashRouter()
router.register('users', RegistrationViewSet, 'user')

urlpatterns = router.urls
