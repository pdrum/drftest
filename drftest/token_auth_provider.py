from django.contrib.auth.models import User
from drftest.auth_provider import AuthProvider
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class TokenAuthProvider(AuthProvider):
    def _new_token(self, user: User):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def set_auth(self, api_client: APIClient, user: User):
        if user is None:
            return
        token = self._new_token(user)
        api_client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))

    def get_auth_headers(self, user: User):
        if user is None:
            return {}
        return {'Authorization': 'Token {}'.format(self._new_token(user))}
