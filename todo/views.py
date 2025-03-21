from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from helpers.models import APIResponseMixin
from todo.models import Todo
from todo.pagination import CustomPageNumberPagination
from todo.serializers import TodoSerializer

class CreateTodoAPIView(CreateAPIView, APIResponseMixin):
    """
        API endpoint that allows users to create a todos-item.
    """
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs) -> APIResponseMixin.api_response:
        """
            Override the create method to customize the response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)

        return self.api_response(
            data=serializer.data,  # Use serializer data, not raw model instance
            message="Todo created successfully",
            status_code=status.HTTP_201_CREATED,
            success=True,
            meta=None,
        )


class TodoListAPIView(ListAPIView, APIResponseMixin):
    """
        API endpoint that allows users to view todos-items.
    """
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # pagination_class = CustomPageNumberPagination

    filterset_fields = ['id', 'title', 'is_complete']
    search_fields = ['id', 'title', 'desc', 'is_complete']
    ordering_fields = ['id', 'title', 'is_complete']

    def get_queryset(self) -> any:
        """
        Return only the todos that belong to the authenticated user.
        """
        return Todo.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs) -> APIResponseMixin.api_response:
        """
        Custom list method to return todos with API response format.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Use self.paginator instead of self
            next_link = self.paginator.get_next_link() if self.paginator else None
            previous_link = self.paginator.get_previous_link() if self.paginator else None
            count = self.paginator.count if self.paginator else queryset.count()
            meta = {
                'links': {
                    'next': next_link,
                    'previous': previous_link,
                },
                'count': count
            }
            return self.api_response(
                data=serializer.data,
                message="Todos retrieved successfully",
                status_code=status.HTTP_200_OK,
                success=True,
                meta=meta,
            )

        serializer = self.get_serializer(queryset, many=True)

        return self.api_response(
            data=serializer.data,
            message="Todos retrieved successfully",
            status_code=status.HTTP_200_OK,
            success=True
        )


class TodoDetailsAPIView(RetrieveAPIView, APIResponseMixin):
    """
        API endpoint that allows users to view a single todos-item.
    """
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self) -> any:
        """
            Return only the todos that belong to the authenticated user.
        """
        return Todo.objects.filter(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs) -> any:
        """
            Custom retrieve method to return todos with API response format.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return self.api_response(
            data=serializer.data,
            message="Todo retrieved successfully",
            status_code=status.HTTP_200_OK,
            success=True,
            meta=None
        )


class TodoUpdateAPIView(UpdateAPIView, APIResponseMixin):
    """
        API endpoint that allows users to update a single todos-item.
    """
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        """
            Return only the todos that belong to the authenticated user.
        """
        return Todo.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        """
            Custom update method to return todos with API response format.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return self.api_response(
            data=serializer.data,
            message="Todo updated successfully",
            status_code=status.HTTP_200_OK,
            success=True,
            meta=None
        )

class TodoDeleteAPIView(DestroyAPIView, APIResponseMixin):
    """
        API endpoint that allows users to delete a single todos-item.
    """
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        """
            Return only the todos that belong to the authenticated user.
        """
        return Todo.objects.filter(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
            Custom destroy method to return todos with API response format.
        """
        instance = self.get_object()
        self.perform_destroy(instance)

        return self.api_response(
            data=None,
            message="Todo deleted successfully",
            status_code=status.HTTP_200_OK,
            success=True,
            meta=None
        )