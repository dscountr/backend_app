import logging
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from decouple import config
from firebase_admin import auth, credentials, initialize_app


private_key = config("PRIVATE_KEY").replace("\\n", "\n")
payload = {
    "type": "service_account",
    "project_id": config("PROJECT_ID"),
    "private_key_id": config("PRIVATE_KEY_ID"),
    "private_key": private_key,
    "client_email": config("CLIENT_EMAIL"),
    "client_id": config("CLIENT_ID"),
    "auth_uri": config("AUTH_URI"),
    "token_uri": config("TOKEN_URI"),
    "auth_provider_x509_cert_url": config("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": config("CLIENT_X509_CERT_URL"),
}

cred = credentials.Certificate(payload)
initialize_app(cred)

User = get_user_model()
logger = logging.getLogger(__name__)


class FirebaseTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = auth.verify_id_token(key)
        except Exception:
            raise exceptions.AuthenticationFailed(
                "Unable to authenticate. Invalid or expired token")
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
