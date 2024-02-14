from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, ProfileView, RegistrationView

app_name = "user"

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
