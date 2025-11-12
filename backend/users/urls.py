from django.urls import path
from .views import (
    RegisterAPIView, LoginAPIView, LogoutAPIView, ProfileAPIView,
    UserDetailAPIView, FollowAPIView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Auth
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profiles
    path('me/', ProfileAPIView.as_view(), name='profile-me'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('users/<int:pk>/follow/', FollowAPIView.as_view(), name='user-follow'),
]