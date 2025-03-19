from django.db import models

from rest_framework.response import Response
from rest_framework import status


class APIResponseMixin:
    """
    A mixin to standardize API responses.
    """

    @staticmethod
    def api_response(
        data:any=None,
        message:str="",
        success:bool=True,
        status_code:any=status.HTTP_200_OK,
        meta: dict = None,
    ) -> Response:
        """
            Returns a standard JSON response format.

            :param data: The response data (can be any serializable type)
            :param message: A string message
            :param success: A boolean indicating success or failure
            :param status_code: The HTTP status code
            :param meta: A dictionary containing metadata
            :return: A DRF Response object
        """
        response_structure = {
            "success": success,
            "message": message,
            "data": data,
            'meta': meta,
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
