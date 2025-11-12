from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenBlacklistView  # Correct import for blacklisting
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .serializers import (
    RegisterSerializer, CustomTokenObtainPairSerializer, UserSerializer, FollowSerializer
)
from .models import User, Follow

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Optional: Auto-issue tokens on register
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            user_data = UserSerializer(user).data
            user_data.update({
                'refresh': str(refresh),
                'access': str(access),
            })
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, email=email, password=password)
        if user:
            if not user.is_active:
                return Response({'error': 'Account is inactive'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Use your custom serializer for token response
            serializer = CustomTokenObtainPairSerializer()
            token_data = {
                'refresh': str(RefreshToken.for_user(user)),
                'access': str(RefreshToken.for_user(user).access_token),
            }
            # Merge with custom fields
            token_data.update({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'bio': user.bio,
                'profile_image': user.profile_image,
                'is_verified': user.is_verified,
                'role': user.role,
            })
            return Response(token_data, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(TokenBlacklistView):
    """
    POST: Blacklist the refresh token for logout.
    Expects: {'refresh': 'your_refresh_token_string'} in request body.
    This invalidates the refresh token server-side; client should discard access token too.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token required for blacklisting'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Let SimpleJWT handle the blacklisting
        response = super().post(request)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({'message': 'Logged out successfully - token blacklisted'}, status=status.HTTP_205_RESET_CONTENT)
        return response

class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Current user's profile
        serializer = UserSerializer(request.user)
        data = serializer.data
        data.update({
            'followers_count': request.user.followers.count(),
            'following_count': request.user.following.count(),
        })
        return Response(data)

    def put(self, request):
        # Update current user's profile (partial allowed)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Change to AllowAny for public profiles

    def get(self, request, pk):
        user = get_object_or_404(User.objects.filter(is_active=True), pk=pk)
        serializer = UserSerializer(user)
        data = serializer.data
        data.update({
            'followers_count': user.followers.count(),
            'following_count': user.following.count(),
            'is_following': Follow.objects.filter(follower=request.user, following=user).exists(),
        })
        return Response(data)

class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user_to_follow = get_object_or_404(User.objects.filter(is_active=True), pk=pk)
        if request.user == user_to_follow:
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if not created:
            return Response({'error': 'Already following'}, status=status.HTTP_400_BAD_REQUEST)
        
        # TODO: Integrate with notifications app
        serializer = FollowSerializer(follow)
        return Response({
            'message': f'Now following {user_to_follow.username}',
            'follow': serializer.data
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user_to_unfollow = get_object_or_404(User.objects.filter(is_active=True), pk=pk)
        follow = get_object_or_404(Follow, follower=request.user, following=user_to_unfollow)
        follow.delete()
        return Response({'message': f'Unfollowed {user_to_unfollow.username}'}, status=status.HTTP_204_NO_CONTENT)