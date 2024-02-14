from rest_framework import serializers

from ..models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user account."""

    photo = serializers.ImageField(required=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    password_confirmation = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        fields = ("photo", "first_name", "last_name", "username", "email", "password", "password_confirmation")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "password": {"write_only": True},
            "password_confirmation": {"write_only": True},
        }

    def validate_password_confirmation(self, value):
        """Check that password and password_confirmation match."""
        password = self.get_initial().get("password")

        if password != value:
            raise serializers.ValidationError("Passwords don't match.")

        return value

    def validate_email(self, value):
        """Check if user exist with this email"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")

        return value

    def create(self, validated_data):
        """Create a new user with encrypted password and return it."""
        validated_data.pop("password_confirmation")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Serializer definition for Login."""

    username_email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        """Meta definition for LoginSerializer."""

        fields = ["username_email", "password"]

    def validate_username_email(self, value):
        """Check if user exist with this email or username"""

        value = value.lower()

        user = User.objects.filter(email=value).first() or User.objects.filter(username=value).first()

        if not user:
            return value

        return user.username


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = User
        fields = ("id", "photo", "first_name", "last_name", "username", "email", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"username": {"required": False}}
