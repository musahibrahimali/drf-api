import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from authentication.models import User


class JwtAuthentication(BaseAuthentication):
    """
        Authentication class for JWT.
    """

    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')

        auth_token = auth_data.split(' ')

        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed("Invalid token")

        token = auth_token[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            username = payload['username']
            user = User.objects.get(username=username)
            return user, token
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired, login again")
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Token is invalid, login again")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Token is invalid, login again")
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")