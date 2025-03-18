from django.db import models

from rest_framework.response import Response
from rest_framework import status


class APIResponseMixin:
    """
    A mixin to standardize API responses.
    """

    @staticmethod
    def api_response(
        data=None,
        message="",
        success=True,
        status_code=status.HTTP_200_OK
    ) -> Response:
        """
            Returns a standard JSON response format.

            :param data: The response data (can be any serializable type)
            :param message: A string message
            :param success: A boolean indicating success or failure
            :param status_code: The HTTP status code
            :return: A DRF Response object
        """
        response_structure = {
            "success": success,
            "message": message,
            "data": data
        }
        return Response(response_structure, status=status_code)


class TrackingModel(models.Model):
    """
        An abstract model to track the creation and updating of records.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)
