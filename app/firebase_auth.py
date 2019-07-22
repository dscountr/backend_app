import logging

from decouple import config
from django.contrib.auth import get_user_model
from firebase_admin import auth, credentials, initialize_app
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

private_key = config("PRIVATE_KEY").replace("\\n", "\n")
payload = {
    "type": "service_account",
    "project_id": config("PROJECT_ID"),
    "private_key": private_key,
    "client_email": config("CLIENT_EMAIL"),
    "token_uri": "https://oauth2.googleapis.com/token",
}

cred = credentials.Certificate(payload)
initialize_app(cred)

User = get_user_model()
logger = logging.getLogger(__name__)


class FirebaseTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, id_token):
        try:
            token = auth.verify_id_token(id_token)
        except Exception as e:
            raise exceptions.AuthenticationFailed()
        else:
            email = token.get("email")
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            logger.error(str(e))
            raise exceptions.AuthenticationFailed("User not found")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted.")
        return (user, token)
