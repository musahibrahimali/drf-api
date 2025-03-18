from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from authentication.models import User
from todo.models import Todo


class TodoUserSerializer(serializers.ModelSerializer):
    """
        Serializer for the User model (only selected fields).
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'created_at', 'updated_at')  # Choose the fields you want to return


class TodoSerializer(ModelSerializer):
    title = serializers.CharField(max_length=255)
    owner = TodoUserSerializer(read_only=True)  # Serialize owner details instead of just ID
    class Meta:
        model = Todo
        fields = '__all__' # ('title', 'desc', 'is_complete')