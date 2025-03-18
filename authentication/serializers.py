from rest_framework import serializers
from authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
        Serializer for the User model.
    """
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        """
            Metaclass for the User model.
        """
        model = User
        fields = ['email', 'username', 'password', 'token']
        read_only_fields = ['token']

    def create(self, validated_data):
        """
            Create and return a new `User` instance, given the validated data.
        """
        user = User.objects.create_user(**validated_data)
        return user


    @staticmethod
    def get_token(obj):
        """
            Method to get the token for the user.
        """
        return obj.token



class LoginSerializer(serializers.ModelSerializer):
    """
        Serializer for the User model.
    """
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)

    class Meta:
        """
            Metaclass for the User model.
        """
        model = User
        fields = ['email', 'password', 'token']

        read_only_fields = ['token']
