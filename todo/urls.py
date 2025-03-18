
from django.urls import path
from todo.views import (
    CreateTodoAPIView,
    TodoListAPIView,
    TodoDetailsAPIView,
    TodoDeleteAPIView
)

urlpatterns = [
    path('add', CreateTodoAPIView.as_view(), name='create-todo'),
    path('list', TodoListAPIView.as_view(), name='todo-list'),
    path('<int:id>', TodoDetailsAPIView.as_view(), name='get-todo'),
    path('delete/<int:id>', TodoDeleteAPIView.as_view(), name='delete-todo'),
]
