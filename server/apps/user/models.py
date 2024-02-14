from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    photo = models.ImageField(upload_to="users/", blank=True, null=True)

    def get_tokens(self):
        """Get access and refresh tokens for user."""

        refresh = RefreshToken.for_user(self)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
