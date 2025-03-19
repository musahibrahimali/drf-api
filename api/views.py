from rest_framework import status
from rest_framework.generics import GenericAPIView

from helpers.models import APIResponseMixin


class TodoAPIView(GenericAPIView, APIResponseMixin):
    """
        Home API View.
    """
    authentication_classes = []
    def get(self, request) -> APIResponseMixin.api_response:
        """
        Get the Home page.
        """
        message = self.get_welcome_message()
        return self.api_response(
            data={'message': message},
            message="Welcome home",
            status_code=status.HTTP_200_OK,
            success=True,
            meta=None,
        )

    @staticmethod
    def get_welcome_message() -> str:
        return "Hello, and welcome to the Todo API!"
