from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from server.apps.core.logic.schemas import BAD_REQUEST, UNAUTHORIZED

from .logic.schemas import AUTH_TOKENS
from .logic.serializers import LoginSerializer, RegistrationSerializer, UserSerializer


class RegistrationView(generics.CreateAPIView):
    """Registration view."""

    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        responses={
            201: openapi.Response(
                description="User successfully registered",
                schema=RegistrationSerializer,
            ),
            400: openapi.Response(
                description="Bad request. Invalid data provided",
                schema=BAD_REQUEST,
            ),
        },
    )
    def post(self, request):
        """Handle User registration request"""
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """Login view."""

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Successfully logged in",
                schema=AUTH_TOKENS,
            ),
            401: openapi.Response(
                description="Unauthorized. Invalid credentials provided",
                schema=UNAUTHORIZED,
            ),
        },
    )
    def post(self, request):
        """Login view for user."""

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data["username_email"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "Username/email or password is incorrect."}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(user.get_tokens(), status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """Profile Retrieve and Update view."""

    serializer_class = UserSerializer

    def get_object(self):
        """Retrieve and return authentication user."""
        return self.request.user

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Successfully retrieved user profile",
                schema=UserSerializer,
            ),
            401: openapi.Response(
                description="Unauthorized. Invalid credentials provided",
                schema=UNAUTHORIZED,
            ),
        },
    )
    def get(self, request):
        """Get user profile"""
        serializer = UserSerializer(self.get_object())

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Successfully updated user profile",
                schema=UserSerializer,
            ),
            400: openapi.Response(
                description="Bad request. Invalid data provided",
                schema=BAD_REQUEST,
            ),
            401: openapi.Response(
                description="Unauthorized. Invalid credentials provided",
                schema=UNAUTHORIZED,
            ),
        },
    )
    def put(self, request):
        """Update user profile"""
        serializer = UserSerializer(self.get_object(), data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
