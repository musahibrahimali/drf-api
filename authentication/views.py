from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from authentication.serializers import RegisterSerializer, LoginSerializer
from helpers.models import APIResponseMixin
from django.contrib.auth import authenticate


class AuthUserAPIView(GenericAPIView, APIResponseMixin):
    """
        Authenticated User API View.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
            Get the authenticated user.
        """
        user = request.user
        serializer = RegisterSerializer(user)
        if user.is_authenticated:
            return self.api_response(
                data={'user': serializer.data},
                message="Authenticated user",
                status_code=status.HTTP_200_OK,
                success=True,
            )

        return self.api_response(
            data={'message': 'User not authenticated'},
            message="User not authenticated",
            status_code=status.HTTP_401_UNAUTHORIZED,
            success=False,
        )


class RegisterAPIView(GenericAPIView, APIResponseMixin):
    """
        Register API View.
    """
    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return self.api_response(
                data={'user': serializer.data, 'token': user.token},
                message='User created successfully',
                status_code=status.HTTP_201_CREATED,
                success=True,
            )

        return self.api_response(
            data=serializer.errors,
            message={'message': "There was an error registering a new user"},
            status_code=status.HTTP_400_BAD_REQUEST,
            success=False,
        )

class LoginAPIView(GenericAPIView, APIResponseMixin):
    """
        Login API View.
    """
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request, email=email, password=password)
            if user:
                serializer = self.get_serializer(user)
                return self.api_response(
                    success=True,
                    data=serializer.data,
                    message="Login successful",
                    status_code=status.HTTP_200_OK,
                )

        return self.api_response(
            data={'message': 'Invalid email or password'},
            message="Invalid email or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
            success=False,
        )
