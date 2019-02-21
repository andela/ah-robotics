import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import (
    get_authorization_header, BaseAuthentication)
from .models import User


class JWTAuthentication(BaseAuthentication):
    """
    Implements jwt authentication using
    authorization header passed on the requests
    with keyword token
    """
    key = "Token"

    def authenticate(self, request):
        """
        :param: request
        returns authorization header from
        the request
        """
        header = get_authorization_header(request).split()
        if not header or header[0].decode().lower() != self.key.lower():
            return None
        if len(header) == 1:
            message = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(message)
        elif len(header) > 2:
            message = 'Invalid token header. ' \
                      'Token should not contain whitespaces.'
            raise exceptions.AuthenticationFailed(message)
        return self.authenticate_credentials(header[1].decode())

    def authenticate_credentials(self, token):
        """
        :param: request
        :param: token
        authenticates the given credentials
        returns user and token upon successful authentication
        otherwise throws an error
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except Exception as e:
            if e.__class__.__name__ == 'ExpiredSignatureError':
                raise exceptions.AuthenticationFailed('Token has expired')
            elif e.__class__.__name__ == 'DecodeError':
                raise exceptions.AuthenticationFailed(
                    'Cannot decode the given token')
            else:
                raise exceptions.AuthenticationFailed(str(e))
        try:
            user = User.objects.get(email=payload['email'])
        except user.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user found')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User has been deactivated')
        return user, token
