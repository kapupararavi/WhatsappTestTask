"""
Contains the authentication class for the endpoint.
"""

import hashlib

from django.utils.translation import gettext_lazy as _

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from wa_messages.models import APIToken


class TokenAuth(TokenAuthentication):
    """
    TokenAuth class inherits the `rest_framework.authentication.TokenAuthentication`,
    and implements the `authenticate_credentials` to get the user object.
    """

    model = APIToken

    @staticmethod
    def get_hashed_token(text: str):
        """
        Returns:
            (str) the hashed token using the `SHA256` function and the value is for the
            parameter `text`.
        """
        return hashlib.sha256(text.encode()).hexdigest()

    def authenticate_credentials(self, key):
        model = self.get_model()
        hashed_token = self.get_hashed_token(key)

        try:
            api_token_obj = APIToken.objects.select_related('user').get(token=hashed_token)
        except model.DoesNotExist as e:
            raise AuthenticationFailed(_('Invalid token.')) from e

        user = api_token_obj.user
        if not user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        return user, api_token_obj
