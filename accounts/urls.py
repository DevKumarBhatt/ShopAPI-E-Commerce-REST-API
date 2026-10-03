from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterView, ProfileView


urlpatterns = [
    # Register
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    # Login
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="login",
    ),

    # Refresh access token
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),

    # Profile
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),
]